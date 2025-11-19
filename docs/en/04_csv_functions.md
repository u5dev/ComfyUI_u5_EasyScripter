# CSV Functions Reference

**Languages**: [日本語](../02_builtin_functions/04_csv_functions.md) | [English](04_csv_functions.md)

[← Back to Built-in Functions Index](00_index.md)

## Overview

Functions for manipulating CSV (comma-separated values) strings. Useful for prompt generation and configuration value management.

- CSV element counting and retrieval
- Random selection for prompt generation
- Duplicate removal and difference detection
- Array-CSV conversion

---

## Function List

### CSVCOUNT(csv_text)

**Description**: Counts CSV elements

**Arguments**:
- csv_text - Comma-separated string

**Return Value**: Number of elements (integer)

**Example**:
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

**Description**: Gets element at specified index from CSV string

**Arguments**:
- csv_text - Comma-separated string
- index - Index of element to retrieve (1-based)

**Return Value**: Element at specified position (string). Empty string if out of range

**Example**:
```vba
element = CSVREAD("apple,banana,orange", 2)
PRINT(element)    ' banana
element = CSVREAD("a,b,c,d", 1)
PRINT(element)    ' a
element = CSVREAD("x,y,z", 10)
PRINT(element)    ' (empty string if out of range)
```

---

### CSVUNIQUE(csv_text)

**Description**: Removes duplicates

**Arguments**:
- csv_text - Comma-separated string

**Return Value**: CSV string after duplicate removal

**Example**:
```vba
result = CSVUNIQUE("a,b,a,c,b")
PRINT(result)    ' a,b,c
result = CSVUNIQUE("1,2,3,2,1")
PRINT(result)    ' 1,2,3
```

---

### CSVMERGE(csv1, csv2, ...)

**Description**: Merges multiple CSV strings

**Arguments**:
- csv1, csv2, ... - Multiple CSV strings (variable-length arguments)

**Return Value**: Merged CSV string

**Example**:
```vba
result = CSVMERGE("a,b", "c,d")
PRINT(result)        ' a,b,c,d
result = CSVMERGE("1,2", "3", "4,5")
PRINT(result)        ' 1,2,3,4,5
```

---

### CSVDIFF(array_name, csv1, csv2)

**Description**: Stores difference of two CSV strings (elements existing in only one) in array

**Arguments**:
- array_name - Array variable name to store result
- csv1 - CSV string 1
- csv2 - CSV string 2

**Return Value**: Number of difference elements (integer)

**Example**:
```vba
' Get elements in csv1 but not csv2, and elements in csv2 but not csv1
DIM diff_array
count = CSVDIFF(diff_array, "a,b,c,d", "b,d,e")
PRINT(count)           ' 3
PRINT(diff_array(0))   ' a
PRINT(diff_array(1))   ' c
PRINT(diff_array(2))   ' e
```

---

### PICKCSV(csv_text, [index])

**Description**: Selects CSV element

**Arguments**:
- csv_text - CSV string
- index - Index (default: random selection)

**Return Value**: Selected element (string)

**Example**:
```vba
result = PICKCSV("red,green,blue", 2)
PRINT(result)     ' green
result = PICKCSV("A,B,C,D")
PRINT(result)     ' One of A, B, C, or D
```

---

### RNDCSV(csv_text, [count])

**Description**: Random selection from CSV (can retrieve multiple elements as array)

**Arguments**:
- csv_text - CSV string
- count - Number of elements to select (default returns one string)

**Return Value**:
- count unspecified: One randomly selected element (string)
- count=1: One randomly selected element (string)
- count≥2: List of randomly selected elements
- count >= element count: Complete array maintaining original sort order

**Example**:
```vba
' Select one element (traditional behavior)
style = RNDCSV("realistic,anime,cartoon,abstract")
PRINT(style)
color = RNDCSV("red,blue,green,yellow,purple")
PRINT(color)

' Get multiple elements as array (with duplicates)
DIM selected[3]
selected = RNDCSV("A,B,B,B,C,C,D", 3)
PRINT(selected)  ' e.g. ["B", "B", "D"]

' If count exceeds element count, returns all elements in original order
DIM all[3]
all = RNDCSV("X,Y,Z", 5)
PRINT(all)  ' ["X", "Y", "Z"] (maintains original order)

' Coordination with RANDOMIZE (fixed seed value)
RANDOMIZE(12345)
result = RNDCSV("1,2,3,4,5", 3)
PRINT(result)  ' Reproducible random selection
```

---

### CSVJOIN(array, [delimiter])

**Description**: Joins array to CSV string

**Arguments**:
- array - Array
- delimiter - Delimiter character (default: comma)

**Return Value**: Joined CSV string

**Example**:
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

**Description**: Sorts CSV elements

**Arguments**:
- csv_text - Delimiter-separated text
- delimiter - Delimiter character (default: ",")
- descending - Descending flag (default: False, 0=ascending, 1 or True=descending)

**Return Value**: Sorted CSV string

**Example**:
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

## Practical Examples

### Random Selection for Prompt Generation

```vba
' Random style selection (one element)
style = RNDCSV("photorealistic,anime,oil painting,watercolor")
PRINT(style)
' Random tone selection
tone = RNDCSV("warm,cool,vivid,muted,monochrome")
PRINT(tone)
' Random time selection
time = RNDCSV("morning,noon,sunset,night")
PRINT(time)

PRINT("1girl, " & style & ", " & tone & " tone, " & time)

' Mix multiple styles (array selection)
DIM styles[3]
styles = RNDCSV("realistic,anime,3d,sketch,oil,watercolor,digital", 3)
PRINT(styles)
stylePrompt = CSVJOIN(styles, ", ")
PRINT(stylePrompt)
PRINT("1girl, " & stylePrompt)
```

### List Deduplication and Merging

```vba
' Merge multiple tag lists
tags1 = "girl,outdoor,sunny,smile"
PRINT(tags1)
tags2 = "outdoor,happy,smile,park"
PRINT(tags2)
tags3 = "girl,smile,nature"
PRINT(tags3)

' Merge
allTags = CSVMERGE(tags1, tags2, tags3)
PRINT(allTags)
' "girl,outdoor,sunny,smile,happy,smile,park,girl,smile,nature"

' Remove duplicates
uniqueTags = CSVUNIQUE(allTags)
PRINT(uniqueTags)
' "girl,outdoor,sunny,smile,happy,park,nature"
```

---

[← Back to Built-in Functions Index](00_index.md)
