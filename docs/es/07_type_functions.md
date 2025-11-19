# Referencia de funciones de conversión y determinación de tipos

[← Volver al índice de funciones integradas](00_index.md)

## Resumen

Las funciones de conversión y determinación de tipos convierten el tipo de valores y determinan el tipo de variables.

**Funciones de conversión de tipos**:
- CSTR - Conversión a cadena
- CINT - Conversión a entero
- CDBL - Conversión a número de coma flotante
- FORMAT - Formatear números/fechas en el formato especificado (compatible con VBA)

**Funciones de determinación de tipos**:
- ISNUMERIC - Determinar si es numérico
- ISDATE - Determinar si es una fecha
- ISARRAY - Determinar si es un array

---

## Funciones de conversión de tipos

### CSTR(value)

**Descripción**: Convierte a cadena

**Argumentos**:
- `value` - Cualquier valor

**Valor de retorno**: Cadena

**Ejemplo**:
```vba
text = CSTR(123)
PRINT(text)             ' 123
text = CSTR(3.14)
PRINT(text)             ' 3.14
```

---

### CINT(value)

**Descripción**: Convierte a entero

**Argumentos**:
- `value` - Número o cadena

**Valor de retorno**: Entero (formato float)

**Ejemplo**:
```vba
number = CINT("123")
PRINT(number)            ' 123
number = CINT(45.67)
PRINT(number)            ' 46 (redondeado)
```

---

### CDBL(value)

**Descripción**: Convierte a número de coma flotante

**Argumentos**:
- `value` - Número o cadena

**Valor de retorno**: float

**Ejemplo**:
```vba
number = CDBL("123.45")
PRINT(number)            ' 123.45
number = CDBL(10)
PRINT(number)            ' 10
```

---

### FORMAT(value, [format_string])

**Descripción**: Formatear números/fechas en el formato especificado (compatible con VBA)

**Argumentos**:
- `value` (Any, requerido) - Valor a formatear (número, cadena, fecha)
- `format_string` (str, opcional) - Especificador de formato (por defecto: "")

**Valor de retorno**: str - Cadena formateada

**Formatos admitidos**:

1. **Formato VBA**:
   - `"0"` - Entero (redondeado)
   - `"0.0"` - 1 decimal
   - `"0.00"` - 2 decimales

2. **Formato Python**:
   - `"{:.2f}"` - Sintaxis de formato Python
   - `","` - Separador de miles

3. **Formato de fecha (strftime)**:
   - `"%Y-%m-%d %H:%M:%S"` - Formato de fecha y hora

**Ejemplo**:
```vba
' Formato VBA
result = FORMAT(123.456, "0")       ' "123" (entero)
PRINT("Entero: " & result)
result = FORMAT(123.456, "0.00")    ' "123.46" (2 decimales)
PRINT("2 decimales: " & result)

' Formato Python
result = FORMAT(3.14159, "{:.2f}")  ' "3.14"
PRINT("Pi: " & result)
```

---

## Funciones de determinación de tipos

### ISNUMERIC(value)

**Descripción**: Determina si es numérico

**Argumentos**:
- `value` - Valor a inspeccionar

**Valor de retorno**: 1 (numérico) o 0

**Ejemplo**:
```vba
result = ISNUMERIC("123")
PRINT(result)                  ' 1
result = ISNUMERIC("abc")
PRINT(result)                  ' 0
```

---

### ISDATE(value)

**Descripción**: Determina si es una fecha

**Argumentos**:
- `value` - Valor a inspeccionar

**Valor de retorno**: 1 (fecha) o 0

**Ejemplo**:
```vba
result = ISDATE("2024-01-15")
PRINT(result)                     ' 1
result = ISDATE("hello")
PRINT(result)                     ' 0
```

---

### ISARRAY(variable_name)

**Descripción**: Determina si es un array

**Importante**: Pase el nombre del array como cadena o pase la referencia de variable del array con notación ARR[].

**Argumentos**:
- `variable_name` - Nombre de variable (cadena) o referencia de variable de array

**Valor de retorno**: 1 (array) o 0

**Ejemplo**:
```vba
REDIM ARR, 10
result = ISARRAY(ARR[])
PRINT(result)                ' 1 (referencia de array)
result = ISARRAY("ARR")
PRINT(result)                ' 1 (cadena de nombre de array)
```

---

[← Volver al índice de funciones integradas](00_index.md)
