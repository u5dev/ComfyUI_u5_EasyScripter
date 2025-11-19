# 日期时间函数参考

[← 返回内置函数索引](00_index.md) | [English](../02_builtin_functions/03_datetime_functions.md) | [日本語](../02_builtin_functions/03_datetime_functions.md) | [Français](../fr/03_datetime_functions.md) | [Español](../es/03_datetime_functions.md)

u5 EasyScripter可用的日期时间函数完整参考。

## 函数一览
提供12个日期时间函数。

---

### NOW()
**说明**: 获取当前日期时间
**参数**: 无
**返回值**: 日期时间字符串（YYYY-MM-DD HH:MM:SS）
**示例**:
```vba
currentTime = NOW()
PRINT(currentTime)    ' "2024-01-15 14:30:45"
PRINT("当前时刻: " & NOW())
```

### DATE()
**说明**: 获取今天的日期
**参数**: 无
**返回值**: 日期字符串（YYYY-MM-DD）
**示例**:
```vba
today = DATE()
PRINT(today)    ' "2024-01-15"
```

### TIME()
**说明**: 获取当前时间
**参数**: 无
**返回值**: 时间字符串（HH:MM:SS）
**示例**:
```vba
currentTime = TIME()
PRINT(currentTime)    ' "14:30:45"
```

### YEAR([date])
**说明**: 获取年份
**参数**: date - 日期字符串（省略时:今天）
**返回值**: 年份（数值）
**示例**:
```vba
result = YEAR()
PRINT(result)              ' 2024（今年）
result = YEAR("2023-12-25")
PRINT(result)              ' 2023
```

### MONTH([date])
**说明**: 获取月份
**参数**: date - 日期字符串（省略时:今天）
**返回值**: 月份（1-12）
**示例**:
```vba
result = MONTH()
PRINT(result)             ' 1（本月）
result = MONTH("2023-12-25")
PRINT(result)             ' 12
```

### DAY([date])
**说明**: 获取日
**参数**: date - 日期字符串（省略时:今天）
**返回值**: 日（1-31）
**示例**:
```vba
result = DAY()
PRINT(result)               ' 15（今天）
result = DAY("2023-12-25")
PRINT(result)               ' 25
```

### HOUR([time])
**说明**: 获取小时
**参数**: time - 时间字符串（省略时:当前）
**返回值**: 小时（0-23）
**示例**:
```vba
result = HOUR()
PRINT(result)              ' 14（当前小时）
result = HOUR("15:30:45")
PRINT(result)              ' 15
```

### MINUTE([time])
**说明**: 获取分钟
**参数**: time - 时间字符串（省略时:当前）
**返回值**: 分钟（0-59）
**示例**:
```vba
result = MINUTE()
PRINT(result)            ' 30（当前分钟）
result = MINUTE("15:30:45")
PRINT(result)            ' 30
```

### SECOND([time])
**说明**: 获取秒
**参数**: time - 时间字符串（省略时:当前）
**返回值**: 秒（0-59）
**示例**:
```vba
result = SECOND()
PRINT(result)            ' 45（当前秒）
result = SECOND("15:30:45")
PRINT(result)            ' 45
```

### DATEADD(interval, number, [date])
**说明**: 日期加减
**参数**:
- interval - 单位（"d"=日, "m"=月, "y"=年, "h"=时, "n"=分, "s"=秒）
- number - 加算的数值
- date - 基准日期时间（省略时:当前）
**返回值**: 计算后的日期时间（YYYY/MM/DD HH:MM:SS格式）
**示例**:
```vba
tomorrow = DATEADD("d", 1, DATE())
PRINT(tomorrow)        ' 明天（例: "2025/10/23 00:00:00"）
nextMonth = DATEADD("m", 1, "2024-01-15")
PRINT(nextMonth)       ' "2024/02/15 00:00:00"
inOneHour = DATEADD("h", 1, NOW())
PRINT(inOneHour)       ' 1小时后（例: "2025/10/22 15:30:00"）
```

### DATEDIFF(interval, date1, [date2])
**说明**: 计算日期差
**参数**:
- interval - 单位（"d"=日, "m"=月, "y"=年, "h"=时, "n"=分, "s"=秒）
- date1 - 开始日期时间
- date2 - 结束日期时间（省略时:当前）
**返回值**: 差值（数值）
**示例**:
```vba
days = DATEDIFF("d", "2024-01-01", "2024-01-15")
PRINT(days)  ' 14
age = DATEDIFF("y", "1990-01-01", DATE())
PRINT(age)   ' 年龄
hours = DATEDIFF("h", "2024-01-15 10:00:00", NOW())
PRINT(hours) ' 经过时间
```

### CDATE(date_string)
**说明**: 将日期字符串转换为日期类型（VBA兼容）
**参数**: date_string - 表示日期的字符串
**返回值**: 日期字符串（YYYY/MM/DD HH:MM:SS格式）
**灵活格式支持**:
- 完整日期时间: `"2025/11/05 15:39:49"` → `2025/11/05 15:39:49`
- 仅日期: `"2025/11/05"` → `2025/11/05 00:00:00` （时间为00:00:00）
- 仅年月: `"2025/11"` → `2025/11/01 00:00:00` （日=1、时间=00:00:00）
- 仅年: `"2025"` → `2025/01/01 00:00:00` （月日=1/1、时间=00:00:00）
- 仅时: `"2025/11/05 15"` → `2025/11/05 15:00:00` （分秒=00）
- 仅时分: `"2025/11/05 15:39"` → `2025/11/05 15:39:00` （秒=00）

**分隔符灵活性**:
- 允许 `/` 和 `-` 和 `:` 和空格混合使用
- `"2025-11-05-15-39-49"` 和 `"2025-11-05 15-39-49"` 和 `"2025-11-05 15:39:49"` 都同样处理

**示例**:
```vba
' 完整日期时间
result = CDATE("2025/11/05 15:39:49")
PRINT(result)  ' "2025/11/05 15:39:49"

' 仅日期（时间为00:00:00）
result = CDATE("2025/11/05")
PRINT(result)  ' "2025/11/05 00:00:00"

' 分隔符混合OK
result = CDATE("2025-11-05 15:39:49")
PRINT(result)  ' "2025/11/05 15:39:49"

' 部分日期（不足部分自动补全）
result = CDATE("2025/11")
PRINT(result)  ' "2025/11/01 00:00:00"
```

---

[← 返回内置函数索引](00_index.md)
