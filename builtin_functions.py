# -*- coding: utf-8 -*-
"""
ビルトイン関数の実装（モジュール化版）
各機能別モジュールから関数をインポートして統合したインターフェースを提供
"""

from typing import Any, Optional
try:
    from .functions import BuiltinFunctions
    from .functions.model_functions import builtin_optimal_latent
    from .functions.loop_functions import builtin_loop_subgraph
    from .functions.http_functions import HttpFunctions, JsonFunctions
    from .functions.python_functions import PythonFunctions
    from .functions.misc_functions import MiscFunctions
except ImportError:
    from functions import BuiltinFunctions
    from functions.model_functions import builtin_optimal_latent
    from functions.loop_functions import builtin_loop_subgraph
    from functions.http_functions import HttpFunctions, JsonFunctions
    from functions.python_functions import PythonFunctions
    from functions.misc_functions import MiscFunctions

# 関数名のマッピング（大文字小文字を区別しない）
BUILTIN_FUNCTIONS = {
    # 数学関数
    'ABS': BuiltinFunctions.ABS,
    'INT': BuiltinFunctions.INT,
    'ROUND': BuiltinFunctions.ROUND,
    'SQRT': BuiltinFunctions.SQRT,
    'SQR': BuiltinFunctions.SQRT,  # VBA互換のSQR
    'POW': BuiltinFunctions.POW,
    'LOG': BuiltinFunctions.LOG,
    'EXP': BuiltinFunctions.EXP,
    'FIX': BuiltinFunctions.FIX,
    'SGN': BuiltinFunctions.SGN,
    'LOG10': BuiltinFunctions.LOG10,
    'CEILING': BuiltinFunctions.CEILING,
    'FLOOR': BuiltinFunctions.FLOOR,
    # 三角関数
    'SIN': BuiltinFunctions.SIN,
    'COS': BuiltinFunctions.COS,
    'TAN': BuiltinFunctions.TAN,
    'ASIN': BuiltinFunctions.ASIN,
    'ACOS': BuiltinFunctions.ACOS,
    'ATAN': BuiltinFunctions.ATAN,
    'RADIANS': BuiltinFunctions.RADIANS,
    'DEGREES': BuiltinFunctions.DEGREES,
    # 集計関数
    'MIN': BuiltinFunctions.MIN,
    'MAX': BuiltinFunctions.MAX,
    'AVG': BuiltinFunctions.AVG,
    'SUM': BuiltinFunctions.SUM,
    # 文字列関数
    'LEN': BuiltinFunctions.LEN,
    'LEFT': BuiltinFunctions.LEFT,
    'RIGHT': BuiltinFunctions.RIGHT,
    'MID': BuiltinFunctions.MID,
    'UPPER': BuiltinFunctions.UPPER,
    'LOWER': BuiltinFunctions.LOWER,
    'UCASE': BuiltinFunctions.UCASE,  # UPPERのエイリアス
    'LCASE': BuiltinFunctions.LCASE,  # LOWERのエイリアス
    'VAL': BuiltinFunctions.VAL,      # 文字列を数値に変換
    'TRIM': BuiltinFunctions.TRIM,
    'REPLACE': BuiltinFunctions.REPLACE,
    'INSTR': BuiltinFunctions.INSTR,
    'INSTRREV': BuiltinFunctions.INSTRREV,
    'LTRIM': BuiltinFunctions.LTRIM,
    'RTRIM': BuiltinFunctions.RTRIM,
    'PROPER': BuiltinFunctions.PROPER,
    'CHR': BuiltinFunctions.CHR,
    'ASC': BuiltinFunctions.ASC,
    'STR': BuiltinFunctions.STR,
    'STRREVERSE': BuiltinFunctions.STRREVERSE,
    'STRCOMP': BuiltinFunctions.STRCOMP,
    'SPACE': BuiltinFunctions.SPACE,
    'STRING': BuiltinFunctions.STRING,
    'URLENCODE': BuiltinFunctions.URLENCODE,
    'URLDECODE': BuiltinFunctions.URLDECODE,
    'ESCAPEPATHSTR': BuiltinFunctions.ESCAPEPATHSTR,
    # 論理関数
    'IIF': BuiltinFunctions.IIF,  # IFはIF文と競合するためIIFのみサポート
    'IF': BuiltinFunctions.IF,    # 関数版のIF（3引数）
    # 乱数関数
    'RAND': BuiltinFunctions.RAND,
    'RND': BuiltinFunctions.RND,   # RANDのエイリアス
    'RANDOMIZE': BuiltinFunctions.RANDOMIZE,
    'RNDCSV': BuiltinFunctions.RNDCSV,
    'RANDCSV': BuiltinFunctions.RANDCSV,  # RNDCSVのエイリアス
    'PICKCSV': BuiltinFunctions.PICKCSV,
    # CSV関数
    'CSVCOUNT': BuiltinFunctions.CSVCOUNT,
    'CSVREAD': BuiltinFunctions.CSVREAD,
    'CSVUNIQUE': BuiltinFunctions.CSVUNIQUE,
    'CSVMERGE': BuiltinFunctions.CSVMERGE,
    'CSVDIFF': BuiltinFunctions.CSVDIFF,
    'CSVSORT': BuiltinFunctions.CSVSORT,
    'CSVJOIN': BuiltinFunctions.CSVJOIN,
    # フォーマット関数
    'FORMAT': BuiltinFunctions.FORMAT,
    # 日付・時刻関数
    'NOW': BuiltinFunctions.NOW,
    'DATE': BuiltinFunctions.DATE,
    'TIME': BuiltinFunctions.TIME,
    'YEAR': BuiltinFunctions.YEAR,
    'MONTH': BuiltinFunctions.MONTH,
    'DAY': BuiltinFunctions.DAY,
    'HOUR': BuiltinFunctions.HOUR,
    'MINUTE': BuiltinFunctions.MINUTE,
    'SECOND': BuiltinFunctions.SECOND,
    'WEEKDAY': BuiltinFunctions.WEEKDAY,
    'DATEADD': BuiltinFunctions.DATEADD,
    'DATEDIFF': BuiltinFunctions.DATEDIFF,
    'DATEVALUE': BuiltinFunctions.DATEVALUE,
    'TIMEVALUE': BuiltinFunctions.TIMEVALUE,
    'TIMER': BuiltinFunctions.TIMER,
    'CDATE': BuiltinFunctions.CDATE,
    # 型変換・検査関数
    'CSTR': BuiltinFunctions.CSTR,
    'CINT': BuiltinFunctions.CINT,
    'CDBL': BuiltinFunctions.CDBL,
    'ISNUMERIC': BuiltinFunctions.ISNUMERIC,
    'ISDATE': BuiltinFunctions.ISDATE,
    'ISARRAY': BuiltinFunctions.ISARRAY,
    'TYPE': BuiltinFunctions.TYPE,
    # I/O関数
    'PRINT': BuiltinFunctions.PRINT,
    'OUTPUT': BuiltinFunctions.OUTPUT,
    'INPUT': BuiltinFunctions.INPUT,
    'ISFILEEXIST': BuiltinFunctions.ISFILEEXIST,
    'VRAMFREE': BuiltinFunctions.VRAMFREE,
    'SLEEP': BuiltinFunctions.SLEEP,
    # 画像処理関数
    'IMAGETOBYTEARRAY': MiscFunctions.IMAGETOBYTEARRAY,
    'IMAGETOBASE64': MiscFunctions.IMAGETOBASE64,
    # 正規表現関数
    'REGEX': BuiltinFunctions.REGEX,
    'REGEX_MATCH': BuiltinFunctions.REGEX_MATCH,
    'REGEXMATCH': BuiltinFunctions.REGEXMATCH,
    'REGEX_FIND': BuiltinFunctions.REGEX_FIND,
    'REGEXREPLACE': BuiltinFunctions.REGEXREPLACE,
    'REGEX_REPLACE': BuiltinFunctions.REGEX_REPLACE,
    'REGEXEXTRACT': BuiltinFunctions.REGEXEXTRACT,
    'REGEXCOUNT': BuiltinFunctions.REGEXCOUNT,
    'REGEXMATCHES': BuiltinFunctions.REGEXMATCHES,
    'REGEX_FINDALL': BuiltinFunctions.REGEX_FINDALL,
    'REGEXSPLIT': BuiltinFunctions.REGEXSPLIT,
    # 配列関数
    'ARRAY': BuiltinFunctions.ARRAY,
    'UBOUND': BuiltinFunctions.UBOUND,
    'REDIM': BuiltinFunctions.REDIM,
    # 文字列配列関数
    'SPLIT': BuiltinFunctions.SPLIT,
    'JOIN': BuiltinFunctions.JOIN,
    # ANY型関数
    'GETANYTYPE': BuiltinFunctions.GETANYTYPE,
    'GETANYWIDTH': BuiltinFunctions.GETANYWIDTH,
    'GETANYHEIGHT': BuiltinFunctions.GETANYHEIGHT,
    'GETANYVALUEINT': BuiltinFunctions.GETANYVALUEINT,
    'GETANYVALUEFLOAT': BuiltinFunctions.GETANYVALUEFLOAT,
    'GETANYSTRING': BuiltinFunctions.GETANYSTRING,
    # モデル関連関数
    'OPTIMAL_LATENT': builtin_optimal_latent,
    'OPTIMALLATENT': builtin_optimal_latent,
    # ループ制御関数
    'LOOP_SUBGRAPH': builtin_loop_subgraph,
    'LOOPSUBGRAPH': builtin_loop_subgraph,
    # HTTP/HTTPS通信関数
    'HTTPGET': HttpFunctions.HTTPGET,
    'HTTPPOST': HttpFunctions.HTTPPOST,
    'HTTPPUT': HttpFunctions.HTTPPUT,
    'HTTPDELETE': HttpFunctions.HTTPDELETE,
    'HTTPJSON': HttpFunctions.HTTPJSON,
    'HTTPSTATUS': HttpFunctions.HTTPSTATUS,
    'HTTPHEADERS': HttpFunctions.HTTPHEADERS,
    # JSON操作関数
    'PARSEJSON': JsonFunctions.PARSEJSON,
    'GETJSON': JsonFunctions.GETJSON,
    'TOJSON': JsonFunctions.TOJSON,
    # Python関数実行
    'PYEXEC': PythonFunctions.PYEXEC,
    'PYLIST': PythonFunctions.PYLIST,
    'PYENCODE': PythonFunctions.PYENCODE,
    'PYDECODE': PythonFunctions.PYDECODE,
}

def is_builtin_function(name: str) -> bool:
    """指定された名前がビルトイン関数かどうかを判定"""
    name_upper = name.upper()
    # 通常のビルトイン関数
    if name_upper in BUILTIN_FUNCTIONS:
        return True
    # 特殊処理関数
    special_functions = ['REDIM', 'ARRAY', 'SPLIT', 'UBOUND', 'JOIN', 'ISARRAY',
                        'REGEXMATCHES', 'REGEXSPLIT', 'CSVDIFF', 'PRINT', 'LOOP_SUBGRAPH']
    return name_upper in special_functions

def get_builtin_function(name: str):
    """ビルトイン関数を取得"""
    return BUILTIN_FUNCTIONS.get(name.upper())

def get_function_usage(func_name: str) -> Optional[str]:
    """
    ビルトイン関数の使用例を取得

    Args:
        func_name: 関数名

    Returns:
        使用例の文字列、または該当しない場合はNone
    """
    func_name_upper = func_name.upper()

    # 各関数の使用例を定義
    usage_examples = {
        # 数学関数
        'ABS': 'ABS(-5) → 5',
        'INT': 'INT(3.7) → 3',
        'ROUND': 'ROUND(3.456, 2) → 3.46',
        'SQRT': 'SQRT(16) → 4',
        'SQR': 'SQR(16) → 4',
        'POW': 'POW(2, 3) → 8',
        'LOG': 'LOG(2.718282) → 1',
        'EXP': 'EXP(1) → 2.718282',

        # 三角関数
        'SIN': 'SIN(RADIANS(30)) → 0.5',
        'COS': 'COS(RADIANS(60)) → 0.5',
        'TAN': 'TAN(RADIANS(45)) → 1',
        'RADIANS': 'RADIANS(180) → 3.14159',
        'DEGREES': 'DEGREES(3.14159) → 180',

        # 集計関数
        'MIN': 'MIN(5, 3, 8) → 3',
        'MAX': 'MAX(5, 3, 8) → 8',
        'AVG': 'AVG(10, 20, 30) → 20',
        'SUM': 'SUM(10, 20, 30) → 60',

        # 文字列関数
        'LEN': 'LEN("Hello") → 5',
        'LEFT': 'LEFT("Hello", 2) → "He"',
        'RIGHT': 'RIGHT("Hello", 2) → "lo"',
        'MID': 'MID("Hello", 2, 2) → "el"',
        'UPPER': 'UPPER("hello") → "HELLO"',
        'LOWER': 'LOWER("HELLO") → "hello"',
        'UCASE': 'UCASE("hello") → "HELLO"',
        'LCASE': 'LCASE("HELLO") → "hello"',
        'VAL': 'VAL("123.45abc") → 123.45',
        'TRIM': 'TRIM("  Hello  ") → "Hello"',
        'REPLACE': 'REPLACE("Hello", "l", "r") → "Herro"',
        'INSTR': 'INSTR("Hello", "ll") → 3',
        'INSTRREV': 'INSTRREV("Hello", "l") → 4',

        # 論理関数
        'IIF': 'IIF(VAL > 10, "大", "小")',

        # 乱数関数
        'RAND': 'RAND() → 0.xxxxx (0-1の乱数)',
        'RND': 'RND() → 0.xxxxx (0-1の乱数)',
        'RANDOMIZE': 'RANDOMIZE(), RANDOMIZE(123), RANDOMIZE(0, 1000)',
        'RNDCSV': 'RNDCSV("A,B,C") → "B" (ランダムに1つ)',
        'PICKCSV': 'PICKCSV("A,B,C", 2) → "B" (2番目を取得)',

        # CSV関数
        'CSVCOUNT': 'CSVCOUNT("a,b,c,d") → 4',
        'CSVREAD': 'CSVREAD("a,b,c", 1) → "b"',
        'CSVUNIQUE': 'CSVUNIQUE("a,b,a,c,b") → "a,b,c"',
        'CSVMERGE': 'CSVMERGE("a,b", "c,d") → "a,b,c,d"',
        'CSVDIFF': 'COUNT = CSVDIFF(ARR, "a,b,c", "b,c,d") → ARR[0]="a", ARR[1]="d"',

        # フォーマット関数
        'FORMAT': 'FORMAT(1234.5, "0,000.00") → "1,234.50"',

        # 日付・時刻関数
        'NOW': 'NOW() → 現在の日時',
        'DATE': 'DATE() → 現在の日付',
        'TIME': 'TIME() → 現在の時刻',
        'YEAR': 'YEAR(NOW()) → 2025',
        'MONTH': 'MONTH(NOW()) → 1-12',
        'DAY': 'DAY(NOW()) → 1-31',
        'HOUR': 'HOUR(NOW()) → 0-23',
        'MINUTE': 'MINUTE(NOW()) → 0-59',
        'SECOND': 'SECOND(NOW()) → 0-59',
        'WEEKDAY': 'WEEKDAY(NOW()) → 1-7 (1=日曜)',
        'DATEADD': 'DATEADD("d", 7, NOW()) → 7日後',
        'DATEDIFF': 'DATEDIFF("d", DATE1, DATE2) → 日数差',

        # 型変換・検査関数
        'CSTR': 'CSTR(123) → "123"',
        'CINT': 'CINT("123") → 123',
        'CDBL': 'CDBL("123.45") → 123.45',
        'ISNUMERIC': 'ISNUMERIC("123") → 1',
        'ISDATE': 'ISDATE("2025/01/01") → 1',
        'ISARRAY': 'ISARRAY(ARR) → 1 (配列なら1)',

        # 追加文字列関数
        'STRREVERSE': 'STRREVERSE("Hello") → "olleH"',
        'STRCOMP': 'STRCOMP("ABC", "abc", 1) → 0 (同じ)',
        'SPACE': 'SPACE(5) → "     "',
        'STRING': 'STRING(3, "A") → "AAA"',

        # 正規表現関数
        'REGEX': 'REGEX("test123", "[0-9]+") → 1 (マッチ)',
        'REGEXMATCH': 'REGEXMATCH("test123", "[0-9]+") → "123"',
        'REGEXREPLACE': 'REGEXREPLACE("test123", "[0-9]+", "X") → "testX"',
        'REGEXEXTRACT': 'REGEXEXTRACT("test123", "([0-9]+)") → "123"',
        'REGEXCOUNT': 'REGEXCOUNT("a1b2c3", "[0-9]") → 3',
        'REGEXMATCHES': 'REGEXMATCHES("a1b2", "[0-9]") → ["1","2"]',
        'REGEXSPLIT': 'REGEXSPLIT("a,b;c", "[,;]") → ["a","b","c"]',

        # 配列関数（特殊）
        'REDIM': 'REDIM ARR[], 10 → 配列のサイズを変更',
        'ARRAY': 'ARRAY ARR[], 1, 2, 3 → 配列を初期化',
        'UBOUND': 'UBOUND(ARR[]) → 最大インデックス',
        'SPLIT': 'SPLIT ARR[], "A,B,C", "," → 文字列を分割して配列に格納',
        'JOIN': 'TXT = JOIN(ARR[], ",") → 配列を結合して文字列に',

        # HTTP/HTTPS通信関数
        'HTTPGET': 'HTTPGET("https://api.example.com/data") → レスポンスボディ',
        'HTTPPOST': 'HTTPPOST("https://api.example.com/post", "{\\"key\\":\\"value\\"}", "Content-Type: application/json") → レスポンスボディ',
        'HTTPPUT': 'HTTPPUT("https://api.example.com/update", "{\\"key\\":\\"value\\"}", "Content-Type: application/json") → レスポンスボディ',
        'HTTPDELETE': 'HTTPDELETE("https://api.example.com/delete") → レスポンスボディ',
        'HTTPJSON': 'HTTPJSON("https://api.example.com/json", "GET") → JSON文字列',
        'HTTPSTATUS': 'HTTPSTATUS() → 200 (最後のHTTPステータスコード)',
        'HTTPHEADERS': 'HTTPHEADERS() → JSON形式のヘッダー情報',

        # Python関数実行
        'PYEXEC': 'PYEXEC("math.sqrt", 16) → 4.0 | PYEXEC("numpy.array", 1, 2, 3) → "1,2,3"',
        'PYLIST': 'data_array = PYLIST("1.0,2.0,3.0") | Result = PYEXEC("numpy.mean", data_array)',
    }

    return usage_examples.get(func_name_upper)