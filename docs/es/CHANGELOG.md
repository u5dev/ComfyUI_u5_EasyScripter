# Historial de actualizaciones (CHANGELOG)

Historial de actualizaciones principales de u5 EasyScripter.

---

## 📝 Historial de actualizaciones


### v3.1.2 (2025-11-18) - Corrección del formato de documentación

#### Fixed
- **Corrección de referencias cruzadas del número de funciones**: Corregido el número de funciones en docs/02_builtin_functions/00_index.md para que coincida con el número real de implementaciones
  - Funciones matemáticas: 24 → 16
  - Funciones CSV: 11 → 9
  - Funciones de array: 7 → 3
  - Funciones de modelo: 3 → 1
  - Funciones de utilidad: 21 → 18
  - Funciones de control de bucle: 9 → 1
  - Funciones de comunicación HTTP: 17 → 9
  - Funciones de ejecución Python: 3 → 4
- **Corrección de la tabla de referencia rápida**: Corregida la tabla de referencia rápida en 00_index.md
  - Eliminadas 8 funciones inexistentes de la tabla de funciones matemáticas (RND, RANDOMIZE, FIX, SGN, ASIN, ACOS, ATAN, ATAN2)
  - Corregidos los argumentos de la función CSVDIFF: CSVDIFF(csv1, csv2) → CSVDIFF(array_name, csv1, csv2)
  - Añadida la función PYDECODE a la tabla de funciones Python
- **Corrección del número de funciones de cadena**: Corregido el número de funciones en docs/02_builtin_functions/02_string_functions.md de 29 → 28
- **Corrección de enlaces de anclaje del índice**: Eliminados los guiones iniciales de los enlaces de anclaje del índice en docs/01_syntax_reference.md (conforme a las especificaciones de Markdown de GitHub)

### v3.1.1 (2025-11-17) - Documentación de funciones de cadena añadida

#### Added
- **Documentación de funciones de cadena añadida**: Documentación de 7 funciones de cadena implementadas
  - **ESCAPEPATHSTR(path, [replacement])**: Reemplaza o elimina caracteres prohibidos en rutas de archivo
  - **URLENCODE(text, [encoding])**: Codificación URL (codificación porcentual)
  - **URLDECODE(text, [encoding])**: Decodificación URL
  - **PROPER(text)**: Convierte a mayúsculas y minúsculas (primera letra de cada palabra en mayúscula)
  - **CHR(code)**: Conversión de código de carácter → carácter (rango ASCII)
  - **ASC(char)**: Conversión de carácter → código de carácter
  - **STR(value)**: Conversión de número → cadena
  - Documentación: docs/02_builtin_functions/02_string_functions.md
  - Número de funciones: 21 → 23 corregido

#### Changed
- **Número total de funciones integradas**: 135 entradas → 137 entradas actualizado
  - 135 funciones únicas (133 funciones + 2 alias)
  - README.md, docs/02_builtin_functions/00_index.md actualizados

### v3.1.0 (2025-11-17) - Soporte para el operador !=

#### Added
- **Operador !=**: Añadido operador de desigualdad estilo C
  - Mismo comportamiento que el operador `<>` (ambos se pueden usar)
  - Implementación: script_parser.py (añadido al array TOKEN_PATTERNS)
  - Pruebas: tests/test_neq_operator.py
  - Documentación: docs/01_syntax_reference.md

### v3.0.0 (2025-11-13) - Mejora del socket de entrada any_input y otros

### Added
- **Función IMAGETOBASE64**: Función añadida para convertir tensor IMAGE o ruta de archivo de imagen a codificación Base64 (o formato de URL de datos)
- **Función IMAGETOBYTEARRAY**: Función añadida para convertir tensor IMAGE o ruta de archivo de imagen a array JSON (o array de bytes)
- **Función FORMAT**: Función añadida para formatear números/fechas en el formato especificado (compatible con VBA)
- **Función GETANYTYPE**: Función añadida para determinar el nombre del tipo de datos de tipo ANY
- **Función GETANYVALUEINT**: Función añadida para obtener un valor entero de datos de tipo ANY
- **Función GETANYVALUEFLOAT**: Función añadida para obtener un valor de coma flotante de datos de tipo ANY
- **Función GETANYSTRING**: Función añadida para obtener una cadena de datos de tipo ANY
- **Función GETANYWIDTH**: Función añadida para obtener el ancho (número de píxeles) de datos de tipo IMAGE/LATENT
- **Función GETANYHEIGHT**: Función añadida para obtener la altura (número de píxeles) de datos de tipo IMAGE/LATENT

### Changed
- **Garantía de ejecución secuencial de LOOPSUBGRAPH**: Las iteraciones ahora se ejecutan secuencialmente en lugar de en paralelo
- **Número total de funciones integradas**: Actualizado a 134 entradas (132 funciones únicas, incluidos 2 alias)

### Fixed
- **Corrección de bug del número de repeticiones de LOOPSUBGRAPH**: Corregido el bug que ejecutaba una vez menos del número especificado
- **Corrección de lógica de adición de dependencias de LOOPSUBGRAPH**: Corregida la adición errónea de dependencias a nodos ComfyUI estándar
- **Corrección de firma del método execute_script**: Corregido el bug de falta del argumento `_iteration_dependency`

*(Continúa el historial completo de versiones en inglés)*

---

Para el historial completo de versiones y detalles técnicos, consulte el archivo CHANGELOG.md original en el repositorio.
