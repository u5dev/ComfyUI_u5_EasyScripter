# 配列関数リファレンス

[← ビルトイン関数索引に戻る](00_index.md)

## 概要

配列関数は、配列の初期化、サイズ変更、境界取得などの操作を提供します。u5 EasyScripterでは配列は0ベースのインデックスを使用し、`[]`記法でアクセスします。

**このカテゴリの関数数**: 3個

## 関数一覧

### UBOUND(array)

**説明**: 配列の上限インデックスを取得

**引数**:
- array - 配列変数

**戻り値**: 上限インデックス（0ベース）

**特殊処理**: script_engine.pyで処理される特殊関数

**例**:
```vba
' 配列の上限を取得
REDIM ARR, 5
upper = UBOUND(ARR[])
PRINT(upper)   ' 4（0から4までの5要素）

' ループで配列全体を処理
ARRAY data[], 10, 20, 30, 40, 50
FOR I = 0 TO UBOUND(data[])
    PRINT(data[I])
NEXT

' 配列サイズの確認
ARRAY items[], "apple", "banana", "orange"
size = UBOUND(items[]) + 1
PRINT(size)  ' 3要素
```

---

### ARRAY(variable_name, value1, value2, ...)

**説明**: 配列を初期化して値を設定

**引数**:
- variable_name - 配列変数名
- value1, value2, ... - 初期値

**特殊処理**: script_engine.pyで処理される特殊関数

**例**:
```vba
' 文字列配列の初期化
ARRAY items[], "apple", "banana", "orange"
' items[0] = "apple", items[1] = "banana", items[2] = "orange"

' 数値配列の初期化
ARRAY numbers[], 10, 20, 30, 40, 50
' numbers[0] = 10, numbers[1] = 20, ...

' 配列要素へのアクセス
ARRAY colors[], "red", "green", "blue"
favoriteColor = colors[1]
PRINT(favoriteColor)  ' "green"

' 配列をループで処理
ARRAY scores[], 85, 92, 78, 95
total = 0
FOR I = 0 TO UBOUND(scores[])
    total = total + scores[I]
NEXT
average = total / (UBOUND(scores[]) + 1)
PRINT(average)
```

---

### REDIM(array_name, size)

**説明**: 配列のサイズを変更（再定義）

**引数**:
- array_name - 配列名（文字列）
- size - 新しいサイズ

**特殊処理**: script_engine.pyで処理される特殊関数

**注意**: REDIMは既存の配列要素をクリアします

**例**:
```vba
' 配列の初期化
REDIM ARR, 10        ' ARR配列を10要素で再定義
REDIM DATA, 100      ' DATA配列を100要素で再定義

' 動的なサイズ変更
size = VAL1
PRINT(size)
REDIM MyArray, size  ' VAL1の値に応じてサイズ変更

' 配列を使った動的データ処理
itemCount = CSVCOUNT(TXT1)
PRINT(itemCount)
REDIM items, itemCount
FOR I = 0 TO itemCount - 1
    items[I] = CSVREAD(TXT1, I + 1)
NEXT
```

## 配列の使用例

### 基本的な配列操作
```vba
' 配列を作成して値を設定
ARRAY names[], "Alice", "Bob", "Charlie", "David"

' 配列のサイズを確認
count = UBOUND(names[]) + 1
PRINT(count)
PRINT("配列要素数: " & count)  ' "配列要素数: 4"

' 配列を順番に処理
FOR I = 0 TO UBOUND(names[])
    PRINT("名前[" & I & "]: " & names[I])
NEXT
```

### 動的配列のサイズ変更
```vba
' 初期サイズで配列を作成
REDIM buffer, 5
FOR I = 0 TO 4
    buffer[I] = I * 10
NEXT

' 必要に応じてサイズ変更
newSize = 10
PRINT(newSize)
REDIM buffer, newSize
' 注意: REDIMは既存のデータをクリアします
```

### 配列とCSVの組み合わせ
```vba
' CSVデータを配列に変換
csvData = "apple,banana,orange,grape,melon"
PRINT(csvData)
itemCount = CSVCOUNT(csvData)
PRINT(itemCount)
REDIM fruits, itemCount

FOR I = 0 TO itemCount - 1
    fruits[I] = CSVREAD(csvData, I + 1)
NEXT

' 配列の内容を確認
FOR I = 0 TO UBOUND(fruits[])
    PRINT("Fruit[" & I & "]: " & fruits[I])
NEXT
```

### 配列の集計処理
```vba
' 数値配列の初期化
ARRAY scores[], 85, 92, 78, 95, 88, 91

' 合計を計算
total = 0
FOR I = 0 TO UBOUND(scores[])
    total = total + scores[I]
NEXT
PRINT(total)

' 平均を計算
count = UBOUND(scores[]) + 1
PRINT(count)
average = total / count
PRINT(average)

' 最大値を検索
maxScore = scores[0]
PRINT(maxScore)
FOR I = 1 TO UBOUND(scores[])
    IF scores[I] > maxScore THEN
        maxScore = scores[I]
        PRINT(maxScore)
    END IF
NEXT

PRINT("合計: " & total)
PRINT("平均: " & ROUND(average, 2))
PRINT("最高点: " & maxScore)
```

---

[← ビルトイン関数索引に戻る](00_index.md)
