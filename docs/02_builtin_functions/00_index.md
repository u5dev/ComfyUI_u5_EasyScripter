# ビルトイン関数完全索引

[← メインドキュメントに戻る](../../README.md)

**このページはu5 EasyScripterのビルトイン関数のリファレンス索引です。**

u5 EasyScripterには、VBAスタイルのスクリプトで使用できる豊富なビルトイン関数が用意されています。

## 関数カテゴリ一覧

### [数学関数リファレンス](01_math_functions.md)
16個の数学関数 - 基本演算、三角関数、対数、統計関数など

### [文字列関数リファレンス](02_string_functions.md)
28個の文字列関数 - 文字列操作、検索、置換、書式化など

### [日時関数リファレンス](03_datetime_functions.md)
12個の日時関数 - 現在日時、日付計算、日時成分の取得、日付変換など

### [CSV関数リファレンス](04_csv_functions.md)
9個のCSV関数 - CSV操作、ランダム選択、重複除去など

### [正規表現関数リファレンス](05_regex_functions.md)
7個の正規表現関数 - パターンマッチング、置換、抽出など

### [配列関数リファレンス](06_array_functions.md)
3個の配列関数 - 配列の初期化、サイズ変更、上限インデックス取得など

### [型変換・型判定関数リファレンス](07_type_functions.md)
7個の型変換・型判定関数 - 型変換、型チェック、フォーマット整形など

### [モデル関数リファレンス](08_model_functions.md)
1個のモデル関数 - AI生成モデルの最適解像度判定

### [ユーティリティ関数リファレンス](09_utility_functions.md)
18個のユーティリティ関数 - デバッグ出力、型判定、ファイル入出力、ファイル存在チェック、メモリ解放、スリープ、画像処理（IMAGE→JSON配列/Base64変換）、画像・Latentデータ取得、ANY型データ取得など


---

## クイックリファレンステーブル

### 数学関数（16個）

| 関数名 | 概要 |
|--------|------|
| **ABS(value)** | 絶対値を返す |
| **INT(value)** | 整数部分を返す（小数点以下切り捨て） |
| **ROUND(value, [digits])** | 四捨五入した値を返す |
| **SQRT(value)** | 平方根を返す |
| **MIN(value1, value2, ...)** | 最小値を返す |
| **MAX(value1, value2, ...)** | 最大値を返す |
| **SIN(radians)** | サイン（正弦）を返す |
| **COS(radians)** | コサイン（余弦）を返す |
| **TAN(radians)** | タンジェント（正接）を返す |
| **RADIANS(degrees)** | 度をラジアンに変換 |
| **DEGREES(radians)** | ラジアンを度に変換 |
| **POW(base, exponent)** | べき乗を計算（base^exponent） |
| **LOG(value, [base])** | 対数を返す（デフォルト：自然対数） |
| **EXP(value)** | e（自然対数の底）のべき乗 |
| **AVG(value1, value2, ...)** | 平均値を計算 |
| **SUM(value1, value2, ...)** | 合計を計算 |

### 文字列関数（28個）

| 関数名 | 概要 |
|--------|------|
| **LEN(text)** | 文字列の長さを返す |
| **LEFT(text, length)** | 左から指定文字数を取得 |
| **RIGHT(text, length)** | 右から指定文字数を取得 |
| **MID(text, start, length)** | 指定位置から部分文字列を取得 |
| **UPPER(text)** | 大文字に変換 |
| **LOWER(text)** | 小文字に変換 |
| **TRIM(text)** | 前後の空白を削除 |
| **REPLACE(text, old, new)** | 文字列を置換 |
| **INSTR([start,] text, search)** | 文字列を検索（位置を返す） |
| **INSTRREV(text, search, [start])** | 文字列を後ろから検索 |
| **STRREVERSE(text)** | 文字列を反転 |
| **STRCOMP(text1, text2, [compare])** | 文字列を比較 |
| **SPACE(number)** | 指定数の空白を生成 |
| **STRING(number, character)** | 文字を繰り返す |
| **FORMAT(value, format_string)** | 値を書式化 |
| **SPLIT(text, [delimiter])** | 文字列を分割して配列化 |
| **JOIN(array, [delimiter])** | 配列を文字列に結合 |
| **LTRIM(text)** | 左の空白を削除 |
| **RTRIM(text)** | 右の空白を削除 |
| **UCASE(text)** | 大文字に変換（UPPERのエイリアス） |
| **LCASE(text)** | 小文字に変換（LOWERのエイリアス） |
| **PROPER(text)** | タイトルケースに変換 |
| **CHR(code)** | 文字コード→文字変換 |
| **ASC(char)** | 文字→文字コード変換 |
| **STR(value)** | 数値→文字列変換 |
| **URLENCODE(text, [encoding])** | URLエンコード |
| **URLDECODE(text, [encoding])** | URLデコード |
| **ESCAPEPATHSTR(path, [replacement])** | ファイルパス禁則文字を処理 |

### 日時関数（12個）

| 関数名 | 概要 |
|--------|------|
| **NOW()** | 現在の日時を取得 |
| **DATE()** | 今日の日付を取得 |
| **TIME()** | 現在時刻を取得 |
| **YEAR([date])** | 年を取得 |
| **MONTH([date])** | 月を取得 |
| **DAY([date])** | 日を取得 |
| **HOUR([time])** | 時を取得 |
| **MINUTE([time])** | 分を取得 |
| **SECOND([time])** | 秒を取得 |
| **DATEADD(interval, number, [date])** | 日付に加算/減算 |
| **DATEDIFF(interval, date1, [date2])** | 日付の差を計算 |
| **WEEKDAY([date], [firstday])** | 曜日を返す（1=日曜） |

### CSV関数（9個）

| 関数名 | 概要 |
|--------|------|
| **CSVCOUNT(csv_text)** | CSV要素数を数える |
| **CSVREAD(csv_text, index)** | CSV文字列から指定インデックスの要素を取得 |
| **CSVUNIQUE(csv_text)** | 重複を除去 |
| **CSVMERGE(csv1, csv2, ...)** | 複数のCSVを結合 |
| **CSVDIFF(array_name, csv1, csv2)** | CSVの差分を取得 |
| **PICKCSV(csv_text, [index])** | CSV要素を選択（省略時：ランダム） |
| **RNDCSV(csv_text)** | CSVからランダム選択（PICKCSVと同じ） |
| **CSVJOIN(array, [delimiter])** | 配列をCSV文字列に結合 |
| **CSVSORT(csv_text, [delimiter], [reverse])** | CSV要素をソート |

### 正規表現関数（7個）

| 関数名 | 概要 |
|--------|------|
| **REGEX(pattern, text)** | パターンマッチをテスト |
| **REGEXMATCH(pattern, text)** | 最初のマッチを取得 |
| **REGEXREPLACE(pattern, text, replacement)** | パターンを置換 |
| **REGEXEXTRACT(pattern, text, [group])** | グループを抽出 |
| **REGEXCOUNT(pattern, text)** | マッチ数を数える |
| **REGEXMATCHES(pattern, text)** | 全マッチを配列で取得 |
| **REGEXSPLIT(pattern, text)** | パターンで分割 |

### 配列関数（3個）

| 関数名 | 概要 |
|--------|------|
| **UBOUND(array)** | 配列の上限インデックスを取得 |
| **ARRAY(variable_name, value1, value2, ...)** | 配列を初期化して値を設定 |
| **REDIM(array_name, size)** | 配列のサイズを変更（再定義） |

### 型変換・型判定関数（7個）

| 関数名 | 概要 |
|--------|------|
| **CSTR(value)** | 文字列に変換 |
| **CINT(value)** | 整数に変換 |
| **CDBL(value)** | 浮動小数点数に変換 |
| **FORMAT(value, [format_string])** | 数値・日時を指定フォーマットで整形（VBA互換） |
| **ISNUMERIC(value)** | 数値かどうか判定 |
| **ISDATE(value)** | 日付かどうか判定 |
| **ISARRAY(variable_name)** | 配列かどうか判定 |

### モデル関数（1個）

| 関数名 | 概要 |
|--------|------|
| **OPTIMAL_LATENT(model_hint, width, height)** | モデル名とアスペクト比から最適なLatent空間のサイズを自動判定 |

### ユーティリティ関数（18個）

| 関数名 | 概要 |
|--------|------|
| **PRINT(message, ...)** | 値をテキストエリアに出力する（デバッグ用） |
| **OUTPUT(arg, [path], [flg])** | テキスト、数値、配列、画像、バイナリデータをファイルに出力 |
| **INPUT(path)** | ComfyUI出力フォルダからファイルを読み込む（動的型判定） |
| **ISFILEEXIST(path, [flg])** | ファイル存在チェックと拡張情報取得（_NNNN検索、画像サイズ、ファイルサイズ） |
| **VRAMFREE([min_free_vram_gb])** | VRAMとRAMを解放（モデルアンロード、キャッシュクリア、GC） |
| **SLEEP([milliseconds])** | 指定したミリ秒だけ処理を一時停止（デフォルト: 10ms） |
| **IMAGETOBYTEARRAY(image_input, [max_size], [format], [return_format])** | IMAGE/ファイルパスを画像JSON配列に変換|
| **IMAGETOBASE64(image_input, [max_size], [format], [return_format])** | IMAGE/ファイルパスをBase64エンコー（Vision API用） |
| **GETANYWIDTH([any_data])** | IMAGE/LATENT型データの幅（ピクセル数）を取得 |
| **GETANYHEIGHT([any_data])** | IMAGE/LATENT型データの高さ（ピクセル数）を取得 |
| **GETANYTYPE([any_data])** | ANY型データの型名を判定 |
| **GETANYVALUEINT([any_data])** | ANY型データから整数値を取得 |
| **GETANYVALUEFLOAT([any_data])** | ANY型データから浮動小数点値を取得 |
| **GETANYSTRING([any_data])** | ANY型データから文字列を取得 |
| **ISNUMERIC(value)** | 値が数値かどうかを判定 |
| **ISDATE(value)** | 値が日付として解析可能かを判定 |
| **ISARRAY(variable_name)** | 変数が配列かどうかを判定 |
| **TYPE(value)** | 変数の型を文字列で返す |



---

[← メインドキュメントに戻る](../../README.md)
