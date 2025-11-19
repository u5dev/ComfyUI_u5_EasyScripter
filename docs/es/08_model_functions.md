# Referencia de funciones de modelos

[← Volver al índice de funciones integradas](00_index.md)

## Resumen

Las funciones de modelos proporcionan funcionalidad para determinar automáticamente la resolución óptima de varios modelos generativos utilizados en ComfyUI. Calcula automáticamente el tamaño óptimo del espacio Latent para ese modelo a partir del nombre del modelo y la relación de aspecto.

Modelos compatibles: Stable Diffusion 1.5/2.1/XL, SD3/3.5, FLUX.1, Hunyuan-DiT, Kandinsky, PixArt, Playground, etc. (más de 30 tipos)

---

## Lista de funciones de modelos

### OPTIMAL_LATENT(model_hint, width, height)

**Descripción**: Determina automáticamente el tamaño Latent óptimo según el nombre del modelo y la relación de aspecto

**Argumentos**:
- model_hint - Pista del nombre del modelo (cadena)
  - Ejemplo: "SDXL", "SD 1.5", "Flux", "Hunyuan"
- width - Ancho deseado (entero)
- height - Altura deseada (entero)

**Valor de retorno**: Array del tamaño Latent óptimo [width, height]

**Modelos compatibles**: SD1.5, SD2.1, SDXL, SD3/3.5, Hunyuan-DiT, FLUX.1, Kandinsky, PixArt, Playground, etc. (30+ modelos)

**Ejemplo**:
```vba
' Obtener resolución óptima 4:3 para SDXL
DIM result
result = OPTIMAL_LATENT("SDXL", 4, 3)
PRINT(result)  ' Confirmar resultado intermedio
PRINT("Tamaño óptimo: " & result(0) & "x" & result(1))
' Salida: "Modelo: SDXL 1.0 (base) | Óptimo: 1152x896 (4:3)"
' Salida: "{0: 1152, 1: 896}"
' Salida: "Tamaño óptimo: 1152x896"

' Obtener 16:9 para Stable Diffusion 1.5
result = OPTIMAL_LATENT("SD 1.5", 16, 9)
PRINT(result)  ' Confirmar resultado intermedio
PRINT(result(0) & "x" & result(1))
' Salida: "Modelo: blue_pencil (SD1.5) | Óptimo: 704x384 (11:6)"
' Salida: "{0: 704, 1: 384}"
' Salida: "704x384"

' Cuadrado para FLUX.1
result = OPTIMAL_LATENT("Flux", 256, 256)
PRINT(result)  ' Confirmar resultado intermedio
' Salida: "Modelo: FLUX.1 (dev/pro) | Óptimo: 1024x1024 (1:1)"
' Salida: "{0: 1024, 1: 1024}"
```

---

## Actualización de datos del modelo

Para agregar un nuevo modelo, edite `data/model_resolutions.csv`.

**Formato CSV**:
```csv
model_key,model_display_name,aliases,version,width,height,aspect_ratio,description
new_model,New Model v1.0,newmodel|new,1.0,1024,1024,1:1,descripción
```

**Nota**: Reinicie ComfyUI para reflejar los nuevos datos.

---

## Ejemplos de uso

### Determinación de resolución óptima en flujo de trabajo SDXL

```vba
' Calcular automáticamente la resolución óptima para SDXL desde resolución de entrada del usuario
DIM user_width
DIM user_height
user_width = 1920  ' Ancho Full HD
PRINT(user_width)  ' Confirmar resultado intermedio
' Salida: "1920"
user_height = 1080 ' Altura Full HD
PRINT(user_height)  ' Confirmar resultado intermedio
' Salida: "1080"

DIM optimal
optimal = OPTIMAL_LATENT("SDXL", user_width, user_height)
PRINT(optimal)  ' Confirmar resultado intermedio
' Salida: "Modelo: SDXL 1.0 (base) | Óptimo: 1344x768 (16:9)"
' Salida: "{0: 1344, 1: 768}"

' Obtener ancho y altura óptimos del array optimal
DIM final_width
DIM final_height
final_width = optimal(0)
PRINT(final_width)  ' Confirmar resultado intermedio
' Salida: "1344"
final_height = optimal(1)
PRINT(final_height)  ' Confirmar resultado intermedio
' Salida: "768"

PRINT("Entrada: " & user_width & "x" & user_height)
PRINT("SDXL Óptimo: " & final_width & "x" & final_height)
' Salida: "Entrada: 1920x1080"
' Salida: "SDXL Óptimo: 1344x768"
```

---

[← Volver al índice de funciones integradas](00_index.md)
