# Referencia de funciones CSV

[← Volver al índice de funciones integradas](00_index.md)

## Resumen

Grupo de funciones para manipular cadenas CSV (valores separados por comas). Útil para generación de prompts y gestión de valores de configuración.

- Conteo y obtención de elementos CSV
- Generación de prompts mediante selección aleatoria
- Eliminación de duplicados y obtención de diferencias
- Conversión entre arrays y CSV

---

## Lista de funciones

### CSVCOUNT(csv_text)

**Descripción**: Cuenta elementos CSV

**Argumentos**:
- csv_text - Cadena separada por comas

**Valor de retorno**: Número de elementos (entero)

**Ejemplo**:
```vba
count = CSVCOUNT("apple,banana,orange")
PRINT(count)    ' 3
count = CSVCOUNT("")
PRINT(count)    ' 0
```

---

### CSVREAD(csv_text, index)

**Descripción**: Obtiene elemento en el índice especificado de cadena CSV

**Argumentos**:
- csv_text - Cadena separada por comas
- index - Índice del elemento a obtener (basado en 1)

**Valor de retorno**: Elemento en la posición especificada (cadena). Cadena vacía si está fuera de rango

**Ejemplo**:
```vba
element = CSVREAD("apple,banana,orange", 2)
PRINT(element)    ' banana
element = CSVREAD("a,b,c,d", 1)
PRINT(element)    ' a
```

---

### CSVUNIQUE(csv_text)

**Descripción**: Elimina duplicados

**Argumentos**:
- csv_text - Cadena separada por comas

**Valor de retorno**: Cadena CSV después de eliminar duplicados

**Ejemplo**:
```vba
result = CSVUNIQUE("a,b,a,c,b")
PRINT(result)    ' a,b,c
result = CSVUNIQUE("1,2,3,2,1")
PRINT(result)    ' 1,2,3
```

---

### CSVMERGE(csv1, csv2, ...)

**Descripción**: Combina múltiples CSV

**Argumentos**:
- csv1, csv2, ... - Múltiples cadenas CSV (argumentos variables)

**Valor de retorno**: Cadena CSV combinada

**Ejemplo**:
```vba
result = CSVMERGE("a,b", "c,d")
PRINT(result)        ' a,b,c,d
result = CSVMERGE("1,2", "3", "4,5")
PRINT(result)        ' 1,2,3,4,5
```

---

### CSVDIFF(array_name, csv1, csv2)

**Descripción**: Almacena en array la diferencia de dos cadenas CSV (elementos que existen solo en una)

**Argumentos**:
- array_name - Nombre de variable del array para almacenar resultado
- csv1 - Cadena CSV 1
- csv2 - Cadena CSV 2

**Valor de retorno**: Número de elementos diferentes (entero)

**Ejemplo**:
```vba
' Obtener elementos en csv1 pero no en csv2, y elementos en csv2 pero no en csv1
DIM diff_array
count = CSVDIFF(diff_array, "a,b,c,d", "b,d,e")
PRINT(count)           ' 3
PRINT(diff_array(0))   ' a
PRINT(diff_array(1))   ' c
PRINT(diff_array(2))   ' e
```

---

### PICKCSV(csv_text, [index])

**Descripción**: Selecciona elemento CSV

**Argumentos**:
- csv_text - Cadena CSV
- index - Índice (omitido: selección aleatoria)

**Valor de retorno**: Elemento seleccionado (cadena)

**Ejemplo**:
```vba
result = PICKCSV("red,green,blue", 2)
PRINT(result)     ' green
result = PICKCSV("A,B,C,D")
PRINT(result)     ' Uno de A, B, C o D
```

---

### RNDCSV(csv_text, [count])

**Descripción**: Selección aleatoria de CSV (también se puede obtener array de múltiples elementos)

**Argumentos**:
- csv_text - Cadena CSV
- count - Número de elementos a seleccionar (omitido: devuelve una cadena)

**Valor de retorno**:
- Si count no se especifica: Un elemento seleccionado aleatoriamente (cadena)
- count=1: Un elemento seleccionado aleatoriamente (cadena)
- count≥2: Lista de elementos seleccionados aleatoriamente
- count >= número de elementos: Array completo manteniendo orden original

**Ejemplo**:
```vba
' Seleccionar un elemento (tradicional)
style = RNDCSV("realistic,anime,cartoon,abstract")
PRINT(style)
color = RNDCSV("red,blue,green,yellow,purple")
PRINT(color)

' Obtener múltiples elementos como array (con duplicados)
DIM selected[3]
selected = RNDCSV("A,B,B,B,C,C,D", 3)
PRINT(selected)  ' Ej: ["B", "B", "D"]
```

---

### CSVJOIN(array, [delimiter])

**Descripción**: Une array en cadena CSV

**Argumentos**:
- array - Array
- delimiter - Carácter separador (omitido: coma)

**Valor de retorno**: Cadena CSV unida

**Ejemplo**:
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

**Descripción**: Ordena elementos CSV

**Argumentos**:
- csv_text - Texto separado por delimitador
- delimiter - Carácter separador (omitido: ",")
- descending - Bandera de orden descendente (omitido: False, 0=ascendente, 1 o True=descendente)

**Valor de retorno**: Cadena CSV ordenada

**Ejemplo**:
```vba
result = CSVSORT("dog,cat,bird,ant")
PRINT(result)      ' ant,bird,cat,dog
result = CSVSORT("3,1,4,1,5,9,2,6")
PRINT(result)      ' 1,1,2,3,4,5,6,9
result = CSVSORT("Z,A,M,B", ",", 1)
PRINT(result)      ' Z,M,B,A
```

---

[← Volver al índice de funciones integradas](00_index.md)
