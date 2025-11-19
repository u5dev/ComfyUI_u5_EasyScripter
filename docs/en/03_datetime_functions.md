# Date/Time Functions Reference

**Languages**: [日本語](../02_builtin_functions/03_datetime_functions.md) | [English](03_datetime_functions.md)

[← Back to Built-in Functions Index](00_index.md)

Complete reference for date/time functions available in u5 EasyScripter.

## Function List
Provides 12 date/time functions.

---

### NOW()
**Description**: Gets the current date and time
**Arguments**: None
**Return Value**: Date/time string (YYYY-MM-DD HH:MM:SS)
**Example**:
```vba
currentTime = NOW()
PRINT(currentTime)    ' "2024-01-15 14:30:45"
PRINT("Current Time: " & NOW())
```

### DATE()
**Description**: Gets today's date
**Arguments**: None
**Return Value**: Date string (YYYY-MM-DD)
**Example**:
```vba
today = DATE()
PRINT(today)    ' "2024-01-15"
```

### TIME()
**Description**: Gets the current time
**Arguments**: None
**Return Value**: Time string (HH:MM:SS)
**Example**:
```vba
currentTime = TIME()
PRINT(currentTime)    ' "14:30:45"
```

### YEAR([date])
**Description**: Extracts the year
**Arguments**: date - Date string (default: today)
**Return Value**: Year (number)
**Example**:
```vba
result = YEAR()
PRINT(result)              ' 2024 (this year)
result = YEAR("2023-12-25")
PRINT(result)              ' 2023
```

### MONTH([date])
**Description**: Extracts the month
**Arguments**: date - Date string (default: today)
**Return Value**: Month (1-12)
**Example**:
```vba
result = MONTH()
PRINT(result)             ' 1 (this month)
result = MONTH("2023-12-25")
PRINT(result)             ' 12
```

### DAY([date])
**Description**: Extracts the day
**Arguments**: date - Date string (default: today)
**Return Value**: Day (1-31)
**Example**:
```vba
result = DAY()
PRINT(result)               ' 15 (today)
result = DAY("2023-12-25")
PRINT(result)               ' 25
```

### HOUR([time])
**Description**: Extracts the hour
**Arguments**: time - Time string (default: now)
**Return Value**: Hour (0-23)
**Example**:
```vba
result = HOUR()
PRINT(result)              ' 14 (current hour)
result = HOUR("15:30:45")
PRINT(result)              ' 15
```

### MINUTE([time])
**Description**: Extracts the minute
**Arguments**: time - Time string (default: now)
**Return Value**: Minute (0-59)
**Example**:
```vba
result = MINUTE()
PRINT(result)            ' 30 (current minute)
result = MINUTE("15:30:45")
PRINT(result)            ' 30
```

### SECOND([time])
**Description**: Extracts the second
**Arguments**: time - Time string (default: now)
**Return Value**: Second (0-59)
**Example**:
```vba
result = SECOND()
PRINT(result)            ' 45 (current second)
result = SECOND("15:30:45")
PRINT(result)            ' 45
```

### DATEADD(interval, number, [date])
**Description**: Adds/subtracts date/time
**Arguments**:
- interval - Unit ("d"=day, "m"=month, "y"=year, "h"=hour, "n"=minute, "s"=second)
- number - Number to add
- date - Base date/time (default: now)
**Return Value**: Calculated date/time (YYYY/MM/DD HH:MM:SS format)
**Example**:
```vba
tomorrow = DATEADD("d", 1, DATE())
PRINT(tomorrow)        ' Tomorrow (e.g. "2025/10/23 00:00:00")
nextMonth = DATEADD("m", 1, "2024-01-15")
PRINT(nextMonth)       ' "2024/02/15 00:00:00"
inOneHour = DATEADD("h", 1, NOW())
PRINT(inOneHour)       ' One hour later (e.g. "2025/10/22 15:30:00")
```

### DATEDIFF(interval, date1, [date2])
**Description**: Calculates date difference
**Arguments**:
- interval - Unit ("d"=day, "m"=month, "y"=year, "h"=hour, "n"=minute, "s"=second)
- date1 - Start date/time
- date2 - End date/time (default: now)
**Return Value**: Difference (number)
**Example**:
```vba
days = DATEDIFF("d", "2024-01-01", "2024-01-15")
PRINT(days)  ' 14
age = DATEDIFF("y", "1990-01-01", DATE())
PRINT(age)   ' Age
hours = DATEDIFF("h", "2024-01-15 10:00:00", NOW())
PRINT(hours) ' Elapsed hours
```

### CDATE(date_string)
**Description**: Converts date string to date type (VBA compatible)
**Arguments**: date_string - String representing a date
**Return Value**: Date string (YYYY/MM/DD HH:MM:SS format)
**Flexible Format Support**:
- Full date/time: `"2025/11/05 15:39:49"` → `2025/11/05 15:39:49`
- Date only: `"2025/11/05"` → `2025/11/05 00:00:00` (time defaults to 00:00:00)
- Year/month only: `"2025/11"` → `2025/11/01 00:00:00` (day=1, time=00:00:00)
- Year only: `"2025"` → `2025/01/01 00:00:00` (month/day=1/1, time=00:00:00)
- Hour only: `"2025/11/05 15"` → `2025/11/05 15:00:00` (minute/second=00)
- Hour/minute only: `"2025/11/05 15:39"` → `2025/11/05 15:39:00` (second=00)

**Delimiter Flexibility**:
- Allows mixing of `/`, `-`, `:`, and spaces
- `"2025-11-05-15-39-49"`, `"2025-11-05 15-39-49"`, `"2025-11-05 15:39:49"` all processed identically

**Example**:
```vba
' Full date/time
result = CDATE("2025/11/05 15:39:49")
PRINT(result)  ' "2025/11/05 15:39:49"

' Date only (time becomes 00:00:00)
result = CDATE("2025/11/05")
PRINT(result)  ' "2025/11/05 00:00:00"

' Mixed delimiters OK
result = CDATE("2025-11-05 15:39:49")
PRINT(result)  ' "2025/11/05 15:39:49"

' Partial dates (missing parts are filled)
result = CDATE("2025/11")
PRINT(result)  ' "2025/11/01 00:00:00"
```

---

[← Back to Built-in Functions Index](00_index.md)
