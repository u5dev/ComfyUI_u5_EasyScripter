# String Functions Reference

[← Back to Built-in Functions Index](00_index.md)

Complete reference for string functions available in u5 EasyScripter.

## Function List
Provides 28 string functions.

---

### LEN(text)
**Description**: Returns the length of a string
**Arguments**: text - A string
**Return Value**: Number of characters
**Example**:
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
**Description**: Extracts specified number of characters from the left
**Arguments**:
- text - A string
- length - Number of characters to extract
**Return Value**: Substring
**Example**:
```vba
result = LEFT("Hello World", 5)
PRINT(result)   ' "Hello"
text1 = "ComfyUI EasyScripter"
result = LEFT(text1, 10)
PRINT(result)   ' "ComfyUI Ea"
result = LEFT("ABC", 10)
PRINT(result)   ' "ABC" (returns entire string if longer than original)
```

### RIGHT(text, length)
**Description**: Extracts specified number of characters from the right
**Arguments**:
- text - A string
- length - Number of characters to extract
**Return Value**: Substring
**Example**:
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
**Description**: Extracts substring from specified position

**Important**: Starting position 0 is treated as 1.

**Arguments**:
- text - A string
- start - Starting position (1-based, 0 is treated as 1)
- length - Number of characters to extract
**Return Value**: Substring
**Example**:
```vba
result = MID("Hello World", 7, 5)
PRINT(result)  ' "World"
result = MID("ABCDEFG", 3, 2)
PRINT(result)  ' "CD"
result = MID("ABCDEFG", 0, 2)
PRINT(result)  ' "AB" (0 is treated as 1)
text1 = "EasyScripter Node"
result = MID(text1, 5, 10)
PRINT(result)  ' "Scripter N"
```

### UPPER(text)
**Description**: Converts to uppercase
**Arguments**: text - A string
**Return Value**: Uppercase string
**Example**:
```vba
result = UPPER("Hello")
PRINT(result)      ' "HELLO"
result = UPPER("abc123XYZ")
PRINT(result)  ' "ABC123XYZ"
```

### LOWER(text)
**Description**: Converts to lowercase
**Arguments**: text - A string
**Return Value**: Lowercase string
**Example**:
```vba
result = LOWER("HELLO")
PRINT(result)      ' "hello"
result = LOWER("ABC123xyz")
PRINT(result)  ' "abc123xyz"
```

### TRIM(text)
**Description**: Removes leading and trailing whitespace
**Arguments**: text - A string
**Return Value**: Trimmed string
**Example**:
```vba
result = TRIM("  Hello  ")
PRINT(result)    ' "Hello"
result = TRIM("   ")
PRINT(result)    ' ""
```

### REPLACE(text, old, new)
**Description**: Replaces strings
**Arguments**:
- text - Target string
- old - Search string
- new - Replacement string
**Return Value**: String after replacement
**Example**:
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
**Description**: Searches for a string (returns position)
**Arguments**:
- start - Starting position for search (default: 1)
- text - Target string
- search - Search string
**Return Value**: Found position (0 = not found)
**Example**:
```vba
result = INSTR("Hello World", "World")
PRINT(result)     ' 7
result = INSTR("ABCABC", "BC")
PRINT(result)     ' 2
result = INSTR(3, "ABCABC", "BC")
PRINT(result)     ' 5 (search from 3rd character)
text1 = "This is a keyword example"
result = INSTR(text1, "keyword")
PRINT(result)     ' 11
```

### INSTRREV(text, search, [start])
**Description**: Searches for a string from the end
**Arguments**:
- text - Target string
- search - Search string
- start - Starting position for search (default: end of string)
**Return Value**: Found position
**Example**:
```vba
result = INSTRREV("Hello World", "o")
PRINT(result)      ' 8 (last 'o')
result = INSTRREV("ABCABC", "BC")
PRINT(result)      ' 5
result = INSTRREV("path/to/file", "/")
PRINT(result)      ' 8 (last slash)
```

### STRREVERSE(text)
**Description**: Reverses a string
**Arguments**: text - A string
**Return Value**: Reversed string
**Example**:
```vba
result = STRREVERSE("Hello")
PRINT(result)    ' "olleH"
result = STRREVERSE("12345")
PRINT(result)    ' "54321"
```

### STRCOMP(text1, text2, [compare])
**Description**: Compares strings
**Arguments**:
- text1 - String 1
- text2 - String 2
- compare - Comparison method (0=binary, 1=text)
**Return Value**: -1/0/1 (less/equal/greater)
**Example**:
```vba
result = STRCOMP("abc", "ABC", 1)
PRINT(result)    ' 0 (case-insensitive)
result = STRCOMP("abc", "ABC", 0)
PRINT(result)    ' 1 (case-sensitive)
result = STRCOMP("a", "b")
PRINT(result)    ' -1
```

### SPACE(number)
**Description**: Generates specified number of spaces
**Arguments**: number - Number of spaces
**Return Value**: Space string
**Example**:
```vba
result = SPACE(5)
PRINT(result)               ' "     "
result = "A" & SPACE(3) & "B"
PRINT(result)   ' "A   B"
```

### STRING(number, character)
**Description**: Repeats a character
**Arguments**:
- number - Number of repetitions
- character - Character to repeat
**Return Value**: Repeated string
**Example**:
```vba
result = STRING(5, "A")
PRINT(result)     ' "AAAAA"
result = STRING(10, "-")
PRINT(result)    ' "----------"
```

### FORMAT(value, format_string)
**Description**: Formats a value
**Arguments**:
- value - Value
- format_string - Format string
**Return Value**: Formatted string
**Supported Formats**:
- `{:.Nf}` - N decimal places
- `{:0Nd}` - N digits with zero padding
- `{:,}` - Comma separator every 3 digits
- `%Y-%m-%d` - Date format
**Example**:
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
**Description**: Splits a string into an array
**Arguments**:
- text - String to split
- delimiter - Delimiter character (default: comma)
**Return Value**: Split array
**Example**:
```vba
' Split comma-separated values
result = SPLIT("apple,banana,cherry")
PRINT(result(0))  ' "apple"
PRINT(result(1))  ' "banana"
' Split space-separated values
result = SPLIT("one two three", " ")
PRINT(result(2))  ' "three"
```

### JOIN(array, [delimiter])
**Description**: Joins an array into a string
**Arguments**:
- array - Array to join
- delimiter - Delimiter character (default: comma)
**Return Value**: Joined string
**Example**:
```vba
ARRAY(arr, "A", "B", "C")
result = JOIN(arr, "-")
PRINT(result)  ' "A-B-C"
result = JOIN(arr)
PRINT(result)  ' "A,B,C"
```

### LTRIM(text)
**Description**: Removes leading whitespace
**Arguments**: text - A string
**Return Value**: Left-trimmed string
**Example**:
```vba
result = LTRIM("  Hello")
PRINT(result)  ' "Hello"
result = LTRIM("  Text  ")
PRINT(result)  ' "Text  "
```

### RTRIM(text)
**Description**: Removes trailing whitespace
**Arguments**: text - A string
**Return Value**: Right-trimmed string
**Example**:
```vba
result = RTRIM("Hello  ")
PRINT(result)  ' "Hello"
result = RTRIM("  Text  ")
PRINT(result)  ' "  Text"
```

### UCASE(text)
**Description**: Converts to uppercase (alias for UPPER)
**Arguments**: text - A string
**Return Value**: Uppercase string
**Example**:
```vba
result = UCASE("hello")
PRINT(result)  ' "HELLO"
```

### LCASE(text)
**Description**: Converts to lowercase (alias for LOWER)
**Arguments**: text - A string
**Return Value**: Lowercase string
**Example**:
```vba
result = LCASE("HELLO")
PRINT(result)  ' "hello"
```

### PROPER(text)
**Description**: Converts to title case (capitalizes first letter of each word)
**Arguments**: text - A string
**Return Value**: Title case string
**Example**:
```vba
result = PROPER("hello world")
PRINT(result)  ' "Hello World"
result = PROPER("easyScripter node")
PRINT(result)  ' "Easyscripter Node"
```

### CHR(code)
**Description**: Converts character code to character
**Arguments**: code - Character code (ASCII range 0-127)
**Return Value**: Corresponding character
**Example**:
```vba
result = CHR(65)
PRINT(result)  ' "A"
result = CHR(97)
PRINT(result)  ' "a"
result = CHR(48)
PRINT(result)  ' "0"
```

### ASC(char)
**Description**: Converts character to character code
**Arguments**: char - A character or string (uses first character)
**Return Value**: Character code (ASCII)
**Example**:
```vba
result = ASC("A")
PRINT(result)  ' 65
result = ASC("Hello")
PRINT(result)  ' 72 (code for "H")
```

### STR(value)
**Description**: Converts number to string
**Arguments**: value - A number
**Return Value**: Stringified number
**Example**:
```vba
result = STR(123)
PRINT(result)  ' "123"
result = STR(3.14)
PRINT(result)  ' "3.14"
```

### URLENCODE(text, [encoding])
**Description**: Performs URL encoding (percent encoding)
**Arguments**:
- text - String to encode
- encoding - Character encoding (default: utf-8)
**Return Value**: URL-encoded string
**Example**:
```vba
' URL encode Japanese text
encoded = URLENCODE("あいうえお")
PRINT(encoded)  ' → %E3%81%82%E3%81%84%E3%81%86%E3%81%88%E3%81%8A
' Encode search query
query = "EasyScripter HTTP 関数"
url = "https://www.google.com/search?q=" & URLENCODE(query)
PRINT(url)
```

### URLDECODE(text, [encoding])
**Description**: Performs URL decoding (decodes percent encoding)
**Arguments**:
- text - String to decode
- encoding - Character encoding (default: utf-8)
**Return Value**: URL-decoded string
**Example**:
```vba
' Decode URL-encoded string
decoded = URLDECODE("%E3%81%82%E3%81%84%E3%81%86%E3%81%88%E3%81%8A")
PRINT(decoded)  ' → あいうえお
' Decode query parameter
param = URLDECODE("EasyScripter+HTTP+%E9%96%A2%E6%95%B0")
PRINT(param)  ' → EasyScripter+HTTP+関数
```

### ESCAPEPATHSTR(path, [replacement])
**Description**: Replaces or removes invalid filename characters
**Arguments**:
- path - String to process
- replacement - Replacement string (omit to delete)
**Return Value**: String with invalid characters processed

**Invalid Characters**: `\`, `/`, `:`, `*`, `?`, `"`, `<`, `>`, `|`

**Reserved Words** (prohibited as entire filename): CON, PRN, AUX, NUL, COM1-9, LPT1-9 (case-insensitive)

**Example**:
```vba
' Replace invalid characters with underscore
safe_name = ESCAPEPATHSTR("file:name*.txt", "_")
PRINT(safe_name)  ' → file_name_.txt

' Delete invalid characters
safe_name = ESCAPEPATHSTR("file:name*.txt")
PRINT(safe_name)  ' → filename.txt

' Process reserved words
safe_name = ESCAPEPATHSTR("CON.txt", "_")
PRINT(safe_name)  ' → _.txt

' Allowed as part of filename
safe_name = ESCAPEPATHSTR("myConFile.txt", "_")
PRINT(safe_name)  ' → myConFile.txt
```

---

[← Back to Built-in Functions Index](00_index.md)
