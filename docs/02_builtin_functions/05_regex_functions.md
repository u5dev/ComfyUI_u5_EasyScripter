# 正規表現関数リファレンス

[← ビルトイン関数索引に戻る](00_index.md)

## 概要

正規表現関数は、パターンマッチング、検索、置換、抽出などの高度なテキスト処理を可能にします。Pythonの正規表現エンジンを使用しており、強力なパターンマッチング機能を提供します。

---

## REGEX(pattern, text)

**説明**: パターンマッチをテスト

**引数**:
- pattern - 正規表現パターン
- text - 検索対象文字列

**戻り値**: 1（マッチ）または0

**例**:
```vba
result = REGEX("\\d+", "abc123def")
PRINT(result)  ' 1（数字あり）

result = REGEX("^[A-Z]", "Hello")
PRINT(result)  ' 1（大文字で開始）

result = REGEX("\\.(jpg|png)$", "a.gif")
PRINT(result)  ' 0（jpgまたはpngでない）
```

---

## REGEXMATCH(pattern, text)

**説明**: 最初のマッチを取得

**引数**:
- pattern - 正規表現パターン
- text - 検索対象文字列

**戻り値**: マッチした文字列（なければ空）

**例**:
```vba
result = REGEXMATCH("\\d+", "abc123def456")
PRINT(result)  ' "123"

result = REGEXMATCH("[A-Z]+", "helloWORLD")
PRINT(result)  ' "WORLD"
```

---

## REGEXREPLACE(pattern, text, replacement)

**説明**: パターンを置換

**引数**:
- pattern - 正規表現パターン
- text - 対象文字列
- replacement - 置換文字列

**戻り値**: 置換後の文字列

**例**:
```vba
result = REGEXREPLACE("\\d+", "abc123def", "XXX")
PRINT(result)  ' "abcXXXdef"

result = REGEXREPLACE("\\s+", "a  b    c", " ")
PRINT(result)  ' "a b c"

result = REGEXREPLACE("[aeiou]", "hello", "*")
PRINT(result)  ' "h*ll*"
```

---

## REGEXEXTRACT(pattern, text, [group])

**説明**: グループを抽出

**引数**:
- pattern - 正規表現パターン（グループ付き）
- text - 対象文字列
- group - グループ番号（省略時:0=全体）

**戻り値**: 抽出された文字列

**例**:
```vba
result = REGEXEXTRACT("(\\d{4})-(\\d{2})", "2024-01-15", 1)
PRINT(result)  ' "2024"

result = REGEXEXTRACT("(\\w+)@(\\w+)", "user@domain", 2)
PRINT(result)  ' "domain"
```

---

## REGEXCOUNT(pattern, text)

**説明**: マッチ数を数える

**引数**:
- pattern - 正規表現パターン
- text - 対象文字列

**戻り値**: マッチした数

**例**:
```vba
count = REGEXCOUNT("\\d", "a1b2c3d4")
PRINT(count)  ' 4

count = REGEXCOUNT("\\w+", "hello world")
PRINT(count)  ' 2
```

---

## REGEXMATCHES(pattern, text)

**説明**: 全マッチを配列で取得

**引数**:
- pattern - 正規表現パターン
- text - 対象文字列

**戻り値**: マッチのリスト

**例**:
```vba
matches = REGEXMATCHES("\\d+", "a10b20c30")
PRINT(matches)  ' ["10", "20", "30"]
```

---

## REGEXSPLIT(pattern, text)

**説明**: パターンで分割

**引数**:
- pattern - 区切りパターン
- text - 対象文字列

**戻り値**: 分割されたリスト

**例**:
```vba
parts = REGEXSPLIT("[,;]", "a,b;c,d")
PRINT(parts)  ' ["a", "b", "c", "d"]
PRINT(parts[0]) ' a

parts = REGEXSPLIT("\\s+", "one  two  three")
PRINT(parts)  ' ["one", "two", "three"]
PRINT(parts[1]) ' two
```

---

[← ビルトイン関数索引に戻る](00_index.md)

