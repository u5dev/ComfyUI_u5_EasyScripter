# 内置函数完整索引

[← 返回主文档](README.md)

**本页面是u5 EasyScripter内置函数的参考索引。**

u5 EasyScripter提供了丰富的内置函数，可在VBA风格的脚本中使用。

## 函数类别一览

### [数学函数参考](01_math_functions.md)
16个数学函数 - 基本运算、三角函数、对数、统计函数等

### [字符串函数参考](02_string_functions.md)
28个字符串函数 - 字符串操作、搜索、替换、格式化等

### [日期时间函数参考](03_datetime_functions.md)
12个日期时间函数 - 当前日期时间、日期计算、日期时间组件获取、日期转换等

### [CSV函数参考](04_csv_functions.md)
9个CSV函数 - CSV操作、随机选择、去重等

### [正则表达式函数参考](05_regex_functions.md)
7个正则表达式函数 - 模式匹配、替换、提取等

### [数组函数参考](06_array_functions.md)
3个数组函数 - 数组初始化、大小调整、获取上限索引等

### [类型转换·类型判断函数参考](07_type_functions.md)
7个类型转换·类型判断函数 - 类型转换、类型检查、格式整形等

### [模型函数参考](08_model_functions.md)
1个模型函数 - AI生成模型的最优分辨率判定

### [实用工具函数参考](09_utility_functions.md)
18个实用工具函数 - 调试输出、类型判定、文件输入输出、文件存在检查、内存释放、休眠、图像处理（IMAGE→JSON数组/Base64转换）、图像·Latent数据获取、ANY型数据获取等


---

## 快速参考表

### 数学函数（16个）

| 函数名 | 概要 |
|--------|------|
| **ABS(value)** | 返回绝对值 |
| **INT(value)** | 返回整数部分（向下取整） |
| **ROUND(value, [digits])** | 返回四舍五入的值 |
| **SQRT(value)** | 返回平方根 |
| **MIN(value1, value2, ...)** | 返回最小值 |
| **MAX(value1, value2, ...)** | 返回最大值 |
| **SIN(radians)** | 返回正弦值 |
| **COS(radians)** | 返回余弦值 |
| **TAN(radians)** | 返回正切值 |
| **RADIANS(degrees)** | 将角度转换为弧度 |
| **DEGREES(radians)** | 将弧度转换为角度 |
| **POW(base, exponent)** | 计算幂次方（base^exponent） |
| **LOG(value, [base])** | 返回对数（默认：自然对数） |
| **EXP(value)** | e（自然对数底）的幂次方 |
| **AVG(value1, value2, ...)** | 计算平均值 |
| **SUM(value1, value2, ...)** | 计算总和 |

### 字符串函数（28个）

| 函数名 | 概要 |
|--------|------|
| **LEN(text)** | 返回字符串长度 |
| **LEFT(text, length)** | 从左侧获取指定字符数 |
| **RIGHT(text, length)** | 从右侧获取指定字符数 |
| **MID(text, start, length)** | 从指定位置获取子字符串 |
| **UPPER(text)** | 转换为大写 |
| **LOWER(text)** | 转换为小写 |
| **TRIM(text)** | 删除前后空白 |
| **REPLACE(text, old, new)** | 替换字符串 |
| **INSTR([start,] text, search)** | 搜索字符串（返回位置） |
| **INSTRREV(text, search, [start])** | 从后向前搜索字符串 |
| **STRREVERSE(text)** | 反转字符串 |
| **STRCOMP(text1, text2, [compare])** | 比较字符串 |
| **SPACE(number)** | 生成指定数量的空格 |
| **STRING(number, character)** | 重复字符 |
| **FORMAT(value, format_string)** | 格式化值 |
| **SPLIT(text, [delimiter])** | 分割字符串为数组 |
| **JOIN(array, [delimiter])** | 将数组连接为字符串 |
| **LTRIM(text)** | 删除左侧空白 |
| **RTRIM(text)** | 删除右侧空白 |
| **UCASE(text)** | 转换为大写（UPPER的别名） |
| **LCASE(text)** | 转换为小写（LOWER的别名） |
| **PROPER(text)** | 转换为标题格式 |
| **CHR(code)** | 字符代码→字符转换 |
| **ASC(char)** | 字符→字符代码转换 |
| **STR(value)** | 数值→字符串转换 |
| **URLENCODE(text, [encoding])** | URL编码 |
| **URLDECODE(text, [encoding])** | URL解码 |
| **ESCAPEPATHSTR(path, [replacement])** | 处理文件路径禁用字符 |

### 日期时间函数（12个）

| 函数名 | 概要 |
|--------|------|
| **NOW()** | 获取当前日期时间 |
| **DATE()** | 获取今天的日期 |
| **TIME()** | 获取当前时间 |
| **YEAR([date])** | 获取年份 |
| **MONTH([date])** | 获取月份 |
| **DAY([date])** | 获取日 |
| **HOUR([time])** | 获取小时 |
| **MINUTE([time])** | 获取分钟 |
| **SECOND([time])** | 获取秒 |
| **DATEADD(interval, number, [date])** | 日期加减 |
| **DATEDIFF(interval, date1, [date2])** | 计算日期差 |
| **WEEKDAY([date], [firstday])** | 返回星期几（1=星期日） |

### CSV函数（9个）

| 函数名 | 概要 |
|--------|------|
| **CSVCOUNT(csv_text)** | 统计CSV元素数量 |
| **CSVREAD(csv_text, index)** | 从CSV字符串获取指定索引的元素 |
| **CSVUNIQUE(csv_text)** | 去除重复 |
| **CSVMERGE(csv1, csv2, ...)** | 合并多个CSV |
| **CSVDIFF(array_name, csv1, csv2)** | 获取CSV的差异 |
| **PICKCSV(csv_text, [index])** | 选择CSV元素（省略时：随机） |
| **RNDCSV(csv_text)** | 从CSV随机选择（与PICKCSV相同） |
| **CSVJOIN(array, [delimiter])** | 将数组连接为CSV字符串 |
| **CSVSORT(csv_text, [delimiter], [reverse])** | 对CSV元素排序 |

### 正则表达式函数（7个）

| 函数名 | 概要 |
|--------|------|
| **REGEX(pattern, text)** | 测试模式匹配 |
| **REGEXMATCH(pattern, text)** | 获取第一个匹配 |
| **REGEXREPLACE(pattern, text, replacement)** | 替换模式 |
| **REGEXEXTRACT(pattern, text, [group])** | 提取组 |
| **REGEXCOUNT(pattern, text)** | 统计匹配数量 |
| **REGEXMATCHES(pattern, text)** | 获取所有匹配的数组 |
| **REGEXSPLIT(pattern, text)** | 按模式分割 |

### 数组函数（3个）

| 函数名 | 概要 |
|--------|------|
| **UBOUND(array)** | 获取数组的上限索引 |
| **ARRAY(variable_name, value1, value2, ...)** | 初始化数组并设置值 |
| **REDIM(array_name, size)** | 更改数组大小（重新定义） |

### 类型转换·类型判断函数（7个）

| 函数名 | 概要 |
|--------|------|
| **CSTR(value)** | 转换为字符串 |
| **CINT(value)** | 转换为整数 |
| **CDBL(value)** | 转换为浮点数 |
| **FORMAT(value, [format_string])** | 以指定格式整形数值·日期时间（VBA兼容） |
| **ISNUMERIC(value)** | 判断是否为数值 |
| **ISDATE(value)** | 判断是否为日期 |
| **ISARRAY(variable_name)** | 判断是否为数组 |

### 模型函数（1个）

| 函数名 | 概要 |
|--------|------|
| **OPTIMAL_LATENT(model_hint, width, height)** | 根据模型名称和纵横比自动判定最优Latent空间大小 |

### 实用工具函数（18个）

| 函数名 | 概要 |
|--------|------|
| **PRINT(message, ...)** | 将值输出到文本区域（用于调试） |
| **OUTPUT(arg, [path], [flg])** | 将文本、数值、数组、图像、二进制数据输出到文件 |
| **INPUT(path)** | 从ComfyUI输出文件夹读取文件（动态类型判定） |
| **ISFILEEXIST(path, [flg])** | 文件存在检查和扩展信息获取（_NNNN搜索、图像大小、文件大小） |
| **VRAMFREE([min_free_vram_gb])** | 释放VRAM和RAM（卸载模型、清除缓存、GC） |
| **SLEEP([milliseconds])** | 暂停处理指定毫秒（默认：10ms） |
| **IMAGETOBYTEARRAY(image_input, [max_size], [format], [return_format])** | 将IMAGE/文件路径转换为图像JSON数组 |
| **IMAGETOBASE64(image_input, [max_size], [format], [return_format])** | 将IMAGE/文件路径转换为Base64编码（用于Vision API） |
| **GETANYWIDTH([any_data])** | 获取IMAGE/LATENT型数据的宽度（像素数） |
| **GETANYHEIGHT([any_data])** | 获取IMAGE/LATENT型数据的高度（像素数） |
| **GETANYTYPE([any_data])** | 判定ANY型数据的类型名 |
| **GETANYVALUEINT([any_data])** | 从ANY型数据获取整数值 |
| **GETANYVALUEFLOAT([any_data])** | 从ANY型数据获取浮点数值 |
| **GETANYSTRING([any_data])** | 从ANY型数据获取字符串 |
| **ISNUMERIC(value)** | 判断值是否为数值 |
| **ISDATE(value)** | 判断值是否可解析为日期 |
| **ISARRAY(variable_name)** | 判断变量是否为数组 |
| **TYPE(value)** | 以字符串形式返回变量类型 |



---

[← 返回主文档](README.md)
