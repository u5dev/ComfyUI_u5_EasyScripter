# Referencia de funciones de arrays

[← Volver al índice de funciones integradas](00_index.md)

## Resumen

Las funciones de arrays proporcionan operaciones como inicialización, cambio de tamaño y obtención de límites. En u5 EasyScripter, los arrays usan índices basados en 0 y se acceden con la notación `[]`.

**Número de funciones en esta categoría**: 3

## Lista de funciones

### UBOUND(array)

**Descripción**: Obtiene el índice superior del array

**Argumentos**:
- array - Variable de array

**Valor de retorno**: Índice superior (basado en 0)

**Procesamiento especial**: Función especial procesada por script_engine.py

**Ejemplo**:
```vba
' Obtener el límite superior del array
REDIM ARR, 5
upper = UBOUND(ARR[])
PRINT(upper)   ' 4 (5 elementos de 0 a 4)

' Procesar todo el array en bucle
ARRAY data[], 10, 20, 30, 40, 50
FOR I = 0 TO UBOUND(data[])
    PRINT(data[I])
NEXT
```

---

### ARRAY(variable_name, value1, value2, ...)

**Descripción**: Inicializa array y establece valores

**Argumentos**:
- variable_name - Nombre de variable del array
- value1, value2, ... - Valores iniciales

**Procesamiento especial**: Función especial procesada por script_engine.py

**Ejemplo**:
```vba
' Inicialización de array de cadenas
ARRAY items[], "apple", "banana", "orange"
' items[0] = "apple", items[1] = "banana", items[2] = "orange"

' Acceso a elementos del array
ARRAY colors[], "red", "green", "blue"
favoriteColor = colors[1]
PRINT(favoriteColor)  ' "green"
```

---

### REDIM(array_name, size)

**Descripción**: Cambia el tamaño del array (redefinir)

**Argumentos**:
- array_name - Nombre del array (cadena)
- size - Nuevo tamaño

**Procesamiento especial**: Función especial procesada por script_engine.py

**Nota**: REDIM limpia los elementos existentes del array

**Ejemplo**:
```vba
' Inicialización del array
REDIM ARR, 10        ' Redefinir array ARR con 10 elementos
REDIM DATA, 100      ' Redefinir array DATA con 100 elementos

' Cambio de tamaño dinámico
size = VAL1
PRINT(size)
REDIM MyArray, size  ' Cambiar tamaño según el valor de VAL1
```

---

[← Volver al índice de funciones integradas](00_index.md)
