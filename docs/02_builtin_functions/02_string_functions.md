# 文字列関数リファレンス

[← ビルトイン関数索引に戻る](00_index.md)

u5 EasyScripterで使用できる文字列関数の完全リファレンスです。

## 関数一覧
28個の文字列関数を提供しています。

---

### LEN(text)
**説明**: 文字列の長さを返す
**引数**: text - 文字列
**戻り値**: 文字数
**例**:
```vba
result = LEN("Hello")
PRINT(result)     ' 5
text1 = "Sample Text"
result = LEN(text1)
PRINT(result)     ' 11
result = LEN("")
PRINT(result)     ' 0
```

### LEFT(text, length)
**説明**: 左から指定文字数を取得
**引数**:
- text - 文字列
- length - 取得する文字数
**戻り値**: 部分文字列
**例**:
```vba
result = LEFT("Hello World", 5)
PRINT(result)   ' "Hello"
text1 = "ComfyUI EasyScripter"
result = LEFT(text1, 10)
PRINT(result)   ' "ComfyUI Ea"
result = LEFT("ABC", 10)
PRINT(result)   ' "ABC"（元より長い場合は全体）
```

### RIGHT(text, length)
**説明**: 右から指定文字数を取得
**引数**:
- text - 文字列
- length - 取得する文字数
**戻り値**: 部分文字列
**例**:
```vba
result = RIGHT("Hello World", 5)
PRINT(result)  ' "World"
text1 = "ComfyUI EasyScripter"
result = RIGHT(text1, 10)
PRINT(result)  ' "syScripter"
result = RIGHT("ABC", 10)
PRINT(result)  ' "ABC"
```

### MID(text, start, length)
**説明**: 指定位置から部分文字列を取得

**重要**: 開始位置0は1として扱われます。

**引数**:
- text - 文字列
- start - 開始位置（1ベース、0は1として扱う）
- length - 取得する文字数
**戻り値**: 部分文字列
**例**:
```vba
result = MID("Hello World", 7, 5)
PRINT(result)  ' "World"
result = MID("ABCDEFG", 3, 2)
PRINT(result)  ' "CD"
result = MID("ABCDEFG", 0, 2)
PRINT(result)  ' "AB"（0は1として扱われる）
text1 = "EasyScripter Node"
result = MID(text1, 5, 10)
PRINT(result)  ' "Scripter N"
```

### UPPER(text)
**説明**: 大文字に変換
**引数**: text - 文字列
**戻り値**: 大文字に変換した文字列
**例**:
```vba
result = UPPER("Hello")
PRINT(result)      ' "HELLO"
result = UPPER("abc123XYZ")
PRINT(result)  ' "ABC123XYZ"
```

### LOWER(text)
**説明**: 小文字に変換
**引数**: text - 文字列
**戻り値**: 小文字に変換した文字列
**例**:
```vba
result = LOWER("HELLO")
PRINT(result)      ' "hello"
result = LOWER("ABC123xyz")
PRINT(result)  ' "abc123xyz"
```

### TRIM(text)
**説明**: 前後の空白を削除
**引数**: text - 文字列
**戻り値**: トリムした文字列
**例**:
```vba
result = TRIM("  Hello  ")
PRINT(result)    ' "Hello"
result = TRIM("   ")
PRINT(result)    ' ""
```

### REPLACE(text, old, new)
**説明**: 文字列を置換
**引数**:
- text - 対象文字列
- old - 検索文字列
- new - 置換文字列
**戻り値**: 置換後の文字列
**例**:
```vba
result = REPLACE("Hello World", "World", "ComfyUI")
PRINT(result)  ' "Hello ComfyUI"
text1 = "Hello World Test"
result = REPLACE(text1, " ", "_")
PRINT(result)  ' "Hello_World_Test"
result = REPLACE("AAABBB", "A", "X")
PRINT(result)  ' "XXXBBB"
```

### INSTR([start,] text, search)
**説明**: 文字列を検索（位置を返す）
**引数**:
- start - 検索開始位置（省略時:1）
- text - 対象文字列
- search - 検索文字列
**戻り値**: 見つかった位置（0=見つからない）
**例**:
```vba
result = INSTR("Hello World", "World")
PRINT(result)     ' 7
result = INSTR("ABCABC", "BC")
PRINT(result)     ' 2
result = INSTR(3, "ABCABC", "BC")
PRINT(result)     ' 5（3文字目から検索）
text1 = "This is a keyword example"
result = INSTR(text1, "keyword")
PRINT(result)     ' 11
```

### INSTRREV(text, search, [start])
**説明**: 文字列を後ろから検索
**引数**:
- text - 対象文字列
- search - 検索文字列
- start - 検索開始位置（省略時:最後）
**戻り値**: 見つかった位置
**例**:
```vba
result = INSTRREV("Hello World", "o")
PRINT(result)      ' 8（最後のo）
result = INSTRREV("ABCABC", "BC")
PRINT(result)      ' 5
result = INSTRREV("path/to/file", "/")
PRINT(result)      ' 8（最後のスラッシュ）
```

### STRREVERSE(text)
**説明**: 文字列を反転
**引数**: text - 文字列
**戻り値**: 反転した文字列
**例**:
```vba
result = STRREVERSE("Hello")
PRINT(result)    ' "olleH"
result = STRREVERSE("12345")
PRINT(result)    ' "54321"
```

### STRCOMP(text1, text2, [compare])
**説明**: 文字列を比較
**引数**:
- text1 - 文字列1
- text2 - 文字列2
- compare - 比較方法（0=バイナリ, 1=テキスト）
**戻り値**: -1/0/1（小さい/等しい/大きい）
**例**:
```vba
result = STRCOMP("abc", "ABC", 1)
PRINT(result)    ' 0（大文字小文字無視）
result = STRCOMP("abc", "ABC", 0)
PRINT(result)    ' 1（大文字小文字区別）
result = STRCOMP("a", "b")
PRINT(result)    ' -1
```

### SPACE(number)
**説明**: 指定数の空白を生成
**引数**: number - 空白の数
**戻り値**: 空白文字列
**例**:
```vba
result = SPACE(5)
PRINT(result)               ' "     "
result = "A" & SPACE(3) & "B"
PRINT(result)   ' "A   B"
```

### STRING(number, character)
**説明**: 文字を繰り返す
**引数**:
- number - 繰り返し回数
- character - 繰り返す文字
**戻り値**: 繰り返した文字列
**例**:
```vba
result = STRING(5, "A")
PRINT(result)     ' "AAAAA"
result = STRING(10, "-")
PRINT(result)    ' "----------"
```

### FORMAT(value, format_string)
**説明**: 値を書式化
**引数**:
- value - 値
- format_string - 書式文字列
**戻り値**: 書式化された文字列
**サポート書式**:
- `{:.Nf}` - 小数点N桁
- `{:0Nd}` - N桁ゼロ埋め
- `{:,}` - 3桁カンマ区切り
- `%Y-%m-%d` - 日付書式
**例**:
```vba
result = FORMAT(3.14159, "{:.2f}")
PRINT(result)      ' "3.14"
result = FORMAT(42, "{:05d}")
PRINT(result)      ' "00042"
result = FORMAT(1234567, "{:,}")
PRINT(result)      ' "1,234,567.0"
result = FORMAT(NOW(), "%Y/%m/%d")
PRINT(result)      ' "2024/01/15"
```

### SPLIT(text, [delimiter])
**説明**: 文字列を分割して配列化
**引数**:
- text - 分割する文字列
- delimiter - 区切り文字（省略時:カンマ）
**戻り値**: 分割された配列
**例**:
```vba
' カンマ区切りを分割
result = SPLIT("apple,banana,cherry")
PRINT(result(0))  ' "apple"
PRINT(result(1))  ' "banana"
' スペース区切りを分割
result = SPLIT("one two three", " ")
PRINT(result(2))  ' "three"
```

### JOIN(array, [delimiter])
**説明**: 配列を文字列に結合
**引数**:
- array - 結合する配列
- delimiter - 区切り文字（省略時:カンマ）
**戻り値**: 結合された文字列
**例**:
```vba
ARRAY(arr, "A", "B", "C")
result = JOIN(arr, "-")
PRINT(result)  ' "A-B-C"
result = JOIN(arr)
PRINT(result)  ' "A,B,C"
```

### LTRIM(text)
**説明**: 左の空白を削除
**引数**: text - 文字列
**戻り値**: 左トリムした文字列
**例**:
```vba
result = LTRIM("  Hello")
PRINT(result)  ' "Hello"
result = LTRIM("  Text  ")
PRINT(result)  ' "Text  "
```

### RTRIM(text)
**説明**: 右の空白を削除
**引数**: text - 文字列
**戻り値**: 右トリムした文字列
**例**:
```vba
result = RTRIM("Hello  ")
PRINT(result)  ' "Hello"
result = RTRIM("  Text  ")
PRINT(result)  ' "  Text"
```

### UCASE(text)
**説明**: 大文字に変換（UPPERのエイリアス）
**引数**: text - 文字列
**戻り値**: 大文字に変換した文字列
**例**:
```vba
result = UCASE("hello")
PRINT(result)  ' "HELLO"
```

### LCASE(text)
**説明**: 小文字に変換（LOWERのエイリアス）
**引数**: text - 文字列
**戻り値**: 小文字に変換した文字列
**例**:
```vba
result = LCASE("HELLO")
PRINT(result)  ' "hello"
```

### PROPER(text)
**説明**: タイトルケースに変換（各単語の先頭を大文字化）
**引数**: text - 文字列
**戻り値**: タイトルケースに変換した文字列
**例**:
```vba
result = PROPER("hello world")
PRINT(result)  ' "Hello World"
result = PROPER("easyScripter node")
PRINT(result)  ' "Easyscripter Node"
```

### CHR(code)
**説明**: 文字コードから文字へ変換
**引数**: code - 文字コード（0-127のASCII範囲）
**戻り値**: 対応する文字
**例**:
```vba
result = CHR(65)
PRINT(result)  ' "A"
result = CHR(97)
PRINT(result)  ' "a"
result = CHR(48)
PRINT(result)  ' "0"
```

### ASC(char)
**説明**: 文字から文字コードへ変換
**引数**: char - 文字または文字列（最初の文字を使用）
**戻り値**: 文字コード（ASCII）
**例**:
```vba
result = ASC("A")
PRINT(result)  ' 65
result = ASC("Hello")
PRINT(result)  ' 72（"H"のコード）
```

### STR(value)
**説明**: 数値を文字列に変換
**引数**: value - 数値
**戻り値**: 文字列化された数値
**例**:
```vba
result = STR(123)
PRINT(result)  ' "123"
result = STR(3.14)
PRINT(result)  ' "3.14"
```

### URLENCODE(text, [encoding])
**説明**: URLエンコード（パーセントエンコーディング）を実行
**引数**:
- text - エンコードする文字列
- encoding - 文字エンコーディング（デフォルト: utf-8）
**戻り値**: URLエンコードされた文字列
**例**:
```vba
' 日本語をURLエンコード
encoded = URLENCODE("あいうえお")
PRINT(encoded)  ' → %E3%81%82%E3%81%84%E3%81%86%E3%81%88%E3%81%8A
' 検索クエリをエンコード
query = "EasyScripter HTTP 関数"
url = "https://www.google.com/search?q=" & URLENCODE(query)
PRINT(url)
```

### URLDECODE(text, [encoding])
**説明**: URLデコード（パーセントエンコーディングのデコード）を実行
**引数**:
- text - デコードする文字列
- encoding - 文字エンコーディング（デフォルト: utf-8）
**戻り値**: URLデコードされた文字列
**例**:
```vba
' URLエンコードされた文字列をデコード
decoded = URLDECODE("%E3%81%82%E3%81%84%E3%81%86%E3%81%88%E3%81%8A")
PRINT(decoded)  ' → あいうえお
' クエリパラメータをデコード
param = URLDECODE("EasyScripter+HTTP+%E9%96%A2%E6%95%B0")
PRINT(param)  ' → EasyScripter+HTTP+関数
```

### ESCAPEPATHSTR(path, [replacement])
**説明**: ファイルパスの禁則文字を置換または削除
**引数**:
- path - 処理対象の文字列
- replacement - 置換文字列（省略時は削除）
**戻り値**: 禁則文字を処理した文字列

**禁則文字**: `\`, `/`, `:`, `*`, `?`, `"`, `<`, `>`, `|`

**予約語**（ファイル名全体として禁止）: CON, PRN, AUX, NUL, COM1-9, LPT1-9（大文字小文字を区別しない）

**例**:
```vba
' 禁則文字をアンダースコアに置換
safe_name = ESCAPEPATHSTR("file:name*.txt", "_")
PRINT(safe_name)  ' → file_name_.txt

' 禁則文字を削除
safe_name = ESCAPEPATHSTR("file:name*.txt")
PRINT(safe_name)  ' → filename.txt

' 予約語の処理
safe_name = ESCAPEPATHSTR("CON.txt", "_")
PRINT(safe_name)  ' → _.txt

' ファイル名の一部としては許容
safe_name = ESCAPEPATHSTR("myConFile.txt", "_")
PRINT(safe_name)  ' → myConFile.txt
```

---

[← ビルトイン関数索引に戻る](00_index.md)
