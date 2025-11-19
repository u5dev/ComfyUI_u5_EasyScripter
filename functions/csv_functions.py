# -*- coding: utf-8 -*-
"""
CSV操作関数のモジュール
CSV manipulation functions module
"""

from typing import Any
import random

class CsvFunctions:
    """CSV操作関数のクラス"""

    @staticmethod
    def RNDCSV(csv_text: Any, count: Any = None):
        """
        CSV形式のテキストからランダムに要素を選択

        Args:
            csv_text: カンマ区切りのテキスト（例: "a,b,c,d,e"）
            count: 選択する要素数（省略時は1つの文字列を返す）

        Returns:
            - count未指定時: ランダムに選択された1つの要素（文字列）
            - count指定時: ランダムに選択された要素のリスト
            - count >= 要素数: 元のソート順を維持した完全配列

        Examples:
            RNDCSV("apple,banana,orange") → "banana" （ランダムに1つ選択）
            RNDCSV("A,B,B,B,C,C,D", 3) → ["B", "B", "D"] （ランダムに3つ選択）
            RNDCSV("A,B,C", 5) → ["A", "B", "C"] （要素数超過時は元の順序で全要素）
        """
        try:
            # 文字列に変換
            text = str(csv_text)

            # カンマで分割（前後の空白を削除）
            elements = [elem.strip() for elem in text.split(',')]

            # 空の要素を除外
            elements = [elem for elem in elements if elem]

            # 要素がない場合
            if not elements:
                if count is None:
                    return ""
                else:
                    return []

            # count未指定時は従来通り1つの文字列を返す
            if count is None:
                return random.choice(elements)

            # count指定時
            try:
                count_int = int(float(count))
            except (ValueError, TypeError):
                # 無効なcountの場合は1つ返す
                return random.choice(elements)

            # count=1の場合は文字列を返す（配列にしない）
            if count_int == 1:
                return random.choice(elements)

            # count >= 要素数の場合は元の順序で全要素を返す
            if count_int >= len(elements):
                return elements

            # ランダムに指定数選択（重複あり）
            return random.choices(elements, k=count_int)

        except Exception:
            # エラーが発生した場合
            if count is None:
                return ""
            else:
                return []

    @staticmethod
    def CSVCOUNT(csv_text: Any) -> float:
        """
        CSV形式のテキストの要素数をカウント

        Args:
            csv_text: カンマ区切りのテキスト

        Returns:
            要素の数

        Examples:
            CSVCOUNT("a,b,c,d") → 4
            CSVCOUNT("apple,banana,orange") → 3
            CSVCOUNT("") → 0
        """
        if csv_text is None or str(csv_text).strip() == "":
            return 0.0

        text_str = str(csv_text).strip()
        # 空文字列の場合は0を返す
        if text_str == "":
            return 0.0

        # カンマで分割して要素数を返す
        elements = text_str.split(",")
        return float(len(elements))

    @staticmethod
    def CSVREAD(csv_text: Any, index: Any) -> str:
        """
        CSV形式のテキストから指定したインデックスの要素を取得

        Args:
            csv_text: カンマ区切りのテキスト
            index: 取得する要素のインデックス（1ベース）

        Returns:
            指定されたインデックスの要素（範囲外の場合は空文字列）

        Examples:
            CSVREAD("a,b,c", 1) → "a"
            CSVREAD("a,b,c", 2) → "b"
            CSVREAD("a,b,c", 3) → "c"
            CSVREAD("a,b,c", 4) → ""
        """
        if csv_text is None or str(csv_text).strip() == "":
            return ""

        text_str = str(csv_text).strip()
        if text_str == "":
            return ""

        try:
            # インデックスを整数に変換
            index_int = int(float(str(index)))
        except (ValueError, TypeError):
            return ""

        # カンマで分割
        elements = text_str.split(",")

        # 1ベースインデックスを0ベースに変換してチェック
        zero_based_index = index_int - 1
        if 0 <= zero_based_index < len(elements):
            return elements[zero_based_index].strip()
        else:
            return ""

    @staticmethod
    def CSVUNIQUE(csv_text: Any) -> str:
        """
        CSV形式のテキストから重複を削除してユニークな要素のみ返す

        Args:
            csv_text: カンマ区切りのテキスト

        Returns:
            重複を削除したCSV文字列

        Examples:
            CSVUNIQUE("a,b,a,c,b") → "a,b,c"
            CSVUNIQUE("1,2,3,2,1") → "1,2,3"
            CSVUNIQUE("Apple,apple,APPLE") → "Apple" (大文字小文字を区別しない)
        """
        if csv_text is None or str(csv_text).strip() == "":
            return ""

        text_str = str(csv_text).strip()
        if text_str == "":
            return ""

        # カンマで分割
        elements = text_str.split(",")

        # 重複を削除（大文字小文字を区別しない）
        seen = {}
        unique_elements = []
        for element in elements:
            element_stripped = element.strip()
            element_upper = element_stripped.upper()
            if element_upper not in seen:
                seen[element_upper] = True
                unique_elements.append(element_stripped)

        return ",".join(unique_elements)

    @staticmethod
    def CSVMERGE(*csv_texts) -> str:
        """
        複数のCSV形式のテキストをマージ

        Args:
            *csv_texts: 可変長のCSVテキスト

        Returns:
            マージされたCSV文字列

        Examples:
            CSVMERGE("a,b", "c,d", "e,f") → "a,b,c,d,e,f"
            CSVMERGE("1,2", "3,4") → "1,2,3,4"
        """
        all_elements = []
        for csv_text in csv_texts:
            if csv_text is not None:
                text_str = str(csv_text).strip()
                # 空文字列も保持（空要素として追加）
                elements = text_str.split(",")
                all_elements.extend([e.strip() for e in elements])

        return ",".join(all_elements)

    @staticmethod
    def CSVSORT(csv_text: Any, delimiter: str = ",", descending: bool = False) -> str:
        """
        CSV形式のテキストをソート

        Args:
            csv_text: 区切り文字で区切られたテキスト
            delimiter: 区切り文字（デフォルト: ","）
            descending: Trueの場合降順、Falseの場合昇順（デフォルト: False）

        Returns:
            ソートされたCSV文字列

        Examples:
            CSVSORT("banana,apple,orange") → "apple,banana,orange"
            CSVSORT("3,1,2") → "1,2,3"  # 文字列として"10,2,5"なら"10,2,5"
            CSVSORT("z,a,m", ",", 1) → "z,m,a"  （降順）
            CSVSORT("z;a;m", ";") → "a;m;z"  （セミコロン区切り、昇順）
        """
        if csv_text is None or str(csv_text).strip() == "":
            return ""

        try:
            text_str = str(csv_text).strip()
            if text_str == "":
                return ""

            # 区切り文字が指定されていない場合はカンマをデフォルトとする
            if delimiter is None or delimiter == "":
                delimiter = ","

            # 区切り文字で分割
            elements = [e.strip() for e in text_str.split(delimiter)]

            # 空要素を除外
            elements = [e for e in elements if e]

            # 常に文字列としてソート（CSV要素は文字列として扱う）
            elements.sort(reverse=bool(descending))
            return delimiter.join(elements)
        except:
            return ""

    @staticmethod
    def PICKCSV(csv_text: Any, index: Any = None) -> str:
        """
        CSV形式のテキストからN番目の要素を選択

        Args:
            csv_text: カンマ区切りのテキスト（例: "a,b,c,d,e"）
            index: 選択する要素のインデックス（1ベース）。0の場合はランダム選択

        Returns:
            指定されたインデックスの要素（文字列）
            インデックスが範囲外の場合はループして要素を選択

        Examples:
            PICKCSV("apple,banana,orange", 1) → "apple" （1番目）
            PICKCSV("apple,banana,orange", 2) → "banana" （2番目）
            PICKCSV("apple,banana,orange", 0) → "orange" （ランダム選択）
            PICKCSV("apple,banana,orange", -1) → "orange" （末尾から1番目）
            PICKCSV("apple,banana,orange", 4) → "apple" （ループして1番目）
        """
        try:
            # 文字列に変換
            text = str(csv_text)

            # カンマで分割（前後の空白を削除）
            elements = [elem.strip() for elem in text.split(',')]

            # 空の要素を除外
            elements = [elem for elem in elements if elem]

            # 要素がない場合は空文字列を返す
            if not elements:
                return ""

            # インデックスを数値に変換
            try:
                idx = int(float(index)) if index is not None else 0
            except (ValueError, TypeError):
                # 無効なインデックスの場合はランダム選択
                return random.choice(elements)

            # インデックスが0の場合はランダム選択
            if idx == 0:
                return random.choice(elements)

            # 負のインデックスの処理（末尾から数える）
            if idx < 0:
                # 負のインデックスをPython式に変換
                idx = len(elements) + idx + 1

            # インデックスが範囲外の場合はモジュロ演算で循環
            if idx > 0:
                # 1ベースを0ベースに変換してモジュロ演算
                idx = ((idx - 1) % len(elements))
            else:
                # インデックスが0以下の場合は最後の要素を選択
                idx = len(elements) - 1

            return elements[idx]

        except Exception:
            # エラーが発生した場合は空文字列を返す
            return ""

    @staticmethod
    def CSVDIFF(csv1: Any, csv2: Any) -> list:
        """
        2つのCSVテキストから排他的要素（片方にしか存在しない要素）を返す

        Args:
            csv1: 1つ目のカンマ区切りテキスト
            csv2: 2つ目のカンマ区切りテキスト

        Returns:
            どちらか片方にしか存在しない要素のリスト

        Examples:
            CSVDIFF("a,b,c", "b,c,d") → ["a", "d"]
            CSVDIFF("1,2,3", "3,4,5") → ["1", "2", "4", "5"]
        """
        # CSV1の要素を取得
        elements1 = set()
        original_elements1 = {}
        if csv1 is not None and str(csv1).strip() != "":
            text1 = str(csv1).strip()
            if text1:
                for e in text1.split(","):
                    stripped = e.strip()
                    upper = stripped.upper()
                    elements1.add(upper)
                    if upper not in original_elements1:
                        original_elements1[upper] = stripped

        # CSV2の要素を取得
        elements2 = set()
        original_elements2 = {}
        if csv2 is not None and str(csv2).strip() != "":
            text2 = str(csv2).strip()
            if text2:
                for e in text2.split(","):
                    stripped = e.strip()
                    upper = stripped.upper()
                    elements2.add(upper)
                    if upper not in original_elements2:
                        original_elements2[upper] = stripped

        # 排他的要素（どちらか片方にしか存在しない要素）
        diff_elements = (elements1 - elements2) | (elements2 - elements1)

        # 元の大文字小文字を保持して結果を作成
        result = []
        for upper_elem in diff_elements:
            if upper_elem in original_elements1:
                result.append(original_elements1[upper_elem])
            elif upper_elem in original_elements2:
                result.append(original_elements2[upper_elem])

        # 結果をソートして返す
        result.sort()
        return result

    @staticmethod
    def CSVJOIN(source_array, delimiter: str = ",") -> str:
        """
        配列の要素を区切り文字で結合してCSV文字列を作成

        Args:
            source_array: 結合する要素のリスト（list型またはScript Engineの辞書型配列 {0: val, 1: val, ...}）
            delimiter: 区切り文字（省略時はカンマ）

        Returns:
            結合されたCSV文字列
        """
        try:
            # Script Engineの辞書型配列 {0: value, 1: value, ...} の場合
            if isinstance(source_array, dict):
                # キーが整数の場合は配列として扱う
                if source_array and all(isinstance(k, int) for k in source_array.keys()):
                    # キーでソートして値を取り出す
                    sorted_items = sorted(source_array.items(), key=lambda x: x[0])
                    str_elements = [str(value) for key, value in sorted_items]
                    return delimiter.join(str_elements)
                else:
                    # 通常の辞書の場合はそのまま文字列化
                    return str(source_array)

            # Pythonのlist型の場合
            if isinstance(source_array, list):
                # すべての要素を文字列に変換
                str_elements = [str(element) for element in source_array]
                return delimiter.join(str_elements)

            # その他の型の場合
            return str(source_array) if source_array is not None else ""
        except:
            return ""

    # エイリアス関数
    @staticmethod
    def RANDCSV(csv_text: Any, count: Any = None):
        """RNDCSVのエイリアス"""
        return CsvFunctions.RNDCSV(csv_text, count)