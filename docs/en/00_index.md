# Built-in Function Complete Index

**Languages**: [日本語](../02_builtin_functions/00_index.md) | [English](00_index.md)

[← Back to Main Documentation](README.md)

**This page is the reference index for u5 EasyScripter's built-in functions.**

u5 EasyScripter provides a rich set of built-in functions usable in VBA-style scripts.

## Function Category List

### [Math Function Reference](01_math_functions.md)
16 math functions - basic operations, trigonometric functions, logarithms, statistical functions, etc.

### [String Function Reference](02_string_functions.md)
28 string functions - string manipulation, search, replace, formatting, etc.

### [Date/Time Function Reference](03_datetime_functions.md)
12 date/time functions - current date/time, date calculations, date/time component extraction, date conversion, etc.

### [CSV Function Reference](04_csv_functions.md)
9 CSV functions - CSV manipulation, random selection, duplicate removal, etc.

### [Regular Expression Function Reference](05_regex_functions.md)
7 regular expression functions - pattern matching, replacement, extraction, etc.

### [Array Function Reference](06_array_functions.md)
3 array functions - array initialization, resizing, upper bound index retrieval, etc.

### [Type Conversion/Type Check Function Reference](07_type_functions.md)
7 type conversion/type check functions - type conversion, type checking, format formatting, etc.

### [Model Function Reference](08_model_functions.md)
1 model function - AI generation model optimal resolution determination

### [Utility Function Reference](09_utility_functions.md)
18 utility functions - debug output, type determination, file I/O, file existence check, memory release, sleep, image processing (IMAGE→JSON array/Base64 conversion), image/Latent data retrieval, ANY type data retrieval, etc.


---

## Quick Reference Table

### Math Functions (16)

| Function Name | Overview |
|---------------|----------|
| **ABS(value)** | Returns absolute value |
| **INT(value)** | Returns integer part (rounds down decimals) |
| **ROUND(value, [digits])** | Returns rounded value |
| **SQRT(value)** | Returns square root |
| **MIN(value1, value2, ...)** | Returns minimum value |
| **MAX(value1, value2, ...)** | Returns maximum value |
| **SIN(radians)** | Returns sine |
| **COS(radians)** | Returns cosine |
| **TAN(radians)** | Returns tangent |
| **RADIANS(degrees)** | Converts degrees to radians |
| **DEGREES(radians)** | Converts radians to degrees |
| **POW(base, exponent)** | Calculates power (base^exponent) |
| **LOG(value, [base])** | Returns logarithm (default: natural logarithm) |
| **EXP(value)** | e (base of natural logarithm) to the power |
| **AVG(value1, value2, ...)** | Calculates average |
| **SUM(value1, value2, ...)** | Calculates sum |

### String Functions (28)

| Function Name | Overview |
|---------------|----------|
| **LEN(text)** | Returns string length |
| **LEFT(text, length)** | Gets specified number of characters from left |
| **RIGHT(text, length)** | Gets specified number of characters from right |
| **MID(text, start, length)** | Gets substring from specified position |
| **UPPER(text)** | Converts to uppercase |
| **LOWER(text)** | Converts to lowercase |
| **TRIM(text)** | Removes leading/trailing whitespace |
| **REPLACE(text, old, new)** | Replaces string |
| **INSTR([start,] text, search)** | Searches string (returns position) |
| **INSTRREV(text, search, [start])** | Searches string from back |
| **STRREVERSE(text)** | Reverses string |
| **STRCOMP(text1, text2, [compare])** | Compares strings |
| **SPACE(number)** | Generates specified number of spaces |
| **STRING(number, character)** | Repeats character |
| **FORMAT(value, format_string)** | Formats value |
| **SPLIT(text, [delimiter])** | Splits string into array |
| **JOIN(array, [delimiter])** | Joins array into string |
| **LTRIM(text)** | Removes left whitespace |
| **RTRIM(text)** | Removes right whitespace |
| **UCASE(text)** | Converts to uppercase (alias for UPPER) |
| **LCASE(text)** | Converts to lowercase (alias for LOWER) |
| **PROPER(text)** | Converts to title case |
| **CHR(code)** | Character code → character conversion |
| **ASC(char)** | Character → character code conversion |
| **STR(value)** | Number → string conversion |
| **URLENCODE(text, [encoding])** | URL encoding |
| **URLDECODE(text, [encoding])** | URL decoding |
| **ESCAPEPATHSTR(path, [replacement])** | Processes forbidden file path characters |

### Date/Time Functions (12)

| Function Name | Overview |
|---------------|----------|
| **NOW()** | Gets current date/time |
| **DATE()** | Gets today's date |
| **TIME()** | Gets current time |
| **YEAR([date])** | Gets year |
| **MONTH([date])** | Gets month |
| **DAY([date])** | Gets day |
| **HOUR([time])** | Gets hour |
| **MINUTE([time])** | Gets minute |
| **SECOND([time])** | Gets second |
| **DATEADD(interval, number, [date])** | Adds/subtracts from date |
| **DATEDIFF(interval, date1, [date2])** | Calculates date difference |
| **WEEKDAY([date], [firstday])** | Returns weekday (1=Sunday) |

### CSV Functions (9)

| Function Name | Overview |
|---------------|----------|
| **CSVCOUNT(csv_text)** | Counts CSV elements |
| **CSVREAD(csv_text, index)** | Gets element at specified index from CSV string |
| **CSVUNIQUE(csv_text)** | Removes duplicates |
| **CSVMERGE(csv1, csv2, ...)** | Merges multiple CSVs |
| **CSVDIFF(array_name, csv1, csv2)** | Gets CSV difference |
| **PICKCSV(csv_text, [index])** | Selects CSV element (omit: random) |
| **RNDCSV(csv_text)** | Random selection from CSV (same as PICKCSV) |
| **CSVJOIN(array, [delimiter])** | Joins array into CSV string |
| **CSVSORT(csv_text, [delimiter], [reverse])** | Sorts CSV elements |

### Regular Expression Functions (7)

| Function Name | Overview |
|---------------|----------|
| **REGEX(pattern, text)** | Tests pattern match |
| **REGEXMATCH(pattern, text)** | Gets first match |
| **REGEXREPLACE(pattern, text, replacement)** | Replaces pattern |
| **REGEXEXTRACT(pattern, text, [group])** | Extracts group |
| **REGEXCOUNT(pattern, text)** | Counts matches |
| **REGEXMATCHES(pattern, text)** | Gets all matches as array |
| **REGEXSPLIT(pattern, text)** | Splits by pattern |

### Array Functions (3)

| Function Name | Overview |
|---------------|----------|
| **UBOUND(array)** | Gets array upper bound index |
| **ARRAY(variable_name, value1, value2, ...)** | Initializes array and sets values |
| **REDIM(array_name, size)** | Resizes array (redimension) |

### Type Conversion/Type Check Functions (7)

| Function Name | Overview |
|---------------|----------|
| **CSTR(value)** | Converts to string |
| **CINT(value)** | Converts to integer |
| **CDBL(value)** | Converts to floating-point number |
| **FORMAT(value, [format_string])** | Formats number/datetime with specified format (VBA compatible) |
| **ISNUMERIC(value)** | Checks if numeric |
| **ISDATE(value)** | Checks if date |
| **ISARRAY(variable_name)** | Checks if array |

### Model Functions (1)

| Function Name | Overview |
|---------------|----------|
| **OPTIMAL_LATENT(model_hint, width, height)** | Automatically determines optimal Latent space size from model name and aspect ratio |

### Utility Functions (18)

| Function Name | Overview |
|---------------|----------|
| **PRINT(message, ...)** | Outputs values to text area (for debugging) |
| **OUTPUT(arg, [path], [flg])** | Outputs text, numbers, arrays, images, binary data to file |
| **INPUT(path)** | Reads file from ComfyUI output folder (dynamic type detection) |
| **ISFILEEXIST(path, [flg])** | File existence check and extended information retrieval (_NNNN search, image size, file size) |
| **VRAMFREE([min_free_vram_gb])** | Frees VRAM and RAM (model unload, cache clear, GC) |
| **SLEEP([milliseconds])** | Pauses processing for specified milliseconds (default: 10ms) |
| **IMAGETOBYTEARRAY(image_input, [max_size], [format], [return_format])** | Converts IMAGE/file path to image JSON array |
| **IMAGETOBASE64(image_input, [max_size], [format], [return_format])** | Base64 encodes IMAGE/file path (for Vision API) |
| **GETANYWIDTH([any_data])** | Gets width (pixels) of IMAGE/LATENT type data |
| **GETANYHEIGHT([any_data])** | Gets height (pixels) of IMAGE/LATENT type data |
| **GETANYTYPE([any_data])** | Determines type name of ANY type data |
| **GETANYVALUEINT([any_data])** | Gets integer value from ANY type data |
| **GETANYVALUEFLOAT([any_data])** | Gets float value from ANY type data |
| **GETANYSTRING([any_data])** | Gets string from ANY type data |
| **ISNUMERIC(value)** | Checks if value is numeric |
| **ISDATE(value)** | Checks if value can be parsed as date |
| **ISARRAY(variable_name)** | Checks if variable is array |
| **TYPE(value)** | Returns variable type as string |



---

[← Back to Main Documentation](README.md)
