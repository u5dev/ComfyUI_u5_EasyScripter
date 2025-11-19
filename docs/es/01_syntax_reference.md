# Referencia del Lenguaje de Scripts

[← Volver al documento principal](README.md)

---

## 📑 Índice

- [Fundamentos de la especificación del lenguaje](#fundamentos-de-la-especificación-del-lenguaje)
- [Variables y asignación](#variables-y-asignación)
- [Variables reservadas (variables de entrada/salida)](#variables-reservadas-variables-de-entradasalida)
- [Sistema de tipos de datos](#sistema-de-tipos-de-datos)
- [Operaciones con arrays](#operaciones-con-arrays)
- [Referencia de operadores](#referencia-de-operadores)
- [Estructuras de control](#estructuras-de-control)
- [Funciones definidas por el usuario (sentencia FUNCTION)](#funciones-definidas-por-el-usuario-sentencia-function)
- [Notación de comentarios](#notación-de-comentarios)

---

## 📖 Fundamentos de la especificación del lenguaje

### Reglas básicas

**Distinción entre mayúsculas y minúsculas**
- **Nombres de variables**: Sin distinción (`value` y `VALUE` son iguales)
- **Nombres de funciones**: Sin distinción (`len` y `LEN` son iguales)
- **Comparación de cadenas**: Sin distinción (`"Hello" = "HELLO"` es True)

**Importante**: Al igual que en VBA, los nombres de variables, funciones y palabras clave no distinguen entre mayúsculas y minúsculas.

---

## 📝 Variables y asignación

Las variables se pueden usar sin declaración. Todas las variables se tratan internamente como números de coma flotante o cadenas.

### Declaración y tipos de variables

```vba
' Las variables se pueden usar sin declaración
x = 10
name = "Alice"

' Declaración explícita con la sentencia DIM (opcional)
DIM result
result = x * 2
PRINT(result)  ' 20

' Los tipos se convierten automáticamente
number = "123"    ' Cadena
result = number + 10
PRINT(result)  ' 133
```

### Asignación básica

```vba
' Asignación de números
a = 10
b = 3.14
c = VAL1 + VAL2

' Asignación de cadenas
name = "World"
message = TXT1

' Asignación de resultados de cálculo
result = a * b + c
PRINT(result)  ' 31.400000000000002
```

---

## 🎯 Variables reservadas (variables de entrada/salida)

Variables reservadas disponibles automáticamente desde ComfyUI:

- **`VAL1`**, **`VAL2`**: Entrada numérica (conectada desde ComfyUI)
- **`TXT1`**, **`TXT2`**: Entrada de cadena (conectada desde ComfyUI)
- **`RETURN1`**, **`RETURN2`**: Valor de retorno del script (número o cadena)
  - `RETURN` es un alias de retrocompatibilidad de RETURN1
- **`RELAY_OUTPUT`**: Controla el valor del socket de salida relay_output (tipo ANY) (implementación Tier 3)
- **`PRINT`**: Para salida de depuración (añadido por la función PRINT)

**Ejemplo de uso**:
```vba
' Procesar valores de entrada
result = VAL1 * 2 + VAL2
PRINT(result)  ' 0

' Almacenar en salida
RETURN1 = result
RETURN2 = "Resultado del cálculo: " & result
```

#### Variable RELAY_OUTPUT

La variable `RELAY_OUTPUT` es una variable especial que controla el valor del socket de salida relay_output (tipo ANY).

**Funcionalidad**:
- Al asignar un valor a `RELAY_OUTPUT` dentro del script, ese valor se emite desde el socket de salida relay_output
- Cuando no se usa RELAY_OUTPUT, la entrada any_input se pasa tal cual (comportamiento tradicional)

**Usos**:
- Pasar imágenes (torch.Tensor) cargadas con la función INPUT a nodos posteriores de ComfyUI
- Pasar cualquier dato de tipo ANY (latent, mask, etc.) a nodos posteriores

**Ejemplo de uso**:
```vba
' Cargar archivo de imagen y pasarlo al nodo posterior
IMG1 = INPUT("reference.png")
RELAY_OUTPUT = IMG1
```

**Notas**:
- Tipos que se pueden asignar a la variable RELAY_OUTPUT: tipo ANY (torch.Tensor, list, dict, str, int, float, etc.)
- No se realiza conversión de tipo (el valor asignado se emite tal cual)
- Opera independientemente de RETURN1/RETURN2

---

## 📊 Sistema de tipos de datos

### Tipos de datos básicos

1. **Tipo numérico**: Enteros y coma flotante (internamente float)
2. **Tipo cadena**: Entre comillas dobles o simples
3. **Tipo array**: Solo se admiten arrays unidimensionales

### Tipos de literales de cadena

#### Literales de cadena normales

```vba
' Comillas dobles
text1 = "Hello, World!"

' Escape estilo VBA: "" representa "
text2 = "He said ""hello"""  ' → He said "hello"

' Secuencias de escape
text3 = "Line1\nLine2"  ' → Se inserta salto de línea
text4 = "Tab\there"     ' → Se inserta tabulación
```

#### Literales de cadena raw

Los literales de cadena raw se usan cuando se desea minimizar el procesamiento de escape y tratar las barras invertidas tal cual.

```vba
' Sintaxis: r"..."
' Solo se procesa el escape estilo VBA (""), no se procesan otras secuencias de escape

' Rutas de Windows (usar barras invertidas tal cual)
path = r"C:\Users\Admin\file.txt"
PRINT(path)  ' C:\Users\Admin\file.txt

' Cadena JSON (usar "" estilo VBA)
json_str = r"{""key"": ""value""}"
PRINT(json_str)  ' {"key": "value"}
result = PYEXEC("json.loads", json_str)
PRINT(result)  ' {"key": "value"}

' Cadena que contiene barras invertidas
pattern = r"Line1\nLine2"
PRINT(pattern)  ' Line1\nLine2
```

**Especificación de cadenas raw**:
- Se escribe en formato `r"..."`
- Solo se procesa el escape estilo VBA `""` (`""` → `"`)
- `\` se trata como un carácter normal (no se procesan escapes como `\n`, `\t`, etc.)
- `\"` se trata como el final de la cadena (para incluir `"` dentro de la cadena, use `""`)

### Conversión automática de tipos

```vba
' Cadena → número
a = "42"
b = a + 8
PRINT(b)  ' 50

' Número → cadena
c = 100
d = "El valor es " & c
PRINT(d)  ' El valor es 100

' Manejo de valores booleanos
trueValue = 1
PRINT(trueValue)  ' 1
falseValue = 0
PRINT(falseValue)  ' 0
```

---

## 🔬 Operaciones con arrays

Los arrays se acceden con la notación `[]`.

### Declaración y uso de arrays

```vba
' Declaración de array (DIM es opcional)
DIM numbers[10]

' Asignación de valores
numbers[0] = 100
numbers[1] = 200
numbers[2] = 300

' Referencia de valores
total = numbers[0] + numbers[1] + numbers[2]
PRINT(total)  ' 600

' Índice dinámico
FOR i = 0 TO 9
    numbers[i] = i * 10
    PRINT(numbers[i])
NEXT
```

### Asignación y referencia en arrays

```vba
' Declaración e inicialización de array
DIM arr[3]

' Asignación a array
arr[0] = 100
arr[1] = 200
arr[2] = arr[0] + arr[1]
PRINT(arr[2])  ' 300

' Referencia de array
RETURN1 = arr[2]
PRINT(RETURN1)  ' 300
```

---

## 🔧 Referencia de operadores

### Operadores aritméticos

| Operador | Descripción | Ejemplo | Resultado |
|--------|------|-----|------|
| + | Suma | `5 + 3` | 8 |
| - | Resta | `10 - 3` | 7 |
| * | Multiplicación | `4 * 3` | 12 |
| / | División | `15 / 3` | 5 |
| ^ | Potencia | `2 ^ 3` | 8 |
| MOD | Módulo | `10 MOD 3` | 1 |
| \\ | División entera | `10 \\ 3` | 3 |

**Ejemplo**:
```vba
' Suma
result = 10 + 5
PRINT(result)  ' 15

' Resta
result = 10 - 3
PRINT(result)  ' 7

' Multiplicación
result = 4 * 3
PRINT(result)  ' 12

' División
result = 15 / 3
PRINT(result)  ' 5

' Potencia
result = 2 ^ 3
PRINT(result)  ' 8

' Módulo (MOD)
result = 10 MOD 3
PRINT(result)  ' 1

' Operación compuesta (prioridad con paréntesis)
result = (10 + 5) * 2
PRINT(result)  ' 30
result = 10 + 5 * 2
PRINT(result)  ' 20
```

### Operadores de comparación

| Operador | Descripción | Ejemplo | Resultado |
|--------|------|-----|------|
| = | Igual | `5 = 5` | 1 (True) |
| <> | Distinto | `5 <> 3` | 1 (True) |
| != | Distinto (estilo C) | `5 != 3` | 1 (True) |
| < | Menor que | `3 < 5` | 1 (True) |
| > | Mayor que | `5 > 3` | 1 (True) |
| <= | Menor o igual | `3 <= 3` | 1 (True) |
| >= | Mayor o igual | `5 >= 5` | 1 (True) |

**Nota**: En la comparación de cadenas, al igual que en VBA, no se distingue entre mayúsculas y minúsculas. Por ejemplo: `"Hello" = "HELLO"` es True.

**Ejemplo**:
```vba
' Igual
result = 5 = 5
PRINT(result)  ' 1
result = 5 = 3
PRINT(result)  ' 0

' Distinto (se puede usar <> o !=)
result = 5 <> 3
PRINT(result)  ' 1
result = 5 != 3
PRINT(result)  ' 1 (también se puede usar estilo C)
result = 5 <> 5
PRINT(result)  ' 0

' Mayor que
result = 10 > 5
PRINT(result)  ' 1

' Menor que
result = 3 < 10
PRINT(result)  ' 1

' Mayor o igual
result = 5 >= 5
PRINT(result)  ' 1
result = 5 >= 6
PRINT(result)  ' 0

' Menor o igual
result = 3 <= 10
PRINT(result)  ' 1
```

### Operadores lógicos

| Operador | Descripción | Ejemplo | Resultado |
|--------|------|-----|------|
| AND | Y lógico | `(5>3) AND (2<4)` | 1 (True) |
| OR | O lógico | `(5<3) OR (2<4)` | 1 (True) |
| NOT | Negación lógica | `NOT (5>3)` | 0 (False) |

**Ejemplo**:
```vba
' Operación AND
result = (5 > 3) AND (10 > 5)
PRINT(result)  ' 1
result = (5 > 3) AND (2 > 5)
PRINT(result)  ' 0

' Operación OR
result = (5 > 3) OR (2 > 5)
PRINT(result)  ' 1
result = (2 > 5) OR (1 > 3)
PRINT(result)  ' 0

' Operación NOT
result = NOT (5 > 3)
PRINT(result)  ' 0
result = NOT (2 > 5)
PRINT(result)  ' 1
```

### Operadores de cadenas

| Operador | Descripción | Ejemplo | Resultado |
|--------|------|-----|------|
| & | Concatenación | `"Hello" & " " & "World"` | "Hello World" |

**Ejemplo**:
```vba
' Concatenación de cadenas (operador &)
greeting = "Hello" & " " & "World"
PRINT(greeting)  ' Hello World
result = "El valor es " & VAL1 & " ."
PRINT(result)
```

---

## 🎮 Estructuras de control

### Sentencia IF (bifurcación condicional)

#### Forma básica: Sentencia IF (formato de bloque)

```vba
IF VAL1 > 50 THEN
    RETURN1 = "grande"
END IF
```

#### Sentencia IF de múltiples líneas

```vba
IF VAL1 > 100 THEN
    RETURN1 = "muy grande"
    PRINT("Valor: " & VAL1)
ELSE
    RETURN1 = "estándar"
END IF
```

#### Ramificación múltiple con ELSEIF

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

#### Sentencias IF anidadas

```vba
IF TXT1 <> "" THEN
    IF LEN(TXT1) > 10 THEN
        IF INSTR(TXT1, "keyword") > 0 THEN
            RETURN1 = "Palabra clave encontrada (texto largo)"
        ELSE
            RETURN1 = "Texto largo (sin palabra clave)"
        END IF
    ELSE
        RETURN1 = "Texto corto"
    END IF
ELSE
    RETURN1 = "Sin entrada"
END IF
```

### Sentencia FOR...NEXT (bucle con número de iteraciones especificado)

#### Forma básica

```vba
' Repetir de 1 a 10
FOR i = 1 TO 10
    PRINT("Cuenta: " & i)
NEXT
```

#### Especificación de STEP

```vba
' Incremento de 2 (solo pares)
sum = 0
FOR i = 0 TO 20 STEP 2
    sum = sum + i
    PRINT(sum)
NEXT

' Orden inverso (cuenta regresiva)
FOR i = 10 TO 1 STEP -1
    PRINT(i & "...")
NEXT
PRINT("¡Despegue!")
```

#### Bucles anidados

```vba
' Crear tabla de multiplicar
FOR i = 1 TO 9
    row = ""
    FOR j = 1 TO 9
        row = row & (i * j) & " "
    NEXT
    PRINT(row)
NEXT
```

### Sentencia WHILE...WEND (bucle condicional)

#### Forma básica

```vba
count = 0
WHILE count < 10
    count = count + 1
    PRINT("Cuenta: " & count)
WEND
```

#### Bucle con condición

```vba
' Buscar un carácter específico en la cadena de entrada
position = 1
found = 0
WHILE position <= LEN(TXT1) AND found = 0
    IF MID(TXT1, position, 1) = "X" THEN
        found = position
    END IF
    position = position + 1
WEND

IF found > 0 THEN
    RETURN1 = "X está en la posición " & found
    PRINT(RETURN1)
ELSE
    RETURN1 = "X no encontrada"
    PRINT(RETURN1)
END IF
```

### Sentencia SELECT CASE (ramificación múltiple)

La sentencia SELECT CASE estilo VBA permite describir múltiples ramificaciones condicionales de forma concisa. Se ejecuta la primera cláusula Case que coincida y no se evalúan las siguientes.

#### Forma básica

```vba
SELECT CASE VAL1
    CASE 1
        RETURN1 = "uno"
    CASE 2
        RETURN1 = "dos"
    CASE 3
        RETURN1 = "tres"
    CASE ELSE
        RETURN1 = "otros"
END SELECT
```

#### Sentencia Case con múltiples valores

```vba
' Especificar múltiples valores separados por comas
value = 5
SELECT CASE value
    CASE 1, 3, 5, 7, 9
        result = "Impar"
    CASE 2, 4, 6, 8, 10
        result = "Par"
    CASE ELSE
        result = "Fuera de rango"
END SELECT
PRINT(result)  ' Impar
```

#### Sentencia Case con especificación de rango

```vba
' Especificar rango con el operador TO
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
        grade = "Inválido"
END SELECT
PRINT(grade)  ' C
```

#### Especificación múltiple separada por comas (ejemplo de día de la semana)

```vba
dayNum = WEEKDAY(NOW())
SELECT CASE dayNum
    CASE 1, 7
        dayType = "fin de semana"
    CASE 2, 3, 4, 5, 6
        dayType = "día laborable"
END SELECT
PRINT(dayType)
```

---

## 🔨 Funciones definidas por el usuario (sentencia FUNCTION)

En u5 EasyScripter, puede crear funciones definidas por el usuario utilizando la sentencia Function estilo VBA. Dentro de las funciones se proporciona un ámbito local independiente, evitando interferencias con variables globales.

### Definición básica de funciones

```vba
' Función para sumar dos números
FUNCTION add(a, b)
    add = a + b  ' Establecer el valor de retorno asignando al nombre de la función
END FUNCTION

' Llamada a la función
result = add(5, 3)
PRINT(result)  ' 8
```

### Función que devuelve el mayor de dos números

```vba
' Función que devuelve el mayor de dos números
FUNCTION maxValue(a, b)
    IF a > b THEN
        maxValue = a
    ELSE
        maxValue = b
    END IF
END FUNCTION

' Ejemplo de uso
result = maxValue(10, 20)
PRINT(result)  ' 20
```

### Función con múltiples argumentos

```vba
' Función para decorar prompts
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

' Ejemplo de uso
finalPrompt = decoratePrompt("portrait", "high", "anime")
PRINT(finalPrompt)  ' portrait, masterpiece, best quality, anime style
```

### Función recursiva

```vba
' Función recursiva para calcular el factorial
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

## 💬 Notación de comentarios

Los comentarios comienzan con una comilla simple (`'`).

```vba
' Esto es un comentario
x = 10  ' También son posibles comentarios al final de la línea
PRINT(x)  ' 10

' Comentarios en múltiples líneas
' Añadir comilla simple al inicio de cada línea
```

---

## 📚 Próximos pasos

- [Referencia de funciones integradas](00_index.md) - Detalles de 120 funciones
- [Documento principal](README.md) - Resumen general y método de instalación

---

**Última actualización**: 3 de octubre de 2024

---

[← Volver al documento principal](README.md)
