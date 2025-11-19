# -*- coding: utf-8 -*-
"""
正規表現関数のモジュール
Regular expression functions module
"""

from typing import Any
import re

class RegexFunctions:
    """正規表現関数のクラス"""

    @staticmethod
    def REGEX(pattern: Any, text: Any) -> float:
        """
        正規表現パターンにマッチするかを判定（真なら1.0、偽なら0.0）

        Args:
            pattern: 正規表現パターン
            text: 検索対象のテキスト

        Returns:
            マッチした場合は1.0、しない場合は0.0
        """
        try:
            pattern_str = str(pattern)
            text_str = str(text) if text is not None else ""

            match = re.search(pattern_str, text_str)
            return 1.0 if match else 0.0
        except re.error:
            return 0.0
        except Exception:
            return 0.0

    @staticmethod
    def REGEXMATCH(pattern: Any, text: Any) -> str:
        """
        正規表現パターンがテキストにマッチするかをチェックし、最初の一致を返す

        Args:
            pattern: 正規表現パターン
            text: 検索対象のテキスト

        Returns:
            最初にマッチした文字列。マッチしない場合は空文字
        """
        try:
            pattern_str = str(pattern)
            text_str = str(text) if text is not None else ""

            match = re.search(pattern_str, text_str)
            if match:
                return match.group(0)
            return ""
        except re.error:
            return ""
        except Exception:
            return ""

    @staticmethod
    def REGEXREPLACE(pattern: Any, text: Any, replacement: Any) -> str:
        """
        正規表現パターンにマッチする部分を置換

        Args:
            pattern: 正規表現パターン
            text: 対象のテキスト
            replacement: 置換文字列（$1, $2 または \1, \2 形式のバックリファレンスをサポート）

        Returns:
            置換後の文字列
        """
        try:
            pattern_str = str(pattern)
            text_str = str(text) if text is not None else ""
            replacement_str = str(replacement) if replacement is not None else ""

            # 置換パターンの処理
            # $1, $2 形式を \g<1>, \g<2> 形式に変換（優先）
            replacement_str = re.sub(r'\$(\d+)', r'\\g<\1>', replacement_str)
            # \1, \2 形式も \g<1>, \g<2> 形式に変換（後方互換性）
            replacement_str = re.sub(r'\\(\d+)', r'\\g<\1>', replacement_str)

            return re.sub(pattern_str, replacement_str, text_str)
        except:
            # エラーの場合は元のテキストを返す
            return str(text) if text is not None else ""

    @staticmethod
    def REGEXEXTRACT(pattern: Any, text: Any, group_index: Any = 0) -> str:
        """
        正規表現パターンの指定グループを抽出

        Args:
            pattern: 正規表現パターン（グループを含む）
            text: 検索対象のテキスト
            group_index: 抽出するグループのインデックス（0は全体）

        Returns:
            抽出した文字列、マッチしない場合は空文字列
        """
        try:
            pattern_str = str(pattern)
            text_str = str(text) if text is not None else ""

            # グループインデックスを整数に変換
            try:
                group_idx = int(float(group_index))
            except:
                group_idx = 0

            if group_idx < 0:
                group_idx = 0

            match = re.search(pattern_str, text_str)
            if match:
                try:
                    return match.group(group_idx)
                except IndexError:
                    # グループが存在しない場合は空文字列
                    return ""
            else:
                return ""
        except:
            return ""

    @staticmethod
    def REGEXCOUNT(pattern: Any, text: Any) -> float:
        """
        正規表現パターンのマッチ数をカウント

        Args:
            pattern: 正規表現パターン
            text: 検索対象のテキスト

        Returns:
            マッチした回数
        """
        try:
            pattern_str = str(pattern)
            text_str = str(text) if text is not None else ""

            matches = re.findall(pattern_str, text_str)
            return float(len(matches))
        except:
            return 0.0

    @staticmethod
    def REGEXMATCHES(pattern: Any, text: Any) -> list:
        """
        正規表現パターンにマッチするすべての文字列を返す
        注：この関数は配列を返すため、script_engine.pyで特殊処理が必要

        Args:
            pattern: 正規表現パターン
            text: 検索対象のテキスト

        Returns:
            マッチした文字列のリスト
        """
        try:
            pattern_str = str(pattern)
            text_str = str(text) if text is not None else ""

            matches = re.findall(pattern_str, text_str)
            return matches if matches else []
        except:
            return []

    @staticmethod
    def REGEXSPLIT(pattern: Any, text: Any) -> list:
        """
        正規表現パターンで文字列を分割
        注：この関数は配列を返すため、script_engine.pyで特殊処理が必要

        Args:
            pattern: 区切りパターン
            text: 分割する文字列

        Returns:
            分割された文字列のリスト
        """
        try:
            pattern_str = str(pattern)
            text_str = str(text) if text is not None else ""

            parts = re.split(pattern_str, text_str)
            return parts if parts else []
        except:
            # エラーの場合は元のテキストを1要素のリストとして返す
            return [str(text) if text is not None else ""]

    # エイリアス関数
    @staticmethod
    def REGEX_MATCH(pattern: Any, text: Any) -> float:
        """REGEXのエイリアス"""
        return RegexFunctions.REGEX(pattern, text)

    @staticmethod
    def REGEX_REPLACE(pattern: Any, text: Any, replacement: Any) -> str:
        """REGEXREPLACEのエイリアス"""
        return RegexFunctions.REGEXREPLACE(pattern, text, replacement)

    @staticmethod
    def REGEX_FIND(pattern: Any, text: Any) -> str:
        """REGEXMATCHのエイリアス"""
        return RegexFunctions.REGEXMATCH(pattern, text)

    @staticmethod
    def REGEX_FINDALL(pattern: Any, text: Any) -> list:
        """REGEXMATCHESのエイリアス"""
        return RegexFunctions.REGEXMATCHES(pattern, text)