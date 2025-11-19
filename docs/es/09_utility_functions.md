# Referencia de funciones de utilidad

[← Volver al índice de funciones integradas](00_index.md)

Las funciones de utilidad son un conjunto de funciones convenientes que ayudan en el desarrollo de scripts, como salida de depuración, determinación de tipos y procesamiento de entrada.

---

## Funciones de salida

### PRINT(message, ...)

**Descripción**: Imprime valores en el área de texto (para depuración)

**Argumentos**:
- message - Valor a imprimir (se pueden especificar múltiples)

**Valor de retorno**: Ninguno (se agrega a la variable PRINT)

**Ejemplo**:
```vba
value = VAL1 * 2
PRINT("value after multiplication: " & value)

FOR i = 1 TO 10
    PRINT("Loop iteration: " & i)
NEXT
```

**Nota**:
- El contenido impreso con PRINT se muestra en el área de texto debajo del nodo
- Útil para verificar valores de variables durante la depuración

---

### OUTPUT(arg, [path], [flg])

**Descripción**: Imprime texto, números, arrays, imágenes y datos binarios a archivo

**Argumentos**:
- arg (Any) - Valor a imprimir (cadena, número, array, torch.Tensor, bytes)
- path (str, opcional) - Ruta de destino (ruta relativa, predeterminado="")
- flg (str, opcional) - Modo de operación ("NEW"=nuevo/evitar duplicados, "ADD"=agregar, predeterminado="NEW")

**Valor de retorno**: str - Ruta absoluta del archivo impreso (cadena vacía en caso de error)

**Funciones**:
1. **Salida de texto**: Imprime cadenas, números, arrays como archivo de texto
2. **Salida de imagen**: Imprime torch.Tensor (datos de imagen ComfyUI) como PNG/JPEG
3. **Salida binaria**: Imprime datos tipo bytes como archivo binario
4. **Modo NEW**: Agrega automáticamente `_0001`, `_0002`... en caso de duplicado
5. **Modo ADD**: Agrega al archivo existente
6. **Seguridad**: Rechaza rutas absolutas/UNC (solo rutas relativas permitidas)
7. **Subdirectorios**: Creación recursiva automática
8. **Extensión automática**: `.txt` (texto), `.png` (imagen)

**Ejemplo**:
```vba
path = OUTPUT("Hello World", "output.txt", "NEW")
PRINT("Destino: " & path)

ARR = ARRAY("apple", "banana", "cherry")
path = OUTPUT(ARR, "fruits.txt")
```

**Restricciones de seguridad**:
- Rechaza rutas absolutas (`C:\...`, `/...`)
- Rechaza rutas UNC (`\\server\...`)
- Solo rutas relativas permitidas

---

### INPUT(path)

**Descripción**: Lee archivos desde la carpeta de salida de ComfyUI (función simétrica a OUTPUT)

**Argumentos**:
- path (str, requerido) - Ruta relativa desde la carpeta de salida de ComfyUI
  - Rutas absolutas (`C:\...`, `/...`) prohibidas
  - Rutas UNC (`\\server\...`) prohibidas
  - Solo rutas relativas permitidas

**Valor de retorno**: Tipo dinámico (determinación automática según formato de archivo)
- Archivo de texto (`.txt`, `.md`) → tipo str
- Número JSON → tipo float
- Array JSON → tipo list
- Archivo de imagen (`.png`, `.jpg`, `.jpeg`, `.bmp`, `.webp`) → tipo torch.Tensor (compatible con ComfyUI)
- Otros → tipo bytes (binario)

**Funciones**:
1. **Determinación automática de tipo**: Lee en el tipo óptimo según formato de archivo
2. **Soporte de datos de imagen**: Formato torch.Tensor que se puede conectar directamente a nodos de imagen ComfyUI
3. **Soporte JSON**: Análisis automático de números/arrays JSON
4. **Seguridad**: Rechaza rutas absolutas/UNC (solo rutas relativas permitidas)
5. **Manejo de errores**: Si no se encuentra el archivo, imprime advertencia y devuelve None

**Ejemplo**:
```vba
prompt = INPUT("prompts/positive.txt")
PRINT("Prompt leído: " & prompt)
RETURN1 = prompt

refImage = INPUT("reference_images/style_sample.png")
' refImage se puede conectar directamente a nodos de entrada de imagen ComfyUI
```

#### Conexión INPUT y RELAY_OUTPUT

Para pasar imágenes y datos leídos con INPUT a nodos posteriores, use la variable RELAY_OUTPUT.

```vba
PROMPT_TEXT = INPUT("prompts/positive.txt")
RELAY_OUTPUT = PROMPT_TEXT

IMG1 = INPUT("reference_images/base.png")
RELAY_OUTPUT = IMG1
```

**RETURN1/RETURN2 vs RELAY_OUTPUT**:
- RETURN1/RETURN2: Solo tipos primitivos (INT, FLOAT, STRING)
- RELAY_OUTPUT: Soporta tipo ANY (también objetos como torch.Tensor, list, dict)

---

### ISFILEEXIST(path, [flg])

**Descripción**: Verifica existencia de archivo en carpeta de salida ComfyUI y obtiene información extendida

**Argumentos**:
- path (str, requerido) - Ruta relativa desde carpeta de salida ComfyUI
- flg (str, opcional) - Bandera de opción (predeterminado: "")
  - `""` (predeterminado): Solo verificación de existencia
  - `"NNNN"`: Búsqueda de ruta de archivo _NNNN con número máximo
  - `"PIXEL"`: Obtener tamaño de imagen (ancho/alto)
  - `"SIZE"`: Obtener tamaño de archivo (bytes)

**Valor de retorno**: Tipo dinámico (varía según flg)
- **flg=""**: `"TRUE"` o `"FALSE"` (tipo str)
- **flg="NNNN"**: Ruta de archivo con número máximo (ruta relativa, tipo str), `"FALSE"` si no existe
- **flg="PIXEL"**: Cadena de array formato `"[width, height]"` (tipo str), `"FALSE"` si no es imagen/no existe
- **flg="SIZE"**: Tamaño de archivo en bytes (tipo str), `"FALSE"` si no existe

**Ejemplo**:
```vba
exists = ISFILEEXIST("output.txt")
IF exists = "TRUE" THEN
    PRINT("El archivo existe")
END IF

latestFile = ISFILEEXIST("ComfyUI_00001_.png", "NNNN")
IF latestFile <> "FALSE" THEN
    PRINT("Último archivo: " & latestFile)
END IF
```

---

### VRAMFREE([min_free_vram_gb])

**Descripción**: Función para liberar VRAM y RAM. Ejecuta descarga de modelos, limpieza de caché y recolección de basura.

**⚠️ ADVERTENCIA**: La descarga de modelos es una operación delicada. Dependiendo del momento de ejecución, puede causar comportamiento inesperado durante la ejecución del workflow. Use con precaución.

**Parámetros**:
- `min_free_vram_gb` (float, opcional): Umbral de ejecución (en GB)
  - Si la VRAM libre actual es igual o mayor a este valor, omite el procesamiento
  - Predeterminado: 0.0 (siempre ejecutar)

**Valor de retorno**: dict (información detallada del resultado de ejecución)
- `success`: Bandera de éxito de ejecución (bool)
- `message`: Mensaje de resultado (str)
- `freed_vram_gb`: Cantidad de VRAM liberada (float)
- `freed_ram_gb`: Cantidad de RAM liberada (float)

**Ejemplo**:
```vba
result = VRAMFREE(0.0)
PRINT("VRAM freed: " & result["freed_vram_gb"] & " GB")

result = VRAMFREE(2.0)
IF result["success"] = TRUE THEN
    PRINT("Cleanup completed")
END IF
```

---

### SLEEP([milliseconds])

**Descripción**: Pausa el procesamiento durante los milisegundos especificados (sleep). Se usa para control de velocidad de bucles WHILE() y sincronización de procesamiento.

**Argumentos**:
- milliseconds (FLOAT, opcional): Tiempo de sleep (milisegundos), predeterminado: 10ms

**Valor de retorno**: Ninguno (internamente devuelve 0.0)

**Ejemplo**:
```vba
SLEEP(500)  ' Sleep de 0.5 segundos

VAL1 = 0
WHILE VAL1 < 100
    VAL1 = VAL1 + 1
    SLEEP(100)  ' Esperar 100ms
WEND
```

---

## Funciones de procesamiento de imágenes

### IMAGETOBYTEARRAY(image_input, [max_size], [format], [return_format])

**Descripción**: Recibe IMAGE tensor o ruta de archivo de imagen, redimensiona/comprime y convierte a byte array o JSON array. Principalmente usado como datos de envío a REST API.

**Argumentos**:
- image_input (str | torch.Tensor, requerido) - Fuente de imagen
  - Cadena: Ruta de archivo de imagen
  - torch.Tensor: Formato IMAGE ComfyUI `[batch, height, width, channels]`
- max_size (int, opcional) - Tamaño máximo después de redimensionar (lado largo, píxeles), predeterminado: 336
- format (str, opcional) - Formato de imagen de salida ("PNG", "JPEG", etc.), predeterminado: "PNG"
- return_format (str, opcional) - Formato de retorno ("bytes" o "json"), predeterminado: "bytes"

**Valor de retorno**: Tipo dinámico (varía según return_format)
- **return_format="bytes"**: tipo bytes (datos binarios crudos)
- **return_format="json"**: tipo str (cadena formato JSON array, ej: `"[137, 80, 78, 71, ...]"`)

**Ejemplo**:
```vba
json_array = IMAGETOBYTEARRAY("C:/path/to/image.png", 336, "JPEG", "json")
PRINT("Longitud JSON array: " & LEN(json_array))

json_array = IMAGETOBYTEARRAY(VAL1, 336, "JPEG", "json")
RETURN1 = json_array
```

---

### IMAGETOBASE64(image_input, [max_size], [format], [return_format])

**Descripción**: Recibe IMAGE tensor o ruta de archivo de imagen, redimensiona/comprime y convierte a codificación Base64 o formato data URL. Principalmente usado como datos de envío a REST API.

**Argumentos**:
- image_input (str | torch.Tensor, requerido) - Fuente de imagen
- max_size (int, opcional) - Tamaño máximo después de redimensionar (lado largo, píxeles), predeterminado: 512
- format (str, opcional) - Formato de imagen de salida ("PNG", "JPEG", etc.), predeterminado: "PNG"
- return_format (str, opcional) - Formato de retorno ("base64" o "data_url"), predeterminado: "base64"

**Valor de retorno**: tipo str (varía según return_format)
- **return_format="base64"**: Cadena codificada en Base64
- **return_format="data_url"**: Cadena formato data URL

**Ejemplo**:
```vba
base64_str = IMAGETOBASE64("C:/path/to/image.png", 512, "PNG", "base64")
PRINT("Longitud Base64: " & LEN(base64_str))

data_url = IMAGETOBASE64(ANY_INPUT, 512, "PNG", "data_url")
RETURN1 = data_url
```

---

## Funciones de obtención de datos de imagen/Latent

### GETANYWIDTH([any_data])
**Descripción**: Obtiene el ancho (píxeles) de datos tipo IMAGE/LATENT
**Argumentos**: any_data (torch.Tensor, opcional) - Datos IMAGE/LATENT
**Valor de retorno**: float - Ancho (píxeles, 0.0 si no se puede obtener)
**Ejemplo**:
```vba
width = GETANYWIDTH()
PRINT("Ancho: " & width)
```

### GETANYHEIGHT([any_data])
**Descripción**: Obtiene el alto (píxeles) de datos tipo IMAGE/LATENT
**Argumentos**: any_data (torch.Tensor, opcional) - Datos IMAGE/LATENT
**Valor de retorno**: float - Alto (píxeles, 0.0 si no se puede obtener)
**Ejemplo**:
```vba
height = GETANYHEIGHT()
PRINT("Alto: " & height)
```

### GETANYTYPE([any_data])
**Descripción**: Determina el nombre de tipo de datos tipo ANY
**Argumentos**: any_data (Any, opcional) - Datos objetivo de determinación de tipo
**Valor de retorno**: str - Nombre de tipo
- "int", "float", "string" - Tipos básicos
- "image", "latent" - Imagen/Latent
- "model", "vae", "clip" - Tipos de modelo ComfyUI
**Ejemplo**:
```vba
type_name = GETANYTYPE()
PRINT("Tipo: " & type_name)
```

### GETANYVALUEINT([any_data])
**Descripción**: Obtiene valor entero de datos tipo ANY
**Valor de retorno**: int - Valor entero (0 si no se puede obtener)

### GETANYVALUEFLOAT([any_data])
**Descripción**: Obtiene valor de punto flotante de datos tipo ANY
**Valor de retorno**: float - Valor de punto flotante (0.0 si no se puede obtener)

### GETANYSTRING([any_data])
**Descripción**: Obtiene cadena de datos tipo ANY
**Valor de retorno**: str - Cadena (cadena vacía si no se puede obtener)

---

## Funciones de determinación de tipos

### ISNUMERIC(value)
**Descripción**: Determina si el valor es numérico
**Argumentos**: value - Valor a inspeccionar
**Valor de retorno**: 1 (numérico) o 0 (no numérico)
**Ejemplo**:
```vba
result = ISNUMERIC("123")  ' 1
result = ISNUMERIC("abc")  ' 0

IF ISNUMERIC(TXT1) THEN
    value = CDBL(TXT1)
    PRINT("Procesar como número: " & value)
END IF
```

### ISDATE(value)
**Descripción**: Determina si el valor se puede analizar como fecha
**Argumentos**: value - Valor a inspeccionar
**Valor de retorno**: 1 (fecha) o 0 (no fecha)
**Ejemplo**:
```vba
result = ISDATE("2024-01-15")  ' 1
result = ISDATE("hello")       ' 0
```

### ISARRAY(variable_name)
**Descripción**: Determina si la variable es un array
**Argumentos**: variable_name - Nombre de variable (cadena) o referencia de variable de array (notación ARR[])
**Valor de retorno**: 1 (array) o 0 (no array)
**Ejemplo**:
```vba
REDIM arr, 10
result = ISARRAY(arr[])   ' 1 (referencia de array)
result = ISARRAY("arr")   ' 1 (cadena de nombre de array)
```

### TYPE(value)
**Descripción**: Devuelve el tipo de variable como cadena
**Argumentos**: value - Valor del que se desea conocer el tipo
**Valor de retorno**: Nombre de tipo ("NUMBER", "STRING", "BOOLEAN", "ARRAY", "NULL", "OBJECT")
**Ejemplo**:
```vba
typeName = TYPE(123)      ' "NUMBER"
typeName = TYPE("hello")  ' "STRING"

dataType = TYPE(myValue)
SELECT CASE dataType
    CASE "NUMBER"
        PRINT("Número: " & myValue)
    CASE "STRING"
        PRINT("Cadena: " & myValue)
END SELECT
```

---

[← Volver al índice de funciones integradas](00_index.md)
