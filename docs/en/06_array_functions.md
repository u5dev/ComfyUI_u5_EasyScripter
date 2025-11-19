# Array Functions Reference

**Languages**: [日本語](../02_builtin_functions/06_array_functions.md) | [English](06_array_functions.md)

[← Back to Built-in Functions Index](00_index.md)

## Overview

Array functions provide operations for array initialization, resizing, and boundary retrieval. In u5 EasyScripter, arrays use 0-based indexing and are accessed using `[]` notation.

**Number of functions in this category**: 3

## Function List

### UBOUND(array)

**Description**: Gets upper bound index of array

**Arguments**:
- array - Array variable

**Return Value**: Upper bound index (0-based)

**Special Processing**: Special function processed in script_engine.py

**Example**:
```vba
' Get array upper bound
REDIM ARR, 5
upper = UBOUND(ARR[])
PRINT(upper)   ' 4 (5 elements from 0 to 4)

' Process entire array with loop
ARRAY data[], 10, 20, 30, 40, 50
FOR I = 0 TO UBOUND(data[])
    PRINT(data[I])
NEXT

' Check array size
ARRAY items[], "apple", "banana", "orange"
size = UBOUND(items[]) + 1
PRINT(size)  ' 3 elements
```

---

### ARRAY(variable_name, value1, value2, ...)

**Description**: Initializes array and sets values

**Arguments**:
- variable_name - Array variable name
- value1, value2, ... - Initial values

**Special Processing**: Special function processed in script_engine.py

**Example**:
```vba
' Initialize string array
ARRAY items[], "apple", "banana", "orange"
' items[0] = "apple", items[1] = "banana", items[2] = "orange"

' Initialize numeric array
ARRAY numbers[], 10, 20, 30, 40, 50
' numbers[0] = 10, numbers[1] = 20, ...

' Access array elements
ARRAY colors[], "red", "green", "blue"
favoriteColor = colors[1]
PRINT(favoriteColor)  ' "green"

' Process array with loop
ARRAY scores[], 85, 92, 78, 95
total = 0
FOR I = 0 TO UBOUND(scores[])
    total = total + scores[I]
NEXT
average = total / (UBOUND(scores[]) + 1)
PRINT(average)
```

---

### REDIM(array_name, size)

**Description**: Resizes array (redimension)

**Arguments**:
- array_name - Array name (string)
- size - New size

**Special Processing**: Special function processed in script_engine.py

**Note**: REDIM clears existing array elements

**Example**:
```vba
' Initialize array
REDIM ARR, 10        ' Redimension ARR array with 10 elements
REDIM DATA, 100      ' Redimension DATA array with 100 elements

' Dynamic resizing
size = VAL1
PRINT(size)
REDIM MyArray, size  ' Resize according to VAL1 value

' Dynamic data processing with array
itemCount = CSVCOUNT(TXT1)
PRINT(itemCount)
REDIM items, itemCount
FOR I = 0 TO itemCount - 1
    items[I] = CSVREAD(TXT1, I + 1)
NEXT
```

## Array Usage Examples

### Basic Array Operations
```vba
' Create array and set values
ARRAY names[], "Alice", "Bob", "Charlie", "David"

' Check array size
count = UBOUND(names[]) + 1
PRINT(count)
PRINT("Array element count: " & count)  ' "Array element count: 4"

' Process array sequentially
FOR I = 0 TO UBOUND(names[])
    PRINT("Name[" & I & "]: " & names[I])
NEXT
```

### Dynamic Array Resizing
```vba
' Create array with initial size
REDIM buffer, 5
FOR I = 0 TO 4
    buffer[I] = I * 10
NEXT

' Resize as needed
newSize = 10
PRINT(newSize)
REDIM buffer, newSize
' Note: REDIM clears existing data
```

### Array and CSV Combination
```vba
' Convert CSV data to array
csvData = "apple,banana,orange,grape,melon"
PRINT(csvData)
itemCount = CSVCOUNT(csvData)
PRINT(itemCount)
REDIM fruits, itemCount

FOR I = 0 TO itemCount - 1
    fruits[I] = CSVREAD(csvData, I + 1)
NEXT

' Check array contents
FOR I = 0 TO UBOUND(fruits[])
    PRINT("Fruit[" & I & "]: " & fruits[I])
NEXT
```

### Array Aggregation Processing
```vba
' Initialize numeric array
ARRAY scores[], 85, 92, 78, 95, 88, 91

' Calculate total
total = 0
FOR I = 0 TO UBOUND(scores[])
    total = total + scores[I]
NEXT
PRINT(total)

' Calculate average
count = UBOUND(scores[]) + 1
PRINT(count)
average = total / count
PRINT(average)

' Find maximum value
maxScore = scores[0]
PRINT(maxScore)
FOR I = 1 TO UBOUND(scores[])
    IF scores[I] > maxScore THEN
        maxScore = scores[I]
        PRINT(maxScore)
    END IF
NEXT

PRINT("Total: " & total)
PRINT("Average: " & ROUND(average, 2))
PRINT("Highest: " & maxScore)
```

---

[← Back to Built-in Functions Index](00_index.md)
