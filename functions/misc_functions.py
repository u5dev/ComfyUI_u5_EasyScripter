# -*- coding: utf-8 -*-
"""
その他の関数（型変換、論理関数、配列関数など）のモジュール
Miscellaneous functions (type conversion, logical functions, array functions, etc.) module
"""

from typing import Any, List, Optional
from datetime import datetime
import os
from pathlib import Path

# グローバルインポート（CLAUDE.md動的インポート禁止ルールに準拠）
# 相対インポートを試し、失敗時はフォールバック（テスト環境対応）
try:
    from .base_functions import BaseFunctions
    from ..type_detector import detect_any_type, extract_dimensions
    from ..locales import get_message
except ImportError:
    from functions.base_functions import BaseFunctions
    try:
        from type_detector import detect_any_type, extract_dimensions
    except ImportError:
        # type_detectorがない環境用フォールバック
        def detect_any_type(data):
            return "unknown"
        def extract_dimensions(data):
            return {"width": 0, "height": 0}
    try:
        from locales import get_message
    except ImportError:
        # localesがない環境用フォールバック
        def get_message(key: str, locale: str = 'en', *args) -> str:
            return key

# OUTPUT関数用のオプショナル依存（Phase 0調査に基づく）
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import folder_paths
    HAS_FOLDER_PATHS = True
except ImportError:
    HAS_FOLDER_PATHS = False

class MiscFunctions:
    """その他の関数のクラス"""

    @staticmethod
    def VAL(value: Any) -> float:
        """
        文字列を数値に変換

        Args:
            value: 文字列または数値

        Returns:
            数値（変換できない場合は0）
        """
        if value is None or value == "":
            return 0.0
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, bool):
            return 1.0 if value else 0.0

        # 文字列の場合
        try:
            # 文字列から数値部分を抽出
            str_value = str(value).strip()
            # 先頭の符号を確認
            sign = 1
            if str_value and str_value[0] == '-':
                sign = -1
                str_value = str_value[1:]
            elif str_value and str_value[0] == '+':
                str_value = str_value[1:]

            # 数値部分を抽出（最初の非数値文字まで）
            num_str = ""
            decimal_found = False
            for char in str_value:
                if char.isdigit():
                    num_str += char
                elif char == '.' and not decimal_found:
                    num_str += char
                    decimal_found = True
                else:
                    break

            if num_str and num_str != ".":
                return float(num_str) * sign
            else:
                return 0.0
        except:
            return 0.0

    # IF関数は base_functions.py に移動

    @staticmethod
    def IIF(condition: Any, true_value: Any, false_value: Any) -> Any:
        """
        即座IF関数（VBA互換）

        Args:
            condition: 評価する条件
            true_value: 条件が真の場合の返値
            false_value: 条件が偽の場合の返値

        Returns:
            条件に応じたtrue_valueまたはfalse_value
        """
        # IF関数と同じ動作（BaseFunctionsから）
        return BaseFunctions.IF(condition, true_value, false_value)

    @staticmethod
    def FORMAT(value: Any, format_string: str = "") -> str:
        """
        VBAのFormat関数を模倣
        数値、文字列を指定のフォーマットで整形

        Args:
            value: フォーマット対象の値
            format_string: フォーマット指定子

        Returns:
            フォーマット済み文字列
        """
        # フォーマット指定が空の場合は値そのものを返却
        if not format_string:
            return str(value)

        try:
            # 【CRITICAL】VBA形式の簡易指定を最優先でチェック（Python標準format()より前）
            if isinstance(value, (int, float)):
                lowered = format_string.lower()
                if lowered == "0":
                    return str(int(round(float(value))))
                if lowered == "0.0":
                    return f"{float(value):.1f}"
                if lowered == "0.00":
                    return f"{float(value):.2f}"
                if lowered in {"#", "#.#", "#.##"}:
                    return f"{float(value):g}"

            # Python の format 構文 (例: "{:.2f}") をそのまま扱う
            if "{" in format_string and "}" in format_string:
                # 【FIX】整数書式指定子（d, b, o, x, X）の場合、valueをintにキャスト
                # これにより、Parser経由で4.0として渡された値でも正しく整数フォーマット可能
                import re
                if isinstance(value, (int, float)) and re.search(r'\{[^}]*[dboxX]\}', format_string):
                    value = int(value)
                return format_string.format(value)

            # strftime 互換指定子を含む場合は日時フォーマットとして扱う
            if "%" in format_string:
                from datetime import datetime as _dt
                dt_candidates = []
                if hasattr(value, "strftime"):
                    dt_candidates.append(value)
                if isinstance(value, str):
                    for fmt in ("%Y/%m/%d %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d", "%Y-%m-%d", "%H:%M:%S"):
                        try:
                            dt_candidates.append(_dt.strptime(value, fmt))
                            break
                        except ValueError:
                            continue
                if not dt_candidates:
                    dt_candidates.append(_dt.now())
                return dt_candidates[0].strftime(format_string)

            # format(value, spec) 形式をサポート (例: ".2f", ",")
            try:
                return format(value, format_string)
            except (ValueError, TypeError):
                pass

            # デフォルトは文字列として返す
            return str(value)
        except Exception:
            return str(value)

    @staticmethod
    def CSTR(value: Any) -> str:
        """
        値を文字列に変換（VBA互換）

        Args:
            value: 変換する値

        Returns:
            文字列化された値
        """
        if value is None:
            return ""
        # VBA準拠: 論理値は数値として扱われる（True=1, False=0）
        elif isinstance(value, bool):
            return "1" if value else "0"
        elif isinstance(value, float):
            # 整数値の場合は小数点なしで表示
            # 論理値（1.0/0.0）も整数として表示
            if value.is_integer():
                return str(int(value))
            return str(value)
        else:
            return str(value)

    @staticmethod
    def CINT(value: Any) -> float:
        """
        値を整数に変換（VBA互換で四捨五入）
        注: ComfyUI内部では数値は全てfloatで扱うため、floatを返す

        Args:
            value: 変換する値

        Returns:
            整数値（floatとして）- 四捨五入される
        """
        try:
            if value is None or value == "":
                return 0.0
            elif isinstance(value, bool):
                return 1.0 if value else 0.0
            elif isinstance(value, str):
                # True/Falseの文字列処理
                val_upper = str(value).upper()
                if val_upper == "TRUE":
                    return 1.0
                elif val_upper == "FALSE":
                    return 0.0
                # 数値文字列の処理 - VBA準拠で四捨五入
                return float(round(float(value)))
            else:
                # VBA準拠で四捨五入
                return float(round(float(value)))
        except:
            return 0.0

    @staticmethod
    def CDBL(value: Any) -> float:
        """
        値を浮動小数点数に変換（VBA互換）

        Args:
            value: 変換する値

        Returns:
            浮動小数点値
        """
        try:
            if value is None or value == "":
                return 0.0
            elif isinstance(value, bool):
                return 1.0 if value else 0.0
            elif isinstance(value, str):
                # True/Falseの文字列処理
                val_upper = str(value).upper()
                if val_upper == "TRUE":
                    return 1.0
                elif val_upper == "FALSE":
                    return 0.0
                # 数値文字列の処理
                return float(value)
            else:
                return float(value)
        except:
            return 0.0

    @staticmethod
    def ISNUMERIC(value: Any) -> float:
        """
        値が数値かどうかを判定（VBA互換）

        Args:
            value: 判定する値

        Returns:
            数値の場合1.0、そうでない場合0.0
        """
        if value is None:
            return 0.0
        try:
            # 文字列の場合は変換を試みる
            if isinstance(value, str):
                # 空文字列は数値ではない
                if value.strip() == "":
                    return 0.0
                # True/Falseは数値として扱わない
                val_upper = value.upper()
                if val_upper in ["TRUE", "FALSE"]:
                    return 0.0
                float(value)
                return 1.0
            # 数値型の場合は真
            elif isinstance(value, (int, float)):
                return 1.0
            # bool型も数値として扱う
            elif isinstance(value, bool):
                return 1.0
            else:
                return 0.0
        except:
            return 0.0

    @staticmethod
    def ISDATE(value: Any) -> float:
        """
        値が日付として解析可能かを判定（VBA互換）

        Args:
            value: 判定する値

        Returns:
            日付として解析可能な場合1.0、そうでない場合0.0
        """
        if value is None or value == "":
            return 0.0

        try:
            date_str = str(value).strip()
            # 様々な日付形式でパースを試みる
            for fmt in ["%Y/%m/%d %H:%M:%S", "%Y/%m/%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d",
                       "%m/%d/%Y", "%d/%m/%Y", "%Y年%m月%d日", "%H:%M:%S", "%H:%M"]:
                try:
                    datetime.strptime(date_str, fmt)
                    return 1.0
                except ValueError:
                    continue
            return 0.0
        except:
            return 0.0

    @staticmethod
    def ISARRAY(variable_name: str) -> float:
        """
        変数が配列かどうかを判定（VBA互換）
        注: この関数はスクリプトエンジンから特殊処理される

        Args:
            variable_name: 判定する変数名

        Returns:
            配列の場合1.0、そうでない場合0.0
        """
        # この関数はscript_engine.pyで特殊処理される
        # ここではデフォルト値を返す
        return 0.0

    @staticmethod
    def TYPE(value: Any) -> str:
        """
        変数の型を文字列で返す

        Args:
            value: 型を調べたい値

        Returns:
            型名（"NUMBER", "STRING", "BOOLEAN", "ARRAY", "NULL"）
        """
        if value is None:
            return "NULL"
        elif isinstance(value, bool):
            return "BOOLEAN"
        elif isinstance(value, (int, float)):
            return "NUMBER"
        elif isinstance(value, list):
            return "ARRAY"
        elif isinstance(value, str):
            return "STRING"
        else:
            return "OBJECT"

    # 配列関数
    @staticmethod
    def ARRAY(*elements) -> list:
        """
        配列を作成

        Args:
            *elements: 配列の要素

        Returns:
            要素のリスト
        """
        return list(elements)

    @staticmethod
    def UBOUND(array: Any, dimension: int = 1) -> float:
        """
        配列の上限インデックスを取得

        Args:
            array: 配列
            dimension: 次元（現在は1次元のみサポート）

        Returns:
            上限インデックス（要素数-1）
        """
        if isinstance(array, list):
            return float(len(array) - 1) if len(array) > 0 else -1.0
        else:
            return -1.0

    @staticmethod
    def REDIM(array_name: str, size: Any) -> list:
        """
        配列のサイズを変更
        注: この関数はスクリプトエンジンから特殊処理される

        Args:
            array_name: 配列変数名
            size: 新しいサイズ（要素数）

        Returns:
            新しい配列
        """
        # この関数はscript_engine.pyで特殊処理される
        try:
            new_size = int(float(size))
            if new_size >= 0:
                return [None] * new_size  # 指定されたサイズの配列を作成
            else:
                return []
        except:
            return []

    # ===== ANY型関数 =====
    # ComfyUIのANY型入力（any_input）の型判定とメタデータ取得用関数

    @staticmethod
    def GETANYTYPE(any_data: Any = None) -> str:
        """
        ANY型データの型名を返す

        Args:
            any_data: 型判定対象のデータ（省略時はNone扱い）

        Returns:
            型名: "int", "float", "string", "image", "latent", "model", "vae",
                  "clip", "conditioning", "lora", "none", "unknown"
        """
        return detect_any_type(any_data)

    @staticmethod
    def GETANYWIDTH(any_data: Any = None) -> float:
        """
        IMAGE/LATENT型の幅を返す

        Args:
            any_data: IMAGE/LATENTデータ

        Returns:
            幅（ピクセル数、取得できない場合は0）
        """
        try:
            dims = extract_dimensions(any_data)
            return float(dims["width"])
        except:
            return 0.0

    @staticmethod
    def GETANYHEIGHT(any_data: Any = None) -> float:
        """
        IMAGE/LATENT型の高さを返す

        Args:
            any_data: IMAGE/LATENTデータ

        Returns:
            高さ（ピクセル数、取得できない場合は0）
        """
        try:
            dims = extract_dimensions(any_data)
            return float(dims["height"])
        except:
            return 0.0

    @staticmethod
    def GETANYVALUEINT(any_data: Any = None) -> float:
        """
        INT型の値を返す

        Args:
            any_data: データ

        Returns:
            INT値（INT型でない場合は0）
        """
        if isinstance(any_data, int) and not isinstance(any_data, bool):
            return float(any_data)
        return 0.0

    @staticmethod
    def GETANYVALUEFLOAT(any_data: Any = None) -> float:
        """
        FLOAT型の値を返す

        Args:
            any_data: データ

        Returns:
            FLOAT値（数値型でない場合は0.0）
        """
        if isinstance(any_data, (int, float)) and not isinstance(any_data, bool):
            return float(any_data)
        return 0.0

    @staticmethod
    def GETANYSTRING(any_data: Any = None) -> str:
        """
        STRING型の値を返す

        Args:
            any_data: データ

        Returns:
            STRING値（STRING型でない場合は空文字列）
        """
        if isinstance(any_data, str):
            return any_data
        return ""

    @staticmethod
    def OUTPUT(arg: Any, path: str = "", flg: str = "NEW", locale: str = "ja") -> str:
        """
        引数をファイルに出力し、出力したファイルの絶対パスを返す

        Args:
            arg: 出力する値（文字列、数値、配列、画像、バイナリ）
                 または予約変数参照（"TXT1", "TXT2", "ANY_INPUT"）
            path: 出力ファイルパス（ComfyUI出力フォルダからの相対パス）
                  省略時は型に応じた自動ファイル名
            flg: 出力モード（"NEW"=新規作成、"ADD"=追記）デフォルトは"NEW"
            locale: ロケール（'en'または'ja'）

        Returns:
            出力したファイルの絶対パス
        """
        # ComfyUI出力ディレクトリ取得（グローバルインポート使用）
        if HAS_FOLDER_PATHS:
            output_dir = folder_paths.get_output_directory()
        else:
            # folder_pathsが利用できない場合（テスト環境等）
            output_dir = os.path.join(os.getcwd(), "output")
            os.makedirs(output_dir, exist_ok=True)
        
        # 第1引数: 予約変数文字列から実際の値を取得
        # 注: "TXT1", "TXT2", "ANY_INPUT" の処理は script_engine.py で行われる想定
        # ここでは引数として渡された値をそのまま使用
        value = arg
        
        # 絶対パス・UNCパスチェック（セキュリティ）
        if isinstance(path, str) and path:
            if (len(path) >= 2 and path[1] == ':') or path.startswith('\\\\'):
                print(get_message('output_warning_absolute_path', locale, path))
                return ""
        
        # 型判定
        value_type = _detect_output_type(value)
        
        # パス解決
        resolved_path = _resolve_output_path(output_dir, path, value_type)
        
        # 出力モード処理
        mode_upper = flg.upper() if isinstance(flg, str) else "NEW"
        if mode_upper == "NEW":
            # 重複時は_NNNN付与
            resolved_path = _handle_duplicate_filename(resolved_path)
        
        # ファイル出力
        try:
            if value_type == "image":
                _write_image_file(value, resolved_path, mode_upper)
            elif value_type in ("text", "number", "array"):
                _write_text_file(value, resolved_path, mode_upper, value_type)
            else:  # binary
                _write_binary_file(value, resolved_path, mode_upper)

            return str(Path(resolved_path).absolute())
        except Exception as e:
            print(get_message('output_error_file_write', locale, e))
            return ""

    @staticmethod
    def INPUT(path: str, locale: str = "ja") -> Any:
        r"""
        ファイル読み込み関数（OUTPUT関数の対称関数）

        Args:
            path: ファイルパス（相対パスまたは絶対パス）
                 - 相対パス: ComfyUI出力フォルダからの相対パス
                 - 絶対パス: Windows絶対パス（C:\...）またはUNCパス（\\server\share）を自動検出
            locale: ロケール（'en'または'ja'）

        Returns:
            読み込んだデータ（型は自動判定: str/float/list/torch.Tensor/bytes）
            ファイル未検出時またはエラー時は None を返す
        """
        # 1. パス種別を自動判定（os.path.isabs()で絶対パス/UNCパスを検出）
        if os.path.isabs(path):
            # 絶対パスまたはUNCパスの場合はそのまま使用
            full_path = path
        else:
            # 2. 相対パスの場合はComfyUI出力ディレクトリと結合
            if HAS_FOLDER_PATHS:
                output_dir = folder_paths.get_output_directory()
            else:
                # folder_pathsが利用できない場合（テスト環境等）
                # 環境変数TEST_OUTPUT_DIRがあればそれを使用
                output_dir = os.environ.get('TEST_OUTPUT_DIR', os.path.join(os.getcwd(), "output"))
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir, exist_ok=True)

            full_path = os.path.join(output_dir, path)

        # 3. ファイル存在確認
        if not os.path.exists(full_path):
            print(get_message('input_warning_file_not_found', locale, path))
            return None  # SKIP扱い

        # 4. ファイル形式判定
        file_type = _detect_input_type(full_path)

        # 5. 型別読み込み
        try:
            if file_type == "text":
                return _load_text_file(full_path)
            elif file_type == "json":
                return _load_json_file(full_path)
            elif file_type == "image":
                return _load_image_file(full_path, locale)
            else:  # binary
                return _load_binary_file(full_path)
        except Exception as e:
            print(get_message('input_error_file_read', locale, e))
            return None

    @staticmethod
    def ISFILEEXIST(path: str, flg: str = "", locale: str = "ja") -> Any:
        """
        ファイル存在チェック関数（拡張版）

        Args:
            path: ComfyUI出力フォルダからの相対パス（必須）
            flg: オプションフラグ（デフォルト: ""）
                 ""      - ファイル存在をTRUE/FALSEで返す
                 "NNNN"  - _NNNN付きファイルの最大番号パスを返す（相対パス）
                 "PIXEL" - 画像の場合、[width, height]配列を返す
                 "SIZE"  - ファイルサイズ（バイト）を返す
            locale: ロケール（'en'または'ja'）

        Returns:
            flg=""     : "TRUE" or "FALSE"
            flg="NNNN" : 最大番号ファイルの相対パス or "FALSE"
            flg="PIXEL": [width, height] or "FALSE"
            flg="SIZE" : ファイルサイズ(int) or "FALSE"
        """
        # 1. パス検証（絶対パス/UNCパス拒否）
        if isinstance(path, str) and path:
            # Windows絶対パス: C:\, D:\, etc.
            if (len(path) >= 2 and path[1] == ':'):
                print(get_message('isfileexist_warning_absolute_path', locale, path))
                return "FALSE"
            # UNCパス: \\server\share
            if path.startswith('\\\\'):
                print(get_message('isfileexist_warning_unc_path', locale, path))
                return "FALSE"
        
        # 2. ComfyUI出力ディレクトリ取得
        if HAS_FOLDER_PATHS:
            output_dir = folder_paths.get_output_directory()
        else:
            # テスト環境用
            output_dir = os.environ.get('TEST_OUTPUT_DIR', os.path.join(os.getcwd(), "output"))
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
        
        # 3. フルパス構築
        full_path = os.path.join(output_dir, path)
        
        # 4. フラグ処理
        flg_upper = flg.upper() if isinstance(flg, str) else ""
        
        if flg_upper == "":
            # デフォルト: 存在チェックのみ
            return "TRUE" if os.path.exists(full_path) else "FALSE"
        
        elif flg_upper == "NNNN":
            # _NNNN付きファイルの最大番号検索
            return _find_max_numbered_file(output_dir, path)
        
        elif flg_upper == "PIXEL":
            # 画像サイズ取得
            return _get_image_pixel_size(full_path, locale)
        
        elif flg_upper == "SIZE":
            # ファイルサイズ取得
            if not os.path.exists(full_path):
                return "FALSE"
            try:
                size = os.path.getsize(full_path)
                return str(size)
            except Exception as e:
                print(get_message('isfileexist_error_size', locale, e))
                return "FALSE"

        else:
            # 不明なフラグ → デフォルト動作
            print(get_message('isfileexist_warning_unknown_flag', locale, flg))
            return "TRUE" if os.path.exists(full_path) else "FALSE"

    @staticmethod
    def VRAMFREE(min_free_vram_gb: float = 0.0) -> Any:
        """
        VRAMとRAMを解放する関数（モデルアンロード、キャッシュクリア）
        
        **WARNING**: この関数は実行タイミングによって想定外の結果を引き起こす可能性があります。
        モデルのアンロードはデリケートな操作であり、ワークフロー実行中に
        予期しない動作を引き起こすリスクがあります。
        
        Args:
            min_free_vram_gb: クリーンアップ実行の閾値（GB）
                              現在の空きVRAMがこの値以上の場合、処理をスキップ
                              デフォルト: 0.0（常に実行）
        
        Returns:
            dict: 実行結果の詳細情報
                {
                    "success": bool,
                    "message": str,
                    "freed_vram_gb": float,
                    "freed_ram_gb": float,
                    "initial_status": dict,
                    "final_status": dict,
                    "actions_performed": list
                }
        
        Example:
            ' 常に実行（閾値なし）
            result = VRAMFREE(0.0)
            
            ' 空きVRAMが2GB未満の場合のみ実行
            result = VRAMFREE(2.0)
        """
        import gc
        import sys
        import time
        import logging
        
        # オプショナル依存関係
        try:
            import torch
            HAS_TORCH = True
        except ImportError:
            HAS_TORCH = False
        
        try:
            import comfy.model_management
            HAS_COMFY = True
        except ImportError:
            HAS_COMFY = False
            logging.warning("ComfyUI model_management not found. VRAMFREE running in limited mode.")
        
        # ヘルパー関数: メモリ状態取得
        def get_memory_status():
            status = {
                "free_vram_gb": 0.0,
                "total_vram_gb": 0.0,
                "used_vram_gb": 0.0,
                "free_ram_gb": 0.0,
                "total_ram_gb": 0.0,
                "used_ram_gb": 0.0,
            }
            
            # GPU メモリ情報
            if HAS_TORCH and torch.cuda.is_available():
                try:
                    free_vram, total_vram = torch.cuda.mem_get_info()
                    status["free_vram_gb"] = free_vram / (1024**3)
                    status["total_vram_gb"] = total_vram / (1024**3)
                    status["used_vram_gb"] = status["total_vram_gb"] - status["free_vram_gb"]
                except Exception as e:
                    logging.warning(f"Failed to get CUDA memory info: {e}")
            
            # システムメモリ情報
            try:
                import psutil
                ram = psutil.virtual_memory()
                status["free_ram_gb"] = ram.available / (1024**3)
                status["total_ram_gb"] = ram.total / (1024**3)
                status["used_ram_gb"] = ram.used / (1024**3)
            except ImportError:
                pass
            except Exception as e:
                logging.warning(f"Failed to get system memory info: {e}")
            
            return status
        
        # ヘルパー関数: メモリサイズフォーマット
        def format_memory_size(size_gb):
            if size_gb < 0.001:
                return "0 GB"
            elif size_gb < 1:
                return f"{size_gb * 1024:.1f} MB"
            else:
                return f"{size_gb:.2f} GB"
        
        # 結果辞書の初期化
        result = {
            "success": True,
            "message": "",
            "freed_vram_gb": 0.0,
            "freed_ram_gb": 0.0,
            "initial_status": {},
            "final_status": {},
            "actions_performed": []
        }
        
        # 初期メモリ状態取得
        result["initial_status"] = get_memory_status()
        current_free_vram = result["initial_status"].get("free_vram_gb", 0.0)
        
        # 閾値チェック（スキップ判定）
        if min_free_vram_gb > 0 and current_free_vram >= min_free_vram_gb:
            result["final_status"] = result["initial_status"]
            result["success"] = True
            result["message"] = (
                f"Cleanup skipped (current free VRAM "
                f"{format_memory_size(current_free_vram)} >= "
                f"threshold {format_memory_size(min_free_vram_gb)})"
            )
            result["actions_performed"].append("Threshold satisfied: cleanup skipped")
            logging.info("VRAMFREE: threshold satisfied - cleanup skipped")
            return result
        
        try:
            # 1. モデルのアンロード (ComfyUI API)
            if HAS_COMFY:
                try:
                    comfy.model_management.unload_all_models()
                    result["actions_performed"].append("Models unloaded")
                    logging.info("Models unloaded successfully")
                except Exception as e:
                    logging.warning(f"Failed to unload models: {e}")
                    result["actions_performed"].append(f"Model unload failed: {e}")
            
            # 2. ソフトキャッシュのクリア (ComfyUI)
            if HAS_COMFY:
                try:
                    comfy.model_management.soft_empty_cache(True)
                    result["actions_performed"].append("Comfy cache cleared")
                    logging.info("ComfyUI soft cache cleared successfully")
                except Exception as e:
                    logging.warning(f"Failed to clear ComfyUI cache: {e}")
                    result["actions_performed"].append(f"Comfy cache clear failed: {e}")
            
            # 3. PyTorchキャッシュクリア
            if HAS_TORCH and torch.cuda.is_available():
                try:
                    torch.cuda.empty_cache()
                    torch.cuda.ipc_collect()
                    result["actions_performed"].append("GPU cache cleared")
                    logging.info("GPU cache cleared successfully")
                except Exception as e:
                    logging.warning(f"Failed to clear GPU cache: {e}")
                    result["actions_performed"].append(f"GPU cache clear failed: {e}")
            
            # 4. Pythonガベージコレクション (& ComfyGC)
            if HAS_COMFY:
                try:
                    comfy.model_management.cleanup_models_gc()
                    result["actions_performed"].append("Comfy model GC cleanup")
                except Exception as gc_err:
                    logging.warning(f"Failed to run Comfy model GC: {gc_err}")
                    result["actions_performed"].append(f"Comfy model GC failed: {gc_err}")
            
            try:
                collected = gc.collect(2)
                result["actions_performed"].append(f"GC collected {collected} objects")
                logging.info(f"Garbage collection completed: {collected} objects collected")
            except Exception as e:
                logging.warning(f"Failed to run garbage collection: {e}")
                result["actions_performed"].append(f"GC failed: {e}")
            
            # 5. prompt_queueへのフラグ設定（ComfyUI統合）
            if HAS_COMFY:
                prompt_queue = None
                prompt_server_module = sys.modules.get("server")
                if prompt_server_module is not None:
                    prompt_server_class = getattr(prompt_server_module, "PromptServer", None)
                    prompt_server_instance = getattr(prompt_server_class, "instance", None) if prompt_server_class else None
                    prompt_queue = getattr(prompt_server_instance, "prompt_queue", None) if prompt_server_instance else None
                if prompt_queue is not None:
                    try:
                        prompt_queue.set_flag("unload_models", True)
                        prompt_queue.set_flag("free_memory", True)
                        result["actions_performed"].append("Prompt queue flagged for cleanup")
                    except Exception as queue_err:
                        logging.warning(f"Failed to set prompt queue flags: {queue_err}")
                        result["actions_performed"].append(f"Prompt queue flag failed: {queue_err}")
            
            # 6. 非同期フラッシュの監視（3秒間ポーリング）
            final_status = get_memory_status()
            best_status = dict(final_status)
            best_vram = final_status.get("free_vram_gb", 0.0)
            best_ram = final_status.get("free_ram_gb", 0.0)
            
            async_observed = False
            if HAS_COMFY:
                deadline = time.time() + 3.0
                while time.time() < deadline:
                    time.sleep(0.15)
                    polled = get_memory_status()
                    polled_vram = polled.get("free_vram_gb", 0.0)
                    polled_ram = polled.get("free_ram_gb", 0.0)
                    if polled_vram > best_vram + 0.01 or polled_ram > best_ram + 0.01:
                        best_status = polled
                        best_vram = polled_vram
                        best_ram = polled_ram
                        async_observed = True
                
                if async_observed:
                    delta_info = []
                    vram_delta = best_vram - final_status.get("free_vram_gb", 0.0)
                    if vram_delta > 0.01:
                        delta_info.append(f"VRAM +{format_memory_size(vram_delta)}")
                    ram_delta = best_ram - final_status.get("free_ram_gb", 0.0)
                    if ram_delta > 0.01:
                        delta_info.append(f"RAM +{format_memory_size(ram_delta)}")
                    if delta_info:
                        result["actions_performed"].append("Async flush observed: " + ", ".join(delta_info))
            
            # 最終状態と解放量の計算
            result["final_status"] = best_status
            result["freed_vram_gb"] = max(0, best_vram - result["initial_status"]["free_vram_gb"])
            result["freed_ram_gb"] = max(0, best_ram - result["initial_status"]["free_ram_gb"])
            result["success"] = True
            result["message"] = f"Cleanup completed. Actions: {', '.join(result['actions_performed'])}"
            
        except Exception as e:
            result["success"] = False
            result["message"] = f"Cleanup failed: {str(e)}"
            logging.error(f"Memory cleanup failed: {e}")
        
        return result

    @staticmethod
    def SLEEP(milliseconds: Any = 10) -> float:
        """
        指定ミリ秒だけスリープする関数
        
        **設計思想**:
        - ComfyUIのスレッドベースキューイング制御（ScriptExecutionQueue）と協調動作
        - 同期的にtime.sleep()でブロック → 他のノードはキューで待機
        - asyncio非使用（ComfyUIはイベントループ駆動ではない）
        
        **用途**:
        - WHILE()ループの速度制御（CPU使用率低減）
        - 処理待ち合わせ（外部API rate limit対応等）
        
        **複数ノード同時実行時の動作**:
        - EasyScripterノードAがSLEEP(5000)実行中、ノードBはキューで待機
        - スレッドセーフはScriptExecutionQueueが保証（追加ロック不要）
        
        Args:
            milliseconds: スリープ時間（ミリ秒）デフォルト: 10ms
                         - 数値型（int/float）に変換可能な値
                         - 負数・ゼロの場合は即座にリターン
        
        Returns:
            float: 常に0.0（戻り値は使用されない想定）
        
        Raises:
            なし（エラー時は警告PRINT + 即座にリターン）
        
        Examples:
            ' デフォルト10msスリープ
            SLEEP()
            
            ' 0.5秒スリープ
            SLEEP(500)
            
            ' WHILE()ループの速度制御
            WHILE VAL1 < 100
                VAL1 = VAL1 + 1
                SLEEP(100)  ' 100ms待機（CPU使用率低減）
            WEND
            
            ' 外部API呼び出し間隔制御
            SLEEP(1000)  ' 1秒待機
            result = HTTP_GET("https://api.example.com/data")
        
        Notes:
            - 精度: OSのスケジューラ依存（Windowsで約15ms、Linuxで約1ms）
            - 長時間スリープ: ComfyUIのタイムアウト（デフォルト120秒）に注意
            - WHILE()ループでの使用推奨: SLEEP()なしの無限ループはCPU 100%消費
        """
        import time
        
        try:
            # ミリ秒 → 秒に変換
            ms = float(milliseconds)
            
            # 負数・ゼロチェック
            if ms <= 0:
                return 0.0
            
            # スリープ実行（秒単位）
            time.sleep(ms / 1000.0)
            
            return 0.0
            
        except (ValueError, TypeError) as e:
            # 型変換エラー → 警告PRINTして即座にリターン
            print(f"SLEEP(): Invalid milliseconds value '{milliseconds}' ({type(milliseconds).__name__}). Skipping sleep.")
            return 0.0
        except Exception as e:
            # 予期しないエラー → 警告PRINTして即座にリターン
            print(f"SLEEP(): Unexpected error - {type(e).__name__}: {e}. Skipping sleep.")
            return 0.0

    @staticmethod
    def IMAGETOBYTEARRAY(image_input, max_size: int = 336, format: str = "PNG", return_format: str = "bytes"):
        """
        画像をリサイズしてバイト配列またはJSON配列文字列に変換（Cloudflare API用）
        
        目的:
            REST API（特にCloudflare Workers AI）に送信するための
            画像データの前処理を行います。
        
        Args:
            image_input: 画像ファイルパス（str）またはIMAGE tensor（torch.Tensor）
            max_size: リサイズ後の最大サイズ（長辺、デフォルト336px）
            format: 出力形式（"PNG", "JPEG"等、デフォルト"PNG"）
            return_format: 戻り値の形式（"bytes"または"json"、デフォルト"bytes"）
        
        Returns:
            bytes: return_format="bytes"の場合、画像データのバイト配列
            str: return_format="json"の場合、整数配列のJSON文字列
                 例: "[137, 80, 78, 71, 13, 10, ...]"
        
        Raises:
            FileNotFoundError: 画像ファイルが存在しない（文字列入力時）
            RuntimeError: 画像処理エラー
            ValueError: return_format が無効、または画像サイズが不正
            TypeError: 無効な入力型
        
        使用例:
            ```vba
            ' ファイルパス入力（従来の方法）
            json_array = IMAGETOBYTEARRAY("C:/path/to/image.png", 336, "JPEG", "json")
            
            ' IMAGE tensor入力（ComfyUIノード接続から）
            ' VAL1にPreviewImageノード等からIMAGE型が渡される
            json_array = IMAGETOBYTEARRAY(VAL1, 336, "JPEG", "json")
            ```
        
        エンコーディング仕様:
            - Base64ではない
            - MIMEエンコードではない
            - return_format="bytes": 生のバイナリデータをbytes型で返す
            - return_format="json": 整数配列 [0-255] のJSON文字列を返す
            - Cloudflare APIでは、JSON配列形式が直接使用可能
        """
        if not HAS_PIL:
            raise RuntimeError("PIL_NOT_AVAILABLE: PIL (Pillow) is not installed. Install with: pip install Pillow")
        
        # return_format検証
        valid_return_formats = ["bytes", "json"]
        if return_format not in valid_return_formats:
            raise ValueError(f"INVALID_RETURN_FORMAT: return_format must be one of {valid_return_formats}, got: {return_format}")
        
        from PIL import Image
        from io import BytesIO
        from pathlib import Path
        import json
        
        # 入力型判定と画像読み込み
        image = None
        
        # パターン1: 文字列（ファイルパス）
        if isinstance(image_input, str):
            print(f"[IMAGETOBYTEARRAY DEBUG] Input type: file path (str)")
            image_file = Path(image_input)
            if not image_file.exists():
                raise FileNotFoundError(f"IMAGE_NOT_FOUND: Image file not found: {image_input}")
            
            image = Image.open(image_input)
            print(f"[IMAGETOBYTEARRAY DEBUG] Loaded from file: {image_input}")
        
        # パターン2: torch.Tensor（ComfyUI IMAGE形式）
        else:
            # torchがインポート可能かチェック
            try:
                import torch
                HAS_TORCH = True
            except ImportError:
                HAS_TORCH = False
            
            if HAS_TORCH and torch.is_tensor(image_input):
                print(f"[IMAGETOBYTEARRAY DEBUG] Input type: torch.Tensor (ComfyUI IMAGE)")
                
                # ComfyUI IMAGE形式: [batch, height, width, channels], 値は0.0-1.0
                if image_input.ndim != 4:
                    raise ValueError(f"INVALID_TENSOR_SHAPE: Expected 4D tensor [batch, height, width, channels], got shape: {image_input.shape}")
                
                # 最初のバッチを取得
                img_tensor = image_input[0]  # [height, width, channels]
                print(f"[IMAGETOBYTEARRAY DEBUG] Tensor shape: {img_tensor.shape}")
                
                # numpy配列に変換し、0-255にスケール
                import numpy as np
                img_array = img_tensor.cpu().numpy()
                img_array = (img_array * 255).clip(0, 255).astype(np.uint8)
                
                # PIL Imageに変換
                image = Image.fromarray(img_array, mode='RGB')
                print(f"[IMAGETOBYTEARRAY DEBUG] Converted tensor to PIL Image")
            else:
                # torch.Tensorでもない、文字列でもない → TypeError
                raise TypeError(f"INVALID_INPUT_TYPE: image_input must be str (file path) or torch.Tensor (IMAGE), got: {type(image_input)}")
        
        # 以降は共通処理
        original_width, original_height = image.size
        print(f"[IMAGETOBYTEARRAY DEBUG] Original size: {original_width}x{original_height}, mode: {image.mode}")
        
        # 画像サイズ検証（ゼロ除算防止）
        if original_width <= 0 or original_height <= 0:
            raise ValueError(f"INVALID_IMAGE_SIZE: Image size must be positive, got {original_width}x{original_height}")
        
        # JPEG形式の場合、RGBAをRGBに変換
        if format.upper() == "JPEG" and image.mode in ('RGBA', 'LA', 'P'):
            print(f"[IMAGETOBYTEARRAY DEBUG] Converting {image.mode} to RGB for JPEG")
            # 白背景でRGBに変換
            rgb_image = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            if image.mode == 'RGBA':
                rgb_image.paste(image, mask=image.split()[3])
            else:
                rgb_image.paste(image)
            image = rgb_image
        
        # リサイズ処理（アスペクト比維持）
        if original_width > max_size or original_height > max_size:
            # アスペクト比を計算（明示的にfloatで計算してからintに変換）
            if original_width > original_height:
                # 横長: 幅をmax_sizeに
                new_width = int(max_size)
                ratio = float(max_size) / float(original_width)
                new_height = int(float(original_height) * ratio)
            else:
                # 縦長または正方形: 高さをmax_sizeに
                new_height = int(max_size)
                ratio = float(max_size) / float(original_height)
                new_width = int(float(original_width) * ratio)
            
            # リサイズ後のサイズが最低1pxであることを保証
            new_width = max(1, new_width)
            new_height = max(1, new_height)
            
            print(f"[IMAGETOBYTEARRAY DEBUG] Resizing to: {new_width}x{new_height}")
            
            # リサイズ実行（LANCZOS = 1）
            resized_image = image.resize((new_width, new_height), 1)
            print(f"[IMAGETOBYTEARRAY DEBUG] Resized image size: {resized_image.size}")
        else:
            # リサイズ不要
            print(f"[IMAGETOBYTEARRAY DEBUG] No resize needed")
            resized_image = image
        
        # バイト配列に変換
        buffered = BytesIO()
        if format.upper() == "JPEG":
            # JPEG品質を50に設定してファイルサイズを削減
            resized_image.save(buffered, format=format, quality=50, optimize=True)
        else:
            resized_image.save(buffered, format=format)
        
        image_bytes = buffered.getvalue()
        bytes_length = len(image_bytes)
        print(f"[IMAGETOBYTEARRAY DEBUG] Bytes length: {bytes_length} ({bytes_length / 1024:.2f} KB)")
        
        # 戻り値形式に応じて変換
        if return_format == "bytes":
            return image_bytes
        elif return_format == "json":
            # bytes → list[int] → JSON文字列
            print(f"[IMAGETOBYTEARRAY DEBUG] Converting to JSON array...")
            image_list = list(image_bytes)
            print(f"[IMAGETOBYTEARRAY DEBUG] List length: {len(image_list)}")
            
            json_string = json.dumps(image_list)
            json_length = len(json_string)
            print(f"[IMAGETOBYTEARRAY DEBUG] JSON string length: {json_length} ({json_length / 1024:.2f} KB)")
            
            return json_string

    @staticmethod
    def IMAGETOBASE64(image_input, max_size: int = 512, format: str = "PNG", return_format: str = "base64"):
        """
        画像をリサイズしてBase64エンコードまたはdata URL形式に変換（Venice API等用）
        
        目的:
            REST API（特にVenice.ai、OpenAI Vision API）に送信するための
            画像データの前処理を行います。
        
        Args:
            image_input: 画像ファイルパス（str）またはIMAGE tensor（torch.Tensor）
            max_size: リサイズ後の最大サイズ（長辺、デフォルト512px）
            format: 出力形式（"PNG", "JPEG"等、デフォルト"PNG"）
            return_format: 戻り値の形式（"base64"または"data_url"、デフォルト"base64"）
        
        Returns:
            str: return_format="base64"の場合、Base64エンコードされた文字列
                 例: "iVBORw0KGgoAAAANSUhEUgAA..."
            str: return_format="data_url"の場合、data URL形式の文字列
                 例: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
        
        Raises:
            FileNotFoundError: 画像ファイルが存在しない（文字列入力時）
            RuntimeError: 画像処理エラー
            ValueError: return_format が無効、または画像サイズが不正
            TypeError: 無効な入力型
        
        使用例:
            ```vba
            ' ファイルパス入力（従来の方法）
            base64_str = IMAGETOBASE64("C:/path/to/image.png", 512, "PNG", "base64")
            
            ' IMAGE tensor入力（ComfyUIノード接続から）
            ' ANY_INPUTにLoadImageノード等からIMAGE型が渡される
            data_url = IMAGETOBASE64(ANY_INPUT, 512, "PNG", "data_url")
            
            ' Venice.ai Vision API送信例
            api_key = TXT1
            model = TXT2
            data_url = IMAGETOBASE64(ANY_INPUT, 512, "PNG", "data_url")
            ' ... HTTPJSON でAPI呼び出し
            ```
        
        エンコーディング仕様:
            - Base64標準エンコーディング
            - return_format="base64": Base64文字列のみを返す
            - return_format="data_url": data URL形式（"data:image/png;base64,..."）で返す
            - Venice.ai、OpenAI等のVision APIで直接使用可能
        """
        if not HAS_PIL:
            raise RuntimeError("PIL_NOT_AVAILABLE: PIL (Pillow) is not installed. Install with: pip install Pillow")
        
        # return_format検証
        valid_return_formats = ["base64", "data_url"]
        if return_format not in valid_return_formats:
            raise ValueError(f"INVALID_RETURN_FORMAT: return_format must be one of {valid_return_formats}, got: {return_format}")
        
        from PIL import Image
        from io import BytesIO
        from pathlib import Path
        import base64
        
        # 入力型判定と画像読み込み
        image = None
        
        # パターン1: 文字列（ファイルパス）
        if isinstance(image_input, str):
            print(f"[IMAGETOBASE64 DEBUG] Input type: file path (str)")
            image_file = Path(image_input)
            if not image_file.exists():
                raise FileNotFoundError(f"IMAGE_NOT_FOUND: Image file not found: {image_input}")
            
            image = Image.open(image_input)
            print(f"[IMAGETOBASE64 DEBUG] Loaded from file: {image_input}")
        
        # パターン2: torch.Tensor（ComfyUI IMAGE形式）
        else:
            # torchがインポート可能かチェック
            try:
                import torch
                HAS_TORCH = True
            except ImportError:
                HAS_TORCH = False
            
            if HAS_TORCH and torch.is_tensor(image_input):
                print(f"[IMAGETOBASE64 DEBUG] Input type: torch.Tensor (ComfyUI IMAGE)")
                
                # ComfyUI IMAGE形式: [batch, height, width, channels], 値は0.0-1.0
                if image_input.ndim != 4:
                    raise ValueError(f"INVALID_TENSOR_SHAPE: Expected 4D tensor [batch, height, width, channels], got shape: {image_input.shape}")
                
                # 最初のバッチを取得
                img_tensor = image_input[0]  # [height, width, channels]
                print(f"[IMAGETOBASE64 DEBUG] Tensor shape: {img_tensor.shape}")
                
                # numpy配列に変換し、0-255にスケール
                import numpy as np
                img_array = img_tensor.cpu().numpy()
                img_array = (img_array * 255).clip(0, 255).astype(np.uint8)
                
                # PIL Imageに変換
                image = Image.fromarray(img_array, mode='RGB')
                print(f"[IMAGETOBASE64 DEBUG] Converted tensor to PIL Image")
            else:
                # torch.Tensorでもない、文字列でもない → TypeError
                raise TypeError(f"INVALID_INPUT_TYPE: image_input must be str (file path) or torch.Tensor (IMAGE), got: {type(image_input)}")
        
        # 以降は共通処理
        original_width, original_height = image.size
        print(f"[IMAGETOBASE64 DEBUG] Original size: {original_width}x{original_height}, mode: {image.mode}")
        
        # 画像サイズ検証（ゼロ除算防止）
        if original_width <= 0 or original_height <= 0:
            raise ValueError(f"INVALID_IMAGE_SIZE: Image size must be positive, got {original_width}x{original_height}")
        
        # JPEG形式の場合、RGBAをRGBに変換
        if format.upper() == "JPEG" and image.mode in ('RGBA', 'LA', 'P'):
            print(f"[IMAGETOBASE64 DEBUG] Converting {image.mode} to RGB for JPEG")
            # 白背景でRGBに変換
            rgb_image = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            if image.mode == 'RGBA':
                rgb_image.paste(image, mask=image.split()[3])
            else:
                rgb_image.paste(image)
            image = rgb_image
        
        # リサイズ処理（アスペクト比維持）
        if original_width > max_size or original_height > max_size:
            # アスペクト比を計算（明示的にfloatで計算してからintに変換）
            if original_width > original_height:
                # 横長: 幅をmax_sizeに
                new_width = int(max_size)
                ratio = float(max_size) / float(original_width)
                new_height = int(float(original_height) * ratio)
            else:
                # 縦長または正方形: 高さをmax_sizeに
                new_height = int(max_size)
                ratio = float(max_size) / float(original_height)
                new_width = int(float(original_width) * ratio)
            
            # リサイズ後のサイズが最低1pxであることを保証
            new_width = max(1, new_width)
            new_height = max(1, new_height)
            
            print(f"[IMAGETOBASE64 DEBUG] Resizing to: {new_width}x{new_height}")
            
            # リサイズ実行（LANCZOS = 1）
            resized_image = image.resize((new_width, new_height), 1)
            print(f"[IMAGETOBASE64 DEBUG] Resized image size: {resized_image.size}")
        else:
            # リサイズ不要
            print(f"[IMAGETOBASE64 DEBUG] No resize needed")
            resized_image = image
        
        # バイト配列に変換
        buffered = BytesIO()
        if format.upper() == "JPEG":
            # JPEG品質を85に設定（Venice APIで高品質維持）
            resized_image.save(buffered, format=format, quality=85, optimize=True)
        else:
            resized_image.save(buffered, format=format)
        
        image_bytes = buffered.getvalue()
        bytes_length = len(image_bytes)
        print(f"[IMAGETOBASE64 DEBUG] Bytes length: {bytes_length} ({bytes_length / 1024:.2f} KB)")
        
        # Base64エンコード
        print(f"[IMAGETOBASE64 DEBUG] Encoding to Base64...")
        base64_bytes = base64.b64encode(image_bytes)
        base64_string = base64_bytes.decode('utf-8')
        base64_length = len(base64_string)
        print(f"[IMAGETOBASE64 DEBUG] Base64 string length: {base64_length} ({base64_length / 1024:.2f} KB)")
        
        # 戻り値形式に応じて変換
        if return_format == "base64":
            return base64_string
        elif return_format == "data_url":
            # data URL形式に変換
            mime_type = "image/png" if format.upper() == "PNG" else "image/jpeg"
            data_url = f"data:{mime_type};base64,{base64_string}"
            data_url_length = len(data_url)
            print(f"[IMAGETOBASE64 DEBUG] Data URL length: {data_url_length} ({data_url_length / 1024:.2f} KB)")
            return data_url


# ===== 内部ヘルパー関数 =====

def _detect_output_type(value: Any) -> str:
    """
    出力値の型を判定
    
    Returns:
        "text", "number", "array", "image", "binary"
    """
    if isinstance(value, str):
        return "text"
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        return "number"
    elif isinstance(value, list):
        return "array"
    # 画像型判定（ComfyUIのtorch.Tensor画像形式）
    elif hasattr(value, 'shape') and hasattr(value, 'dtype'):
        # torch.Tensor形式の画像: shape=(B, H, W, C)
        if len(getattr(value, 'shape', [])) == 4:
            return "image"
    elif hasattr(value, '__array_interface__'):  # numpy配列
        return "image"
    return "binary"


def _resolve_output_path(output_dir: str, path: str, value_type: str) -> str:
    """
    出力パスを解決し、拡張子を補完
    
    Args:
        output_dir: ComfyUI出力ディレクトリ
        path: ユーザー指定パス
        value_type: 値の型
    
    Returns:
        解決済み絶対パス
    """
    import os
    from pathlib import Path
    
    # pathが空の場合はデフォルトファイル名
    if not path:
        if value_type == "image":
            path = "output.png"
        elif value_type in ("text", "number", "array"):
            path = "output.txt"
        else:
            path = "output.bin"
    
    # 相対パスとして結合
    full_path = Path(output_dir) / path
    
    # ディレクトリが存在しない場合は再帰的に作成
    full_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 拡張子が指定されていない場合は補完
    if not full_path.suffix:
        if value_type == "image":
            full_path = full_path.with_suffix(".png")
        elif value_type in ("text", "number", "array"):
            full_path = full_path.with_suffix(".txt")
        else:
            full_path = full_path.with_suffix(".bin")
    
    return str(full_path)


def _handle_duplicate_filename(file_path: str) -> str:
    """
    ファイル名が重複する場合、_NNNNを付与
    
    既存の_NNNN付きファイルの最大番号を検索し、その次の番号を使用する。
    
    Args:
        file_path: ファイルパス
    
    Returns:
        重複回避済みパス
    """
    import os
    import re
    from pathlib import Path
    
    path_obj = Path(file_path)
    
    if not path_obj.exists():
        return file_path
    
    # 既存の_NNNN付きファイルの最大番号を検索
    stem = path_obj.stem
    suffix = path_obj.suffix
    parent = path_obj.parent
    
    # パターン: {stem}_NNNN{suffix}
    pattern = re.compile(rf"^{re.escape(stem)}_(\d{{4}}){re.escape(suffix)}$")
    
    max_number = 0  # 0から開始（最初のファイルは_0001）
    
    # 同じディレクトリ内の全ファイルをスキャン
    for file in parent.iterdir():
        if file.is_file():
            match = pattern.match(file.name)
            if match:
                number = int(match.group(1))
                if number > max_number:
                    max_number = number
    
    # 最大値+1の番号で新しいファイル名を生成
    new_number = max_number + 1
    new_name = f"{stem}_{new_number:04d}{suffix}"
    new_path = parent / new_name
    
    # 安全装置: 9999を超えないようにする
    if new_number > 9999:
        # whileループで未使用の番号を探す（元のロジックに戻る）
        counter = 1
        while counter <= 9999:
            new_name = f"{stem}_{counter:04d}{suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                return str(new_path)
            counter += 1
        # それでも見つからない場合は元のファイルパスを返す
        return file_path
    
    return str(new_path)


def _write_image_file(value: Any, file_path: str, mode: str):
    """
    画像ファイルに出力
    
    Args:
        value: 画像データ（torch.Tensor または numpy配列）
        file_path: 出力パス
        mode: "NEW" or "ADD"（画像は追記不可）
    """
    from pathlib import Path
    import io
    # PILは37行目でグローバルインポート済み（HAS_PIL=True）
    
    # 拡張子取得
    ext = Path(file_path).suffix.lower()
    
    # torch.Tensorからnumpy配列に変換
    if hasattr(value, 'cpu') and hasattr(value, 'numpy'):
        # torch.Tensor形式: (B, H, W, C) → 最初のバッチを取得
        # numpyは49行目でグローバルインポート済み（HAS_NUMPY=True）
        img_array = value.cpu().numpy()[0]  # 最初の画像を取得
        
        # 正規化されている場合（0-1範囲）は0-255に変換
        if img_array.max() <= 1.0:
            img_array = (img_array * 255).astype(np.uint8)
        else:
            img_array = img_array.astype(np.uint8)
        
        # PIL Imageに変換
        img = Image.fromarray(img_array)
    else:
        # 既にPIL Image形式の場合
        img = value
    
    # フォーマット別保存
    if ext in (".jpg", ".jpeg"):
        # JPEG: 無圧縮プログレッシブ
        img.convert("RGB").save(file_path, "JPEG", quality=100, progressive=True)
    elif ext == ".bmp":
        img.save(file_path, "BMP")
    elif ext == ".tga":
        img.save(file_path, "TGA")
    elif ext == ".webp":
        img.save(file_path, "WEBP", quality=100)
    elif ext in (".tiff", ".tif"):
        img.save(file_path, "TIFF")
    else:  # PNG（デフォルト）
        img.save(file_path, "PNG")


def _write_text_file(value: Any, file_path: str, mode: str, value_type: str):
    """
    テキストファイルに出力
    
    Args:
        value: 出力値
        file_path: 出力パス
        mode: "NEW" or "ADD"
        value_type: "text", "number", "array"
    """
    # テキスト変換
    if value_type == "array":
        # Python標準出力形式
        text = str(value)
    elif value_type == "number":
        # 浮動小数点数が整数値の場合は整数表記に変換
        if isinstance(value, float) and value.is_integer():
            text = str(int(value))
        else:
            text = str(value)
    else:
        text = str(value)
    
    # 出力
    if mode == "ADD":
        with open(file_path, "a", encoding="utf-8") as f:
            f.write("\n" + text)
    else:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)


def _write_binary_file(value: Any, file_path: str, mode: str):
    """
    バイナリファイルに出力
    
    Args:
        value: バイナリデータ
        file_path: 出力パス
        mode: "NEW" or "ADD"
    """
    # bytes変換
    if isinstance(value, bytes):
        data = value
    else:
        # その他の型はstrにしてからUTF-8バイト列化
        data = str(value).encode("utf-8")
    
    # 出力
    if mode == "ADD":
        with open(file_path, "ab") as f:
            f.write(data)
    else:
        with open(file_path, "wb") as f:
            f.write(data)


# ===== INPUT関数用ヘルパー関数 =====

def _detect_input_type(file_path: str) -> str:
    """
    ファイル形式を判定（INPUT関数用）

    Args:
        file_path: ファイルの絶対パス

    Returns:
        "text", "json", "image", "binary"
    """
    ext = os.path.splitext(file_path)[1].lower()

    # 拡張子ベース判定
    if ext in ['.txt', '.md']:
        return "text"
    elif ext == '.json':
        return "json"
    elif ext in ['.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tga', '.tiff', '.tif']:
        return "image"

    # 拡張子不明 → 内容解析（簡易）
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(512)  # 最初の512バイトのみ読む
            if content.startswith('[') or content.startswith('{'):
                return "json"
            return "text"
    except UnicodeDecodeError:
        # バイナリファイル
        return "binary"


def _load_text_file(file_path: str) -> str:
    """
    テキストファイル読み込み

    Args:
        file_path: ファイルの絶対パス

    Returns:
        ファイル内容（文字列）
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def _load_json_file(file_path: str) -> Any:
    """
    JSONファイル読み込み（数値/配列/その他を自動判定）

    Args:
        file_path: ファイルの絶対パス

    Returns:
        JSONデータ（float/list/dict等、型は動的）
    """
    import json

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 単一数値 → float変換
    if isinstance(data, (int, float)):
        return float(data)

    # その他（配列、オブジェクト等）はそのまま返却
    return data


def _load_image_file(file_path: str, locale: str = "ja"):
    """
    画像ファイル読み込み（OUTPUT関数の _write_image_file の逆処理）

    Args:
        file_path: 画像ファイルの絶対パス
        locale: ロケール（'en'または'ja'）

    Returns:
        torch.Tensor: shape=(1, H, W, C), dtype=float32, range=0-1
        または numpy配列（torchがない場合）
    """
    if not HAS_PIL:
        raise ImportError(get_message('input_error_pil_not_installed', locale))

    # PIL.Imageで読み込み
    img = Image.open(file_path)

    # RGBに変換（透明度チャネル削除）
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # numpy配列に変換
    if HAS_NUMPY:
        # numpyは49行目でグローバルインポート済み（HAS_NUMPY=True）
        img_array = np.array(img).astype(np.float32) / 255.0  # 0-1範囲に正規化
    else:
        # numpyがない場合の簡易変換（リスト形式）
        # 注: これは非効率ですが、フォールバック用
        width, height = img.size
        pixels = list(img.getdata())
        img_array = [[[pixels[y * width + x][c] / 255.0 for c in range(3)]
                      for x in range(width)]
                     for y in range(height)]

    # torch.Tensorに変換（ComfyUI互換形式）
    if HAS_TORCH:
        import torch
        # (H, W, C) → (1, H, W, C) バッチ次元追加
        if HAS_NUMPY:
            img_tensor = torch.from_numpy(img_array).unsqueeze(0)
        else:
            img_tensor = torch.tensor(img_array, dtype=torch.float32).unsqueeze(0)
        return img_tensor
    else:
        # torchがない場合はnumpy配列またはリストのまま返却
        if HAS_NUMPY:
            return np.expand_dims(img_array, axis=0)
        else:
            return [img_array]  # リストでラップ


def _load_binary_file(file_path: str) -> bytes:
    """
    バイナリファイル読み込み

    Args:
        file_path: ファイルの絶対パス

    Returns:
        ファイル内容（バイト列）
    """
    with open(file_path, 'rb') as f:
        return f.read()


# ===== ISFILEEXIST関数用ヘルパー関数 =====

def _find_max_numbered_file(output_dir: str, path: str) -> str:
    """
    _NNNN付きファイルの最大番号を検索

    Args:
        output_dir: ComfyUI出力ディレクトリ
        path: ベースファイルパス（例: "output.txt"）

    Returns:
        最大番号ファイルの相対パス or "FALSE"

    Examples:
        output_0001.txt, output_0005.txt が存在する場合
        → "output_0005.txt" を返す
    """
    from pathlib import Path
    import re

    # パスを分解
    base_path = Path(path)
    stem = base_path.stem  # 拡張子なしファイル名
    suffix = base_path.suffix  # 拡張子
    parent_rel = base_path.parent  # 相対的な親ディレクトリ

    # 検索ディレクトリ
    search_dir = Path(output_dir) / parent_rel

    if not search_dir.exists():
        return "FALSE"

    # パターン: {stem}_NNNN{suffix}
    pattern = re.compile(rf"^{re.escape(stem)}_(\d{{4}}){re.escape(suffix)}$")

    max_number = -1
    max_file = None

    for file in search_dir.iterdir():
        if file.is_file():
            match = pattern.match(file.name)
            if match:
                number = int(match.group(1))
                if number > max_number:
                    max_number = number
                    max_file = file

    if max_file is None:
        return "FALSE"

    # 相対パスで返す
    relative_path = max_file.relative_to(output_dir)
    return str(relative_path).replace('\\', '/')  # Windowsパス区切りを統一


def _get_image_pixel_size(file_path: str, locale: str = "ja") -> str:
    """
    画像ファイルのピクセルサイズを取得

    Args:
        file_path: 画像ファイルの絶対パス
        locale: ロケール（'en'または'ja'）

    Returns:
        "[width, height]" or "FALSE"
    """
    if not os.path.exists(file_path):
        return "FALSE"

    # 画像形式判定
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ['.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tga', '.tiff', '.tif']:
        return "FALSE"

    if not HAS_PIL:
        print(get_message('isfileexist_warning_pil_not_installed', locale))
        return "FALSE"

    try:
        img = Image.open(file_path)
        width, height = img.size
        return f"[{width}, {height}]"
    except Exception as e:
        print(get_message('isfileexist_error_image_load', locale, e))
        return "FALSE"

