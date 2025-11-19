# Índice completo de funciones integradas

[← Volver al documento principal](README.md)

**Esta página es el índice de referencia de las funciones integradas de u5 EasyScripter.**

u5 EasyScripter proporciona una abundante variedad de funciones integradas que se pueden usar en scripts estilo VBA.

## Lista de categorías de funciones

### [Referencia de funciones matemáticas](01_math_functions.md)
16 funciones matemáticas - operaciones básicas, funciones trigonométricas, logaritmos, funciones estadísticas, etc.

### [Referencia de funciones de cadenas](02_string_functions.md)
28 funciones de cadenas - manipulación de cadenas, búsqueda, reemplazo, formato, etc.

### [Referencia de funciones de fecha y hora](03_datetime_functions.md)
12 funciones de fecha y hora - fecha y hora actual, cálculos de fechas, obtención de componentes de fecha y hora, conversión de fechas, etc.

### [Referencia de funciones CSV](04_csv_functions.md)
9 funciones CSV - operaciones CSV, selección aleatoria, eliminación de duplicados, etc.

### [Referencia de funciones de expresiones regulares](05_regex_functions.md)
7 funciones de expresiones regulares - coincidencia de patrones, reemplazo, extracción, etc.

### [Referencia de funciones de arrays](06_array_functions.md)
3 funciones de arrays - inicialización de arrays, cambio de tamaño, obtención del índice superior, etc.

### [Referencia de funciones de conversión y determinación de tipos](07_type_functions.md)
7 funciones de conversión y determinación de tipos - conversión de tipos, verificación de tipos, formato, etc.

### [Referencia de funciones de modelos](08_model_functions.md)
1 función de modelos - determinación de resolución óptima para modelos de generación de IA

### [Referencia de funciones de utilidad](09_utility_functions.md)
18 funciones de utilidad - salida de depuración, determinación de tipos, entrada/salida de archivos, verificación de existencia de archivos, liberación de memoria, espera, procesamiento de imágenes (conversión de IMAGE a array JSON/Base64), obtención de datos de imagen/Latent, obtención de datos de tipo ANY, etc.

---

## Tabla de referencia rápida

### Funciones matemáticas (16)

| Nombre de función | Resumen |
|--------|------|
| **ABS(value)** | Devuelve el valor absoluto |
| **INT(value)** | Devuelve la parte entera (trunca decimales) |
| **ROUND(value, [digits])** | Devuelve el valor redondeado |
| **SQRT(value)** | Devuelve la raíz cuadrada |
| **MIN(value1, value2, ...)** | Devuelve el valor mínimo |
| **MAX(value1, value2, ...)** | Devuelve el valor máximo |
| **SIN(radians)** | Devuelve el seno |
| **COS(radians)** | Devuelve el coseno |
| **TAN(radians)** | Devuelve la tangente |
| **RADIANS(degrees)** | Convierte grados a radianes |
| **DEGREES(radians)** | Convierte radianes a grados |
| **POW(base, exponent)** | Calcula la potencia (base^exponent) |
| **LOG(value, [base])** | Devuelve el logaritmo (por defecto: logaritmo natural) |
| **EXP(value)** | e (base del logaritmo natural) elevado a la potencia |
| **AVG(value1, value2, ...)** | Calcula el promedio |
| **SUM(value1, value2, ...)** | Calcula la suma |

### Funciones de cadenas (28)

| Nombre de función | Resumen |
|--------|------|
| **LEN(text)** | Devuelve la longitud de la cadena |
| **LEFT(text, length)** | Obtiene el número especificado de caracteres desde la izquierda |
| **RIGHT(text, length)** | Obtiene el número especificado de caracteres desde la derecha |
| **MID(text, start, length)** | Obtiene subcadena desde la posición especificada |
| **UPPER(text)** | Convierte a mayúsculas |
| **LOWER(text)** | Convierte a minúsculas |
| **TRIM(text)** | Elimina espacios al principio y al final |
| **REPLACE(text, old, new)** | Reemplaza cadena |
| **INSTR([start,] text, search)** | Busca cadena (devuelve posición) |
| **INSTRREV(text, search, [start])** | Busca cadena desde atrás |
| **STRREVERSE(text)** | Invierte cadena |
| **STRCOMP(text1, text2, [compare])** | Compara cadenas |
| **SPACE(number)** | Genera número especificado de espacios |
| **STRING(number, character)** | Repite carácter |
| **FORMAT(value, format_string)** | Formatea valor |
| **SPLIT(text, [delimiter])** | Divide cadena en array |
| **JOIN(array, [delimiter])** | Une array en cadena |
| **LTRIM(text)** | Elimina espacios a la izquierda |
| **RTRIM(text)** | Elimina espacios a la derecha |
| **UCASE(text)** | Convierte a mayúsculas (alias de UPPER) |
| **LCASE(text)** | Convierte a minúsculas (alias de LOWER) |
| **PROPER(text)** | Convierte a mayúsculas y minúsculas |
| **CHR(code)** | Conversión de código de carácter → carácter |
| **ASC(char)** | Conversión de carácter → código de carácter |
| **STR(value)** | Conversión de número → cadena |
| **URLENCODE(text, [encoding])** | Codificación URL |
| **URLDECODE(text, [encoding])** | Decodificación URL |
| **ESCAPEPATHSTR(path, [replacement])** | Procesa caracteres prohibidos en rutas de archivo |

### Funciones de fecha y hora (12)

| Nombre de función | Resumen |
|--------|------|
| **NOW()** | Obtiene la fecha y hora actual |
| **DATE()** | Obtiene la fecha de hoy |
| **TIME()** | Obtiene la hora actual |
| **YEAR([date])** | Obtiene el año |
| **MONTH([date])** | Obtiene el mes |
| **DAY([date])** | Obtiene el día |
| **HOUR([time])** | Obtiene la hora |
| **MINUTE([time])** | Obtiene los minutos |
| **SECOND([time])** | Obtiene los segundos |
| **DATEADD(interval, number, [date])** | Suma/resta a fecha |
| **DATEDIFF(interval, date1, [date2])** | Calcula diferencia de fechas |
| **WEEKDAY([date], [firstday])** | Devuelve día de la semana (1=domingo) |

### Funciones CSV (9)

| Nombre de función | Resumen |
|--------|------|
| **CSVCOUNT(csv_text)** | Cuenta elementos CSV |
| **CSVREAD(csv_text, index)** | Obtiene elemento en el índice especificado de cadena CSV |
| **CSVUNIQUE(csv_text)** | Elimina duplicados |
| **CSVMERGE(csv1, csv2, ...)** | Combina múltiples CSV |
| **CSVDIFF(array_name, csv1, csv2)** | Obtiene diferencia de CSV |
| **PICKCSV(csv_text, [index])** | Selecciona elemento CSV (omitido: aleatorio) |
| **RNDCSV(csv_text)** | Selección aleatoria de CSV (igual que PICKCSV) |
| **CSVJOIN(array, [delimiter])** | Une array en cadena CSV |
| **CSVSORT(csv_text, [delimiter], [reverse])** | Ordena elementos CSV |

### Funciones de expresiones regulares (7)

| Nombre de función | Resumen |
|--------|------|
| **REGEX(pattern, text)** | Prueba coincidencia de patrón |
| **REGEXMATCH(pattern, text)** | Obtiene primera coincidencia |
| **REGEXREPLACE(pattern, text, replacement)** | Reemplaza patrón |
| **REGEXEXTRACT(pattern, text, [group])** | Extrae grupo |
| **REGEXCOUNT(pattern, text)** | Cuenta coincidencias |
| **REGEXMATCHES(pattern, text)** | Obtiene todas las coincidencias en array |
| **REGEXSPLIT(pattern, text)** | Divide por patrón |

### Funciones de arrays (3)

| Nombre de función | Resumen |
|--------|------|
| **UBOUND(array)** | Obtiene el índice superior del array |
| **ARRAY(variable_name, value1, value2, ...)** | Inicializa array y establece valores |
| **REDIM(array_name, size)** | Cambia el tamaño del array (redefinir) |

### Funciones de conversión y determinación de tipos (7)

| Nombre de función | Resumen |
|--------|------|
| **CSTR(value)** | Convierte a cadena |
| **CINT(value)** | Convierte a entero |
| **CDBL(value)** | Convierte a número de coma flotante |
| **FORMAT(value, [format_string])** | Formatea número/fecha en el formato especificado (compatible con VBA) |
| **ISNUMERIC(value)** | Determina si es numérico |
| **ISDATE(value)** | Determina si es una fecha |
| **ISARRAY(variable_name)** | Determina si es un array |

### Funciones de modelos (1)

| Nombre de función | Resumen |
|--------|------|
| **OPTIMAL_LATENT(model_hint, width, height)** | Determina automáticamente el tamaño óptimo del espacio Latent según el nombre del modelo y la relación de aspecto |

### Funciones de utilidad (18)

| Nombre de función | Resumen |
|--------|------|
| **PRINT(message, ...)** | Emite valor al área de texto (para depuración) |
| **OUTPUT(arg, [path], [flg])** | Emite texto, números, arrays, imágenes, datos binarios a archivo |
| **INPUT(path)** | Carga archivo desde la carpeta de salida de ComfyUI (determinación de tipo dinámico) |
| **ISFILEEXIST(path, [flg])** | Verificación de existencia de archivo e información extendida (_NNNN búsqueda, tamaño de imagen, tamaño de archivo) |
| **VRAMFREE([min_free_vram_gb])** | Libera VRAM y RAM (descarga de modelo, limpieza de caché, GC) |
| **SLEEP([milliseconds])** | Pausa el procesamiento durante los milisegundos especificados (por defecto: 10ms) |
| **IMAGETOBYTEARRAY(image_input, [max_size], [format], [return_format])** | Convierte IMAGE/ruta de archivo a array JSON de imagen |
| **IMAGETOBASE64(image_input, [max_size], [format], [return_format])** | Codifica IMAGE/ruta de archivo a Base64 (para API Vision) |
| **GETANYWIDTH([any_data])** | Obtiene el ancho (número de píxeles) de datos de tipo IMAGE/LATENT |
| **GETANYHEIGHT([any_data])** | Obtiene la altura (número de píxeles) de datos de tipo IMAGE/LATENT |
| **GETANYTYPE([any_data])** | Determina el nombre del tipo de datos de tipo ANY |
| **GETANYVALUEINT([any_data])** | Obtiene valor entero de datos de tipo ANY |
| **GETANYVALUEFLOAT([any_data])** | Obtiene valor de coma flotante de datos de tipo ANY |
| **GETANYSTRING([any_data])** | Obtiene cadena de datos de tipo ANY |
| **ISNUMERIC(value)** | Determina si el valor es numérico |
| **ISDATE(value)** | Determina si el valor es analizable como fecha |
| **ISARRAY(variable_name)** | Determina si la variable es un array |
| **TYPE(value)** | Devuelve el tipo de variable como cadena |

---

[← Volver al documento principal](README.md)
