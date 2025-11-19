# -*- coding: utf-8 -*-
"""
u5 Loader Wrapper Nodes - ファイル名出力機能付きローダー
各種ComfyUIローダーをラップし、選択されたファイル名を出力する
"""

import folder_paths
import comfy.sd
import comfy.utils
import comfy.controlnet
import comfy.model_management
import nodes

# UI更新用（PromptServer経由でフロントエンドに通知）
try:
    from server import PromptServer
    HAS_PROMPT_SERVER = True
except ImportError:
    HAS_PROMPT_SERVER = False
    print("[u5_loaders] Warning: PromptServer not available, UI updates disabled")


# ==================== 統一マッチロジック（OPTIMAL_LATENT準拠）====================
# OPTIMAL_LATENTのidentify_model()と同じマッチロジックをファイル名検索に適用


def normalize_text(text: str) -> str:
    """
    テキストを正規化（空白・ハイフン・アンダースコア除去、小文字化）
    
    OPTIMAL_LATENTのnormalize_text()と同じ処理
    
    Args:
        text: 正規化対象のテキスト
    
    Returns:
        正規化されたテキスト
    """
    return text.replace(" ", "").replace("-", "").replace("_", "").lower()


def generate_numeric_variations(word: str) -> list:
    """
    数値を含む単語のバリエーションを生成
    
    OPTIMAL_LATENTのgenerate_numeric_variations()と同じ処理
    
    ルール:
    - 小数点を含む場合: 小数点を除去したパターンも生成 (例: "1.5" -> ["1.5", "15"])
    - 二桁の数字: 1の位を省略したパターンも生成 (例: "2.0" -> ["2.0", "20", "2"])
    
    Args:
        word: 単語（例: "1.5", "2.0", "turbo"）
    
    Returns:
        バリエーションのリスト（元の単語を含む）
    """
    variations = [word]
    
    # 小数点を含む数値の場合
    if '.' in word:
        # 小数点除去 (例: "1.5" -> "15")
        no_dot = word.replace('.', '')
        variations.append(no_dot)
        
        # 1の位省略 (例: "2.0" -> "2")
        parts = word.split('.')
        if len(parts) == 2 and parts[1] == '0':
            variations.append(parts[0])
    
    # 二桁の数字の場合（小数点なし）
    elif word.isdigit() and len(word) == 2:
        # 1の位省略 (例: "20" -> "2")
        variations.append(word[0])
    
    return variations


def multiword_file_match(text: str, file_list: list) -> str:
    """
    複数単語検索によるファイル名マッチング（AND検索）
    
    OPTIMAL_LATENTのidentify_model_multiword()と同じ処理をファイル名に適用
    
    仕様:
    1. スペース(" "または"　")で単語分割
    2. 各単語について数値バリエーションを生成
    3. AND検索: 全単語が全てマッチする必要あり
    4. 大文字小文字区別なし
    
    Args:
        text: 検索文字列（例: "sd 1.5", "stable diffusion 2.0"）
        file_list: ファイル名リスト
    
    Returns:
        マッチしたファイル名、または見つからない場合None
    """
    # スペース分割（半角・全角対応）
    words = text.replace('　', ' ').split(' ')
    words = [w.strip() for w in words if w.strip()]
    
    if len(words) < 2:
        # 単語が1つの場合は複数単語検索不要
        return None
    
    # 各単語のバリエーション生成
    word_variations = []
    for word in words:
        variations = generate_numeric_variations(word)
        # 大文字小文字区別なしのため全て小文字化
        variations = [v.lower() for v in variations]
        word_variations.append(variations)
    
    # 全ファイルに対してAND検索
    for filename in file_list:
        # ファイル名を正規化（スペース・ハイフン・アンダースコア除去）
        normalized_filename = normalize_text(filename)
        
        # AND検索: 全単語のいずれかのバリエーションがマッチする必要あり
        all_matched = True
        for variations in word_variations:
            word_matched = False
            for variation in variations:
                # スペース・ハイフン・アンダースコア除去後の文字列に含まれるか
                clean_variation = variation.replace(' ', '').replace('-', '').replace('_', '')
                if clean_variation in normalized_filename:
                    word_matched = True
                    break
            
            if not word_matched:
                all_matched = False
                break
        
        if all_matched:
            return filename
    
    return None


def select_file_smart(text_input: str, file_list: list, dropdown_value: str) -> str:
    """
    OPTIMAL_LATENTのidentify_model()と同じロジックでファイル名を検索
    
    優先順位:
    1. スペース含む場合、まず完全一致を試みる（スペースそのままで）
    2. 完全一致（正規化後）
    3. 部分一致（より長いマッチを優先）
    4. 複数単語検索（スペース含む場合のAND検索）
    5. なければドロップダウン値を返す
    
    Args:
        text_input: 検索文字列
        file_list: ファイル名リスト
        dropdown_value: マッチしない場合のデフォルト値
    
    Returns:
        マッチしたファイル名、またはドロップダウン値
    """
    # 空文字列・空白のみの場合はドロップダウン値
    if not text_input or not text_input.strip():
        return dropdown_value
    
    text_input = text_input.strip()
    normalized_input = normalize_text(text_input)
    
    # Phase 0: スペース含む場合、まず完全一致を試みる（スペースそのままで）
    if ' ' in text_input or '　' in text_input:
        for filename in file_list:
            if filename.lower() == text_input.lower():
                return filename
    
    # Phase 1: 完全一致・部分一致検索
    exact_matches = []
    partial_matches = []
    
    for filename in file_list:
        normalized_filename = normalize_text(filename)
        
        # 完全一致
        if normalized_filename == normalized_input:
            exact_matches.append((filename, len(normalized_filename)))
        # 部分一致（より長いマッチを記録）
        elif normalized_input in normalized_filename or normalized_filename in normalized_input:
            match_score = len(normalized_filename)
            partial_matches.append((filename, match_score))
    
    # 完全一致が優先
    if exact_matches:
        # 同じ正規化長の場合、最初のマッチを返す
        return exact_matches[0][0]
    
    if partial_matches:
        # 部分一致の場合、マッチ長が長い順にソート
        partial_matches.sort(key=lambda x: x[1], reverse=True)
        return partial_matches[0][0]
    
    # Phase 1.5: 複数単語検索（スペース含む場合）
    if ' ' in text_input or '　' in text_input:
        multiword_result = multiword_file_match(text_input, file_list)
        if multiword_result:
            return multiword_result
    
    # マッチなし: ドロップダウン値を返す
    return dropdown_value


# ==================== 統一マッチロジック終了 ====================


def send_widget_update(node_type: str, widget_name: str, new_value: str, unique_id: str = None):
    """
    フロントエンドにUI更新メッセージを送信

    Args:
        node_type: ノードタイプ（例: "u5_CheckpointLoader"）
        widget_name: ウィジェット名（例: "ckpt_name"）
        new_value: 新しい値（例: "model.safetensors"）
        unique_id: ノードの一意ID（取得可能な場合のみ）
    """
    if not HAS_PROMPT_SERVER:
        return

    try:
        message = {
            "node_type": node_type,
            "widget_name": widget_name,
            "new_value": new_value
        }
        if unique_id:
            message["unique_id"] = unique_id

        PromptServer.instance.send_sync("u5_widget_update", message)
        print(f"[u5_loaders] UI update sent: {node_type}.{widget_name} = {new_value}")
    except Exception as e:
        print(f"[u5_loaders] Failed to send UI update: {e}")


class u5_CheckpointLoader:
    """CheckpointLoaderSimpleのラッパー - ファイル名出力付き"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "ckpt_name": (folder_paths.get_filename_list("checkpoints"),),
            },
            "optional": {
                "text_input": ("STRING", {"default": "", "forceInput": True}),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "STRING")
    RETURN_NAMES = ("MODEL", "CLIP", "VAE", "filename")
    FUNCTION = "load_checkpoint"
    CATEGORY = "u5/EasyScripter"

    def load_checkpoint(self, ckpt_name, text_input=""):
        # ファイル名選択（部分一致 → ドロップダウン）
        selected_name = self._select_file(text_input, ckpt_name, "checkpoints")

        # UI更新メッセージを送信（text_inputが使われた場合のみ）
        if text_input and text_input.strip() and selected_name != ckpt_name:
            send_widget_update("u5_CheckpointLoader", "ckpt_name", selected_name)

        # オリジナルローダー呼び出し
        ckpt_path = folder_paths.get_full_path_or_raise("checkpoints", selected_name)
        out = comfy.sd.load_checkpoint_guess_config(
            ckpt_path,
            output_vae=True,
            output_clip=True,
            embedding_directory=folder_paths.get_folder_paths("embeddings")
        )

        return (out[0], out[1], out[2], selected_name)

    @staticmethod
    def _select_file(text_input, dropdown_value, folder_type):
        """
        統一マッチロジック（OPTIMAL_LATENT準拠）のラッパー
        
        旧実装との後方互換性のため、select_file_smart()を呼び出す。
        """
        files = folder_paths.get_filename_list(folder_type)
        return select_file_smart(text_input, files, dropdown_value)


class u5_LoraLoader:
    """LoraLoaderのラッパー - ファイル名出力付き"""

    def __init__(self):
        self.loaded_lora = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "lora_name": (folder_paths.get_filename_list("loras"),),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01}),
            },
            "optional": {
                "text_input": ("STRING", {"default": "", "forceInput": True}),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "STRING")
    RETURN_NAMES = ("MODEL", "CLIP", "filename")
    FUNCTION = "load_lora"
    CATEGORY = "u5/EasyScripter"

    def load_lora(self, model, clip, lora_name, strength_model, strength_clip, text_input=""):
        # ファイル名選択
        selected_name = u5_CheckpointLoader._select_file(text_input, lora_name, "loras")

        # UI更新メッセージを送信
        if text_input and text_input.strip() and selected_name != lora_name:
            send_widget_update("u5_LoraLoader", "lora_name", selected_name)

        if strength_model == 0 and strength_clip == 0:
            return (model, clip, selected_name)

        lora_path = folder_paths.get_full_path_or_raise("loras", selected_name)
        lora = None
        if self.loaded_lora is not None:
            if self.loaded_lora[0] == lora_path:
                lora = self.loaded_lora[1]
            else:
                self.loaded_lora = None

        if lora is None:
            lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
            self.loaded_lora = (lora_path, lora)

        model_lora, clip_lora = comfy.sd.load_lora_for_models(model, clip, lora, strength_model, strength_clip)
        return (model_lora, clip_lora, selected_name)


class u5_VAELoader:
    """VAELoaderのラッパー - ファイル名出力付き"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "vae_name": (folder_paths.get_filename_list("vae"),),
            },
            "optional": {
                "text_input": ("STRING", {"default": "", "forceInput": True}),
            }
        }

    RETURN_TYPES = ("VAE", "STRING")
    RETURN_NAMES = ("VAE", "filename")
    FUNCTION = "load_vae"
    CATEGORY = "u5/EasyScripter"

    def load_vae(self, vae_name, text_input=""):
        # ファイル名選択
        selected_name = u5_CheckpointLoader._select_file(text_input, vae_name, "vae")

        # UI更新メッセージを送信
        if text_input and text_input.strip() and selected_name != vae_name:
            send_widget_update("u5_VAELoader", "vae_name", selected_name)

        vae_path = folder_paths.get_full_path_or_raise("vae", selected_name)
        sd = comfy.utils.load_torch_file(vae_path)
        vae = comfy.sd.VAE(sd=sd)
        return (vae, selected_name)


class u5_ControlNetLoader:
    """ControlNetLoaderのラッパー - ファイル名出力付き"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "control_net_name": (folder_paths.get_filename_list("controlnet"),),
            },
            "optional": {
                "text_input": ("STRING", {"default": "", "forceInput": True}),
            }
        }

    RETURN_TYPES = ("CONTROL_NET", "STRING")
    RETURN_NAMES = ("CONTROL_NET", "filename")
    FUNCTION = "load_controlnet"
    CATEGORY = "u5/EasyScripter"

    def load_controlnet(self, control_net_name, text_input=""):
        # ファイル名選択
        selected_name = u5_CheckpointLoader._select_file(text_input, control_net_name, "controlnet")

        # UI更新メッセージを送信
        if text_input and text_input.strip() and selected_name != control_net_name:
            send_widget_update("u5_ControlNetLoader", "control_net_name", selected_name)

        controlnet_path = folder_paths.get_full_path_or_raise("controlnet", selected_name)
        controlnet = comfy.controlnet.load_controlnet(controlnet_path)
        if controlnet is None:
            raise RuntimeError("ERROR: controlnet file is invalid and does not contain a valid controlnet model.")
        return (controlnet, selected_name)


class u5_CLIPVisionLoader:
    """CLIPVisionLoaderのラッパー - ファイル名出力付き"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "clip_name": (folder_paths.get_filename_list("clip_vision"),),
            },
            "optional": {
                "text_input": ("STRING", {"default": "", "forceInput": True}),
            }
        }

    RETURN_TYPES = ("CLIP_VISION", "STRING")
    RETURN_NAMES = ("CLIP_VISION", "filename")
    FUNCTION = "load_clip"
    CATEGORY = "u5/EasyScripter"

    def load_clip(self, clip_name, text_input=""):
        # ファイル名選択
        selected_name = u5_CheckpointLoader._select_file(text_input, clip_name, "clip_vision")

        # UI更新メッセージを送信
        if text_input and text_input.strip() and selected_name != clip_name:
            send_widget_update("u5_CLIPVisionLoader", "clip_name", selected_name)

        clip_path = folder_paths.get_full_path_or_raise("clip_vision", selected_name)
        clip_vision = comfy.clip_vision.load(clip_path)
        return (clip_vision, selected_name)


class u5_StyleModelLoader:
    """StyleModelLoaderのラッパー - ファイル名出力付き"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "style_model_name": (folder_paths.get_filename_list("style_models"),),
            },
            "optional": {
                "text_input": ("STRING", {"default": "", "forceInput": True}),
            }
        }

    RETURN_TYPES = ("STYLE_MODEL", "STRING")
    RETURN_NAMES = ("STYLE_MODEL", "filename")
    FUNCTION = "load_style_model"
    CATEGORY = "u5/EasyScripter"

    def load_style_model(self, style_model_name, text_input=""):
        # ファイル名選択
        selected_name = u5_CheckpointLoader._select_file(text_input, style_model_name, "style_models")

        # UI更新メッセージを送信
        if text_input and text_input.strip() and selected_name != style_model_name:
            send_widget_update("u5_StyleModelLoader", "style_model_name", selected_name)

        style_model_path = folder_paths.get_full_path_or_raise("style_models", selected_name)
        style_model = comfy.sd.load_style_model(style_model_path)
        return (style_model, selected_name)


class u5_GLIGENLoader:
    """GLIGENLoaderのラッパー - ファイル名出力付き"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "gligen_name": (folder_paths.get_filename_list("gligen"),),
            },
            "optional": {
                "text_input": ("STRING", {"default": "", "forceInput": True}),
            }
        }

    RETURN_TYPES = ("GLIGEN", "STRING")
    RETURN_NAMES = ("GLIGEN", "filename")
    FUNCTION = "load_gligen"
    CATEGORY = "u5/EasyScripter"

    def load_gligen(self, gligen_name, text_input=""):
        # ファイル名選択
        selected_name = u5_CheckpointLoader._select_file(text_input, gligen_name, "gligen")

        # UI更新メッセージを送信
        if text_input and text_input.strip() and selected_name != gligen_name:
            send_widget_update("u5_GLIGENLoader", "gligen_name", selected_name)

        gligen_path = folder_paths.get_full_path_or_raise("gligen", selected_name)
        gligen = comfy.sd.load_gligen(gligen_path)
        return (gligen, selected_name)


class u5_UNETLoader:
    """UNETLoaderのラッパー - ファイル名出力付き"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "unet_name": (folder_paths.get_filename_list("diffusion_models"),),
            },
            "optional": {
                "text_input": ("STRING", {"default": "", "forceInput": True}),
            }
        }

    RETURN_TYPES = ("MODEL", "STRING")
    RETURN_NAMES = ("MODEL", "filename")
    FUNCTION = "load_unet"
    CATEGORY = "u5/EasyScripter"

    def load_unet(self, unet_name, text_input=""):
        # ファイル名選択
        selected_name = u5_CheckpointLoader._select_file(text_input, unet_name, "diffusion_models")

        # UI更新メッセージを送信
        if text_input and text_input.strip() and selected_name != unet_name:
            send_widget_update("u5_UNETLoader", "unet_name", selected_name)

        unet_path = folder_paths.get_full_path_or_raise("diffusion_models", selected_name)
        model = comfy.sd.load_diffusion_model(unet_path)
        return (model, selected_name)


class u5_CLIPLoader:
    """CLIPLoaderのラッパー - ファイル名出力付き"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "clip_name": (folder_paths.get_filename_list("text_encoders"),),
            },
            "optional": {
                "text_input": ("STRING", {"default": "", "forceInput": True}),
            }
        }

    RETURN_TYPES = ("CLIP", "STRING")
    RETURN_NAMES = ("CLIP", "filename")
    FUNCTION = "load_clip"
    CATEGORY = "u5/EasyScripter"

    def load_clip(self, clip_name, text_input=""):
        # ファイル名選択
        selected_name = u5_CheckpointLoader._select_file(text_input, clip_name, "text_encoders")

        # UI更新メッセージを送信
        if text_input and text_input.strip() and selected_name != clip_name:
            send_widget_update("u5_CLIPLoader", "clip_name", selected_name)

        clip_path = folder_paths.get_full_path_or_raise("text_encoders", selected_name)
        # comfy.sd.load_clipはリストを要求するため、パスをリストでラップ
        clip = comfy.sd.load_clip([clip_path], embedding_directory=folder_paths.get_folder_paths("embeddings"))
        return (clip, selected_name)
