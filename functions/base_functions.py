# -*- coding: utf-8 -*-
"""
基本関数モジュール
Base functions module - 頻繁に使用される基本的な関数群
"""

from typing import Any

class BaseFunctions:
    """基本的なビルトイン関数のクラス"""

    @staticmethod
    def ROUND(value: Any, digits: int = 0) -> float:
        """
        四捨五入した値を返す

        Args:
            value: 数値または数値に変換可能な値
            digits: 小数点以下の桁数（デフォルト: 0）

        Returns:
            四捨五入した値
        """
        try:
            num_value = float(value)
            digits_int = int(digits) if digits else 0
            return round(num_value, digits_int)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def LEFT(value: Any, length: int) -> str:
        """
        文字列の左側から指定文字数を取得

        Args:
            value: 文字列
            length: 取得する文字数

        Returns:
            左側から指定文字数分の文字列
        """
        try:
            str_value = str(value)
            length_int = int(length)
            if length_int <= 0:
                return ""
            return str_value[:length_int]
        except:
            return ""

    @staticmethod
    def RIGHT(value: Any, length: int) -> str:
        """
        文字列の右側から指定文字数を取得

        Args:
            value: 文字列
            length: 取得する文字数

        Returns:
            右側から指定文字数分の文字列
        """
        try:
            str_value = str(value)
            length_int = int(length)
            if length_int <= 0:
                return ""
            return str_value[-length_int:]
        except:
            return ""

    @staticmethod
    def MID(value: Any, start: int, length: int) -> str:
        """
        文字列の中間部分を取得

        Args:
            value: 文字列
            start: 開始位置（1ベース、0は1として扱う）
            length: 取得する文字数

        Returns:
            指定位置から指定文字数分の文字列
        """
        try:
            str_value = str(value)
            start_int = int(start)
            # VBAでは0は1として扱われる
            if start_int <= 0:
                start_int = 1
            start_int = start_int - 1  # 1ベースを0ベースに変換
            length_int = int(length)
            if length_int <= 0:
                return ""
            return str_value[start_int:start_int + length_int]
        except:
            return ""

    @staticmethod
    def INSTR(*args) -> float:
        """
        文字列内で部分文字列を検索（前から）

        Args:
            引数パターン1: INSTR(string1, string2)
            引数パターン2: INSTR(string1, string2, compare)
            引数パターン3: INSTR(start, string1, string2)
            引数パターン4: INSTR(start, string1, string2, compare)

            start: 検索開始位置（1ベース、省略時は1）
            string1: 検索対象文字列
            string2: 検索する文字列
            compare: 0=バイナリ比較（大文字小文字を区別）、1=テキスト比較（区別しない）
                    省略時は1（VBA互換で大文字小文字を区別しない）

        Returns:
            見つかった位置（1ベース）、見つからない場合は0
        """
        try:
            # 引数の解析
            if len(args) == 2:
                # INSTR(string1, string2)
                start = 1
                string1 = str(args[0])
                string2 = str(args[1])
                compare = 1  # デフォルトは大文字小文字を区別しない
            elif len(args) == 3:
                # 第一引数が数値の場合は INSTR(start, string1, string2)
                # 第三引数が数値の場合は INSTR(string1, string2, compare)
                try:
                    # 第一引数を数値として解釈してみる
                    start_val = float(str(args[0]))
                    if start_val >= 1:  # 有効な開始位置
                        # INSTR(start, string1, string2)
                        start = int(start_val)
                        string1 = str(args[1])
                        string2 = str(args[2])
                        compare = 1
                    else:
                        raise ValueError("Invalid start position")
                except (ValueError, TypeError):
                    # INSTR(string1, string2, compare)
                    start = 1
                    string1 = str(args[0])
                    string2 = str(args[1])
                    compare = int(float(str(args[2])))
            elif len(args) == 4:
                # INSTR(start, string1, string2, compare)
                start = int(float(str(args[0])))
                string1 = str(args[1])
                string2 = str(args[2])
                compare = int(float(str(args[3])))
            else:
                return 0.0

            # 開始位置の調整（1ベースから0ベースへ）
            if start < 1:
                return 0.0
            start_idx = start - 1

            # string1の長さチェック
            if len(string1) == 0:
                return 0.0

            # string2が空の場合はstartを返す（VBA仕様）
            if len(string2) == 0:
                return float(start)

            # 開始位置が文字列長を超える場合
            if start_idx >= len(string1):
                return 0.0

            # 検索実行
            if compare == 0:
                # バイナリ比較（大文字小文字を区別）
                pos = string1.find(string2, start_idx)
            else:
                # テキスト比較（大文字小文字を区別しない）
                pos = string1.upper().find(string2.upper(), start_idx)

            # 結果を1ベースで返す（見つからない場合は-1が返るので0に変換）
            return float(pos + 1) if pos >= 0 else 0.0

        except Exception:
            return 0.0

    @staticmethod
    def IF(condition: Any, true_value: Any, false_value: Any) -> Any:
        """
        条件分岐

        Args:
            condition: 評価する条件
            true_value: 条件が真の場合の返値
            false_value: 条件が偽の場合の返値

        Returns:
            条件に応じたtrue_valueまたはfalse_value
        """
        # 条件を真偽値として評価
        is_true = False
        if isinstance(condition, bool):
            is_true = condition
        elif isinstance(condition, (int, float)):
            is_true = condition != 0
        elif isinstance(condition, str):
            is_true = len(condition) > 0 and condition.upper() not in ['FALSE', '0', '']

        return true_value if is_true else false_value

    @staticmethod
    def PRINT(value: Any) -> str:
        """
        出力関数（スクリプトエンジンで特殊処理される）

        Args:
            value: 出力する値

        Returns:
            文字列化された値
        """
        # この関数はscript_engine.pyで特殊処理される
        return str(value) if value is not None else ""