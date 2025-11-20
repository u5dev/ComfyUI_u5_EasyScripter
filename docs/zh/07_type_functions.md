# 类型转换·类型判断函数参考

[← 返回内置函数索引](00_index.md)

## 概述

类型转换·类型判断函数是用于转换值的类型或判定变量类型的函数群。

**类型转换函数**:
- CSTR - 转换为字符串
- CINT - 转换为整数
- CDBL - 转换为浮点数
- FORMAT - 以指定格式整形数值·日期时间（VBA兼容）

**类型判断函数**:
- ISNUMERIC - 判断是否为数值
- ISDATE - 判断是否为日期
- ISARRAY - 判断是否为数组

---

## 类型转换函数

### CSTR(value)

**说明**: 转换为字符串

**参数**:
- `value` - 任意值

**返回值**: 字符串

**示例**:
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

**说明**: 转换为整数

**参数**:
- `value` - 数值或字符串

**返回值**: 整数（float格式）

**示例**:
```vba
number = CINT("123")
PRINT(number)            ' 123
number = CINT(45.67)
PRINT(number)            ' 46（四舍五入）
number = CINT("3.14")
PRINT(number)            ' 3
```

---

### CDBL(value)

**说明**: 转换为浮点数

**参数**:
- `value` - 数值或字符串

**返回值**: float

**示例**:
```vba
number = CDBL("123.45")
PRINT(number)            ' 123.45
number = CDBL(10)
PRINT(number)            ' 10
```

---

### FORMAT(value, [format_string])

**说明**: 以指定格式整形数值·日期时间（VBA兼容）

**参数**:
- `value` (Any, 必须) - 格式化对象值（数值、字符串、日期时间）
- `format_string` (str, optional) - 格式指定符（默认: ""）

**返回值**: str - 格式化后的字符串

**支持的格式形式**:

1. **VBA格式**:
   - `"0"` - 整数（四舍五入）
   - `"0.0"` - 小数点1位
   - `"0.00"` - 小数点2位
   - `"#"`, `"#.#"`, `"#.##"` - 自动精度

2. **Python format格式**:
   - `"{:.2f}"` - Python format语法
   - `".2f"`, `","` - format spec

3. **日期时间格式（strftime）**:
   - `"%Y-%m-%d %H:%M:%S"` - 日期时间格式
   - `"%Y/%m/%d"` - 仅日期

**示例**:
```vba
' VBA格式
result = FORMAT(123.456, "0")       ' "123"（整数）
PRINT("整数: " & result)
result = FORMAT(123.456, "0.0")     ' "123.5"（小数1位）
PRINT("小数1位: " & result)
result = FORMAT(123.456, "0.00")    ' "123.46"（小数2位）
PRINT("小数2位: " & result)

' Python format格式
result = FORMAT(3.14159, "{:.2f}")  ' "3.14"
PRINT("圆周率: " & result)
result = FORMAT(1234567, ",")       ' "1,234,567"
PRINT("逗号分隔: " & result)

' 日期时间格式
now_str = NOW()
result = FORMAT(now_str, "%Y-%m-%d %H:%M:%S")
PRINT("日期时间: " & result)             ' "2024-01-15 14:30:00"
result = FORMAT(now_str, "%Y年%m月%d日")
PRINT("日期: " & result)             ' "2024年01月15日"
```

**注意**:
- 省略`format_string`时将值原样字符串化
- 不支持的格式将使用str()返回值

---

## 类型判断函数

### ISNUMERIC(value)

**说明**: 判断是否为数值

**参数**:
- `value` - 检查的值

**返回值**: 1（数值）或0

**示例**:
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

**说明**: 判断是否为日期

**参数**:
- `value` - 检查的值

**返回值**: 1（日期）或0

**示例**:
```vba
result = ISDATE("2024-01-15")
PRINT(result)                     ' 1
result = ISDATE("2024/01/15")
PRINT(result)                     ' 1
result = ISDATE("15:30:00")
PRINT(result)                     ' 1（时间也可以）
result = ISDATE("hello")
PRINT(result)                     ' 0
```

---

### ISARRAY(variable_name)

**说明**: 判断是否为数组

**重要**: 请将数组名作为字符串传递，或使用ARR[]记法传递数组变量引用。

**参数**:
- `variable_name` - 变量名（字符串）或数组变量引用

**返回值**: 1（数组）或0

**示例**:
```vba
REDIM ARR, 10
result = ISARRAY(ARR[])
PRINT(result)                ' 1（数组引用）
result = ISARRAY("ARR")
PRINT(result)                ' 1（数组名字符串）
result = ISARRAY("VAL1")
PRINT(result)                ' 0（普通变量）
```

---

[← 返回内置函数索引](00_index.md)
