# 型変換・型判定関数リファレンス

[← ビルトイン関数索引に戻る](00_index.md)

## 概要

型変換・型判定関数は、値の型を変換したり、変数の型を判定するための関数群です。

**型変換関数**:
- CSTR - 文字列への変換
- CINT - 整数への変換
- CDBL - 浮動小数点数への変換
- FORMAT - 数値・日時を指定フォーマットで整形（VBA互換）

**型判定関数**:
- ISNUMERIC - 数値かどうか判定
- ISDATE - 日付かどうか判定
- ISARRAY - 配列かどうか判定

---

## 型変換関数

### CSTR(value)

**説明**: 文字列に変換

**引数**:
- `value` - 任意の値

**戻り値**: 文字列

**例**:
```vba
text = CSTR(123)
PRINT(text)             ' 123
text = CSTR(3.14)
PRINT(text)             ' 3.14
text = CSTR(True)
PRINT(text)             ' 1
```

---

### CINT(value)

**説明**: 整数に変換

**引数**:
- `value` - 数値または文字列

**戻り値**: 整数（float形式）

**例**:
```vba
number = CINT("123")
PRINT(number)            ' 123
number = CINT(45.67)
PRINT(number)            ' 46（四捨五入）
number = CINT("3.14")
PRINT(number)            ' 3
```

---

### CDBL(value)

**説明**: 浮動小数点数に変換

**引数**:
- `value` - 数値または文字列

**戻り値**: float

**例**:
```vba
number = CDBL("123.45")
PRINT(number)            ' 123.45
number = CDBL(10)
PRINT(number)            ' 10
```

---

### FORMAT(value, [format_string])

**説明**: 数値・日時を指定フォーマットで整形（VBA互換）

**引数**:
- `value` (Any, 必須) - フォーマット対象の値（数値、文字列、日時）
- `format_string` (str, optional) - フォーマット指定子（デフォルト: ""）

**戻り値**: str - フォーマット済み文字列

**対応フォーマット形式**:

1. **VBA形式**:
   - `"0"` - 整数（四捨五入）
   - `"0.0"` - 小数点1桁
   - `"0.00"` - 小数点2桁
   - `"#"`, `"#.#"`, `"#.##"` - 自動精度

2. **Python format形式**:
   - `"{:.2f}"` - Python format構文
   - `".2f"`, `","` - format spec

3. **日時形式（strftime）**:
   - `"%Y-%m-%d %H:%M:%S"` - 日時フォーマット
   - `"%Y/%m/%d"` - 日付のみ

**例**:
```vba
' VBA形式
result = FORMAT(123.456, "0")       ' "123"（整数）
PRINT("整数: " & result)
result = FORMAT(123.456, "0.0")     ' "123.5"（小数1桁）
PRINT("小数1桁: " & result)
result = FORMAT(123.456, "0.00")    ' "123.46"（小数2桁）
PRINT("小数2桁: " & result)

' Python format形式
result = FORMAT(3.14159, "{:.2f}")  ' "3.14"
PRINT("円周率: " & result)
result = FORMAT(1234567, ",")       ' "1,234,567"
PRINT("カンマ区切り: " & result)

' 日時フォーマット
now_str = NOW()
result = FORMAT(now_str, "%Y-%m-%d %H:%M:%S")
PRINT("日時: " & result)             ' "2024-01-15 14:30:00"
result = FORMAT(now_str, "%Y年%m月%d日")
PRINT("日付: " & result)             ' "2024年01月15日"
```

**注意**:
- `format_string`省略時は値をそのまま文字列化
- 対応しないフォーマットは値をstr()で返す

---

## 型判定関数

### ISNUMERIC(value)

**説明**: 数値かどうか判定

**引数**:
- `value` - 検査する値

**戻り値**: 1（数値）または0

**例**:
```vba
result = ISNUMERIC("123")
PRINT(result)                  ' 1
result = ISNUMERIC("12.34")
PRINT(result)                  ' 1
result = ISNUMERIC("abc")
PRINT(result)                  ' 0
result = ISNUMERIC("")
PRINT(result)                  ' 0
```

---

### ISDATE(value)

**説明**: 日付かどうか判定

**引数**:
- `value` - 検査する値

**戻り値**: 1（日付）または0

**例**:
```vba
result = ISDATE("2024-01-15")
PRINT(result)                     ' 1
result = ISDATE("2024/01/15")
PRINT(result)                     ' 1
result = ISDATE("15:30:00")
PRINT(result)                     ' 1（時刻も）
result = ISDATE("hello")
PRINT(result)                     ' 0
```

---

### ISARRAY(variable_name)

**説明**: 配列かどうか判定

**重要**: 配列名を文字列として渡すか、ARR[]記法で配列変数参照を渡してください。

**引数**:
- `variable_name` - 変数名（文字列）または配列変数参照

**戻り値**: 1（配列）または0

**例**:
```vba
REDIM ARR, 10
result = ISARRAY(ARR[])
PRINT(result)                ' 1（配列参照）
result = ISARRAY("ARR")
PRINT(result)                ' 1（配列名文字列）
result = ISARRAY("VAL1")
PRINT(result)                ' 0（通常変数）
```

---

[← ビルトイン関数索引に戻る](00_index.md)
