# 正则表达式函数参考

[← 返回内置函数索引](00_index.md) | [English](../02_builtin_functions/05_regex_functions.md) | [日本語](../02_builtin_functions/05_regex_functions.md) | [Français](../fr/05_regex_functions.md) | [Español](../es/05_regex_functions.md)

## 概述

正则表达式函数可实现模式匹配、搜索、替换、提取等高级文本处理。使用Python的正则表达式引擎，提供强大的模式匹配功能。

---

## REGEX(pattern, text)

**说明**: 测试模式匹配

**参数**:
- pattern - 正则表达式模式
- text - 搜索对象字符串

**返回值**: 1（匹配）或0

**示例**:
```vba
result = REGEX("\\d+", "abc123def")
PRINT(result)  ' 1（有数字）

result = REGEX("^[A-Z]", "Hello")
PRINT(result)  ' 1（以大写字母开始）

result = REGEX("\\.(jpg|png)$", "a.gif")
PRINT(result)  ' 0（不是jpg或png）
```

---

## REGEXMATCH(pattern, text)

**说明**: 获取第一个匹配

**参数**:
- pattern - 正则表达式模式
- text - 搜索对象字符串

**返回值**: 匹配的字符串（没有则为空）

**示例**:
```vba
result = REGEXMATCH("\\d+", "abc123def456")
PRINT(result)  ' "123"

result = REGEXMATCH("[A-Z]+", "helloWORLD")
PRINT(result)  ' "WORLD"
```

---

## REGEXREPLACE(pattern, text, replacement)

**说明**: 替换模式

**参数**:
- pattern - 正则表达式模式
- text - 目标字符串
- replacement - 替换字符串

**返回值**: 替换后的字符串

**示例**:
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

**说明**: 提取组

**参数**:
- pattern - 正则表达式模式（带组）
- text - 目标字符串
- group - 组号（省略时:0=整体）

**返回值**: 提取的字符串

**示例**:
```vba
result = REGEXEXTRACT("(\\d{4})-(\\d{2})", "2024-01-15", 1)
PRINT(result)  ' "2024"

result = REGEXEXTRACT("(\\w+)@(\\w+)", "user@domain", 2)
PRINT(result)  ' "domain"
```

---

## REGEXCOUNT(pattern, text)

**说明**: 统计匹配数量

**参数**:
- pattern - 正则表达式模式
- text - 目标字符串

**返回值**: 匹配的数量

**示例**:
```vba
count = REGEXCOUNT("\\d", "a1b2c3d4")
PRINT(count)  ' 4

count = REGEXCOUNT("\\w+", "hello world")
PRINT(count)  ' 2
```

---

## REGEXMATCHES(pattern, text)

**说明**: 以数组获取所有匹配

**参数**:
- pattern - 正则表达式模式
- text - 目标字符串

**返回值**: 匹配的列表

**示例**:
```vba
matches = REGEXMATCHES("\\d+", "a10b20c30")
PRINT(matches)  ' ["10", "20", "30"]
```

---

## REGEXSPLIT(pattern, text)

**说明**: 按模式分割

**参数**:
- pattern - 分隔模式
- text - 目标字符串

**返回值**: 分割后的列表

**示例**:
```vba
parts = REGEXSPLIT("[,;]", "a,b;c,d")
PRINT(parts)  ' ["a", "b", "c", "d"]
PRINT(parts[0]) ' a

parts = REGEXSPLIT("\\s+", "one  two  three")
PRINT(parts)  ' ["one", "two", "three"]
PRINT(parts[1]) ' two
```

---

[← 返回内置函数索引](00_index.md)
