# CSV関数リファレンス

[← ビルトイン関数索引に戻る](00_index.md)

## 概要

CSV（カンマ区切り値）文字列を操作するための関数群です。プロンプト生成や設定値の管理に便利です。

- CSV要素の数え上げ・取得
- ランダム選択によるプロンプト生成
- 重複除去や差分取得
- 配列とCSVの相互変換

---

## 関数一覧

### CSVCOUNT(csv_text)

**説明**: CSV要素数を数える

**引数**:
- csv_text - カンマ区切り文字列

**戻り値**: 要素数（整数）

**例**:
```vba
count = CSVCOUNT("apple,banana,orange")
PRINT(count)    ' 3
count = CSVCOUNT("")
PRINT(count)    ' 0
count = CSVCOUNT("single")
PRINT(count)    ' 1
```

---

### CSVREAD(csv_text, index)

**説明**: CSV文字列から指定インデックスの要素を取得

**引数**:
- csv_text - カンマ区切り文字列
- index - 取得する要素のインデックス（1ベース）

**戻り値**: 指定位置の要素（文字列）。範囲外の場合は空文字列

**例**:
```vba
element = CSVREAD("apple,banana,orange", 2)
PRINT(element)    ' banana
element = CSVREAD("a,b,c,d", 1)
PRINT(element)    ' a
element = CSVREAD("x,y,z", 10)
PRINT(element)    ' （範囲外は空文字列）
```

---

### CSVUNIQUE(csv_text)

**説明**: 重複を除去

**引数**:
- csv_text - カンマ区切り文字列

**戻り値**: 重複除去後のCSV文字列

**例**:
```vba
result = CSVUNIQUE("a,b,a,c,b")
PRINT(result)    ' a,b,c
result = CSVUNIQUE("1,2,3,2,1")
PRINT(result)    ' 1,2,3
```

---

### CSVMERGE(csv1, csv2, ...)

**説明**: 複数のCSVを結合

**引数**:
- csv1, csv2, ... - 複数のCSV文字列（可変長引数）

**戻り値**: 結合されたCSV文字列

**例**:
```vba
result = CSVMERGE("a,b", "c,d")
PRINT(result)        ' a,b,c,d
result = CSVMERGE("1,2", "3", "4,5")
PRINT(result)        ' 1,2,3,4,5
```

---

### CSVDIFF(array_name, csv1, csv2)

**説明**: 2つのCSV文字列の差分（どちらか片方にしか存在しない要素）を配列に格納

**引数**:
- array_name - 結果を格納する配列の変数名
- csv1 - CSV文字列1
- csv2 - CSV文字列2

**戻り値**: 差分要素の数（整数）

**例**:
```vba
' csv1にあってcsv2にない要素、およびcsv2にあってcsv1にない要素を取得
DIM diff_array
count = CSVDIFF(diff_array, "a,b,c,d", "b,d,e")
PRINT(count)           ' 3
PRINT(diff_array(0))   ' a
PRINT(diff_array(1))   ' c
PRINT(diff_array(2))   ' e
```

---

### PICKCSV(csv_text, [index])

**説明**: CSV要素を選択

**引数**:
- csv_text - CSV文字列
- index - インデックス（省略時:ランダム選択）

**戻り値**: 選択された要素（文字列）

**例**:
```vba
result = PICKCSV("red,green,blue", 2)
PRINT(result)     ' green
result = PICKCSV("A,B,C,D")
PRINT(result)     ' A, B, C, または D のいずれか
```

---

### RNDCSV(csv_text, [count])

**説明**: CSVからランダム選択（複数要素の配列取得も可能）

**引数**:
- csv_text - CSV文字列
- count - 選択する要素数（省略時は1つの文字列を返す）

**戻り値**:
- count未指定時: ランダムに選ばれた1つの要素（文字列）
- count=1: ランダムに選ばれた1つの要素（文字列）
- count≥2: ランダムに選ばれた要素のリスト
- count >= 要素数: 元のソート順を維持した完全配列

**例**:
```vba
' 1つの要素を選択（従来通り）
style = RNDCSV("realistic,anime,cartoon,abstract")
PRINT(style)
color = RNDCSV("red,blue,green,yellow,purple")
PRINT(color)

' 複数要素を配列として取得（重複あり）
DIM selected[3]
selected = RNDCSV("A,B,B,B,C,C,D", 3)
PRINT(selected)  ' 例: ["B", "B", "D"]

' 要素数を超える場合は元の順序で全要素
DIM all[3]
all = RNDCSV("X,Y,Z", 5)
PRINT(all)  ' ["X", "Y", "Z"] (元の順序を維持)

' RANDOMIZEと連携(Seed値固定)
RANDOMIZE(12345)
result = RNDCSV("1,2,3,4,5", 3)
PRINT(result)  ' 再現可能なランダム選択
```

---

### CSVJOIN(array, [delimiter])

**説明**: 配列をCSV文字列に結合

**引数**:
- array - 配列
- delimiter - 区切り文字（省略時:カンマ）

**戻り値**: 結合されたCSV文字列

**例**:
```vba
DIM items(2)
items(0) = "apple"
items(1) = "banana"
items(2) = "orange"
result = CSVJOIN(items)
PRINT(result)           ' apple,banana,orange
result = CSVJOIN(items, "|")
PRINT(result)           ' apple|banana|orange
```

---

### CSVSORT(csv_text, [delimiter], [descending])

**説明**: CSV要素をソート

**引数**:
- csv_text - 区切り文字で区切られたテキスト
- delimiter - 区切り文字（省略時: ","）
- descending - 降順フラグ（省略時: False、0=昇順, 1またはTrue=降順）

**戻り値**: ソートされたCSV文字列

**例**:
```vba
result = CSVSORT("dog,cat,bird,ant")
PRINT(result)      ' ant,bird,cat,dog
result = CSVSORT("3,1,4,1,5,9,2,6")
PRINT(result)      ' 1,1,2,3,4,5,6,9
result = CSVSORT("Z,A,M,B", ",", 1)
PRINT(result)      ' Z,M,B,A
result = CSVSORT("z;a;m;b", ";")
PRINT(result)      ' a;b;m;z
```

---

## 実用例

### プロンプト生成でのランダム選択

```vba
' スタイルをランダム選択（1つ）
style = RNDCSV("photorealistic,anime,oil painting,watercolor")
PRINT(style)
' 色調をランダム選択
tone = RNDCSV("warm,cool,vivid,muted,monochrome")
PRINT(tone)
' 時間帯をランダム選択
time = RNDCSV("morning,noon,sunset,night")
PRINT(time)

PRINT("1girl, " & style & ", " & tone & " tone, " & time)

' 複数のスタイルをミックス（配列選択）
DIM styles[3]
styles = RNDCSV("realistic,anime,3d,sketch,oil,watercolor,digital", 3)
PRINT(styles)
stylePrompt = CSVJOIN(styles, ", ")
PRINT(stylePrompt)
PRINT("1girl, " & stylePrompt)
```


### リストの重複除去と結合

```vba
' 複数のタグリストを結合
tags1 = "girl,outdoor,sunny,smile"
PRINT(tags1)
tags2 = "outdoor,happy,smile,park"
PRINT(tags2)
tags3 = "girl,smile,nature"
PRINT(tags3)

' 結合
allTags = CSVMERGE(tags1, tags2, tags3)
PRINT(allTags)
' "girl,outdoor,sunny,smile,happy,smile,park,girl,smile,nature"

' 重複を除去
uniqueTags = CSVUNIQUE(allTags)
PRINT(uniqueTags)
' "girl,outdoor,sunny,smile,happy,park,nature"
```

---

[← ビルトイン関数索引に戻る](00_index.md)
