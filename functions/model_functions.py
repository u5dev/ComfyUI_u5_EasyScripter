# -*- coding: utf-8 -*-
"""
モデル別最適Latentサイズ判定機能
"""

import os
import csv
import re
from typing import List, Dict, Optional, Tuple

# データファイルパス（スクリプトからの相対パス）
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
MODEL_RESOLUTIONS_CSV = os.path.join(DATA_DIR, "model_resolutions.csv")


class ModelResolutionDatabase:
    """モデル解像度データベース"""

    def __init__(self):
        self.models: Dict[str, Dict] = {}
        self.load_data()

    def load_data(self):
        """CSVからデータをロード"""
        if not os.path.exists(MODEL_RESOLUTIONS_CSV):
            raise FileNotFoundError(f"Model resolution data not found: {MODEL_RESOLUTIONS_CSV}")

        with open(MODEL_RESOLUTIONS_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                model_key = row['model_key']
                if model_key not in self.models:
                    self.models[model_key] = {
                        'display_name': row['model_display_name'],
                        'aliases': [alias.strip() for alias in row['aliases'].split('|')],
                        'version': row['version'],
                        'resolutions': []
                    }

                self.models[model_key]['resolutions'].append({
                    'width': int(row['width']),
                    'height': int(row['height']),
                    'ratio': row['aspect_ratio'],
                    'description': row['description']
                })

    def reload(self):
        """データをリロード（メンテナンス後に呼び出し可能）"""
        self.models.clear()
        self.load_data()


# グローバルインスタンス（初回ロード）
_db_instance = None


def get_database() -> ModelResolutionDatabase:
    """シングルトンパターンでデータベースインスタンスを取得"""
    global _db_instance
    if _db_instance is None:
        _db_instance = ModelResolutionDatabase()
    return _db_instance


def normalize_text(text: str) -> str:
    """
    テキストを正規化（空白・ハイフン除去、小文字化）

    Args:
        text: 正規化対象のテキスト

    Returns:
        正規化されたテキスト
    """
    return text.replace(" ", "").replace("-", "").lower()


def extract_version(text: str) -> Optional[str]:
    """
    バージョン番号を抽出

    例:
    - "SD 2.1" -> "2.1"
    - "SD-V2.1" -> "2.1"
    - "SD v2x" -> "2.x"
    - "PixArt-α" -> None (バージョンではない)

    Args:
        text: バージョン抽出対象のテキスト

    Returns:
        抽出されたバージョン文字列、またはNone
    """
    # Vプレフィックスを除去
    normalized = text.replace("v", "").replace("V", "")

    # ハイフン後が数値パターンの場合のみバージョンとして認識
    # 例: "model-2", "model-2.1", "model-2.x", "model2x"
    # パターン: 数字 + (オプション: .数字 or .x or x)
    match = re.search(r'[-\s]*(\d+(?:\.\d+|\.x|x)?)\b', normalized)
    if match:
        version = match.group(1)
        # "2x" を "2.x" に正規化
        if version.endswith('x') and not version.endswith('.x'):
            version = version[:-1] + '.x'
        return version

    return None


def generate_numeric_variations(word: str) -> list:
    """
    数値を含む単語のバリエーションを生成
    
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


def identify_model_multiword(text: str, db: ModelResolutionDatabase) -> Optional[str]:
    """
    複数単語検索によるモデル識別
    
    仕様:
    1. スペース(" "または"　")で単語分割
    2. 各単語について数値バリエーションを生成
    3. AND検索: 全単語が全てマッチする必要あり
    4. 大文字小文字区別なし
    
    Args:
        text: 検索文字列（例: "sd 1.5", "stable diffusion 2.0"）
        db: ModelResolutionDatabase
    
    Returns:
        モデルキー、または見つからない場合None
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
    
    # 全モデルに対してAND検索
    for model_key, model_data in db.models.items():
        # モデル名とエイリアスを全て小文字化して結合
        searchable_texts = [
            model_data['display_name'].lower(),
            model_key.lower(),
        ] + [alias.lower() for alias in model_data['aliases']]
        
        # バージョンも検索対象に追加
        searchable_texts.append(model_data['version'].lower())
        
        # 全検索対象テキストを結合（スペース除去）
        combined_text = ' '.join(searchable_texts).replace(' ', '').replace('-', '')
        
        # AND検索: 全単語のいずれかのバリエーションがマッチする必要あり
        all_matched = True
        for variations in word_variations:
            word_matched = False
            for variation in variations:
                # スペース・ハイフン除去後の文字列に含まれるか
                clean_variation = variation.replace(' ', '').replace('-', '')
                if clean_variation in combined_text:
                    word_matched = True
                    break
            
            if not word_matched:
                all_matched = False
                break
        
        if all_matched:
            return model_key
    
    return None


def identify_model(text: str, db: ModelResolutionDatabase) -> Optional[str]:
    """
    テキストからモデルキーを識別
    
    優先順位:
    1. エイリアス完全一致
    2. エイリアス部分一致（より長いマッチを優先）
    3. 複数単語検索（スペース含む場合）
    4. バージョン考慮の絞り込み
    
    Args:
        text: モデル識別用のテキスト
        db: ModelResolutionDatabase
    
    Returns:
        モデルキー、または識別失敗時はNone
    """
    normalized_input = normalize_text(text)
    input_version = extract_version(text)
    
    # Phase 0: スペース含む場合、まず完全一致を試みる（スペースそのままで）
    if ' ' in text or '　' in text:
        # スペース含む全文での完全一致検索
        for model_key, model_data in db.models.items():
            for alias in model_data['aliases']:
                if alias.lower() == text.lower():
                    return model_key
    
    # Phase 1: エイリアス一致検索（完全一致優先、次に部分一致）
    exact_matches = []
    partial_matches = []
    
    for model_key, model_data in db.models.items():
        for alias in model_data['aliases']:
            normalized_alias = normalize_text(alias)
            
            # 完全一致
            if normalized_alias == normalized_input:
                exact_matches.append((model_key, model_data, len(normalized_alias)))
                break
            # 部分一致（より長いマッチを記録）
            elif normalized_alias in normalized_input or normalized_input in normalized_alias:
                match_score = len(normalized_alias)
                partial_matches.append((model_key, model_data, match_score))
                break
    
    # 完全一致が優先
    if exact_matches:
        matches = [(m[0], m[1]) for m in exact_matches]
    elif partial_matches:
        # 部分一致の場合、マッチ長が長い順にソート
        partial_matches.sort(key=lambda x: x[2], reverse=True)
        matches = [(m[0], m[1]) for m in partial_matches]
    else:
        # Phase 1.5: 複数単語検索（スペース含む場合）
        if ' ' in text or '　' in text:
            multiword_result = identify_model_multiword(text, db)
            if multiword_result:
                return multiword_result
        
        return None
    
    # Phase 2: バージョン絞り込み
    if input_version:
        # ワイルドカード処理（例: "2.x" → "2.1", "2.2"等にマッチ）
        if '.x' in input_version:
            base_version = input_version.split('.')[0]
            filtered = [m for m in matches if m[1]['version'].startswith(base_version + '.')]
        else:
            # 完全一致優先
            filtered = [m for m in matches if m[1]['version'] == input_version]
            
            # 小数点なし（例: "3"）の場合、"3.0"にもマッチ
            if not filtered and '.' not in input_version:
                # ただし、"3.5"がある場合は"3"で"3.5"を選ばない（厳密マッチ）
                filtered = [m for m in matches if m[1]['version'].split('.')[0] == input_version]
                # さらに絞り込み: "3.0"を優先、"3.5"は除外
                exact_matches = [m for m in filtered if m[1]['version'] == f"{input_version}.0"]
                if exact_matches:
                    filtered = exact_matches
        
        if filtered:
            matches = filtered
    
    # Phase 3: 最も関連性の高いものを返す（最初のマッチ）
    return matches[0][0] if matches else None


def find_closest_resolution(target_width: int, target_height: int,
                           resolutions: List[Dict]) -> Dict:
    """
    最も近いアスペクト比の解像度を選択

    Args:
        target_width: 希望する幅
        target_height: 希望する高さ
        resolutions: 解像度候補のリスト

    Returns:
        最も近いアスペクト比の解像度情報
    """
    target_ratio = target_width / target_height
    min_diff = float('inf')
    best_match = resolutions[0]  # デフォルト: 最初の解像度

    for res in resolutions:
        res_ratio = res['width'] / res['height']
        diff = abs(res_ratio - target_ratio)
        if diff < min_diff:
            min_diff = diff
            best_match = res

    return best_match


def builtin_optimal_latent(engine, text, width, height):
    """
    モデル名とアスペクト比から最適なLatentサイズを返す

    Args:
        engine: ScriptEngineインスタンス
        text: モデル名ヒント (str)
        width: 希望幅 (int/float)
        height: 希望高さ (int/float)

    Returns:
        [optimal_width, optimal_height] (list)

    使用例:
        result = OPTIMAL_LATENT("SDXL", 1200, 900)
        PRINT result(0) & "x" & result(1)
    """
    try:
        # データベース取得
        db = get_database()

        # 型変換
        width = int(width)
        height = int(height)

        # モデル識別
        model_key = identify_model(str(text), db)

        if model_key is None:
            # デフォルト: SD1.5の512x512
            engine.print_stack.append("WARNING: Model not identified. Using default (SD1.5 512x512)")
            return [512, 512]

        model_data = db.models[model_key]

        # アスペクト比選択
        resolution = find_closest_resolution(width, height, model_data['resolutions'])

        # ログ出力
        log_message = f"Model: {model_data['display_name']} | Optimal: {resolution['width']}x{resolution['height']} ({resolution['ratio']})"
        engine.print_stack.append(log_message)

        # 結果返却
        return [resolution['width'], resolution['height']]

    except Exception as e:
        engine.print_stack.append(f"ERROR in OPTIMAL_LATENT: {str(e)}")
        return [512, 512]  # フォールバック
