# -*- coding: utf-8 -*-
"""
ComfyUI ANY型データの型判定とメタデータ抽出

任意の型のデータを受け取り、型名やメタデータを抽出する
"""

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


def detect_any_type(data):
    """
    ANY型データの型を判定

    Args:
        data: 任意の型のデータ

    Returns:
        str: "int", "float", "string", "image", "latent", "model", "vae", "lora",
             "conditioning", "clip", "control_net", "clip_vision", "style_model",
             "gligen", "none", "unknown"
    """
    if data is None:
        return "none"

    # Python基本型
    if isinstance(data, bool):
        # boolはintのサブクラスなので先に判定
        return "int"
    if isinstance(data, int):
        return "int"
    if isinstance(data, float):
        return "float"
    if isinstance(data, str):
        return "string"

    # PyTorchテンソル（IMAGE/LATENT）
    if TORCH_AVAILABLE and torch.is_tensor(data):
        return _detect_tensor_type(data)

    # ComfyUI固有型（MODEL/VAE/CLIP/CONDITIONING）
    comfy_type = _detect_comfy_type(data)
    if comfy_type != "unknown":
        return comfy_type

    return "unknown"


def _detect_tensor_type(tensor):
    """
    PyTorchテンソルの型を判定（IMAGE or LATENT）

    Args:
        tensor: PyTorchテンソル

    Returns:
        str: "image", "latent", "unknown"
    """
    if not hasattr(tensor, 'shape'):
        return "unknown"

    shape = tensor.shape

    # 4次元テンソルの場合
    if len(shape) == 4:
        # ComfyUIの規則:
        # IMAGE: [batch, height, width, channels] - channels = 3 or 4
        # LATENT: [batch, channels, height, width] - channels = 4

        # 最小次元がchannels軸と推定
        if shape[3] in [1, 3, 4] and shape[1] > 4:
            # [B, H, W, C] パターン - IMAGE
            return "image"
        elif shape[1] == 4 and shape[2] > 4 and shape[3] > 4:
            # [B, C, H, W] パターン - LATENT
            return "latent"
        else:
            # 形状から推定できない場合、latentとみなす
            return "latent"

    # 3次元テンソルの場合（単一画像の可能性）
    if len(shape) == 3:
        if shape[2] in [1, 3, 4]:
            # [H, W, C] パターン - IMAGE
            return "image"
        elif shape[0] == 4:
            # [C, H, W] パターン - LATENT
            return "latent"

    return "unknown"


def _detect_comfy_type(data):
    """
    ComfyUI固有型を判定

    Args:
        data: 任意のオブジェクト

    Returns:
        str: "model", "vae", "clip", "conditioning", "control_net", "clip_vision",
             "style_model", "gligen", "lora", "unknown"
    """
    # クラス名での判定
    class_name = type(data).__name__.lower()

    # CONTROL_NET判定（MODELより先に判定）
    if 'controlnet' in class_name or 'controllora' in class_name:
        return "control_net"
    if hasattr(data, 'control_model') and hasattr(data, 'load_device'):
        return "control_net"

    # CLIP_VISION判定（CLIPより先に判定）
    if 'clipvision' in class_name or 'clip_vision' in class_name:
        return "clip_vision"
    if hasattr(data, 'encode_image'):
        return "clip_vision"

    # STYLE_MODEL判定
    if 'style' in class_name and 'model' in class_name:
        return "style_model"

    # GLIGEN判定
    if 'gligen' in class_name:
        return "gligen"

    # MODEL判定
    if any(keyword in class_name for keyword in ['model', 'unet', 'diffusion']):
        if 'vae' not in class_name and 'clip' not in class_name:
            return "model"

    # VAE判定
    if 'vae' in class_name or (hasattr(data, 'decode') and hasattr(data, 'encode')):
        return "vae"

    # CLIP判定
    if 'clip' in class_name or hasattr(data, 'tokenize'):
        return "clip"

    # CONDITIONING判定（リスト形式）
    if isinstance(data, list) and len(data) > 0:
        if isinstance(data[0], list) and len(data[0]) >= 2:
            # CONDITIONINGは[[tensor, dict], ...]形式
            if TORCH_AVAILABLE and torch.is_tensor(data[0][0]):
                return "conditioning"

    # LoRA判定（困難なため暫定実装）
    if 'lora' in class_name:
        return "lora"

    return "unknown"


def extract_dimensions(data):
    """
    IMAGE/LATENTの幅・高さを取得

    Args:
        data: 任意の型のデータ

    Returns:
        dict: {"width": int, "height": int}
    """
    if not TORCH_AVAILABLE or not torch.is_tensor(data):
        return {"width": 0, "height": 0}

    if not hasattr(data, 'shape'):
        return {"width": 0, "height": 0}

    shape = data.shape

    # 4次元テンソル
    if len(shape) == 4:
        # IMAGE: [batch, height, width, channels]
        if shape[3] in [1, 3, 4] and shape[1] > 4:
            return {"width": int(shape[2]), "height": int(shape[1])}
        # LATENT: [batch, channels, height, width]
        elif shape[1] == 4:
            return {"width": int(shape[3]), "height": int(shape[2])}
        else:
            # デフォルト推定: [B, C, H, W]
            return {"width": int(shape[3]), "height": int(shape[2])}

    # 3次元テンソル
    if len(shape) == 3:
        # [H, W, C]
        if shape[2] in [1, 3, 4]:
            return {"width": int(shape[1]), "height": int(shape[0])}
        # [C, H, W]
        elif shape[0] == 4:
            return {"width": int(shape[2]), "height": int(shape[1])}

    return {"width": 0, "height": 0}


