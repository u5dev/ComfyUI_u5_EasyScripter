# Mathematical Functions Reference

[← Back to Built-in Functions Index](00_index.md)

Complete reference for mathematical functions available in u5 EasyScripter.

## Function List
Provides 24 mathematical functions.

---

## Mathematical Functions
Provides basic mathematical operations.
Note: In examples, infinite repeating decimals (0.9999...) are rounded for convenience.


### ABS(value)
**Description**: Returns the absolute value
**Arguments**: value - A number or value convertible to a number
**Return Value**: Absolute value (float)
**Example**:
```vba
result = ABS(-5.5)
PRINT(result)  ' 5.5
result = ABS(10)
PRINT(result)  ' 10
result = ABS("-3.14")
PRINT(result)  ' 3.14
```

### INT(value)
**Description**: Returns the integer part (rounds down the decimal)
**Arguments**: value - A number
**Return Value**: Integer part (in float format)
**Example**:
```vba
result = INT(5.9)
PRINT(result)  ' 5
result = INT(-2.3)
PRINT(result)  ' -2
result = INT("10.5")
PRINT(result)  ' 10
```

### ROUND(value, [digits])
**Description**: Returns a rounded value
**Arguments**:
- value - A number
- digits - Number of decimal places (default: 0)
**Return Value**: Rounded value
**Example**:
```vba
result = ROUND(3.14159, 2)
PRINT(result)  ' 3.14
result = ROUND(5.5)
PRINT(result)  ' 6
result = ROUND(123.456, 1)
PRINT(result)  ' 123.5
```

### SQRT(value)
**Description**: Returns the square root
**Arguments**: value - A non-negative number
**Return Value**: Square root
**Error**: Negative values cause an error
**Example**:
```vba
result = SQRT(16)
PRINT(result)  ' 4
result = SQRT(2)
PRINT(result)  ' 1.4142135623730951
' result = SQRT(-1) ' Error!
```

### MIN(value1, value2, ...)
**Description**: Returns the minimum value
**Arguments**: Multiple numbers
**Return Value**: Minimum value
**Example**:
```vba
result = MIN(5, 2, 8, 1)
PRINT(result)  ' 1
result = MIN(VAL1, VAL2)
PRINT(result)  ' The smaller of two input values
```

### MAX(value1, value2, ...)
**Description**: Returns the maximum value
**Arguments**: Multiple numbers
**Return Value**: Maximum value
**Example**:
```vba
result = MAX(5, 2, 8, 1)
PRINT(result)  ' 8
result = MAX(0, VAL1)
PRINT(result)  ' Clamp to 0 or higher
```

### SIN(radians)
**Description**: Returns the sine
**Arguments**: radians - Angle in radians
**Return Value**: Value between -1 and 1
**Example**:
```vba
result = SIN(0)
PRINT(result)  ' 0
result = SIN(3.14159/2)
PRINT(result)  ' 0.9999999999991198 (approximately 1)
result = SIN(RADIANS(30))
PRINT(result)  ' 0.49999999999999994 (approximately 0.5)
```

### COS(radians)
**Description**: Returns the cosine
**Arguments**: radians - Angle in radians
**Return Value**: Value between -1 and 1
**Example**:
```vba
result = COS(0)
PRINT(result)  ' 1
result = COS(3.14159)
PRINT(result)  ' -0.9999999999964793 (approximately -1)
result = COS(RADIANS(60))
PRINT(result)  ' 0.5000000000000001 (approximately 0.5)
```

### TAN(radians)
**Description**: Returns the tangent
**Arguments**: radians - Angle in radians
**Return Value**: Tangent value
**Example**:
```vba
result = TAN(0)
PRINT(result)  ' 0
result = TAN(3.14159/4)
PRINT(result)  ' 0.9999986732059836 (approximately 1)
result = TAN(RADIANS(45))
PRINT(result)  ' 0.9999999999999999 (approximately 1)
```

### RADIANS(degrees)
**Description**: Converts degrees to radians
**Arguments**: degrees - Angle in degrees
**Return Value**: Radians
**Example**:
```vba
result = RADIANS(180)
PRINT(result)  ' 3.141592653589793
result = RADIANS(90)
PRINT(result)  ' 1.5707963267948966
result = RADIANS(45)
PRINT(result)  ' 0.7853981633974483
```

### DEGREES(radians)
**Description**: Converts radians to degrees
**Arguments**: radians - Angle in radians
**Return Value**: Degrees
**Example**:
```vba
result = DEGREES(3.14159)
PRINT(result)  ' 179.9998479605043 (approximately 180)
result = DEGREES(1.5708)
PRINT(result)  ' 90.00021045914971 (approximately 90)
result = DEGREES(0.7854)
PRINT(result)  ' 45.00010522957486 (approximately 45)
```

### POW(base, exponent)
**Description**: Calculates power (base^exponent)
**Arguments**:
- base - Base number
- exponent - Exponent
**Return Value**: Result of exponentiation
**Example**:
```vba
result = POW(2, 10)
PRINT(result)  ' 1024
result = POW(5, 3)
PRINT(result)  ' 125
result = POW(10, -2)
PRINT(result)  ' 0.01
```

### LOG(value, [base])
**Description**: Returns the logarithm

**Important**: LOG function returns natural logarithm (base e) by default.

**Arguments**:
- value - A positive number
- base - Logarithm base (default: natural logarithm e)
**Return Value**: Logarithm
**Example**:
```vba
result = LOG(2.718282)
PRINT(result)  ' 1.0000000631063886 (approximately 1)
result = LOG(8, 2)
PRINT(result)  ' 3 (base 2)
result = LOG(1000, 10)
PRINT(result)  ' 2.9999999999999996 (approximately 3)
```

### EXP(value)
**Description**: e (base of natural logarithm) raised to a power
**Arguments**: value - Exponent
**Return Value**: e^value
**Example**:
```vba
result = EXP(0)
PRINT(result)  ' 1
result = EXP(1)
PRINT(result)  ' 2.718281828459045
result = EXP(2)
PRINT(result)  ' 7.38905609893065
```

### AVG(value1, value2, ...)
**Description**: Calculates the average
**Arguments**: Multiple numbers
**Return Value**: Average value
**Example**:
```vba
result = AVG(10, 20, 30)
PRINT(result)  ' 20
result = AVG(1, 2, 3, 4, 5)
PRINT(result)  ' 3
```

### SUM(value1, value2, ...)
**Description**: Calculates the sum
**Arguments**: Multiple numbers
**Return Value**: Sum
**Example**:
```vba
result = SUM(10, 20, 30)
PRINT(result)  ' 60
result = SUM(1, 2, 3, 4, 5)
PRINT(result)  ' 15
```

---

[← Back to Built-in Functions Index](00_index.md)
