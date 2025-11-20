# CSV函数参考

[← 返回内置函数索引](00_index.md)

## 概述

操作CSV（逗号分隔值）字符串的函数群。方便用于提示词生成和设置值管理。

- CSV元素的计数·获取
- 通过随机选择生成提示词
- 去重和差异获取
- 数组和CSV的相互转换

---

## 函数一览

### CSVCOUNT(csv_text)

**说明**: 统计CSV元素数量

**参数**:
- csv_text - 逗号分隔字符串

**返回值**: 元素数量（整数）

**示例**:
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

**说明**: 从CSV字符串获取指定索引的元素

**参数**:
- csv_text - 逗号分隔字符串
- index - 获取元素的索引（1-based）

**返回值**: 指定位置的元素（字符串）。超出范围时返回空字符串

**示例**:
```vba
element = CSVREAD("apple,banana,orange", 2)
PRINT(element)    ' banana
element = CSVREAD("a,b,c,d", 1)
PRINT(element)    ' a
element = CSVREAD("x,y,z", 10)
PRINT(element)    ' （超出范围时返回空字符串）
```

---

### CSVUNIQUE(csv_text)

**说明**: 去除重复

**参数**:
- csv_text - 逗号分隔字符串

**返回值**: 去重后的CSV字符串

**示例**:
```vba
result = CSVUNIQUE("a,b,a,c,b")
PRINT(result)    ' a,b,c
result = CSVUNIQUE("1,2,3,2,1")
PRINT(result)    ' 1,2,3
```

---

### CSVMERGE(csv1, csv2, ...)

**说明**: 合并多个CSV

**参数**:
- csv1, csv2, ... - 多个CSV字符串（可变长参数）

**返回值**: 合并后的CSV字符串

**示例**:
```vba
result = CSVMERGE("a,b", "c,d")
PRINT(result)        ' a,b,c,d
result = CSVMERGE("1,2", "3", "4,5")
PRINT(result)        ' 1,2,3,4,5
```

---

### CSVDIFF(array_name, csv1, csv2)

**说明**: 将2个CSV字符串的差异（仅存在于其中一个的元素）存储到数组

**参数**:
- array_name - 存储结果的数组变量名
- csv1 - CSV字符串1
- csv2 - CSV字符串2

**返回值**: 差异元素的数量（整数）

**示例**:
```vba
' 获取csv1中存在但csv2中不存在的元素，以及csv2中存在但csv1中不存在的元素
DIM diff_array
count = CSVDIFF(diff_array, "a,b,c,d", "b,d,e")
PRINT(count)           ' 3
PRINT(diff_array(0))   ' a
PRINT(diff_array(1))   ' c
PRINT(diff_array(2))   ' e
```

---

### PICKCSV(csv_text, [index])

**说明**: 选择CSV元素

**参数**:
- csv_text - CSV字符串
- index - 索引（省略时:随机选择）

**返回值**: 选择的元素（字符串）

**示例**:
```vba
result = PICKCSV("red,green,blue", 2)
PRINT(result)     ' green
result = PICKCSV("A,B,C,D")
PRINT(result)     ' A, B, C, 或 D 之一
```

---

### RNDCSV(csv_text, [count])

**说明**: 从CSV随机选择（也可获取多个元素的数组）

**参数**:
- csv_text - CSV字符串
- count - 选择的元素数量（省略时返回1个字符串）

**返回值**:
- count未指定时: 随机选择的1个元素（字符串）
- count=1: 随机选择的1个元素（字符串）
- count≥2: 随机选择的元素列表
- count >= 元素数: 保持原始排序顺序的完整数组

**示例**:
```vba
' 选择1个元素（传统方式）
style = RNDCSV("realistic,anime,cartoon,abstract")
PRINT(style)
color = RNDCSV("red,blue,green,yellow,purple")
PRINT(color)

' 作为数组获取多个元素（允许重复）
DIM selected[3]
selected = RNDCSV("A,B,B,B,C,C,D", 3)
PRINT(selected)  ' 例: ["B", "B", "D"]

' 超过元素数时返回原始顺序的全部元素
DIM all[3]
all = RNDCSV("X,Y,Z", 5)
PRINT(all)  ' ["X", "Y", "Z"] (保持原始顺序)

' 与RANDOMIZE联动(固定Seed值)
RANDOMIZE(12345)
result = RNDCSV("1,2,3,4,5", 3)
PRINT(result)  ' 可重现的随机选择
```

---

### CSVJOIN(array, [delimiter])

**说明**: 将数组连接为CSV字符串

**参数**:
- array - 数组
- delimiter - 分隔符（省略时:逗号）

**返回值**: 连接后的CSV字符串

**示例**:
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

**说明**: 对CSV元素排序

**参数**:
- csv_text - 由分隔符分隔的文本
- delimiter - 分隔符（省略时: ","）
- descending - 降序标志（省略时: False、0=升序, 1或True=降序）

**返回值**: 排序后的CSV字符串

**示例**:
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

## 实用示例

### 提示词生成中的随机选择

```vba
' 随机选择样式（1个）
style = RNDCSV("photorealistic,anime,oil painting,watercolor")
PRINT(style)
' 随机选择色调
tone = RNDCSV("warm,cool,vivid,muted,monochrome")
PRINT(tone)
' 随机选择时间段
time = RNDCSV("morning,noon,sunset,night")
PRINT(time)

PRINT("1girl, " & style & ", " & tone & " tone, " & time)

' 混合多个样式（数组选择）
DIM styles[3]
styles = RNDCSV("realistic,anime,3d,sketch,oil,watercolor,digital", 3)
PRINT(styles)
stylePrompt = CSVJOIN(styles, ", ")
PRINT(stylePrompt)
PRINT("1girl, " & stylePrompt)
```


### 列表的去重和合并

```vba
' 合并多个标签列表
tags1 = "girl,outdoor,sunny,smile"
PRINT(tags1)
tags2 = "outdoor,happy,smile,park"
PRINT(tags2)
tags3 = "girl,smile,nature"
PRINT(tags3)

' 合并
allTags = CSVMERGE(tags1, tags2, tags3)
PRINT(allTags)
' "girl,outdoor,sunny,smile,happy,smile,park,girl,smile,nature"

' 去除重复
uniqueTags = CSVUNIQUE(allTags)
PRINT(uniqueTags)
' "girl,outdoor,sunny,smile,happy,park,nature"
```

---

[← 返回内置函数索引](00_index.md)
