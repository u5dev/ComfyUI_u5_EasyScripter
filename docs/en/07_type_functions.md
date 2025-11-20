# Type Conversion/Type Detection Functions Reference

[← Back to Built-in Functions Index](00_index.md)

## Overview

Type conversion and type detection functions for converting value types and determining variable types.

**Type Conversion Functions**:
- CSTR - Convert to string
- CINT - Convert to integer
- CDBL - Convert to floating-point number
- FORMAT - Format numbers/dates with specified format (VBA compatible)

**Type Detection Functions**:
- ISNUMERIC - Determine if numeric
- ISDATE - Determine if date
- ISARRAY - Determine if array

---

## Type Conversion Functions

### CSTR(value)

**Description**: Converts to string

**Arguments**:
- `value` - Any value

**Return Value**: String

**Example**:
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

**Description**: Converts to integer

**Arguments**:
- `value` - Number or string

**Return Value**: Integer (float format)

**Example**:
```vba
number = CINT("123")
PRINT(number)            ' 123
number = CINT(45.67)
PRINT(number)            ' 46 (rounded)
number = CINT("3.14")
PRINT(number)            ' 3
```

---

### CDBL(value)

**Description**: Converts to floating-point number

**Arguments**:
- `value` - Number or string

**Return Value**: float

**Example**:
```vba
number = CDBL("123.45")
PRINT(number)            ' 123.45
number = CDBL(10)
PRINT(number)            ' 10
```

---

### FORMAT(value, [format_string])

**Description**: Formats numbers/dates with specified format (VBA compatible)

**Arguments**:
- `value` (Any, required) - Value to format (number, string, date/time)
- `format_string` (str, optional) - Format specifier (default: "")

**Return Value**: str - Formatted string

**Supported Format Types**:

1. **VBA Format**:
   - `"0"` - Integer (rounded)
   - `"0.0"` - 1 decimal place
   - `"0.00"` - 2 decimal places
   - `"#"`, `"#.#"`, `"#.##"` - Auto precision

2. **Python format Format**:
   - `"{:.2f}"` - Python format syntax
   - `".2f"`, `","` - format spec

3. **Date/Time Format (strftime)**:
   - `"%Y-%m-%d %H:%M:%S"` - Date/time format
   - `"%Y/%m/%d"` - Date only

**Example**:
```vba
' VBA format
result = FORMAT(123.456, "0")       ' "123" (integer)
PRINT("Integer: " & result)
result = FORMAT(123.456, "0.0")     ' "123.5" (1 decimal)
PRINT("1 decimal: " & result)
result = FORMAT(123.456, "0.00")    ' "123.46" (2 decimals)
PRINT("2 decimals: " & result)

' Python format format
result = FORMAT(3.14159, "{:.2f}")  ' "3.14"
PRINT("Pi: " & result)
result = FORMAT(1234567, ",")       ' "1,234,567"
PRINT("Comma separator: " & result)

' Date/time format
now_str = NOW()
result = FORMAT(now_str, "%Y-%m-%d %H:%M:%S")
PRINT("Date/time: " & result)             ' "2024-01-15 14:30:00"
result = FORMAT(now_str, "%Y年%m月%d日")
PRINT("Date: " & result)             ' "2024年01月15日"
```

**Note**:
- If `format_string` is omitted, value is converted to string as-is
- Unsupported formats return value as str()

---

## Type Detection Functions

### ISNUMERIC(value)

**Description**: Determines if numeric

**Arguments**:
- `value` - Value to check

**Return Value**: 1 (numeric) or 0

**Example**:
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

**Description**: Determines if date

**Arguments**:
- `value` - Value to check

**Return Value**: 1 (date) or 0

**Example**:
```vba
result = ISDATE("2024-01-15")
PRINT(result)                     ' 1
result = ISDATE("2024/01/15")
PRINT(result)                     ' 1
result = ISDATE("15:30:00")
PRINT(result)                     ' 1 (time too)
result = ISDATE("hello")
PRINT(result)                     ' 0
```

---

### ISARRAY(variable_name)

**Description**: Determines if array

**Important**: Pass array name as string or array variable reference with ARR[] notation.

**Arguments**:
- `variable_name` - Variable name (string) or array variable reference

**Return Value**: 1 (array) or 0

**Example**:
```vba
REDIM ARR, 10
result = ISARRAY(ARR[])
PRINT(result)                ' 1 (array reference)
result = ISARRAY("ARR")
PRINT(result)                ' 1 (array name string)
result = ISARRAY("VAL1")
PRINT(result)                ' 0 (regular variable)
```

---

[← Back to Built-in Functions Index](00_index.md)
