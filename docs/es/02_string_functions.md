# Referencia de funciones de cadenas

[← Volver al índice de funciones integradas](00_index.md)

Referencia completa de las funciones de cadenas que se pueden usar en u5 EasyScripter.

## Lista de funciones
Se proporcionan 28 funciones de cadenas.

---

### LEN(text)
**Descripción**: Devuelve la longitud de la cadena
**Argumentos**: text - Cadena
**Valor de retorno**: Número de caracteres
**Ejemplo**:
```vba
result = LEN("Hello")
PRINT(result)  ' 5
```

### LEFT(text, length)
**Descripción**: Obtiene los caracteres desde la izquierda
**Argumentos**:
- text - Cadena
- length - Número de caracteres a obtener
**Valor de retorno**: Subcadena
**Ejemplo**:
```vba
result = LEFT("Hello World", 5)
PRINT(result)  ' "Hello"
```

### RIGHT(text, length)
**Descripción**: Obtiene los caracteres desde la derecha
**Argumentos**:
- text - Cadena
- length - Número de caracteres a obtener
**Valor de retorno**: Subcadena
**Ejemplo**:
```vba
result = RIGHT("Hello World", 5)
PRINT(result)  ' "World"
```

### MID(text, start, length)
**Descripción**: Obtiene subcadena desde la posición especificada

**Importante**: La posición inicial 0 se trata como 1.

**Argumentos**:
- text - Cadena
- start - Posición inicial (basada en 1, 0 se trata como 1)
- length - Número de caracteres a obtener
**Valor de retorno**: Subcadena
**Ejemplo**:
```vba
result = MID("Hello World", 7, 5)
PRINT(result)  ' "World"
result = MID("ABCDEFG", 0, 2)
PRINT(result)  ' "AB" (0 se trata como 1)
```

### UPPER(text)
**Descripción**: Convierte a mayúsculas
**Argumentos**: text - Cadena
**Valor de retorno**: Cadena en mayúsculas
**Ejemplo**:
```vba
result = UPPER("Hello")
PRINT(result)  ' "HELLO"
```

### LOWER(text)
**Descripción**: Convierte a minúsculas
**Argumentos**: text - Cadena
**Valor de retorno**: Cadena en minúsculas
**Ejemplo**:
```vba
result = LOWER("HELLO")
PRINT(result)  ' "hello"
```

### TRIM(text)
**Descripción**: Elimina espacios al inicio y final
**Argumentos**: text - Cadena
**Valor de retorno**: Cadena sin espacios
**Ejemplo**:
```vba
result = TRIM("  Hello  ")
PRINT(result)  ' "Hello"
```

### REPLACE(text, old, new)
**Descripción**: Reemplaza cadena
**Argumentos**:
- text - Cadena objetivo
- old - Cadena a buscar
- new - Cadena de reemplazo
**Valor de retorno**: Cadena reemplazada
**Ejemplo**:
```vba
result = REPLACE("Hello World", "World", "ComfyUI")
PRINT(result)  ' "Hello ComfyUI"
```

### INSTR([start,] text, search)
**Descripción**: Busca cadena (devuelve posición)
**Argumentos**:
- start - Posición de inicio (omitido:1)
- text - Cadena objetivo
- search - Cadena a buscar
**Valor de retorno**: Posición encontrada (0=no encontrado)
**Ejemplo**:
```vba
result = INSTR("Hello World", "World")
PRINT(result)  ' 7
```

### INSTRREV(text, search, [start])
**Descripción**: Busca cadena desde el final
**Argumentos**:
- text - Cadena objetivo
- search - Cadena a buscar
- start - Posición de inicio (omitido:final)
**Valor de retorno**: Posición encontrada
**Ejemplo**:
```vba
result = INSTRREV("Hello World", "o")
PRINT(result)  ' 8 (última o)
```

### STRREVERSE(text)
**Descripción**: Invierte la cadena
**Argumentos**: text - Cadena
**Valor de retorno**: Cadena invertida
**Ejemplo**:
```vba
result = STRREVERSE("Hello")
PRINT(result)  ' "olleH"
```

### STRCOMP(text1, text2, [compare])
**Descripción**: Compara cadenas
**Argumentos**:
- text1 - Cadena 1
- text2 - Cadena 2
- compare - Método de comparación (0=binario, 1=texto)
**Valor de retorno**: -1/0/1 (menor/igual/mayor)
**Ejemplo**:
```vba
result = STRCOMP("abc", "ABC", 1)
PRINT(result)  ' 0 (ignora mayúsculas/minúsculas)
```

### SPACE(number)
**Descripción**: Genera espacios
**Argumentos**: number - Número de espacios
**Valor de retorno**: Cadena de espacios
**Ejemplo**:
```vba
result = SPACE(5)
PRINT(result)  ' "     "
```

### STRING(number, character)
**Descripción**: Repite carácter
**Argumentos**:
- number - Número de repeticiones
- character - Carácter a repetir
**Valor de retorno**: Cadena repetida
**Ejemplo**:
```vba
result = STRING(5, "A")
PRINT(result)  ' "AAAAA"
```

### FORMAT(value, format_string)
**Descripción**: Formatea valor
**Argumentos**:
- value - Valor
- format_string - Cadena de formato
**Valor de retorno**: Cadena formateada
**Formatos soportados**:
- `{:.Nf}` - N decimales
- `{:0Nd}` - Relleno con ceros de N dígitos
- `{:,}` - Separador de miles
- `%Y-%m-%d` - Formato de fecha
**Ejemplo**:
```vba
result = FORMAT(3.14159, "{:.2f}")
PRINT(result)  ' "3.14"
result = FORMAT(42, "{:05d}")
PRINT(result)  ' "00042"
```

### SPLIT(text, [delimiter])
**Descripción**: Divide cadena en array
**Argumentos**:
- text - Cadena a dividir
- delimiter - Carácter separador (omitido:coma)
**Valor de retorno**: Array dividido
**Ejemplo**:
```vba
result = SPLIT("apple,banana,cherry")
PRINT(result(0))  ' "apple"
```

### JOIN(array, [delimiter])
**Descripción**: Une array en cadena
**Argumentos**:
- array - Array a unir
- delimiter - Carácter separador (omitido:coma)
**Valor de retorno**: Cadena unida
**Ejemplo**:
```vba
ARRAY(arr, "A", "B", "C")
result = JOIN(arr, "-")
PRINT(result)  ' "A-B-C"
```

### LTRIM(text)
**Descripción**: Elimina espacios a la izquierda
**Argumentos**: text - Cadena
**Valor de retorno**: Cadena sin espacios a la izquierda
**Ejemplo**:
```vba
result = LTRIM("  Hello")
PRINT(result)  ' "Hello"
```

### RTRIM(text)
**Descripción**: Elimina espacios a la derecha
**Argumentos**: text - Cadena
**Valor de retorno**: Cadena sin espacios a la derecha
**Ejemplo**:
```vba
result = RTRIM("Hello  ")
PRINT(result)  ' "Hello"
```

### UCASE(text)
**Descripción**: Convierte a mayúsculas (alias de UPPER)
**Argumentos**: text - Cadena
**Valor de retorno**: Cadena en mayúsculas
**Ejemplo**:
```vba
result = UCASE("hello")
PRINT(result)  ' "HELLO"
```

### LCASE(text)
**Descripción**: Convierte a minúsculas (alias de LOWER)
**Argumentos**: text - Cadena
**Valor de retorno**: Cadena en minúsculas
**Ejemplo**:
```vba
result = LCASE("HELLO")
PRINT(result)  ' "hello"
```

### PROPER(text)
**Descripción**: Convierte a formato título (capitaliza primera letra de cada palabra)
**Argumentos**: text - Cadena
**Valor de retorno**: Cadena en formato título
**Ejemplo**:
```vba
result = PROPER("hello world")
PRINT(result)  ' "Hello World"
```

### CHR(code)
**Descripción**: Convierte código de carácter a carácter
**Argumentos**: code - Código de carácter (rango ASCII 0-127)
**Valor de retorno**: Carácter correspondiente
**Ejemplo**:
```vba
result = CHR(65)
PRINT(result)  ' "A"
```

### ASC(char)
**Descripción**: Convierte carácter a código de carácter
**Argumentos**: char - Carácter o cadena (usa el primer carácter)
**Valor de retorno**: Código de carácter (ASCII)
**Ejemplo**:
```vba
result = ASC("A")
PRINT(result)  ' 65
```

### STR(value)
**Descripción**: Convierte número a cadena
**Argumentos**: value - Número
**Valor de retorno**: Número convertido a cadena
**Ejemplo**:
```vba
result = STR(123)
PRINT(result)  ' "123"
```

### URLENCODE(text, [encoding])
**Descripción**: Realiza codificación URL (percent encoding)
**Argumentos**:
- text - Cadena a codificar
- encoding - Codificación de caracteres (predeterminado: utf-8)
**Valor de retorno**: Cadena codificada en URL
**Ejemplo**:
```vba
encoded = URLENCODE("あいうえお")
PRINT(encoded)  ' → %E3%81%82%E3%81%84%E3%81%86%E3%81%88%E3%81%8A
```

### URLDECODE(text, [encoding])
**Descripción**: Realiza decodificación URL
**Argumentos**:
- text - Cadena a decodificar
- encoding - Codificación de caracteres (predeterminado: utf-8)
**Valor de retorno**: Cadena decodificada
**Ejemplo**:
```vba
decoded = URLDECODE("%E3%81%82%E3%81%84%E3%81%86%E3%81%88%E3%81%8A")
PRINT(decoded)  ' → あいうえお
```

### ESCAPEPATHSTR(path, [replacement])
**Descripción**: Reemplaza o elimina caracteres prohibidos en rutas de archivo
**Argumentos**:
- path - Cadena a procesar
- replacement - Cadena de reemplazo (omitido: eliminar)
**Valor de retorno**: Cadena con caracteres prohibidos procesados

**Caracteres prohibidos**: `\`, `/`, `:`, `*`, `?`, `"`, `<`, `>`, `|`

**Palabras reservadas** (prohibidas como nombre de archivo completo): CON, PRN, AUX, NUL, COM1-9, LPT1-9

**Ejemplo**:
```vba
safe_name = ESCAPEPATHSTR("file:name*.txt", "_")
PRINT(safe_name)  ' → file_name_.txt
safe_name = ESCAPEPATHSTR("CON.txt", "_")
PRINT(safe_name)  ' → _.txt
```

---

[← Volver al índice de funciones integradas](00_index.md)
