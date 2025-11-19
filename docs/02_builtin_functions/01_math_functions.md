# 数学関数リファレンス

[← ビルトイン関数索引に戻る](00_index.md)

u5 EasyScripterで使用できる数学関数の完全リファレンスです。

## 関数一覧
24個の数学関数を提供しています。

---

## 数学関数
基本的な数学関連の機能を提供します。
作例の期待では、無限循環数(0.9999...)は便宜上丸めています。


### ABS(value)
**説明**: 絶対値を返す
**引数**: value - 数値または数値に変換可能な値
**戻り値**: 絶対値（float）
**例**:
```vba
result = ABS(-5.5)
PRINT(result)  ' 5.5
result = ABS(10)
PRINT(result)  ' 10
result = ABS("-3.14")
PRINT(result)  ' 3.14
```

### INT(value)
**説明**: 整数部分を返す（小数点以下切り捨て）
**引数**: value - 数値
**戻り値**: 整数部分（float形式）
**例**:
```vba
result = INT(5.9)
PRINT(result)  ' 5
result = INT(-2.3)
PRINT(result)  ' -2
result = INT("10.5")
PRINT(result)  ' 10
```

### ROUND(value, [digits])
**説明**: 四捨五入した値を返す
**引数**:
- value - 数値
- digits - 小数点以下の桁数（省略時:0）
**戻り値**: 四捨五入した値
**例**:
```vba
result = ROUND(3.14159, 2)
PRINT(result)  ' 3.14
result = ROUND(5.5)
PRINT(result)  ' 6
result = ROUND(123.456, 1)
PRINT(result)  ' 123.5
```

### SQRT(value)
**説明**: 平方根を返す
**引数**: value - 0以上の数値
**戻り値**: 平方根
**エラー**: 負の値はエラー
**例**:
```vba
result = SQRT(16)
PRINT(result)  ' 4
result = SQRT(2)
PRINT(result)  ' 1.4142135623730951
' result = SQRT(-1) ' エラー！
```

### MIN(value1, value2, ...)
**説明**: 最小値を返す
**引数**: 複数の数値
**戻り値**: 最小値
**例**:
```vba
result = MIN(5, 2, 8, 1)
PRINT(result)  ' 1
result = MIN(VAL1, VAL2)
PRINT(result)  ' 2つの入力値の小さい方
```

### MAX(value1, value2, ...)
**説明**: 最大値を返す
**引数**: 複数の数値
**戻り値**: 最大値
**例**:
```vba
result = MAX(5, 2, 8, 1)
PRINT(result)  ' 8
result = MAX(0, VAL1)
PRINT(result)  ' 0以上にクランプ
```

### SIN(radians)
**説明**: サイン（正弦）を返す
**引数**: radians - ラジアン単位の角度
**戻り値**: -1から1の間の値
**例**:
```vba
result = SIN(0)
PRINT(result)  ' 0
result = SIN(3.14159/2)
PRINT(result)  ' 0.9999999999991198（約1）
result = SIN(RADIANS(30))
PRINT(result)  ' 0.49999999999999994（約0.5）
```

### COS(radians)
**説明**: コサイン（余弦）を返す
**引数**: radians - ラジアン単位の角度
**戻り値**: -1から1の間の値
**例**:
```vba
result = COS(0)
PRINT(result)  ' 1
result = COS(3.14159)
PRINT(result)  ' -0.9999999999964793（約-1）
result = COS(RADIANS(60))
PRINT(result)  ' 0.5000000000000001（約0.5）
```

### TAN(radians)
**説明**: タンジェント（正接）を返す
**引数**: radians - ラジアン単位の角度
**戻り値**: タンジェント値
**例**:
```vba
result = TAN(0)
PRINT(result)  ' 0
result = TAN(3.14159/4)
PRINT(result)  ' 0.9999986732059836（約1）
result = TAN(RADIANS(45))
PRINT(result)  ' 0.9999999999999999（約1）
```

### RADIANS(degrees)
**説明**: 度をラジアンに変換
**引数**: degrees - 度単位の角度
**戻り値**: ラジアン
**例**:
```vba
result = RADIANS(180)
PRINT(result)  ' 3.141592653589793
result = RADIANS(90)
PRINT(result)  ' 1.5707963267948966
result = RADIANS(45)
PRINT(result)  ' 0.7853981633974483
```

### DEGREES(radians)
**説明**: ラジアンを度に変換
**引数**: radians - ラジアン単位の角度
**戻り値**: 度
**例**:
```vba
result = DEGREES(3.14159)
PRINT(result)  ' 179.9998479605043（約180）
result = DEGREES(1.5708)
PRINT(result)  ' 90.00021045914971（約90）
result = DEGREES(0.7854)
PRINT(result)  ' 45.00010522957486（約45）
```

### POW(base, exponent)
**説明**: べき乗を計算（base^exponent）
**引数**:
- base - 基数
- exponent - 指数
**戻り値**: べき乗の結果
**例**:
```vba
result = POW(2, 10)
PRINT(result)  ' 1024
result = POW(5, 3)
PRINT(result)  ' 125
result = POW(10, -2)
PRINT(result)  ' 0.01
```

### LOG(value, [base])
**説明**: 対数を返す

**重要**: LOG関数はデフォルトで自然対数（底e）を返します。

**引数**:
- value - 正の数値
- base - 底（省略時:自然対数e）
**戻り値**: 対数
**例**:
```vba
result = LOG(2.718282)
PRINT(result)  ' 1.0000000631063886（約1）
result = LOG(8, 2)
PRINT(result)  ' 3（2を底とする）
result = LOG(1000, 10)
PRINT(result)  ' 2.9999999999999996（約3）
```

### EXP(value)
**説明**: e（自然対数の底）のべき乗
**引数**: value - 指数
**戻り値**: e^value
**例**:
```vba
result = EXP(0)
PRINT(result)  ' 1
result = EXP(1)
PRINT(result)  ' 2.718281828459045
result = EXP(2)
PRINT(result)  ' 7.38905609893065
```

### AVG(value1, value2, ...)
**説明**: 平均値を計算
**引数**: 複数の数値
**戻り値**: 平均値
**例**:
```vba
result = AVG(10, 20, 30)
PRINT(result)  ' 20
result = AVG(1, 2, 3, 4, 5)
PRINT(result)  ' 3
```

### SUM(value1, value2, ...)
**説明**: 合計を計算
**引数**: 複数の数値
**戻り値**: 合計値
**例**:
```vba
result = SUM(10, 20, 30)
PRINT(result)  ' 60
result = SUM(1, 2, 3, 4, 5)
PRINT(result)  ' 15
```

---

[← ビルトイン関数索引に戻る](00_index.md)
