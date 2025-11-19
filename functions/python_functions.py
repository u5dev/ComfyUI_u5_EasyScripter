# -*- coding: utf-8 -*-
"""
Python Functions for EasyScripter
Python関数呼び出しブリッジ

PYEXEC() - Generic Python Function Executor
"""

import importlib
import json
import base64
import builtins
from typing import Any

# グローバルインポート（CLAUDE.md動的インポート禁止ルールに準拠）
# ComfyUI環境ではnumpyは必須依存関係（requirements.txt:8）
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


class PythonFunctions:
    """Pythonネイティブ関数実行用クラス"""

    # セキュリティ: ブラックリスト方式
    BLOCKED_MODULES = {
        'os', 'sys', 'subprocess',
        'eval', 'exec', 'compile', '__import__',
        'pickle', 'shelve', 'code', 'pdb',
        'importlib.import_module',  # 動的importも制限
    }

    # サイズ制限
    MAX_RETURN_SIZE = 20 * 1024 * 1024  # 20MB（画像処理対応）
    MAX_LIST_ELEMENTS = 20 * 1024 * 1024  # 20MB対応（バイト配列用）
    MAX_ARGS = 10

    @staticmethod
    def PYEXEC(func_path: str, *args) -> Any:
        """
        汎用Python関数実行エンジン

        Args:
            func_path: "module.function" 形式の関数パス
                      例: "math.sqrt", "random.randint", "numpy.array"
                      オブジェクトメソッド呼び出しの場合: "method_name"
            *args: 関数に渡す引数(最大10個)
                   第1引数がPythonオブジェクトの場合、そのオブジェクトのメソッドを呼び出す

        Returns:
            EasyScripter互換の型(float, str)に変換された戻り値

        Raises:
            RuntimeError: セキュリティ違反、モジュール未検出、型変換失敗等

        Examples:
            >>> PYEXEC("math.sqrt", 16.0)
            4.0
            >>> PYEXEC("str.upper", "hello")
            "HELLO"
            >>> PYEXEC("random.randint", 1, 10)
            7.0
            >>> hash_obj = PYEXEC("hashlib.sha256", encoded_data)
            >>> PYEXEC("hexdigest", hash_obj)  # オブジェクトメソッド呼び出し
            "abc123..."
        """
        # 引数数制限
        if len(args) > PythonFunctions.MAX_ARGS:
            raise RuntimeError(
                f"TOO_MANY_ARGS: PYEXEC()は最大{PythonFunctions.MAX_ARGS}個の引数まで対応。"
                f"{len(args)}個渡されました。"
            )

        # 引数の前処理: __PYBYTES__マーカーをバイト列に変換
        converted_args = []
        for arg in args:
            if isinstance(arg, str) and arg.startswith("__PYBYTES__:"):
                # Base64デコードしてバイト列に変換
                try:
                    base64_str = arg.replace("__PYBYTES__:", "")
                    bytes_data = base64.b64decode(base64_str)
                    converted_args.append(bytes_data)
                except Exception as e:
                    raise RuntimeError(
                        f"PYBYTES_DECODE_ERROR: __PYBYTES__マーカーのデコードに失敗しました。\n"
                        f"引数: {arg[:50]}...\n"
                        f"詳細エラー: {str(e)}"
                    )
            else:
                converted_args.append(arg)

        # オブジェクトメソッド呼び出しチェック
        # 第1引数がPythonオブジェクトで、func_pathがメソッド名のみの場合
        if (len(converted_args) > 0 and 
            hasattr(converted_args[0], '__module__') and 
            '.' not in func_path):
            # オブジェクトメソッド呼び出しモード
            obj = converted_args[0]
            method_name = func_path
            remaining_args = converted_args[1:]

            # メソッドの取得
            try:
                method = getattr(obj, method_name)
            except AttributeError:
                raise RuntimeError(
                    f"METHOD_NOT_FOUND: オブジェクト {type(obj).__name__} にメソッド '{method_name}' が見つかりません。\n"
                    f"利用可能なメソッドを確認してください。"
                )

            # メソッド実行
            try:
                result = method(*remaining_args)
            except Exception as e:
                raise RuntimeError(
                    f"METHOD_EXECUTION_ERROR: メソッド '{method_name}' の実行中にエラーが発生しました。\n"
                    f"引数: {remaining_args}\n"
                    f"詳細エラー: {type(e).__name__}: {str(e)}"
                )

            # 戻り値の型変換
            try:
                converted_result = PythonFunctions._convert_return_value(result)
            except Exception as e:
                raise RuntimeError(
                    f"TYPE_CONVERSION_ERROR: 戻り値の型変換中にエラーが発生しました。\n"
                    f"戻り値の型: {type(result)}\n"
                    f"詳細エラー: {str(e)}"
                )

            # サイズ制限チェック
            if isinstance(converted_result, str):
                if len(converted_result) > PythonFunctions.MAX_RETURN_SIZE:
                    raise RuntimeError(
                        f"RETURN_TOO_LARGE: 戻り値が大きすぎます({len(converted_result)} bytes)。\n"
                        f"最大サイズ: {PythonFunctions.MAX_RETURN_SIZE} bytes"
                    )

            return converted_result

        # 通常のモジュール関数呼び出しモード
        # func_path解析
        if '.' not in func_path:
            # builtins関数の場合(len, abs等)
            module_name = 'builtins'
            func_name = func_path
        else:
            parts = func_path.rsplit('.', 1)
            if len(parts) != 2:
                raise RuntimeError(
                    f"INVALID_FORMAT: 関数パスは 'module.function' 形式である必要があります。"
                    f"入力値: '{func_path}'"
                )
            module_name, func_name = parts

            # ビルトインクラスのメソッド呼び出しチェック(str.upper, list.append等)
            builtin_types = {'str', 'list', 'dict', 'tuple', 'set', 'frozenset', 'bytes', 'bytearray'}
            if module_name in builtin_types:
                module_name = 'builtins'

        # セキュリティチェック: ブラックリスト
        if module_name in PythonFunctions.BLOCKED_MODULES or func_name in PythonFunctions.BLOCKED_MODULES:
            raise RuntimeError(
                f"BLOCKED_MODULE: セキュリティ上の理由により、モジュール '{module_name}' "
                f"または関数 '{func_name}' の使用は禁止されています。\n"
                f"ブロック対象: {PythonFunctions.BLOCKED_MODULES}"
            )

        # モジュールのインポート
        try:
            if module_name == 'builtins':
                module = builtins
            else:
                module = importlib.import_module(module_name)
        except ModuleNotFoundError as e:
            # ユーザーフレンドリーなエラーメッセージ
            module_install_name = module_name.replace('_', '-')
            raise RuntimeError(
                f"MODULE_NOT_FOUND: モジュール '{module_name}' が見つかりません。\n"
                f"インストールが必要な場合: pip install {module_install_name}\n"
                f"詳細エラー: {str(e)}"
            )
        except Exception as e:
            raise RuntimeError(
                f"MODULE_IMPORT_ERROR: モジュール '{module_name}' のインポート中にエラーが発生しました。\n"
                f"詳細エラー: {str(e)}"
            )

        # 関数の取得
        try:
            # ビルトインクラスのメソッド呼び出しの場合
            parts_original = func_path.rsplit('.', 1)
            builtin_types = {'str', 'list', 'dict', 'tuple', 'set', 'frozenset', 'bytes', 'bytearray'}

            if len(parts_original) == 2 and parts_original[0] in builtin_types:
                # str.upper の場合: builtins.str を取得して、upperメソッドをゲット
                type_class = getattr(module, parts_original[0])
                func = getattr(type_class, func_name)
            else:
                # 通常のモジュール関数の場合
                func = getattr(module, func_name)
        except AttributeError:
            raise RuntimeError(
                f"FUNCTION_NOT_FOUND: モジュール '{module_name}' に関数 '{func_name}' が見つかりません。\n"
                f"利用可能な関数を確認してください。"
            )

        # 関数実行(変換後の引数を使用)
        try:
            result = func(*converted_args)
        except Exception as e:
            raise RuntimeError(
                f"FUNCTION_EXECUTION_ERROR: 関数 '{func_path}' の実行中にエラーが発生しました。\n"
                f"引数: {args}\n"
                f"詳細エラー: {type(e).__name__}: {str(e)}"
            )

        # 戻り値の型変換
        try:
            converted_result = PythonFunctions._convert_return_value(result)
        except Exception as e:
            raise RuntimeError(
                f"TYPE_CONVERSION_ERROR: 戻り値の型変換中にエラーが発生しました。\n"
                f"戻り値の型: {type(result)}\n"
                f"詳細エラー: {str(e)}"
            )

        # サイズ制限チェック
        if isinstance(converted_result, str):
            if len(converted_result) > PythonFunctions.MAX_RETURN_SIZE:
                raise RuntimeError(
                    f"RETURN_TOO_LARGE: 戻り値が大きすぎます({len(converted_result)} bytes)。\n"
                    f"最大サイズ: {PythonFunctions.MAX_RETURN_SIZE} bytes"
                )

        return converted_result

    @staticmethod
    def _convert_return_value(value: Any) -> Any:
        """
        Python戻り値 → EasyScripter互換型への変換

        型変換マッピング:
        - None → 0.0
        - bool → 1.0 (True) / 0.0 (False)
        - int → float
        - float → float
        - str → str
        - list/tuple → CSV文字列 "a,b,c"
        - dict → JSON文字列
        - bytes → UTF-8文字列
        - numpy.ndarray → CSV文字列
        - pandas.DataFrame → JSON文字列
        - file handle → 自動読み込み + クローズ
        - Pythonオブジェクト → そのまま保持（PYEXECチェーン用）
        """
        # None → 0.0
        if value is None:
            return 0.0

        # bool → 1.0 / 0.0
        if isinstance(value, bool):
            return 1.0 if value else 0.0

        # int → float
        if isinstance(value, int):
            return float(value)

        # float → float
        if isinstance(value, float):
            return value

        # str → str
        if isinstance(value, str):
            return value

        # bytes → UTF-8文字列
        if isinstance(value, bytes):
            try:
                return value.decode('utf-8')
            except UnicodeDecodeError:
                # バイナリデータの場合はBase64エンコード
                return base64.b64encode(value).decode('ascii')

        # list/tuple → CSV文字列
        if isinstance(value, (list, tuple)):
            if len(value) > PythonFunctions.MAX_LIST_ELEMENTS:
                raise RuntimeError(
                    f"TOO_MANY_ELEMENTS: リスト要素数が多すぎます({len(value)}個)。\n"
                    f"最大要素数: {PythonFunctions.MAX_LIST_ELEMENTS}"
                )
            # 再帰的に要素を変換
            converted_elements = [str(PythonFunctions._convert_return_value(item)) for item in value]
            return ','.join(converted_elements)

        # dict → JSON文字列
        if isinstance(value, dict):
            try:
                return json.dumps(value, ensure_ascii=False)
            except (TypeError, ValueError) as e:
                raise RuntimeError(f"DICT_TO_JSON_ERROR: 辞書のJSON変換に失敗しました。詳細: {str(e)}")

        # NumPy ndarray → CSV文字列
        # numpyは18行目でグローバルインポート済み（HAS_NUMPY=True）
        if HAS_NUMPY:
            if isinstance(value, np.ndarray):
                if value.size > PythonFunctions.MAX_LIST_ELEMENTS:
                    raise RuntimeError(
                        f"TOO_MANY_ELEMENTS: NumPy配列要素数が多すぎます({value.size}個)。\n"
                        f"最大要素数: {PythonFunctions.MAX_LIST_ELEMENTS}"
                    )
                # 1次元配列に変換してCSV化
                flat_array = value.flatten()
                return ','.join(str(x) for x in flat_array)

        # Pandas DataFrame → JSON文字列
        try:
            import pandas as pd
            if isinstance(value, pd.DataFrame):
                # to_json()でJSON文字列化
                return value.to_json(orient='records', force_ascii=False)
        except ImportError:
            pass  # Pandasがインストールされていない場合はスキップ

        # File handle → 自動読み込み + クローズ
        if hasattr(value, 'read') and hasattr(value, 'close'):
            try:
                content = value.read()
                value.close()

                # バイナリモードの場合はデコード
                if isinstance(content, bytes):
                    try:
                        content = content.decode('utf-8')
                    except UnicodeDecodeError:
                        content = base64.b64encode(content).decode('ascii')

                # サイズチェック
                if len(content) > PythonFunctions.MAX_RETURN_SIZE:
                    raise RuntimeError(
                        f"RETURN_TOO_LARGE: ファイル内容が大きすぎます({len(content)} bytes)。\n"
                        f"最大サイズ: {PythonFunctions.MAX_RETURN_SIZE} bytes"
                    )

                return content
            except Exception as e:
                raise RuntimeError(f"FILE_READ_ERROR: ファイルの読み込み中にエラーが発生しました。詳細: {str(e)}")

        # Pythonオブジェクト(hashlib HASH等) → そのまま保持
        # PYEXEC連鎖呼び出し用: hash_obj = PYEXEC("hashlib.sha256", data) → PYEXEC("hashlib.hexdigest", hash_obj)
        # hasattr(value, '__module__') でPythonオブジェクトかチェック
        if hasattr(value, '__module__'):
            # 特定のモジュールのオブジェクトはそのまま保持
            allowed_modules = ['hashlib', '_hashlib', 'datetime', 're', 'json', 'pathlib']
            if any(value.__module__.startswith(module) for module in allowed_modules):
                return value

        # 上記以外の型(callableオブジェクト、カスタムクラス等)
        # → エラー(EasyScripterでは対応不可)
        raise RuntimeError(
            f"UNSUPPORTED_TYPE: 戻り値の型 {type(value).__name__} はEasyScripterで対応していません。\n"
            f"対応型: None, bool, int, float, str, bytes, list, tuple, dict, "
            f"numpy.ndarray, pandas.DataFrame, file handle, Python標準ライブラリオブジェクト\n"
            f"戻り値: {repr(value)}"
        )

    @staticmethod
    def PYLIST(value):
        """
        PYEXEC戻り値をEasyScripter配列形式に変換（CSV文字列化を回避）
        
        Args:
            value: CSV文字列または辞書型配列
        
        Returns:
            dict: 辞書型配列 {0: elem0, 1: elem1, ...}
        
        Raises:
            RuntimeError: サポート外の型が渡された場合
        
        使用例:
            data_array = PYLIST(PYEXEC("json.loads", "[1,2,3,4,5]"))
            Result = PYEXEC("numpy.mean", data_array)
        """
        # 既に辞書型配列の場合はそのまま返す（冪等性）
        if isinstance(value, dict) and all(isinstance(k, int) for k in value.keys()):
            return value
        
        # CSV文字列の場合はパースして辞書型配列に変換
        if isinstance(value, str):
            # 空文字列の場合は空配列
            if not value.strip():
                return {}
            
            elements = value.split(',')
            array_dict = {}
            
            for i, elem in enumerate(elements):
                elem_stripped = elem.strip()
                
                # 数値変換を試行
                try:
                    # 小数点が含まれる場合は浮動小数点
                    if '.' in elem_stripped:
                        array_dict[i] = float(elem_stripped)
                    else:
                        # 整数として解釈
                        array_dict[i] = float(int(elem_stripped))
                except ValueError:
                    # 数値変換失敗時は文字列として格納
                    array_dict[i] = elem_stripped
            
            return array_dict
        
        # その他の型はエラー
        raise RuntimeError(
            f"PYLIST_TYPE_ERROR: PYLISTはCSV文字列または辞書型配列のみ対応しています。\n"
            f"受け取った型: {type(value).__name__}\n"
            f"値: {repr(value)}"
        )

    @staticmethod
    def PYENCODE(text, encoding='utf-8'):
        """
        文字列をバイト列にエンコード（PYEXEC引数準備用）

        Args:
            text: エンコードする文字列
            encoding: エンコーディング方式（デフォルト: 'utf-8'）

        Returns:
            str: Base64エンコードされた文字列（PYEXECでバイト列として扱える）

        Raises:
            RuntimeError: エンコードに失敗した場合

        使用例:
            data_str = "test_data"
            encoded = PYENCODE(data_str)
            hash_obj = PYEXEC("hashlib.sha256", encoded)
        """
        try:
            # 文字列に変換（数値等が渡された場合）
            if not isinstance(text, str):
                text = str(text)

            # UTF-8バイト列にエンコード
            bytes_data = text.encode(encoding)

            # Base64エンコードして文字列として返す
            # （EasyScripter内部ではバイト列を直接扱えないため）
            base64_encoded = base64.b64encode(bytes_data).decode('ascii')

            # 特殊マーカーを付与してPYEXECで識別可能にする
            return f"__PYBYTES__:{base64_encoded}"

        except UnicodeEncodeError as e:
            raise RuntimeError(
                f"PYENCODE_ERROR: エンコードに失敗しました。\n"
                f"テキスト: {text[:50]}...\n"
                f"エンコーディング: {encoding}\n"
                f"詳細エラー: {str(e)}"
            )
        except LookupError as e:
            raise RuntimeError(
                f"PYENCODE_INVALID_ENCODING: 無効なエンコーディングが指定されました。\n"
                f"指定されたエンコーディング: {encoding}\n"
                f"詳細エラー: {str(e)}"
            )
        except Exception as e:
            raise RuntimeError(
                f"PYENCODE_ERROR: エンコード中にエラーが発生しました。\n"
                f"詳細エラー: {type(e).__name__}: {str(e)}"
            )

    @staticmethod
    def PYDECODE(bytes_data, encoding='utf-8'):
        """
        バイト列を文字列にデコード

        Args:
            bytes_data: デコードするバイト列（Base64エンコードされた文字列）
            encoding: エンコーディング方式（デフォルト: 'utf-8'）

        Returns:
            str: デコードされた文字列

        Raises:
            RuntimeError: デコードに失敗した場合

        使用例:
            encoded = PYENCODE("test")
            decoded = PYDECODE(encoded)
        """
        try:
            # PYENCODEの出力形式を確認
            if isinstance(bytes_data, str) and bytes_data.startswith("__PYBYTES__:"):
                # Base64デコード
                base64_str = bytes_data.replace("__PYBYTES__:", "")
                decoded_bytes = base64.b64decode(base64_str)
            else:
                # 直接Base64文字列として扱う
                decoded_bytes = base64.b64decode(bytes_data)

            # 文字列にデコード
            return decoded_bytes.decode(encoding)

        except base64.binascii.Error as e:
            raise RuntimeError(
                f"PYDECODE_INVALID_DATA: Base64デコードに失敗しました。\n"
                f"データ: {str(bytes_data)[:50]}...\n"
                f"詳細エラー: {str(e)}"
            )
        except UnicodeDecodeError as e:
            raise RuntimeError(
                f"PYDECODE_ERROR: デコードに失敗しました。\n"
                f"エンコーディング: {encoding}\n"
                f"詳細エラー: {str(e)}"
            )
        except LookupError as e:
            raise RuntimeError(
                f"PYDECODE_INVALID_ENCODING: 無効なエンコーディングが指定されました。\n"
                f"指定されたエンコーディング: {encoding}\n"
                f"詳細エラー: {str(e)}"
            )
        except Exception as e:
            raise RuntimeError(
                f"PYDECODE_ERROR: デコード中にエラーが発生しました。\n"
                f"詳細エラー: {type(e).__name__}: {str(e)}"
            )
