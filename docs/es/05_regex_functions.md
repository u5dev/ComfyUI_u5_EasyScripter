# Referencia de funciones de expresiones regulares

[← Volver al índice de funciones integradas](00_index.md)

## Resumen

Las funciones de expresiones regulares permiten procesamiento avanzado de texto como coincidencia de patrones, búsqueda, reemplazo y extracción. Utilizan el motor de expresiones regulares de Python, proporcionando potentes capacidades de coincidencia de patrones.

---

## REGEX(pattern, text)

**Descripción**: Prueba coincidencia de patrón

**Argumentos**:
- pattern - Patrón de expresión regular
- text - Cadena a buscar

**Valor de retorno**: 1 (coincide) o 0

**Ejemplo**:
```vba
result = REGEX("\\d+", "abc123def")
PRINT(result)  ' 1 (contiene números)

result = REGEX("^[A-Z]", "Hello")
PRINT(result)  ' 1 (comienza con mayúscula)
```

---

## REGEXMATCH(pattern, text)

**Descripción**: Obtiene la primera coincidencia

**Argumentos**:
- pattern - Patrón de expresión regular
- text - Cadena a buscar

**Valor de retorno**: Cadena coincidente (vacío si no coincide)

**Ejemplo**:
```vba
result = REGEXMATCH("\\d+", "abc123def456")
PRINT(result)  ' "123"

result = REGEXMATCH("[A-Z]+", "helloWORLD")
PRINT(result)  ' "WORLD"
```

---

## REGEXREPLACE(pattern, text, replacement)

**Descripción**: Reemplaza patrón

**Argumentos**:
- pattern - Patrón de expresión regular
- text - Cadena objetivo
- replacement - Cadena de reemplazo

**Valor de retorno**: Cadena después del reemplazo

**Ejemplo**:
```vba
result = REGEXREPLACE("\\d+", "abc123def", "XXX")
PRINT(result)  ' "abcXXXdef"

result = REGEXREPLACE("\\s+", "a  b    c", " ")
PRINT(result)  ' "a b c"
```

---

## REGEXEXTRACT(pattern, text, [group])

**Descripción**: Extrae grupo

**Argumentos**:
- pattern - Patrón de expresión regular (con grupos)
- text - Cadena objetivo
- group - Número de grupo (omitido: 0=completo)

**Valor de retorno**: Cadena extraída

**Ejemplo**:
```vba
result = REGEXEXTRACT("(\\d{4})-(\\d{2})", "2024-01-15", 1)
PRINT(result)  ' "2024"

result = REGEXEXTRACT("(\\w+)@(\\w+)", "user@domain", 2)
PRINT(result)  ' "domain"
```

---

## REGEXCOUNT(pattern, text)

**Descripción**: Cuenta coincidencias

**Argumentos**:
- pattern - Patrón de expresión regular
- text - Cadena objetivo

**Valor de retorno**: Número de coincidencias

**Ejemplo**:
```vba
count = REGEXCOUNT("\\d", "a1b2c3d4")
PRINT(count)  ' 4

count = REGEXCOUNT("\\w+", "hello world")
PRINT(count)  ' 2
```

---

## REGEXMATCHES(pattern, text)

**Descripción**: Obtiene todas las coincidencias en array

**Argumentos**:
- pattern - Patrón de expresión regular
- text - Cadena objetivo

**Valor de retorno**: Lista de coincidencias

**Ejemplo**:
```vba
matches = REGEXMATCHES("\\d+", "a10b20c30")
PRINT(matches)  ' ["10", "20", "30"]
```

---

## REGEXSPLIT(pattern, text)

**Descripción**: Divide por patrón

**Argumentos**:
- pattern - Patrón separador
- text - Cadena objetivo

**Valor de retorno**: Lista dividida

**Ejemplo**:
```vba
parts = REGEXSPLIT("[,;]", "a,b;c,d")
PRINT(parts)  ' ["a", "b", "c", "d"]
PRINT(parts[0]) ' a
```

---

[← Volver al índice de funciones integradas](00_index.md)
