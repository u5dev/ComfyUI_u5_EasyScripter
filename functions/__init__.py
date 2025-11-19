# -*- coding: utf-8 -*-
"""
ビルトイン関数モジュール
各機能別モジュールから関数をインポートし、統合されたインターフェースを提供
"""

# 各モジュールから関数クラスをインポート
from .base_functions import BaseFunctions
from .math_functions import MathFunctions
from .string_functions import StringFunctions
from .date_functions import DateFunctions
from .csv_functions import CsvFunctions
from .regex_functions import RegexFunctions
from .misc_functions import MiscFunctions

# 全ての関数を一つのクラスにまとめる
class BuiltinFunctions(
    BaseFunctions,
    MathFunctions,
    StringFunctions,
    DateFunctions,
    CsvFunctions,
    RegexFunctions,
    MiscFunctions
):
    """
    全てのビルトイン関数を統合したクラス
    各機能モジュールから継承して、統一されたインターフェースを提供
    """
    pass

# モジュールレベルでの関数マッピング（後方互換性のため）
__all__ = [
    'BuiltinFunctions',
    'BaseFunctions',
    'MathFunctions',
    'StringFunctions',
    'DateFunctions',
    'CsvFunctions',
    'RegexFunctions',
    'MiscFunctions'
]