# 脚本语言参考

[日本語](../01_syntax_reference.md) | [English](../en/01_syntax_reference.md) | [中文](../zh/01_syntax_reference.md) | [Español](../es/01_syntax_reference.md) | [Français](../fr/01_syntax_reference.md) | [Deutsch](../de/01_syntax_reference.md)

---

[← 返回主文档](README.md)

---

## 📑 目录

- [语言规范基础](#语言规范基础)
- [变量与赋值](#变量与赋值)
- [保留变量(输入输出变量)](#保留变量输入输出变量)
- [数据类型系统](#数据类型系统)
- [数组操作](#数组操作)
- [运算符参考](#运算符参考)
- [控制结构](#控制结构)
- [用户定义函数(FUNCTION语句)](#用户定义函数function语句)
- [注释记法](#注释记法)

---

## 📖 语言规范基础

### 基本规则

**大小写区分**
- **变量名**: 不区分大小写(`value`和`VALUE`相同)
- **函数名**: 不区分大小写(`len`和`LEN`相同)
- **字符串比较**: 不区分大小写(`"Hello" = "HELLO"`为True)

**重要**: 与VBA相同,变量名、函数名、关键字不区分大小写。

---

## 📝 变量与赋值

变量可以不声明直接使用。所有变量内部都作为浮点数或字符串处理。

### 变量的声明和类型

```vba
' 变量可以不声明直接使用
x = 10
name = "Alice"

' 使用DIM语句显式声明(可省略)
DIM result
result = x * 2
PRINT(result)  ' 20

' 类型会自动转换
number = "123"    ' 字符串
result = number + 10
PRINT(result)  ' 133
```

### 基本赋值

```vba
' 数值赋值
a = 10
b = 3.14
c = VAL1 + VAL2

' 字符串赋值
name = "World"
message = TXT1

' 计算结果赋值
result = a * b + c
PRINT(result)  ' 31.400000000000002
```

---

## 🎯 保留变量(输入输出变量)

从ComfyUI自动可用的保留变量:

- **`VAL1`**, **`VAL2`**: 数值输入(从ComfyUI连接)
- **`TXT1`**, **`TXT2`**: 字符串输入(从ComfyUI连接)
- **`RETURN1`**, **`RETURN2`**: 脚本返回值(数值或字符串)
  - `RETURN`是RETURN1的向后兼容别名
- **`RELAY_OUTPUT`**: 控制relay_output输出套接字(ANY类型)的值(Tier 3实现)
- **`PRINT`**: 用于调试输出(使用PRINT函数追加)

**使用示例**:
```vba
' 处理输入值
result = VAL1 * 2 + VAL2
PRINT(result)  ' 0

' 存储到输出
RETURN1 = result
RETURN2 = "计算结果: " & result
```

#### RELAY_OUTPUT变量

`RELAY_OUTPUT`变量是控制relay_output输出套接字(ANY类型)值的特殊变量。

**功能**:
- 在脚本中给`RELAY_OUTPUT`赋值时,该值会从relay_output输出套接字输出
- 未使用RELAY_OUTPUT时,按照传统方式直通any_input输入

**用途**:
- 将INPUT函数读取的图像(torch.Tensor)传递给后续ComfyUI节点
- 将任意ANY类型数据(latent、mask等)传递给后续节点

**使用示例**:
```vba
' 读取图像文件并传递给后续节点
IMG1 = INPUT("reference.png")
RELAY_OUTPUT = IMG1
```

**注意事项**:
- 可赋值给RELAY_OUTPUT变量的类型: ANY类型(torch.Tensor、list、dict、str、int、float等)
- 不进行类型转换(赋值的值会原样输出)
- 与RETURN1/RETURN2独立运作

---

## 📊 数据类型系统

### 基本数据类型

1. **数值型**: 整数和浮点数(内部为float)
2. **字符串型**: 用双引号或单引号括起来
3. **数组型**: 仅支持一维数组

### 字符串字面量的类型

#### 普通字符串字面量

```vba
' 双引号
text1 = "Hello, World!"

' VBA式转义: ""表示"
text2 = "He said ""hello"""  ' → He said "hello"

' 转义序列
text3 = "Line1\nLine2"  ' → 插入换行
text4 = "Tab\there"     ' → 插入制表符
```

#### Raw字符串字面量

Raw字符串字面量用于最小化转义处理,原样处理反斜杠的情况。

```vba
' 语法: r"..."
' 仅处理VBA式转义(""),其他转义序列不处理

' Windows路径(原样使用反斜杠)
path = r"C:\Users\Admin\file.txt"
PRINT(path)  ' C:\Users\Admin\file.txt

' JSON字符串(使用VBA式"")
json_str = r"{""key"": ""value""}"
PRINT(json_str)  ' {"key": "value"}
result = PYEXEC("json.loads", json_str)
PRINT(result)  ' {"key": "value"}

' 包含反斜杠的字符串
pattern = r"Line1\nLine2"
PRINT(pattern)  ' Line1\nLine2
```

**Raw字符串的规范**:
- 使用`r"..."`形式记述
- 仅处理VBA式转义`""`(`""`→`"`)
- `\`作为普通字符处理(不处理`\n`、`\t`等转义)
- `\"`作为字符串结束处理(要在字符串中包含`"`,请使用`""`)

### 类型的自动转换

```vba
' 字符串→数值
a = "42"
b = a + 8
PRINT(b)  ' 50

' 数值→字符串
c = 100
d = "值是 " & c
PRINT(d)  ' 值是 100

' 布尔值的处理
trueValue = 1
PRINT(trueValue)  ' 1
falseValue = 0
PRINT(falseValue)  ' 0
```

---

## 🔬 数组操作

使用`[]`记法访问数组。

### 数组的声明和使用

```vba
' 数组声明(DIM可省略)
DIM numbers[10]

' 值的赋值
numbers[0] = 100
numbers[1] = 200
numbers[2] = 300

' 值的引用
total = numbers[0] + numbers[1] + numbers[2]
PRINT(total)  ' 600

' 动态索引
FOR i = 0 TO 9
    numbers[i] = i * 10
    PRINT(numbers[i])
NEXT
```

### 对数组的赋值和引用

```vba
' 数组的声明和初始化
DIM arr[3]

' 对数组赋值
arr[0] = 100
arr[1] = 200
arr[2] = arr[0] + arr[1]
PRINT(arr[2])  ' 300

' 数组的引用
RETURN1 = arr[2]
PRINT(RETURN1)  ' 300
```

---

## 🔧 运算符参考

### 算术运算符

| 运算符 | 说明 | 示例 | 结果 |
|--------|------|------|------|
| + | 加法 | `5 + 3` | 8 |
| - | 减法 | `10 - 3` | 7 |
| * | 乘法 | `4 * 3` | 12 |
| / | 除法 | `15 / 3` | 5 |
| ^ | 幂运算 | `2 ^ 3` | 8 |
| MOD | 取余 | `10 MOD 3` | 1 |
| \\ | 整数除法 | `10 \\ 3` | 3 |

**示例**:
```vba
' 加法
result = 10 + 5
PRINT(result)  ' 15

' 减法
result = 10 - 3
PRINT(result)  ' 7

' 乘法
result = 4 * 3
PRINT(result)  ' 12

' 除法
result = 15 / 3
PRINT(result)  ' 5

' 幂运算
result = 2 ^ 3
PRINT(result)  ' 8

' 取余(MOD)
result = 10 MOD 3
PRINT(result)  ' 1

' 复合运算(括号优先级)
result = (10 + 5) * 2
PRINT(result)  ' 30
result = 10 + 5 * 2
PRINT(result)  ' 20
```

### 比较运算符

| 运算符 | 说明 | 示例 | 结果 |
|--------|------|------|------|
| = | 等于 | `5 = 5` | 1 (True) |
| <> | 不等于 | `5 <> 3` | 1 (True) |
| != | 不等于 (C语言风格) | `5 != 3` | 1 (True) |
| < | 小于 | `3 < 5` | 1 (True) |
| > | 大于 | `5 > 3` | 1 (True) |
| <= | 小于等于 | `3 <= 3` | 1 (True) |
| >= | 大于等于 | `5 >= 5` | 1 (True) |

**注意**: 字符串比较与VBA相同,不区分大小写。例:`"Hello" = "HELLO"`为True。

**示例**:
```vba
' 等于
result = 5 = 5
PRINT(result)  ' 1
result = 5 = 3
PRINT(result)  ' 0

' 不等于 (可使用<>或!=)
result = 5 <> 3
PRINT(result)  ' 1
result = 5 != 3
PRINT(result)  ' 1 (也可使用C语言风格)
result = 5 <> 5
PRINT(result)  ' 0

' 大于
result = 10 > 5
PRINT(result)  ' 1

' 小于
result = 3 < 10
PRINT(result)  ' 1

' 大于等于
result = 5 >= 5
PRINT(result)  ' 1
result = 5 >= 6
PRINT(result)  ' 0

' 小于等于
result = 3 <= 10
PRINT(result)  ' 1
```

### 逻辑运算符

| 运算符 | 说明 | 示例 | 结果 |
|--------|------|------|------|
| AND | 逻辑与 | `(5>3) AND (2<4)` | 1 (True) |
| OR | 逻辑或 | `(5<3) OR (2<4)` | 1 (True) |
| NOT | 逻辑非 | `NOT (5>3)` | 0 (False) |

**示例**:
```vba
' AND运算
result = (5 > 3) AND (10 > 5)
PRINT(result)  ' 1
result = (5 > 3) AND (2 > 5)
PRINT(result)  ' 0

' OR运算
result = (5 > 3) OR (2 > 5)
PRINT(result)  ' 1
result = (2 > 5) OR (1 > 3)
PRINT(result)  ' 0

' NOT运算
result = NOT (5 > 3)
PRINT(result)  ' 0
result = NOT (2 > 5)
PRINT(result)  ' 1
```

### 字符串运算符

| 运算符 | 说明 | 示例 | 结果 |
|--------|------|------|------|
| & | 连接 | `"Hello" & " " & "World"` | "Hello World" |

**示例**:
```vba
' 字符串连接(&运算符)
greeting = "Hello" & " " & "World"
PRINT(greeting)  ' Hello World
result = "值是 " & VAL1 & " です"
PRINT(result)
```

---

## 🎮 控制结构

### IF语句(条件分支)

#### 基本形式:IF语句(块形式)

```vba
IF VAL1 > 50 THEN
    RETURN1 = "大"
END IF
```

#### 多行IF语句

```vba
IF VAL1 > 100 THEN
    RETURN1 = "非常大"
    PRINT("值: " & VAL1)
ELSE
    RETURN1 = "标准"
END IF
```

#### 使用ELSEIF的多分支

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

#### 嵌套IF语句

```vba
IF TXT1 <> "" THEN
    IF LEN(TXT1) > 10 THEN
        IF INSTR(TXT1, "keyword") > 0 THEN
            RETURN1 = "发现关键词(长文本)"
        ELSE
            RETURN1 = "长文本(无关键词)"
        END IF
    ELSE
        RETURN1 = "短文本"
    END IF
ELSE
    RETURN1 = "无输入"
END IF
```

### FOR...NEXT语句(计数循环)

#### 基本形式

```vba
' 从1到10重复
FOR i = 1 TO 10
    PRINT("计数: " & i)
NEXT
```

#### 指定STEP

```vba
' 每次增加2(仅偶数)
sum = 0
FOR i = 0 TO 20 STEP 2
    sum = sum + i
    PRINT(sum)
NEXT

' 逆序(倒计时)
FOR i = 10 TO 1 STEP -1
    PRINT(i & "...")
NEXT
PRINT("发射!")
```

#### 嵌套循环

```vba
' 创建乘法表
FOR i = 1 TO 9
    row = ""
    FOR j = 1 TO 9
        row = row & (i * j) & " "
    NEXT
    PRINT(row)
NEXT
```

### WHILE...WEND语句(条件循环)

#### 基本形式

```vba
count = 0
WHILE count < 10
    count = count + 1
    PRINT("计数: " & count)
WEND
```

#### 条件循环

```vba
' 从输入字符串中查找特定字符
position = 1
found = 0
WHILE position <= LEN(TXT1) AND found = 0
    IF MID(TXT1, position, 1) = "X" THEN
        found = position
    END IF
    position = position + 1
WEND

IF found > 0 THEN
    RETURN1 = "X在第" & found & "个字符"
    PRINT(RETURN1)
ELSE
    RETURN1 = "未找到X"
    PRINT(RETURN1)
END IF
```

### SELECT CASE语句(多分支)

使用VBA风格的SELECT CASE语句,可以简洁地描述多个条件分支。执行第一个匹配的Case子句后,不再进行后续评估。

#### 基本形式

```vba
SELECT CASE VAL1
    CASE 1
        RETURN1 = "一"
    CASE 2
        RETURN1 = "二"
    CASE 3
        RETURN1 = "三"
    CASE ELSE
        RETURN1 = "其他"
END SELECT
```

#### 多值Case语句

```vba
' 用逗号分隔指定多个值
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

#### 范围指定的Case语句

```vba
' 使用TO运算符指定范围
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

#### 用逗号分隔指定多个值(星期示例)

```vba
dayNum = WEEKDAY(NOW())
SELECT CASE dayNum
    CASE 1, 7
        dayType = "周末"
    CASE 2, 3, 4, 5, 6
        dayType = "工作日"
END SELECT
PRINT(dayType)
```

---

## 🔨 用户定义函数(FUNCTION语句)

在u5 EasyScripter中,可以使用VBA风格的Function语句创建用户定义函数。函数内提供独立的本地作用域,防止与全局变量干扰。

### 基本函数定义

```vba
' 加法函数
FUNCTION add(a, b)
    add = a + b  ' 赋值给函数名设置返回值
END FUNCTION

' 函数调用
result = add(5, 3)
PRINT(result)  ' 8
```

### 返回两个数中较大值的函数

```vba
' 返回两个数中较大值的函数
FUNCTION maxValue(a, b)
    IF a > b THEN
        maxValue = a
    ELSE
        maxValue = b
    END IF
END FUNCTION

' 使用示例
result = maxValue(10, 20)
PRINT(result)  ' 20
```

### 具有多个参数的函数

```vba
' 装饰提示词的函数
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

' 使用示例
finalPrompt = decoratePrompt("portrait", "high", "anime")
PRINT(finalPrompt)  ' portrait, masterpiece, best quality, anime style
```

### 递归函数

```vba
' 计算阶乘的递归函数
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

## 💬 注释记法

注释以单引号(`'`)开始。

```vba
' 这是注释
x = 10  ' 行尾注释也可以
PRINT(x)  ' 10

' 跨多行的注释
' 每行开头都要加单引号
```

---

## 📚 下一步

- [内置函数参考](00_index.md) - 120个函数的详细信息
- [主文档](README.md) - 整体概述和安装方法

---

**最后更新**: 2024年10月3日

---

[← 返回主文档](README.md)
