# Regular Expression Functions Reference

**Languages**: [日本語](../02_builtin_functions/05_regex_functions.md) | [English](05_regex_functions.md)

[← Back to Built-in Functions Index](00_index.md)

## Overview

Regular expression functions enable advanced text processing such as pattern matching, searching, replacement, and extraction. Uses Python's regex engine and provides powerful pattern matching capabilities.

---

## REGEX(pattern, text)

**Description**: Tests pattern match

**Arguments**:
- pattern - Regular expression pattern
- text - Text to search

**Return Value**: 1 (match) or 0

**Example**:
```vba
result = REGEX("\\d+", "abc123def")
PRINT(result)  ' 1 (contains digits)

result = REGEX("^[A-Z]", "Hello")
PRINT(result)  ' 1 (starts with uppercase)

result = REGEX("\\.(jpg|png)$", "a.gif")
PRINT(result)  ' 0 (not jpg or png)
```

---

## REGEXMATCH(pattern, text)

**Description**: Gets first match

**Arguments**:
- pattern - Regular expression pattern
- text - Text to search

**Return Value**: Matched string (empty if no match)

**Example**:
```vba
result = REGEXMATCH("\\d+", "abc123def456")
PRINT(result)  ' "123"

result = REGEXMATCH("[A-Z]+", "helloWORLD")
PRINT(result)  ' "WORLD"
```

---

## REGEXREPLACE(pattern, text, replacement)

**Description**: Replaces pattern

**Arguments**:
- pattern - Regular expression pattern
- text - Target string
- replacement - Replacement string

**Return Value**: String after replacement

**Example**:
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

**Description**: Extracts groups

**Arguments**:
- pattern - Regular expression pattern (with groups)
- text - Target string
- group - Group number (default: 0=entire match)

**Return Value**: Extracted string

**Example**:
```vba
result = REGEXEXTRACT("(\\d{4})-(\\d{2})", "2024-01-15", 1)
PRINT(result)  ' "2024"

result = REGEXEXTRACT("(\\w+)@(\\w+)", "user@domain", 2)
PRINT(result)  ' "domain"
```

---

## REGEXCOUNT(pattern, text)

**Description**: Counts matches

**Arguments**:
- pattern - Regular expression pattern
- text - Target string

**Return Value**: Number of matches

**Example**:
```vba
count = REGEXCOUNT("\\d", "a1b2c3d4")
PRINT(count)  ' 4

count = REGEXCOUNT("\\w+", "hello world")
PRINT(count)  ' 2
```

---

## REGEXMATCHES(pattern, text)

**Description**: Gets all matches as array

**Arguments**:
- pattern - Regular expression pattern
- text - Target string

**Return Value**: List of matches

**Example**:
```vba
matches = REGEXMATCHES("\\d+", "a10b20c30")
PRINT(matches)  ' ["10", "20", "30"]
```

---

## REGEXSPLIT(pattern, text)

**Description**: Splits by pattern

**Arguments**:
- pattern - Separator pattern
- text - Target string

**Return Value**: Split list

**Example**:
```vba
parts = REGEXSPLIT("[,;]", "a,b;c,d")
PRINT(parts)  ' ["a", "b", "c", "d"]
PRINT(parts[0]) ' a

parts = REGEXSPLIT("\\s+", "one  two  three")
PRINT(parts)  ' ["one", "two", "three"]
PRINT(parts[1]) ' two
```

---

[← Back to Built-in Functions Index](00_index.md)
