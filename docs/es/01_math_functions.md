# Referencia de funciones matemáticas

[← Volver al índice de funciones integradas](00_index.md)

Referencia completa de las funciones matemáticas que se pueden usar en u5 EasyScripter.

## Lista de funciones
Se proporcionan 24 funciones matemáticas.

---

## Funciones matemáticas
Proporcionan funcionalidad matemática básica.
En los ejemplos, los números infinitos cíclicos (0.9999...) se redondean por conveniencia.

### ABS(value)
**Descripción**: Devuelve el valor absoluto
**Argumentos**: value - Número o valor convertible a número
**Valor de retorno**: Valor absoluto (float)
**Ejemplo**:
```vba
result = ABS(-5.5)
PRINT(result)  ' 5.5
result = ABS(10)
PRINT(result)  ' 10
```

### INT(value)
**Descripción**: Devuelve la parte entera (trunca decimales)
**Argumentos**: value - Número
**Valor de retorno**: Parte entera (formato float)
**Ejemplo**:
```vba
result = INT(5.9)
PRINT(result)  ' 5
result = INT(-2.3)
PRINT(result)  ' -2
```

### ROUND(value, [digits])
**Descripción**: Devuelve el valor redondeado
**Argumentos**:
- value - Número
- digits - Número de decimales (omitido:0)
**Valor de retorno**: Valor redondeado
**Ejemplo**:
```vba
result = ROUND(3.14159, 2)
PRINT(result)  ' 3.14
result = ROUND(5.5)
PRINT(result)  ' 6
```

### SQRT(value)
**Descripción**: Devuelve la raíz cuadrada
**Argumentos**: value - Número ≥ 0
**Valor de retorno**: Raíz cuadrada
**Error**: Error con valores negativos
**Ejemplo**:
```vba
result = SQRT(16)
PRINT(result)  ' 4
result = SQRT(2)
PRINT(result)  ' 1.4142135623730951
```

### MIN(value1, value2, ...)
**Descripción**: Devuelve el valor mínimo
**Argumentos**: Múltiples números
**Valor de retorno**: Valor mínimo
**Ejemplo**:
```vba
result = MIN(5, 2, 8, 1)
PRINT(result)  ' 1
```

### MAX(value1, value2, ...)
**Descripción**: Devuelve el valor máximo
**Argumentos**: Múltiples números
**Valor de retorno**: Valor máximo
**Ejemplo**:
```vba
result = MAX(5, 2, 8, 1)
PRINT(result)  ' 8
```

### SIN(radians)
**Descripción**: Devuelve el seno
**Argumentos**: radians - Ángulo en radianes
**Valor de retorno**: Valor entre -1 y 1
**Ejemplo**:
```vba
result = SIN(0)
PRINT(result)  ' 0
result = SIN(RADIANS(30))
PRINT(result)  ' 0.5
```

### COS(radians)
**Descripción**: Devuelve el coseno
**Argumentos**: radians - Ángulo en radianes
**Valor de retorno**: Valor entre -1 y 1
**Ejemplo**:
```vba
result = COS(0)
PRINT(result)  ' 1
result = COS(RADIANS(60))
PRINT(result)  ' 0.5
```

### TAN(radians)
**Descripción**: Devuelve la tangente
**Argumentos**: radians - Ángulo en radianes
**Valor de retorno**: Valor tangente
**Ejemplo**:
```vba
result = TAN(0)
PRINT(result)  ' 0
result = TAN(RADIANS(45))
PRINT(result)  ' 1
```

### RADIANS(degrees)
**Descripción**: Convierte grados a radianes
**Argumentos**: degrees - Ángulo en grados
**Valor de retorno**: Radianes
**Ejemplo**:
```vba
result = RADIANS(180)
PRINT(result)  ' 3.141592653589793
result = RADIANS(90)
PRINT(result)  ' 1.5707963267948966
```

### DEGREES(radians)
**Descripción**: Convierte radianes a grados
**Argumentos**: radians - Ángulo en radianes
**Valor de retorno**: Grados
**Ejemplo**:
```vba
result = DEGREES(3.14159)
PRINT(result)  ' 180
```

### POW(base, exponent)
**Descripción**: Calcula potencia (base^exponent)
**Argumentos**:
- base - Base
- exponent - Exponente
**Valor de retorno**: Resultado de la potencia
**Ejemplo**:
```vba
result = POW(2, 10)
PRINT(result)  ' 1024
result = POW(5, 3)
PRINT(result)  ' 125
```

### LOG(value, [base])
**Descripción**: Devuelve el logaritmo

**Importante**: LOG devuelve por defecto el logaritmo natural (base e).

**Argumentos**:
- value - Número positivo
- base - Base (omitido: logaritmo natural e)
**Valor de retorno**: Logaritmo
**Ejemplo**:
```vba
result = LOG(2.718282)
PRINT(result)  ' 1
result = LOG(8, 2)
PRINT(result)  ' 3 (base 2)
```

### EXP(value)
**Descripción**: Potencia de e (base del logaritmo natural)
**Argumentos**: value - Exponente
**Valor de retorno**: e^value
**Ejemplo**:
```vba
result = EXP(0)
PRINT(result)  ' 1
result = EXP(1)
PRINT(result)  ' 2.718281828459045
```

### AVG(value1, value2, ...)
**Descripción**: Calcula el promedio
**Argumentos**: Múltiples números
**Valor de retorno**: Promedio
**Ejemplo**:
```vba
result = AVG(10, 20, 30)
PRINT(result)  ' 20
```

### SUM(value1, value2, ...)
**Descripción**: Calcula la suma
**Argumentos**: Múltiples números
**Valor de retorno**: Suma total
**Ejemplo**:
```vba
result = SUM(10, 20, 30)
PRINT(result)  ' 60
```

---

[← Volver al índice de funciones integradas](00_index.md)
