# 数学函数参考

[← 返回内置函数索引](00_index.md) | [English](../02_builtin_functions/01_math_functions.md) | [日本語](../02_builtin_functions/01_math_functions.md) | [Français](../fr/01_math_functions.md) | [Español](../es/01_math_functions.md)

u5 EasyScripter可用的数学函数完整参考。

## 函数一览
提供16个数学函数。

---

## 数学函数
提供基本的数学相关功能。
示例中的期望值，无限循环小数（0.9999...）为便于显示已进行四舍五入。


### ABS(value)
**说明**: 返回绝对值
**参数**: value - 数值或可转换为数值的值
**返回值**: 绝对值（float）
**示例**:
```vba
result = ABS(-5.5)
PRINT(result)  ' 5.5
result = ABS(10)
PRINT(result)  ' 10
result = ABS("-3.14")
PRINT(result)  ' 3.14
```

### INT(value)
**说明**: 返回整数部分（向下取整）
**参数**: value - 数值
**返回值**: 整数部分（float格式）
**示例**:
```vba
result = INT(5.9)
PRINT(result)  ' 5
result = INT(-2.3)
PRINT(result)  ' -2
result = INT("10.5")
PRINT(result)  ' 10
```

### ROUND(value, [digits])
**说明**: 返回四舍五入的值
**参数**:
- value - 数值
- digits - 小数点后的位数（省略时:0）
**返回值**: 四舍五入后的值
**示例**:
```vba
result = ROUND(3.14159, 2)
PRINT(result)  ' 3.14
result = ROUND(5.5)
PRINT(result)  ' 6
result = ROUND(123.456, 1)
PRINT(result)  ' 123.5
```

### SQRT(value)
**说明**: 返回平方根
**参数**: value - 0以上的数值
**返回值**: 平方根
**错误**: 负值会产生错误
**示例**:
```vba
result = SQRT(16)
PRINT(result)  ' 4
result = SQRT(2)
PRINT(result)  ' 1.4142135623730951
' result = SQRT(-1) ' 错误！
```

### MIN(value1, value2, ...)
**说明**: 返回最小值
**参数**: 多个数值
**返回值**: 最小值
**示例**:
```vba
result = MIN(5, 2, 8, 1)
PRINT(result)  ' 1
result = MIN(VAL1, VAL2)
PRINT(result)  ' 两个输入值中的较小值
```

### MAX(value1, value2, ...)
**说明**: 返回最大值
**参数**: 多个数值
**返回值**: 最大值
**示例**:
```vba
result = MAX(5, 2, 8, 1)
PRINT(result)  ' 8
result = MAX(0, VAL1)
PRINT(result)  ' 钳制为0以上
```

### SIN(radians)
**说明**: 返回正弦值
**参数**: radians - 弧度单位的角度
**返回值**: -1到1之间的值
**示例**:
```vba
result = SIN(0)
PRINT(result)  ' 0
result = SIN(3.14159/2)
PRINT(result)  ' 0.9999999999991198（约1）
result = SIN(RADIANS(30))
PRINT(result)  ' 0.49999999999999994（约0.5）
```

### COS(radians)
**说明**: 返回余弦值
**参数**: radians - 弧度单位的角度
**返回值**: -1到1之间的值
**示例**:
```vba
result = COS(0)
PRINT(result)  ' 1
result = COS(3.14159)
PRINT(result)  ' -0.9999999999964793（约-1）
result = COS(RADIANS(60))
PRINT(result)  ' 0.5000000000000001（约0.5）
```

### TAN(radians)
**说明**: 返回正切值
**参数**: radians - 弧度单位的角度
**返回值**: 正切值
**示例**:
```vba
result = TAN(0)
PRINT(result)  ' 0
result = TAN(3.14159/4)
PRINT(result)  ' 0.9999986732059836（约1）
result = TAN(RADIANS(45))
PRINT(result)  ' 0.9999999999999999（约1）
```

### RADIANS(degrees)
**说明**: 将角度转换为弧度
**参数**: degrees - 角度单位的角度
**返回值**: 弧度
**示例**:
```vba
result = RADIANS(180)
PRINT(result)  ' 3.141592653589793
result = RADIANS(90)
PRINT(result)  ' 1.5707963267948966
result = RADIANS(45)
PRINT(result)  ' 0.7853981633974483
```

### DEGREES(radians)
**说明**: 将弧度转换为角度
**参数**: radians - 弧度单位的角度
**返回值**: 角度
**示例**:
```vba
result = DEGREES(3.14159)
PRINT(result)  ' 179.9998479605043（约180）
result = DEGREES(1.5708)
PRINT(result)  ' 90.00021045914971（约90）
result = DEGREES(0.7854)
PRINT(result)  ' 45.00010522957486（约45）
```

### POW(base, exponent)
**说明**: 计算幂次方（base^exponent）
**参数**:
- base - 基数
- exponent - 指数
**返回值**: 幂次方的结果
**示例**:
```vba
result = POW(2, 10)
PRINT(result)  ' 1024
result = POW(5, 3)
PRINT(result)  ' 125
result = POW(10, -2)
PRINT(result)  ' 0.01
```

### LOG(value, [base])
**说明**: 返回对数

**重要**: LOG函数默认返回自然对数（底e）。

**参数**:
- value - 正数值
- base - 底（省略时:自然对数e）
**返回值**: 对数
**示例**:
```vba
result = LOG(2.718282)
PRINT(result)  ' 1.0000000631063886（约1）
result = LOG(8, 2)
PRINT(result)  ' 3（以2为底）
result = LOG(1000, 10)
PRINT(result)  ' 2.9999999999999996（约3）
```

### EXP(value)
**说明**: e（自然对数底）的幂次方
**参数**: value - 指数
**返回值**: e^value
**示例**:
```vba
result = EXP(0)
PRINT(result)  ' 1
result = EXP(1)
PRINT(result)  ' 2.718281828459045
result = EXP(2)
PRINT(result)  ' 7.38905609893065
```

### AVG(value1, value2, ...)
**说明**: 计算平均值
**参数**: 多个数值
**返回值**: 平均值
**示例**:
```vba
result = AVG(10, 20, 30)
PRINT(result)  ' 20
result = AVG(1, 2, 3, 4, 5)
PRINT(result)  ' 3
```

### SUM(value1, value2, ...)
**说明**: 计算总和
**参数**: 多个数值
**返回值**: 总和值
**示例**:
```vba
result = SUM(10, 20, 30)
PRINT(result)  ' 60
result = SUM(1, 2, 3, 4, 5)
PRINT(result)  ' 15
```

---

[← 返回内置函数索引](00_index.md)
