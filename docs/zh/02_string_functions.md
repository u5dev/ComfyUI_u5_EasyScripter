# 字符串函数参考

[← 返回内置函数索引](00_index.md)

u5 EasyScripter可用的字符串函数完整参考。

## 函数一览
提供28个字符串函数。

---

### LEN(text)
**说明**: 返回字符串长度
**参数**: text - 字符串
**返回值**: 字符数
**示例**:
```vba
result = LEN("Hello")
PRINT(result)     ' 5
text1 = "Sample Text"
result = LEN(text1)
PRINT(result)     ' 11
result = LEN("")
PRINT(result)     ' 0
```

### LEFT(text, length)
**说明**: 从左侧获取指定字符数
**参数**:
- text - 字符串
- length - 获取的字符数
**返回值**: 子字符串
**示例**:
```vba
result = LEFT("Hello World", 5)
PRINT(result)   ' "Hello"
text1 = "ComfyUI EasyScripter"
result = LEFT(text1, 10)
PRINT(result)   ' "ComfyUI Ea"
result = LEFT("ABC", 10)
PRINT(result)   ' "ABC"（比原始长度长时返回全部）
```

### RIGHT(text, length)
**说明**: 从右侧获取指定字符数
**参数**:
- text - 字符串
- length - 获取的字符数
**返回值**: 子字符串
**示例**:
```vba
result = RIGHT("Hello World", 5)
PRINT(result)  ' "World"
text1 = "ComfyUI EasyScripter"
result = RIGHT(text1, 10)
PRINT(result)  ' "syScripter"
result = RIGHT("ABC", 10)
PRINT(result)  ' "ABC"
```

### MID(text, start, length)
**说明**: 从指定位置获取子字符串

**重要**: 起始位置0将被视为1。

**参数**:
- text - 字符串
- start - 起始位置（1-based，0被视为1）
- length - 获取的字符数
**返回值**: 子字符串
**示例**:
```vba
result = MID("Hello World", 7, 5)
PRINT(result)  ' "World"
result = MID("ABCDEFG", 3, 2)
PRINT(result)  ' "CD"
result = MID("ABCDEFG", 0, 2)
PRINT(result)  ' "AB"（0被视为1）
text1 = "EasyScripter Node"
result = MID(text1, 5, 10)
PRINT(result)  ' "Scripter N"
```

### UPPER(text)
**说明**: 转换为大写
**参数**: text - 字符串
**返回值**: 转换为大写的字符串
**示例**:
```vba
result = UPPER("Hello")
PRINT(result)      ' "HELLO"
result = UPPER("abc123XYZ")
PRINT(result)  ' "ABC123XYZ"
```

### LOWER(text)
**说明**: 转换为小写
**参数**: text - 字符串
**返回值**: 转换为小写的字符串
**示例**:
```vba
result = LOWER("HELLO")
PRINT(result)      ' "hello"
result = LOWER("ABC123xyz")
PRINT(result)  ' "abc123xyz"
```

### TRIM(text)
**说明**: 删除前后的空白
**参数**: text - 字符串
**返回值**: 修剪后的字符串
**示例**:
```vba
result = TRIM("  Hello  ")
PRINT(result)    ' "Hello"
result = TRIM("   ")
PRINT(result)    ' ""
```

### REPLACE(text, old, new)
**说明**: 替换字符串
**参数**:
- text - 目标字符串
- old - 搜索字符串
- new - 替换字符串
**返回值**: 替换后的字符串
**示例**:
```vba
result = REPLACE("Hello World", "World", "ComfyUI")
PRINT(result)  ' "Hello ComfyUI"
text1 = "Hello World Test"
result = REPLACE(text1, " ", "_")
PRINT(result)  ' "Hello_World_Test"
result = REPLACE("AAABBB", "A", "X")
PRINT(result)  ' "XXXBBB"
```

### INSTR([start,] text, search)
**说明**: 搜索字符串（返回位置）
**参数**:
- start - 搜索起始位置（省略时:1）
- text - 目标字符串
- search - 搜索字符串
**返回值**: 找到的位置（0=未找到）
**示例**:
```vba
result = INSTR("Hello World", "World")
PRINT(result)     ' 7
result = INSTR("ABCABC", "BC")
PRINT(result)     ' 2
result = INSTR(3, "ABCABC", "BC")
PRINT(result)     ' 5（从第3个字符开始搜索）
text1 = "This is a keyword example"
result = INSTR(text1, "keyword")
PRINT(result)     ' 11
```

### INSTRREV(text, search, [start])
**说明**: 从后向前搜索字符串
**参数**:
- text - 目标字符串
- search - 搜索字符串
- start - 搜索起始位置（省略时:末尾）
**返回值**: 找到的位置
**示例**:
```vba
result = INSTRREV("Hello World", "o")
PRINT(result)      ' 8（最后的o）
result = INSTRREV("ABCABC", "BC")
PRINT(result)      ' 5
result = INSTRREV("path/to/file", "/")
PRINT(result)      ' 8（最后的斜杠）
```

### STRREVERSE(text)
**说明**: 反转字符串
**参数**: text - 字符串
**返回值**: 反转后的字符串
**示例**:
```vba
result = STRREVERSE("Hello")
PRINT(result)    ' "olleH"
result = STRREVERSE("12345")
PRINT(result)    ' "54321"
```

### STRCOMP(text1, text2, [compare])
**说明**: 比较字符串
**参数**:
- text1 - 字符串1
- text2 - 字符串2
- compare - 比较方法（0=二进制, 1=文本）
**返回值**: -1/0/1（小于/等于/大于）
**示例**:
```vba
result = STRCOMP("abc", "ABC", 1)
PRINT(result)    ' 0（忽略大小写）
result = STRCOMP("abc", "ABC", 0)
PRINT(result)    ' 1（区分大小写）
result = STRCOMP("a", "b")
PRINT(result)    ' -1
```

### SPACE(number)
**说明**: 生成指定数量的空格
**参数**: number - 空格数量
**返回值**: 空格字符串
**示例**:
```vba
result = SPACE(5)
PRINT(result)               ' "     "
result = "A" & SPACE(3) & "B"
PRINT(result)   ' "A   B"
```

### STRING(number, character)
**说明**: 重复字符
**参数**:
- number - 重复次数
- character - 重复的字符
**返回值**: 重复后的字符串
**示例**:
```vba
result = STRING(5, "A")
PRINT(result)     ' "AAAAA"
result = STRING(10, "-")
PRINT(result)    ' "----------"
```

### FORMAT(value, format_string)
**说明**: 格式化值
**参数**:
- value - 值
- format_string - 格式字符串
**返回值**: 格式化后的字符串
**支持格式**:
- `{:.Nf}` - 小数点N位
- `{:0Nd}` - N位零填充
- `{:,}` - 3位逗号分隔
- `%Y-%m-%d` - 日期格式
**示例**:
```vba
result = FORMAT(3.14159, "{:.2f}")
PRINT(result)      ' "3.14"
result = FORMAT(42, "{:05d}")
PRINT(result)      ' "00042"
result = FORMAT(1234567, "{:,}")
PRINT(result)      ' "1,234,567.0"
result = FORMAT(NOW(), "%Y/%m/%d")
PRINT(result)      ' "2024/01/15"
```

### SPLIT(text, [delimiter])
**说明**: 分割字符串为数组
**参数**:
- text - 分割的字符串
- delimiter - 分隔符（省略时:逗号）
**返回值**: 分割后的数组
**示例**:
```vba
' 分割逗号分隔
result = SPLIT("apple,banana,cherry")
PRINT(result(0))  ' "apple"
PRINT(result(1))  ' "banana"
' 分割空格分隔
result = SPLIT("one two three", " ")
PRINT(result(2))  ' "three"
```

### JOIN(array, [delimiter])
**说明**: 将数组连接为字符串
**参数**:
- array - 连接的数组
- delimiter - 分隔符（省略时:逗号）
**返回值**: 连接后的字符串
**示例**:
```vba
ARRAY(arr, "A", "B", "C")
result = JOIN(arr, "-")
PRINT(result)  ' "A-B-C"
result = JOIN(arr)
PRINT(result)  ' "A,B,C"
```

### LTRIM(text)
**说明**: 删除左侧空白
**参数**: text - 字符串
**返回值**: 左修剪后的字符串
**示例**:
```vba
result = LTRIM("  Hello")
PRINT(result)  ' "Hello"
result = LTRIM("  Text  ")
PRINT(result)  ' "Text  "
```

### RTRIM(text)
**说明**: 删除右侧空白
**参数**: text - 字符串
**返回值**: 右修剪后的字符串
**示例**:
```vba
result = RTRIM("Hello  ")
PRINT(result)  ' "Hello"
result = RTRIM("  Text  ")
PRINT(result)  ' "  Text"
```

### UCASE(text)
**说明**: 转换为大写（UPPER的别名）
**参数**: text - 字符串
**返回值**: 转换为大写的字符串
**示例**:
```vba
result = UCASE("hello")
PRINT(result)  ' "HELLO"
```

### LCASE(text)
**说明**: 转换为小写（LOWER的别名）
**参数**: text - 字符串
**返回值**: 转换为小写的字符串
**示例**:
```vba
result = LCASE("HELLO")
PRINT(result)  ' "hello"
```

### PROPER(text)
**说明**: 转换为标题格式（每个单词首字母大写）
**参数**: text - 字符串
**返回值**: 转换为标题格式的字符串
**示例**:
```vba
result = PROPER("hello world")
PRINT(result)  ' "Hello World"
result = PROPER("easyScripter node")
PRINT(result)  ' "Easyscripter Node"
```

### CHR(code)
**说明**: 从字符代码转换为字符
**参数**: code - 字符代码（0-127的ASCII范围）
**返回值**: 对应的字符
**示例**:
```vba
result = CHR(65)
PRINT(result)  ' "A"
result = CHR(97)
PRINT(result)  ' "a"
result = CHR(48)
PRINT(result)  ' "0"
```

### ASC(char)
**说明**: 从字符转换为字符代码
**参数**: char - 字符或字符串（使用第一个字符）
**返回值**: 字符代码（ASCII）
**示例**:
```vba
result = ASC("A")
PRINT(result)  ' 65
result = ASC("Hello")
PRINT(result)  ' 72（"H"的代码）
```

### STR(value)
**说明**: 将数值转换为字符串
**参数**: value - 数值
**返回值**: 字符串化的数值
**示例**:
```vba
result = STR(123)
PRINT(result)  ' "123"
result = STR(3.14)
PRINT(result)  ' "3.14"
```

### URLENCODE(text, [encoding])
**说明**: 执行URL编码（百分比编码）
**参数**:
- text - 编码的字符串
- encoding - 字符编码（默认: utf-8）
**返回值**: URL编码的字符串
**示例**:
```vba
' 日语URL编码
encoded = URLENCODE("あいうえお")
PRINT(encoded)  ' → %E3%81%82%E3%81%84%E3%81%86%E3%81%88%E3%81%8A
' 搜索查询编码
query = "EasyScripter HTTP 関数"
url = "https://www.google.com/search?q=" & URLENCODE(query)
PRINT(url)
```

### URLDECODE(text, [encoding])
**说明**: 执行URL解码（百分比编码的解码）
**参数**:
- text - 解码的字符串
- encoding - 字符编码（默认: utf-8）
**返回值**: URL解码的字符串
**示例**:
```vba
' URL编码的字符串解码
decoded = URLDECODE("%E3%81%82%E3%81%84%E3%81%86%E3%81%88%E3%81%8A")
PRINT(decoded)  ' → あいうえお
' 查询参数解码
param = URLDECODE("EasyScripter+HTTP+%E9%96%A2%E6%95%B0")
PRINT(param)  ' → EasyScripter+HTTP+関数
```

### ESCAPEPATHSTR(path, [replacement])
**说明**: 替换或删除文件路径的禁用字符
**参数**:
- path - 处理对象的字符串
- replacement - 替换字符串（省略时删除）
**返回值**: 处理禁用字符后的字符串

**禁用字符**: `\`, `/`, `:`, `*`, `?`, `"`, `<`, `>`, `|`

**保留字**（文件名整体禁止）: CON, PRN, AUX, NUL, COM1-9, LPT1-9（不区分大小写）

**示例**:
```vba
' 将禁用字符替换为下划线
safe_name = ESCAPEPATHSTR("file:name*.txt", "_")
PRINT(safe_name)  ' → file_name_.txt

' 删除禁用字符
safe_name = ESCAPEPATHSTR("file:name*.txt")
PRINT(safe_name)  ' → filename.txt

' 处理保留字
safe_name = ESCAPEPATHSTR("CON.txt", "_")
PRINT(safe_name)  ' → _.txt

' 作为文件名的一部分时允许
safe_name = ESCAPEPATHSTR("myConFile.txt", "_")
PRINT(safe_name)  ' → myConFile.txt
```

---

[← 返回内置函数索引](00_index.md)
