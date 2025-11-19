# 数组函数参考

[← 返回内置函数索引](00_index.md) | [English](../02_builtin_functions/06_array_functions.md) | [日本語](../02_builtin_functions/06_array_functions.md) | [Français](../fr/06_array_functions.md) | [Español](../es/06_array_functions.md)

## 概述

数组函数提供数组的初始化、大小调整、边界获取等操作。u5 EasyScripter中数组使用0-based索引，通过`[]`记法访问。

**此类别的函数数量**: 3个

## 函数一览

### UBOUND(array)

**说明**: 获取数组的上限索引

**参数**:
- array - 数组变量

**返回值**: 上限索引（0-based）

**特殊处理**: 由script_engine.py处理的特殊函数

**示例**:
```vba
' 获取数组上限
REDIM ARR, 5
upper = UBOUND(ARR[])
PRINT(upper)   ' 4（0到4共5个元素）

' 循环处理整个数组
ARRAY data[], 10, 20, 30, 40, 50
FOR I = 0 TO UBOUND(data[])
    PRINT(data[I])
NEXT

' 确认数组大小
ARRAY items[], "apple", "banana", "orange"
size = UBOUND(items[]) + 1
PRINT(size)  ' 3个元素
```

---

### ARRAY(variable_name, value1, value2, ...)

**说明**: 初始化数组并设置值

**参数**:
- variable_name - 数组变量名
- value1, value2, ... - 初始值

**特殊处理**: 由script_engine.py处理的特殊函数

**示例**:
```vba
' 字符串数组的初始化
ARRAY items[], "apple", "banana", "orange"
' items[0] = "apple", items[1] = "banana", items[2] = "orange"

' 数值数组的初始化
ARRAY numbers[], 10, 20, 30, 40, 50
' numbers[0] = 10, numbers[1] = 20, ...

' 访问数组元素
ARRAY colors[], "red", "green", "blue"
favoriteColor = colors[1]
PRINT(favoriteColor)  ' "green"

' 循环处理数组
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

**说明**: 更改数组大小（重新定义）

**参数**:
- array_name - 数组名（字符串）
- size - 新大小

**特殊处理**: 由script_engine.py处理的特殊函数

**注意**: REDIM会清除现有的数组元素

**示例**:
```vba
' 数组的初始化
REDIM ARR, 10        ' 以10个元素重新定义ARR数组
REDIM DATA, 100      ' 以100个元素重新定义DATA数组

' 动态调整大小
size = VAL1
PRINT(size)
REDIM MyArray, size  ' 根据VAL1的值调整大小

' 使用数组进行动态数据处理
itemCount = CSVCOUNT(TXT1)
PRINT(itemCount)
REDIM items, itemCount
FOR I = 0 TO itemCount - 1
    items[I] = CSVREAD(TXT1, I + 1)
NEXT
```

## 数组使用示例

### 基本数组操作
```vba
' 创建数组并设置值
ARRAY names[], "Alice", "Bob", "Charlie", "David"

' 确认数组大小
count = UBOUND(names[]) + 1
PRINT(count)
PRINT("数组元素数: " & count)  ' "数组元素数: 4"

' 按顺序处理数组
FOR I = 0 TO UBOUND(names[])
    PRINT("名称[" & I & "]: " & names[I])
NEXT
```

### 动态数组大小调整
```vba
' 以初始大小创建数组
REDIM buffer, 5
FOR I = 0 TO 4
    buffer[I] = I * 10
NEXT

' 根据需要调整大小
newSize = 10
PRINT(newSize)
REDIM buffer, newSize
' 注意: REDIM会清除现有数据
```

### 数组与CSV的组合
```vba
' 将CSV数据转换为数组
csvData = "apple,banana,orange,grape,melon"
PRINT(csvData)
itemCount = CSVCOUNT(csvData)
PRINT(itemCount)
REDIM fruits, itemCount

FOR I = 0 TO itemCount - 1
    fruits[I] = CSVREAD(csvData, I + 1)
NEXT

' 确认数组内容
FOR I = 0 TO UBOUND(fruits[])
    PRINT("Fruit[" & I & "]: " & fruits[I])
NEXT
```

### 数组的汇总处理
```vba
' 数值数组的初始化
ARRAY scores[], 85, 92, 78, 95, 88, 91

' 计算总和
total = 0
FOR I = 0 TO UBOUND(scores[])
    total = total + scores[I]
NEXT
PRINT(total)

' 计算平均值
count = UBOUND(scores[]) + 1
PRINT(count)
average = total / count
PRINT(average)

' 搜索最大值
maxScore = scores[0]
PRINT(maxScore)
FOR I = 1 TO UBOUND(scores[])
    IF scores[I] > maxScore THEN
        maxScore = scores[I]
        PRINT(maxScore)
    END IF
NEXT

PRINT("总计: " & total)
PRINT("平均: " & ROUND(average, 2))
PRINT("最高分: " & maxScore)
```

---

[← 返回内置函数索引](00_index.md)
