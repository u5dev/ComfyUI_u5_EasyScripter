# -*- coding: utf-8 -*-
"""
文字列操作関数のモジュール
String manipulation functions module
"""

import re
from typing import Any
from urllib.parse import quote, unquote

class StringFunctions:
    """文字列操作関数のクラス"""

    @staticmethod
    def LEN(value: Any) -> float:
        """
        文字列の長さを返す

        Args:
            value: 文字列または文字列に変換可能な値

        Returns:
            文字列の長さ
        """
        try:
            # 数値の場合、整数化してから文字列に変換（VBA仕様）
            if isinstance(value, float) and value.is_integer():
                str_value = str(int(value))
            else:
                str_value = str(value)
            return float(len(str_value))
        except:
            return 0.0

    # LEFT関数は base_functions.py に移動

    # RIGHT関数は base_functions.py に移動

    # MID関数は base_functions.py に移動

    @staticmethod
    def UPPER(value: Any) -> str:
        """
        文字列を大文字に変換

        Args:
            value: 文字列

        Returns:
            大文字に変換された文字列
        """
        try:
            return str(value).upper()
        except:
            return ""

    @staticmethod
    def LOWER(value: Any) -> str:
        """
        文字列を小文字に変換

        Args:
            value: 文字列

        Returns:
            小文字に変換された文字列
        """
        try:
            return str(value).lower()
        except:
            return ""

    @staticmethod
    def UCASE(value: Any) -> str:
        """
        文字列を大文字に変換（UPPERのエイリアス）

        Args:
            value: 文字列

        Returns:
            大文字に変換された文字列
        """
        return StringFunctions.UPPER(value)

    @staticmethod
    def LCASE(value: Any) -> str:
        """
        文字列を小文字に変換（LOWERのエイリアス）

        Args:
            value: 文字列

        Returns:
            小文字に変換された文字列
        """
        return StringFunctions.LOWER(value)

    @staticmethod
    def TRIM(value: Any) -> str:
        """
        文字列の前後の空白を削除

        Args:
            value: 文字列

        Returns:
            前後の空白を削除した文字列
        """
        try:
            return str(value).strip()
        except:
            return ""

    @staticmethod
    def LTRIM(value: Any) -> str:
        """
        文字列の左側の空白を削除

        Args:
            value: 文字列

        Returns:
            左側の空白を削除した文字列
        """
        try:
            return str(value).lstrip()
        except:
            return ""

    @staticmethod
    def RTRIM(value: Any) -> str:
        """
        文字列の右側の空白を削除

        Args:
            value: 文字列

        Returns:
            右側の空白を削除した文字列
        """
        try:
            return str(value).rstrip()
        except:
            return ""

    @staticmethod
    def REPLACE(string: Any, old: Any, new: Any) -> str:
        """
        文字列置換

        Args:
            string: 対象文字列
            old: 置換元文字列
            new: 置換先文字列

        Returns:
            置換後の文字列
        """
        try:
            str_value = str(string)
            old_value = str(old)
            new_value = str(new)
            return str_value.replace(old_value, new_value)
        except:
            return ""

    # INSTR関数は base_functions.py に移動

    @staticmethod
    def INSTRREV(*args) -> float:
        """
        文字列内で部分文字列を検索（後ろから）

        Args:
            引数パターン1: INSTRREV(stringcheck, stringmatch)
            引数パターン2: INSTRREV(stringcheck, stringmatch, start)
            引数パターン3: INSTRREV(stringcheck, stringmatch, start, compare)

            stringcheck: 検索対象文字列
            stringmatch: 検索する文字列
            start: 検索開始位置（1ベース、省略時は-1で末尾から）
            compare: 0=バイナリ比較、1=テキスト比較（省略時は1）

        Returns:
            見つかった位置（1ベース）、見つからない場合は0
        """
        try:
            # 引数の解析
            if len(args) < 2:
                return 0.0

            stringcheck = str(args[0])
            stringmatch = str(args[1])

            # startパラメータ
            if len(args) >= 3:
                start = int(float(str(args[2])))
                if start == -1 or start > len(stringcheck):
                    start = len(stringcheck)
                elif start < 1:
                    return 0.0
            else:
                start = len(stringcheck)

            # compareパラメータ
            if len(args) >= 4:
                compare = int(float(str(args[3])))
            else:
                compare = 1  # デフォルトは大文字小文字を区別しない

            # 空文字列チェック
            if len(stringcheck) == 0:
                return 0.0

            if len(stringmatch) == 0:
                return float(start)

            # 検索実行（後ろから）
            if compare == 0:
                # バイナリ比較（大文字小文字を区別）
                pos = -1
                search_start = 0
                while True:
                    temp_pos = stringcheck.find(stringmatch, search_start)
                    if temp_pos == -1:
                        break
                    # マッチの終了位置を計算
                    end_pos = temp_pos + len(stringmatch)
                    if end_pos <= start:
                        pos = temp_pos
                    search_start = temp_pos + 1
            else:
                # テキスト比較（大文字小文字を区別しない）
                pos = -1
                search_start = 0
                upper_check = stringcheck.upper()
                upper_match = stringmatch.upper()
                while True:
                    temp_pos = upper_check.find(upper_match, search_start)
                    if temp_pos == -1:
                        break
                    # マッチの終了位置を計算
                    end_pos = temp_pos + len(stringmatch)
                    if end_pos <= start:
                        pos = temp_pos
                    search_start = temp_pos + 1

            # 結果を1ベースで返す
            return float(pos + 1) if pos >= 0 else 0.0

        except Exception:
            return 0.0

    @staticmethod
    def PROPER(value: Any) -> str:
        """
        各単語の先頭を大文字に変換（タイトルケース）

        Args:
            value: 文字列

        Returns:
            タイトルケースに変換した文字列
        """
        try:
            return str(value).title()
        except:
            return ""

    @staticmethod
    def CHR(value: Any) -> str:
        """
        文字コードから文字へ変換

        Args:
            value: 文字コード（ASCII）

        Returns:
            対応する文字
        """
        try:
            code = int(float(value))
            if 0 <= code <= 127:
                return chr(code)
            else:
                return ""
        except:
            return ""

    @staticmethod
    def ASC(value: Any) -> float:
        """
        文字から文字コードへ変換

        Args:
            value: 文字または文字列（最初の文字を使用）

        Returns:
            文字コード（ASCII）
        """
        try:
            str_value = str(value)
            if str_value:
                return float(ord(str_value[0]))
            else:
                return 0.0
        except:
            return 0.0

    @staticmethod
    def STR(value: Any) -> str:
        """
        数値を文字列に変換

        Args:
            value: 数値

        Returns:
            文字列化された数値
        """
        try:
            num_value = float(value)
            # 整数の場合は小数点なしで返す
            if num_value.is_integer():
                return str(int(num_value))
            else:
                return str(num_value)
        except:
            return str(value) if value is not None else ""

    @staticmethod
    def STRREVERSE(text: Any) -> str:
        """
        文字列を反転（VBA互換）

        Args:
            text: 反転する文字列

        Returns:
            反転した文字列
        """
        if text is None:
            return ""
        return str(text)[::-1]

    @staticmethod
    def STRCOMP(string1: Any, string2: Any, compare: int = 0) -> float:
        """
        文字列を比較（VBA互換）

        Args:
            string1: 比較する文字列1
            string2: 比較する文字列2
            compare: 比較方法（0=バイナリ，1=テキスト（大文字小文字を区別しない））

        Returns:
            -1: string1 < string2
             0: string1 = string2
             1: string1 > string2
        """
        try:
            str1 = str(string1) if string1 is not None else ""
            str2 = str(string2) if string2 is not None else ""

            # 比較モードの判定
            try:
                cmp_mode = int(float(compare))
            except:
                cmp_mode = 0

            # テキスト比較の場合、大文字小文字を区別しない
            if cmp_mode == 1:
                str1 = str1.upper()
                str2 = str2.upper()

            # 比較
            if str1 < str2:
                return -1.0
            elif str1 > str2:
                return 1.0
            else:
                return 0.0
        except:
            return 0.0

    @staticmethod
    def SPACE(number: Any) -> str:
        """
        指定した数のスペースを生成（VBA互換）

        Args:
            number: スペースの数

        Returns:
            指定した数のスペース
        """
        try:
            num = int(float(number))
            if num < 0:
                return ""
            return " " * num
        except:
            return ""

    @staticmethod
    def STRING(number: Any, character: Any = None) -> str:
        """
        指定した文字を繰り返した文字列を生成（VBA互換）

        Args:
            number: 繰り返し数
            character: 繰り返す文字（省略時はスペース）

        Returns:
            指定した文字を繰り返した文字列
        """
        try:
            num = int(float(number))
            if num < 0:
                return ""

            if character is None or character == "":
                char = " "
            else:
                char_str = str(character)
                # 最初の1文字のみ使用
                char = char_str[0] if char_str else " "

            return char * num
        except:
            return ""

    # 配列操作関数（文字列関連）
    @staticmethod
    def SPLIT(expression: Any, delimiter: str = " ") -> list:
        """
        文字列を区切り文字で分割して配列を返す

        Args:
            expression: 分割する文字列
            delimiter: 区切り文字（省略時はスペース）

        Returns:
            分割された文字列のリスト
        """
        try:
            text = str(expression) if expression is not None else ""
            if delimiter == "":
                # 空の区切り文字の場合は各文字に分割
                return list(text)
            else:
                return text.split(delimiter)
        except:
            return []

    @staticmethod
    def JOIN(source_array: list, delimiter: str = " ") -> str:
        """
        配列の要素を区切り文字で結合

        Args:
            source_array: 結合する要素のリスト
            delimiter: 区切り文字（省略時はスペース）

        Returns:
            結合された文字列
        """
        try:
            if not isinstance(source_array, list):
                return str(source_array) if source_array is not None else ""

            # すべての要素を文字列に変換
            str_elements = [str(element) for element in source_array]
            return delimiter.join(str_elements)
        except:
            return ""

    @staticmethod
    def URLENCODE(text: str, encoding: str = "utf-8") -> str:
        """
        URLエンコード（パーセントエンコーディング）を実行

        Args:
            text: エンコードする文字列
            encoding: 文字エンコーディング（デフォルト: utf-8）

        Returns:
            URLエンコードされた文字列

        Example:
            ' 日本語をURLエンコード
            encoded = URLENCODE("あいうえお")
            PRINT(encoded)  ' → %E3%81%82%E3%81%84%E3%81%86%E3%81%88%E3%81%8A

            ' 検索クエリをエンコード
            query = "EasyScripter HTTP 関数"
            url = "https://www.google.com/search?q=" & URLENCODE(query)
        """
        if not isinstance(text, str):
            raise ValueError("URLENCODE: 引数は文字列である必要があります")
        
        # URLエンコード（RFC 3986準拠）
        # safe='' で全ての特殊文字をエンコード
        return quote(text, safe='', encoding=encoding)

    @staticmethod
    def URLDECODE(text: str, encoding: str = "utf-8") -> str:
        """
        URLデコード（パーセントエンコーディングのデコード）を実行

        Args:
            text: デコードする文字列
            encoding: 文字エンコーディング（デフォルト: utf-8）

        Returns:
            URLデコードされた文字列

        Example:
            ' URLエンコードされた文字列をデコード
            decoded = URLDECODE("%E3%81%82%E3%81%84%E3%81%86%E3%81%88%E3%81%8A")
            PRINT(decoded)  ' → あいうえお

            ' クエリパラメータをデコード
            param = URLDECODE("EasyScripter+HTTP+%E9%96%A2%E6%95%B0")
            PRINT(param)  ' → EasyScripter+HTTP+関数
        """
        if not isinstance(text, str):
            raise ValueError("URLDECODE: 引数は文字列である必要があります")
        
        # URLデコード
        return unquote(text, encoding=encoding)

    @staticmethod
    def ESCAPEPATHSTR(path: str, replacement: str = "") -> str:
        """
        ファイルパスの禁則文字を置換または削除
        
        Linux/Windowsでファイル名・パスに使用できない文字を処理します。
        
        Args:
            path: 処理対象の文字列
            replacement: 置換文字列（省略時は削除）
        
        Returns:
            禁則文字を処理した文字列
        
        禁則文字:
            \\, /, :, *, ?, ", <, >, |
        
        予約語（ファイル名全体として禁止）:
            CON, PRN, AUX, NUL, COM1-9, LPT1-9
            ※大文字小文字を区別しない
            ※ファイル名の一部としては許容
        
        Example:
            ' 禁則文字をアンダースコアに置換
            safe_name = ESCAPEPATHSTR("file:name*.txt", "_")
            PRINT(safe_name)  ' → file_name_.txt
            
            ' 禁則文字を削除
            safe_name = ESCAPEPATHSTR("file:name*.txt")
            PRINT(safe_name)  ' → filename.txt
            
            ' 予約語の処理
            safe_name = ESCAPEPATHSTR("CON.txt", "_")
            PRINT(safe_name)  ' → _.txt
        """
        if not isinstance(path, str):
            raise ValueError("ESCAPEPATHSTR: 第1引数は文字列である必要があります")
        
        if not isinstance(replacement, str):
            raise ValueError("ESCAPEPATHSTR: 第2引数は文字列である必要があります")
        
        # 空文字列の場合はそのまま返す
        if not path:
            return path
        
        # 禁則文字: \, /, :, *, ?, ", <, >, |
        forbidden_chars = r'[\\/:*?"<>|]'
        result = re.sub(forbidden_chars, replacement, path)
        
        # 予約語リスト（大文字小文字を区別しない）
        # CON, PRN, AUX, NUL, COM1-9, LPT1-9
        reserved_names = [
            'CON', 'PRN', 'AUX', 'NUL',
            'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
            'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
        ]
        
        # ファイル名全体が予約語かチェック
        # 予約語または予約語.拡張子の形式をチェック
        name_upper = result.upper()
        
        # 完全一致（拡張子なし）
        if name_upper in reserved_names:
            return replacement
        
        # 予約語.拡張子の形式をチェック
        for reserved in reserved_names:
            # 予約語.任意の拡張子
            if name_upper == reserved or name_upper.startswith(reserved + '.'):
                # ファイル名部分（最初のドットの前）が予約語と完全一致する場合
                dot_pos = result.find('.')
                if dot_pos > 0:
                    name_part = result[:dot_pos].upper()
                    if name_part == reserved:
                        # 予約語部分を置換
                        result = replacement + result[dot_pos:]
                        break
                elif name_upper == reserved:
                    result = replacement
                    break
        
        return result
