# Scripting Language Reference

**Languages**: [日本語](../01_syntax_reference.md) | [English](01_syntax_reference.md)

[← Back to Main Documentation](README.md)

---

## 📑 Table of Contents

- [Language Basics](#language-basics)
- [Variables and Assignment](#variables-and-assignment)
- [Reserved Variables (Input/Output Variables)](#reserved-variables-inputoutput-variables)
- [Data Type System](#data-type-system)
- [Array Operations](#array-operations)
- [Operator Reference](#operator-reference)
- [Control Structures](#control-structures)
- [User-Defined Functions (FUNCTION Statement)](#user-defined-functions-function-statement)
- [Comment Syntax](#comment-syntax)

---

## 📖 Language Basics

### Basic Rules

**Case Sensitivity**
- **Variable names**: Case-insensitive (`value` and `VALUE` are the same)
- **Function names**: Case-insensitive (`len` and `LEN` are the same)
- **String comparison**: Case-insensitive (`"Hello" = "HELLO"` is True)

**Important**: Like VBA, variable names, function names, and keywords are case-insensitive.

---

## 📝 Variables and Assignment

Variables can be used without declaration. All variables are internally treated as floating-point numbers or strings.

### Variable Declaration and Types

```vba
' Variables can be used without declaration
x = 10
name = "Alice"

' Explicit declaration with DIM statement (optional)
DIM result
result = x * 2
PRINT(result)  ' 20

' Types are automatically converted
number = "123"    ' String
result = number + 10
PRINT(result)  ' 133
```

### Basic Assignment

```vba
' Numeric assignment
a = 10
b = 3.14
c = VAL1 + VAL2

' String assignment
name = "World"
message = TXT1

' Assignment of calculation results
result = a * b + c
PRINT(result)  ' 31.400000000000002
```

---

## 🎯 Reserved Variables (Input/Output Variables)

Reserved variables automatically available from ComfyUI:

- **`VAL1`**, **`VAL2`**: Numeric inputs (connected from ComfyUI)
- **`TXT1`**, **`TXT2`**: String inputs (connected from ComfyUI)
- **`RETURN1`**, **`RETURN2`**: Script return values (numeric or string)
  - `RETURN` is a backward compatibility alias for RETURN1
- **`RELAY_OUTPUT`**: Controls relay_output output socket (ANY type) value (Tier 3 implementation)
- **`PRINT`**: For debug output (appended via PRINT function)

**Usage Example**:
```vba
' Process input values
result = VAL1 * 2 + VAL2
PRINT(result)  ' 0

' Store in output
RETURN1 = result
RETURN2 = "Calculation result: " & result
```

#### RELAY_OUTPUT Variable

The `RELAY_OUTPUT` variable is a special variable that controls the value of the relay_output output socket (ANY type).

**Features**:
- When a value is assigned to `RELAY_OUTPUT` in the script, that value is output from the relay_output output socket
- When RELAY_OUTPUT is not used, the any_input input is passed through as before

**Use Cases**:
- Pass images (torch.Tensor) loaded with INPUT function to subsequent ComfyUI nodes
- Pass any ANY-type data (latent, mask, etc.) to subsequent nodes

**Usage Example**:
```vba
' Load an image file and pass to subsequent nodes
IMG1 = INPUT("reference.png")
RELAY_OUTPUT = IMG1
```

**Notes**:
- Types assignable to RELAY_OUTPUT variable: ANY type (torch.Tensor, list, dict, str, int, float, etc.)
- No type conversion is performed (assigned value is output as-is)
- Operates independently from RETURN1/RETURN2

---

## 📊 Data Type System

### Basic Data Types

1. **Numeric Type**: Integers and floating-point (internally float)
2. **String Type**: Enclosed in double quotes or single quotes
3. **Array Type**: Only 1-dimensional arrays supported

### String Literal Types

#### Normal String Literals

```vba
' Double quotes
text1 = "Hello, World!"

' VBA-style escape: "" represents "
text2 = "He said ""hello"""  ' → He said "hello"

' Escape sequences
text3 = "Line1\nLine2"  ' → Newline inserted
text4 = "Tab\there"     ' → Tab inserted
```

#### Raw String Literals

Raw string literals are used when you want to minimize escape processing and treat backslashes as-is.

```vba
' Syntax: r"..."
' Only VBA-style escape ("") is processed, other escape sequences are not processed

' Windows path (use backslashes as-is)
path = r"C:\Users\Admin\file.txt"
PRINT(path)  ' C:\Users\Admin\file.txt

' JSON string (using VBA-style "")
json_str = r"{""key"": ""value""}"
PRINT(json_str)  ' {"key": "value"}
result = PYEXEC("json.loads", json_str)
PRINT(result)  ' {"key": "value"}

' String with backslashes
pattern = r"Line1\nLine2"
PRINT(pattern)  ' Line1\nLine2
```

**Raw String Specifications**:
- Written in `r"..."` format
- Only VBA-style escape `""` is processed (`""` → `"`)
- `\` is treated as a regular character (`\n`, `\t`, etc. escapes are not processed)
- `\"` is treated as string terminator (use `""` to include `"` in string)

### Automatic Type Conversion

```vba
' String → Number
a = "42"
b = a + 8
PRINT(b)  ' 50

' Number → String
c = 100
d = "Value is " & c
PRINT(d)  ' Value is 100

' Boolean handling
trueValue = 1
PRINT(trueValue)  ' 1
falseValue = 0
PRINT(falseValue)  ' 0
```

---

## 🔬 Array Operations

Arrays are accessed using `[]` notation.

### Array Declaration and Usage

```vba
' Array declaration (DIM is optional)
DIM numbers[10]

' Value assignment
numbers[0] = 100
numbers[1] = 200
numbers[2] = 300

' Value reference
total = numbers[0] + numbers[1] + numbers[2]
PRINT(total)  ' 600

' Dynamic indexing
FOR i = 0 TO 9
    numbers[i] = i * 10
    PRINT(numbers[i])
NEXT
```

### Array Assignment and Reference

```vba
' Array declaration and initialization
DIM arr[3]

' Array assignment
arr[0] = 100
arr[1] = 200
arr[2] = arr[0] + arr[1]
PRINT(arr[2])  ' 300

' Array reference
RETURN1 = arr[2]
PRINT(RETURN1)  ' 300
```

---

## 🔧 Operator Reference

### Arithmetic Operators

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| + | Addition | `5 + 3` | 8 |
| - | Subtraction | `10 - 3` | 7 |
| * | Multiplication | `4 * 3` | 12 |
| / | Division | `15 / 3` | 5 |
| ^ | Exponentiation | `2 ^ 3` | 8 |
| MOD | Modulus | `10 MOD 3` | 1 |
| \\ | Integer Division | `10 \\ 3` | 3 |

**Examples**:
```vba
' Addition
result = 10 + 5
PRINT(result)  ' 15

' Subtraction
result = 10 - 3
PRINT(result)  ' 7

' Multiplication
result = 4 * 3
PRINT(result)  ' 12

' Division
result = 15 / 3
PRINT(result)  ' 5

' Exponentiation
result = 2 ^ 3
PRINT(result)  ' 8

' Modulus (MOD)
result = 10 MOD 3
PRINT(result)  ' 1

' Compound operations (precedence with parentheses)
result = (10 + 5) * 2
PRINT(result)  ' 30
result = 10 + 5 * 2
PRINT(result)  ' 20
```

### Comparison Operators

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| = | Equal | `5 = 5` | 1 (True) |
| <> | Not equal | `5 <> 3` | 1 (True) |
| != | Not equal (C-style) | `5 != 3` | 1 (True) |
| < | Less than | `3 < 5` | 1 (True) |
| > | Greater than | `5 > 3` | 1 (True) |
| <= | Less than or equal | `3 <= 3` | 1 (True) |
| >= | Greater than or equal | `5 >= 5` | 1 (True) |

**Note**: String comparisons are case-insensitive like VBA. For example: `"Hello" = "HELLO"` is True.

**Examples**:
```vba
' Equal
result = 5 = 5
PRINT(result)  ' 1
result = 5 = 3
PRINT(result)  ' 0

' Not equal (<> or != can be used)
result = 5 <> 3
PRINT(result)  ' 1
result = 5 != 3
PRINT(result)  ' 1 (C-style also available)
result = 5 <> 5
PRINT(result)  ' 0

' Greater than
result = 10 > 5
PRINT(result)  ' 1

' Less than
result = 3 < 10
PRINT(result)  ' 1

' Greater than or equal
result = 5 >= 5
PRINT(result)  ' 1
result = 5 >= 6
PRINT(result)  ' 0

' Less than or equal
result = 3 <= 10
PRINT(result)  ' 1
```

### Logical Operators

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| AND | Logical AND | `(5>3) AND (2<4)` | 1 (True) |
| OR | Logical OR | `(5<3) OR (2<4)` | 1 (True) |
| NOT | Logical NOT | `NOT (5>3)` | 0 (False) |

**Examples**:
```vba
' AND operation
result = (5 > 3) AND (10 > 5)
PRINT(result)  ' 1
result = (5 > 3) AND (2 > 5)
PRINT(result)  ' 0

' OR operation
result = (5 > 3) OR (2 > 5)
PRINT(result)  ' 1
result = (2 > 5) OR (1 > 3)
PRINT(result)  ' 0

' NOT operation
result = NOT (5 > 3)
PRINT(result)  ' 0
result = NOT (2 > 5)
PRINT(result)  ' 1
```

### String Operators

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| & | Concatenation | `"Hello" & " " & "World"` | "Hello World" |

**Examples**:
```vba
' String concatenation (& operator)
greeting = "Hello" & " " & "World"
PRINT(greeting)  ' Hello World
result = "Value is " & VAL1 & " ."
PRINT(result)
```

---

## 🎮 Control Structures

### IF Statement (Conditional Branching)

#### Basic Form: IF Statement (Block Form)

```vba
IF VAL1 > 50 THEN
    RETURN1 = "Large"
END IF
```

#### Multi-line IF Statement

```vba
IF VAL1 > 100 THEN
    RETURN1 = "Very large"
    PRINT("Value: " & VAL1)
ELSE
    RETURN1 = "Standard"
END IF
```

#### Multi-branch with ELSEIF

```vba
IF VAL1 > 100 THEN
    grade = "A"
ELSEIF VAL1 > 80 THEN
    grade = "B"
ELSEIF VAL1 > 60 THEN
    grade = "C"
ELSE
    grade = "D"
END IF
PRINT(grade)
```

#### Nested IF Statements

```vba
IF TXT1 <> "" THEN
    IF LEN(TXT1) > 10 THEN
        IF INSTR(TXT1, "keyword") > 0 THEN
            RETURN1 = "Keyword found (long text)"
        ELSE
            RETURN1 = "Long text (no keyword)"
        END IF
    ELSE
        RETURN1 = "Short text"
    END IF
ELSE
    RETURN1 = "No input"
END IF
```

### FOR...NEXT Statement (Count Loop)

#### Basic Form

```vba
' Repeat from 1 to 10
FOR i = 1 TO 10
    PRINT("Count: " & i)
NEXT
```

#### With STEP

```vba
' Increment by 2 (even numbers only)
sum = 0
FOR i = 0 TO 20 STEP 2
    sum = sum + i
    PRINT(sum)
NEXT

' Reverse order (countdown)
FOR i = 10 TO 1 STEP -1
    PRINT(i & "...")
NEXT
PRINT("Launch!")
```

#### Nested Loops

```vba
' Create multiplication table
FOR i = 1 TO 9
    row = ""
    FOR j = 1 TO 9
        row = row & (i * j) & " "
    NEXT
    PRINT(row)
NEXT
```

### WHILE...WEND Statement (Conditional Loop)

#### Basic Form

```vba
count = 0
WHILE count < 10
    count = count + 1
    PRINT("Count: " & count)
WEND
```

#### Conditional Loop

```vba
' Find specific character in input string
position = 1
found = 0
WHILE position <= LEN(TXT1) AND found = 0
    IF MID(TXT1, position, 1) = "X" THEN
        found = position
    END IF
    position = position + 1
WEND

IF found > 0 THEN
    RETURN1 = "X is at position " & found
    PRINT(RETURN1)
ELSE
    RETURN1 = "X not found"
    PRINT(RETURN1)
END IF
```

### SELECT CASE Statement (Multi-branch)

VBA-style SELECT CASE statement allows concise description of multiple conditional branches. The first matching Case clause is executed, and subsequent evaluation is not performed.

#### Basic Form

```vba
SELECT CASE VAL1
    CASE 1
        RETURN1 = "One"
    CASE 2
        RETURN1 = "Two"
    CASE 3
        RETURN1 = "Three"
    CASE ELSE
        RETURN1 = "Other"
END SELECT
```

#### Multiple Value Case Statement

```vba
' Specify multiple values separated by commas
value = 5
SELECT CASE value
    CASE 1, 3, 5, 7, 9
        result = "Odd"
    CASE 2, 4, 6, 8, 10
        result = "Even"
    CASE ELSE
        result = "Out of range"
END SELECT
PRINT(result)  ' Odd
```

#### Range Case Statement

```vba
' Specify range with TO operator
score = 75
SELECT CASE score
    CASE 0 TO 59
        grade = "F"
    CASE 60 TO 69
        grade = "D"
    CASE 70 TO 79
        grade = "C"
    CASE 80 TO 89
        grade = "B"
    CASE 90 TO 100
        grade = "A"
    CASE ELSE
        grade = "Invalid"
END SELECT
PRINT(grade)  ' C
```

#### Multiple Values with Comma Separation (Weekday Example)

```vba
dayNum = WEEKDAY(NOW())
SELECT CASE dayNum
    CASE 1, 7
        dayType = "Weekend"
    CASE 2, 3, 4, 5, 6
        dayType = "Weekday"
END SELECT
PRINT(dayType)
```

---

## 🔨 User-Defined Functions (FUNCTION Statement)

u5 EasyScripter allows you to create user-defined functions using VBA-style Function statements. Functions provide independent local scope, preventing interference with global variables.

### Basic Function Definition

```vba
' Function to add two numbers
FUNCTION add(a, b)
    add = a + b  ' Set return value by assigning to function name
END FUNCTION

' Function call
result = add(5, 3)
PRINT(result)  ' 8
```

### Function to Return Maximum of Two Numbers

```vba
' Function to return the larger of two numbers
FUNCTION maxValue(a, b)
    IF a > b THEN
        maxValue = a
    ELSE
        maxValue = b
    END IF
END FUNCTION

' Usage example
result = maxValue(10, 20)
PRINT(result)  ' 20
```

### Function with Multiple Arguments

```vba
' Function to decorate prompt
FUNCTION decoratePrompt(prompt, quality, style)
    decorated = prompt

    IF quality = "high" THEN
        decorated = decorated & ", masterpiece, best quality"
    END IF

    IF style <> "" THEN
        decorated = decorated & ", " & style & " style"
    END IF

    decoratePrompt = decorated
END FUNCTION

' Usage example
finalPrompt = decoratePrompt("portrait", "high", "anime")
PRINT(finalPrompt)  ' portrait, masterpiece, best quality, anime style
```

### Recursive Function

```vba
' Recursive function to calculate factorial
FUNCTION factorial(n)
    IF n <= 1 THEN
        factorial = 1
    ELSE
        factorial = n * factorial(n - 1)
    END IF
END FUNCTION

result = factorial(5)
PRINT(result)  ' 120
```

---

## 💬 Comment Syntax

Comments start with a single quote (`'`).

```vba
' This is a comment
x = 10  ' End-of-line comments are also possible
PRINT(x)  ' 10

' Multi-line comments
' Place single quote at the beginning of each line
```

---

## 📚 Next Steps

- [Built-in Function Reference](00_index.md) - Details of 120+ functions
- [Main Documentation](README.md) - Overall overview and installation

---

**Last Updated**: October 3, 2024

---

[← Back to Main Documentation](README.md)
