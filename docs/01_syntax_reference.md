# スクリプト言語リファレンス

[← メインドキュメントに戻る](../README.md)

---

## 📑 目次

- [言語仕様の基本](#言語仕様の基本)
- [変数と代入](#変数と代入)
- [予約変数（入出力変数）](#予約変数入出力変数)
- [データ型システム](#データ型システム)
- [配列操作](#配列操作)
- [演算子リファレンス](#演算子リファレンス)
- [制御構造](#制御構造)
- [ユーザー定義関数（FUNCTION文）](#ユーザー定義関数function文)
- [コメント記法](#コメント記法)

---

## 📖 言語仕様の基本

### 基本的なルール

**大文字小文字の区別**
- **変数名**: 区別なし（`value`と`VALUE`は同じ）
- **関数名**: 区別なし（`len`と`LEN`は同じ）
- **文字列比較**: 区別なし（`"Hello" = "HELLO"`はTrue）

**重要**: VBAと同様に、変数名、関数名、キーワードは大文字小文字を区別しません。

---

## 📝 変数と代入

変数は宣言なしで使用できます。すべての変数は内部的に浮動小数点数または文字列として扱われます。

### 変数の宣言と型

```vba
' 変数は宣言なしで使用可能
x = 10
name = "Alice"

' DIM文での明示的な宣言（省略可能）
DIM result
result = x * 2
PRINT(result)  ' 20

' 型は自動的に変換される
number = "123"    ' 文字列
result = number + 10
PRINT(result)  ' 133
```

### 基本的な代入

```vba
' 数値の代入
a = 10
b = 3.14
c = VAL1 + VAL2

' 文字列の代入
name = "World"
message = TXT1

' 計算結果の代入
result = a * b + c
PRINT(result)  ' 31.400000000000002
```

---

## 🎯 予約変数（入出力変数）

ComfyUIから自動的に利用可能な予約変数：

- **`VAL1`**, **`VAL2`**: 数値入力（ComfyUIから接続）
- **`TXT1`**, **`TXT2`**: 文字列入力（ComfyUIから接続）
- **`RETURN1`**, **`RETURN2`**: スクリプトの戻り値（数値または文字列）
  - `RETURN`はRETURN1の後方互換エイリアス
- **`RELAY_OUTPUT`**: relay_output出力ソケット（ANY型）の値を制御（Tier 3実装）
- **`PRINT`**: デバッグ出力用（PRINT関数で追記）

**使用例**:
```vba
' 入力値を処理
result = VAL1 * 2 + VAL2
PRINT(result)  ' 0

' 出力に格納
RETURN1 = result
RETURN2 = "計算結果: " & result
```

#### RELAY_OUTPUT変数

`RELAY_OUTPUT`変数はrelay_output出力ソケット（ANY型）の値を制御する特殊変数です。

**機能**:
- スクリプト内で`RELAY_OUTPUT`に値を代入すると、その値がrelay_output出力ソケットから出力されます
- RELAY_OUTPUT未使用時は、従来通りany_input入力をパススルーします

**用途**:
- INPUT関数で読み込んだ画像（torch.Tensor）を後続のComfyUIノードに渡す
- 任意のANY型データ（latent, mask等）を後続ノードに渡す

**使用例**:
```vba
' 画像ファイルを読み込み、後続ノードに渡す
IMG1 = INPUT("reference.png")
RELAY_OUTPUT = IMG1
```

**注意事項**:
- RELAY_OUTPUT変数に代入できる型: ANY型（torch.Tensor, list, dict, str, int, float等）
- 型変換は行われません（代入した値がそのまま出力されます）
- RETURN1/RETURN2とは独立して動作します

---

## 📊 データ型システム

### 基本データ型

1. **数値型**: 整数と浮動小数点（内部的にはfloat）
2. **文字列型**: ダブルクォートまたはシングルクォートで囲む
3. **配列型**: 1次元配列のみサポート

### 文字列リテラルの種類

#### 通常文字列リテラル

```vba
' ダブルクォート
text1 = "Hello, World!"

' VBA式エスケープ: ""は"を表す
text2 = "He said ""hello"""  ' → He said "hello"

' エスケープシーケンス
text3 = "Line1\nLine2"  ' → 改行が挿入される
text4 = "Tab\there"     ' → タブが挿入される
```

#### Raw文字列リテラル

Raw文字列リテラルは、エスケープ処理を最小限にし、バックスラッシュをそのまま扱いたい場合に使用します。

```vba
' 構文: r"..."
' VBA式エスケープ("")のみ処理され、その他のエスケープシーケンスは処理されない

' Windowsパス（バックスラッシュをそのまま使用）
path = r"C:\Users\Admin\file.txt"
PRINT(path)  ' C:\Users\Admin\file.txt

' JSON文字列（VBA式""を使用）
json_str = r"{""key"": ""value""}"
PRINT(json_str)  ' {"key": "value"}
result = PYEXEC("json.loads", json_str)
PRINT(result)  ' {"key": "value"}

' バックスラッシュを含む文字列
pattern = r"Line1\nLine2"
PRINT(pattern)  ' Line1\nLine2
```

**Raw文字列の仕様**:
- `r"..."`形式で記述
- VBA式エスケープ`""`のみ処理（`""`→`"`）
- `\`は通常文字として扱われる（`\n`, `\t`等のエスケープは処理されない）
- `\"`は文字列の終端として扱われる（文字列内に`"`を含めるには`""`を使用）

### 型の自動変換

```vba
' 文字列→数値
a = "42"
b = a + 8
PRINT(b)  ' 50

' 数値→文字列
c = 100
d = "値は " & c
PRINT(d)  ' 値は 100

' 真偽値の扱い
trueValue = 1
PRINT(trueValue)  ' 1
falseValue = 0
PRINT(falseValue)  ' 0
```

---

## 🔬 配列操作

配列は`[]`記法でアクセスします。

### 配列の宣言と使用

```vba
' 配列の宣言（DIMは省略可能）
DIM numbers[10]

' 値の代入
numbers[0] = 100
numbers[1] = 200
numbers[2] = 300

' 値の参照
total = numbers[0] + numbers[1] + numbers[2]
PRINT(total)  ' 600

' 動的なインデックス
FOR i = 0 TO 9
    numbers[i] = i * 10
    PRINT(numbers[i])
NEXT
```

### 配列への代入と参照

```vba
' 配列の宣言と初期化
DIM arr[3]

' 配列への代入
arr[0] = 100
arr[1] = 200
arr[2] = arr[0] + arr[1]
PRINT(arr[2])  ' 300

' 配列の参照
RETURN1 = arr[2]
PRINT(RETURN1)  ' 300
```

---

## 🔧 演算子リファレンス

### 算術演算子

| 演算子 | 説明 | 例 | 結果 |
|--------|------|-----|------|
| + | 加算 | `5 + 3` | 8 |
| - | 減算 | `10 - 3` | 7 |
| * | 乗算 | `4 * 3` | 12 |
| / | 除算 | `15 / 3` | 5 |
| ^ | べき乗 | `2 ^ 3` | 8 |
| MOD | 剰余 | `10 MOD 3` | 1 |
| \\ | 整数除算 | `10 \\ 3` | 3 |

**例**:
```vba
' 加算
result = 10 + 5
PRINT(result)  ' 15

' 減算
result = 10 - 3
PRINT(result)  ' 7

' 乗算
result = 4 * 3
PRINT(result)  ' 12

' 除算
result = 15 / 3
PRINT(result)  ' 5

' べき乗
result = 2 ^ 3
PRINT(result)  ' 8

' 剰余（MOD）
result = 10 MOD 3
PRINT(result)  ' 1

' 複合演算（括弧による優先順位）
result = (10 + 5) * 2
PRINT(result)  ' 30
result = 10 + 5 * 2
PRINT(result)  ' 20
```

### 比較演算子

| 演算子 | 説明 | 例 | 結果 |
|--------|------|-----|------|
| = | 等しい | `5 = 5` | 1 (True) |
| <> | 等しくない | `5 <> 3` | 1 (True) |
| != | 等しくない (C言語スタイル) | `5 != 3` | 1 (True) |
| < | より小さい | `3 < 5` | 1 (True) |
| > | より大きい | `5 > 3` | 1 (True) |
| <= | 以下 | `3 <= 3` | 1 (True) |
| >= | 以上 | `5 >= 5` | 1 (True) |

**注意**: 文字列の比較では、VBAと同様に大文字小文字を区別しません。例：`"Hello" = "HELLO"` は True となります。

**例**:
```vba
' 等しい
result = 5 = 5
PRINT(result)  ' 1
result = 5 = 3
PRINT(result)  ' 0

' 等しくない (<> または != を使用可能)
result = 5 <> 3
PRINT(result)  ' 1
result = 5 != 3
PRINT(result)  ' 1 (C言語スタイルも使用可能)
result = 5 <> 5
PRINT(result)  ' 0

' より大きい
result = 10 > 5
PRINT(result)  ' 1

' より小さい
result = 3 < 10
PRINT(result)  ' 1

' 以上
result = 5 >= 5
PRINT(result)  ' 1
result = 5 >= 6
PRINT(result)  ' 0

' 以下
result = 3 <= 10
PRINT(result)  ' 1
```

### 論理演算子

| 演算子 | 説明 | 例 | 結果 |
|--------|------|-----|------|
| AND | 論理積 | `(5>3) AND (2<4)` | 1 (True) |
| OR | 論理和 | `(5<3) OR (2<4)` | 1 (True) |
| NOT | 論理否定 | `NOT (5>3)` | 0 (False) |

**例**:
```vba
' AND演算
result = (5 > 3) AND (10 > 5)
PRINT(result)  ' 1
result = (5 > 3) AND (2 > 5)
PRINT(result)  ' 0

' OR演算
result = (5 > 3) OR (2 > 5)
PRINT(result)  ' 1
result = (2 > 5) OR (1 > 3)
PRINT(result)  ' 0

' NOT演算
result = NOT (5 > 3)
PRINT(result)  ' 0
result = NOT (2 > 5)
PRINT(result)  ' 1
```

### 文字列演算子

| 演算子 | 説明 | 例 | 結果 |
|--------|------|-----|------|
| & | 連結 | `"Hello" & " " & "World"` | "Hello World" |

**例**:
```vba
' 文字列連結（&演算子）
greeting = "Hello" & " " & "World"
PRINT(greeting)  ' Hello World
result = "値は " & VAL1 & " です"
PRINT(result)
```

---

## 🎮 制御構造

### IF文（条件分岐）

#### 基本形：IF文（ブロック形式）

```vba
IF VAL1 > 50 THEN
    RETURN1 = "大きい"
END IF
```

#### 複数行IF文

```vba
IF VAL1 > 100 THEN
    RETURN1 = "非常に大きい"
    PRINT("値: " & VAL1)
ELSE
    RETURN1 = "標準的"
END IF
```

#### ELSEIF による多分岐

```vba
IF VAL1 > 100 THEN
    grade = "A"
ELSEIF VAL1 > 80 THEN
    grade = "B"
ELSEIF VAL1 > 60 THEN
    grade = "C"
ELSE
    grade = "D"
END IF
PRINT(grade)
```

#### 入れ子のIF文

```vba
IF TXT1 <> "" THEN
    IF LEN(TXT1) > 10 THEN
        IF INSTR(TXT1, "keyword") > 0 THEN
            RETURN1 = "キーワード発見（長文）"
        ELSE
            RETURN1 = "長文（キーワードなし）"
        END IF
    ELSE
        RETURN1 = "短文"
    END IF
ELSE
    RETURN1 = "入力なし"
END IF
```

### FOR...NEXT文（回数指定ループ）

#### 基本形

```vba
' 1から10まで繰り返し
FOR i = 1 TO 10
    PRINT("カウント: " & i)
NEXT
```

#### STEP指定

```vba
' 2ずつ増加（偶数のみ）
sum = 0
FOR i = 0 TO 20 STEP 2
    sum = sum + i
    PRINT(sum)
NEXT

' 逆順（カウントダウン）
FOR i = 10 TO 1 STEP -1
    PRINT(i & "...")
NEXT
PRINT("発射！")
```

#### 入れ子ループ

```vba
' 九九の表を作成
FOR i = 1 TO 9
    row = ""
    FOR j = 1 TO 9
        row = row & (i * j) & " "
    NEXT
    PRINT(row)
NEXT
```

### WHILE...WEND文（条件ループ）

#### 基本形

```vba
count = 0
WHILE count < 10
    count = count + 1
    PRINT("カウント: " & count)
WEND
```

#### 条件付きループ

```vba
' 入力文字列から特定の文字を探す
position = 1
found = 0
WHILE position <= LEN(TXT1) AND found = 0
    IF MID(TXT1, position, 1) = "X" THEN
        found = position
    END IF
    position = position + 1
WEND

IF found > 0 THEN
    RETURN1 = "Xは" & found & "文字目にあります"
    PRINT(RETURN1)
ELSE
    RETURN1 = "Xは見つかりません"
    PRINT(RETURN1)
END IF
```

### SELECT CASE文（多分岐）

VBA風のSELECT CASE文により、複数の条件分岐を簡潔に記述できます。最初にマッチしたCase節が実行され、その後の評価は行われません。

#### 基本形

```vba
SELECT CASE VAL1
    CASE 1
        RETURN1 = "一"
    CASE 2
        RETURN1 = "二"
    CASE 3
        RETURN1 = "三"
    CASE ELSE
        RETURN1 = "その他"
END SELECT
```

#### 複数値のCase文

```vba
' カンマ区切りで複数の値を指定
value = 5
SELECT CASE value
    CASE 1, 3, 5, 7, 9
        result = "Odd"
    CASE 2, 4, 6, 8, 10
        result = "Even"
    CASE ELSE
        result = "Out of range"
END SELECT
PRINT(result)  ' Odd
```

#### 範囲指定のCase文

```vba
' TO演算子で範囲を指定
score = 75
SELECT CASE score
    CASE 0 TO 59
        grade = "F"
    CASE 60 TO 69
        grade = "D"
    CASE 70 TO 79
        grade = "C"
    CASE 80 TO 89
        grade = "B"
    CASE 90 TO 100
        grade = "A"
    CASE ELSE
        grade = "Invalid"
END SELECT
PRINT(grade)  ' C
```

#### カンマ区切りで複数指定（曜日の例）

```vba
dayNum = WEEKDAY(NOW())
SELECT CASE dayNum
    CASE 1, 7
        dayType = "週末"
    CASE 2, 3, 4, 5, 6
        dayType = "平日"
END SELECT
PRINT(dayType)
```

---

## 🔨 ユーザー定義関数（FUNCTION文）

u5 EasyScripterでは、VBA風のFunction文を使用してユーザー定義関数を作成できます。関数内では独立したローカルスコープが提供され、グローバル変数との干渉を防ぎます。

### 基本的な関数定義

```vba
' 2つの数値を加算する関数
FUNCTION add(a, b)
    add = a + b  ' 関数名への代入で戻り値を設定
END FUNCTION

' 関数の呼び出し
result = add(5, 3)
PRINT(result)  ' 8
```

### 2つの数の大きい方を返す関数

```vba
' 2つの数の大きい方を返す関数
FUNCTION maxValue(a, b)
    IF a > b THEN
        maxValue = a
    ELSE
        maxValue = b
    END IF
END FUNCTION

' 使用例
result = maxValue(10, 20)
PRINT(result)  ' 20
```

### 複数の引数を持つ関数

```vba
' プロンプトを装飾する関数
FUNCTION decoratePrompt(prompt, quality, style)
    decorated = prompt

    IF quality = "high" THEN
        decorated = decorated & ", masterpiece, best quality"
    END IF

    IF style <> "" THEN
        decorated = decorated & ", " & style & " style"
    END IF

    decoratePrompt = decorated
END FUNCTION

' 使用例
finalPrompt = decoratePrompt("portrait", "high", "anime")
PRINT(finalPrompt)  ' portrait, masterpiece, best quality, anime style
```

### 再帰関数

```vba
' 階乗を計算する再帰関数
FUNCTION factorial(n)
    IF n <= 1 THEN
        factorial = 1
    ELSE
        factorial = n * factorial(n - 1)
    END IF
END FUNCTION

result = factorial(5)
PRINT(result)  ' 120
```

---

## 💬 コメント記法

コメントはシングルクォート（`'`）で始めます。

```vba
' これはコメントです
x = 10  ' 行末コメントも可能
PRINT(x)  ' 10

' 複数行にわたるコメント
' 各行の先頭にシングルクォートを付けます
```

---

## 📚 次のステップ

- [ビルトイン関数リファレンス](02_builtin_functions/00_index.md) - 120個の関数の詳細
- [メインドキュメント](../README.md) - 全体概要とインストール方法

---

**最終更新**: 2024年10月3日

---

[← メインドキュメントに戻る](../README.md)
