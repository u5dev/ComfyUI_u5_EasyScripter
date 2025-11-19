# u5 EasyScripter Node

[日本語](../../README.md) | [English](../en/README.md) | [中文](../zh/README.md) | [Español](../es/README.md) | [Français](../fr/README.md) | [Deutsch](../de/README.md)

---

## ¿Qué es esto?
- Es un nodo personalizado que permite ejecutar **scripts sencillos estilo VBA** en ComfyUI
- Puede incorporar ramificaciones condicionales, generación de prompts, procesamiento repetitivo, llamadas a API externas, entre otros.
- **Proporciona ejemplos para copiar y pegar para casi todas las funciones**, por lo que no necesitas experiencia en programación
- También se han reforzado e integrado los nodos secuenciales y las herramientas de liberación de memoria que están disponibles en otros lugares

```
Lo creé porque la configuración se volvía redundante con nodos estándar o individuales, y el control detallado era complicado
```

---

## Funciones y usos recomendados
- Puedes lanzar imágenes de pantalla de flujos de trabajo en ComfyUI y usarlas inmediatamente

### Crea muchas variaciones automáticamente
- Es tedioso pensar en un prompt cada vez. ¡Solo genera muchos resultados rápidamente como una presentación de diapositivas!
```vba
'Prompt base + reemplazar aleatoriamente con expresión y pose cada vez para crear un prompt
'→"base prompt" & "," & RNDCSV("CSV de poses candidatas") & "," & RNDCSV("CSV de expresiones candidatas")

RETURN1 = "woman, a girl, nurse, with a bandage, pale skin, green eyes, pink hair, blunt bangs,upper body, full body shot, masterpiece, best quality, high quality," & RNDCSV("looking at viewer, looking away, looking back, wink, making a peace sign, making a heart with hands, making a thumbs up, waving at the camera") & "," & RNDCSV("blush, smiling, embarrassed, sleepy, serious expression, fear")
```
<img src="../img/AUTO_SLIDESHOW.png" alt="Ejemplo de script de generación de prompts en el nodo EasyScripter" width="80%"><br>
  ↓<br>
  Pegando solo una línea<br>
  ↓<br>
<img src="../img/SLIDES.png" alt="Presentación de diapositivas de imágenes de variación generadas automáticamente" width="100%">

### Ajuste automático del tamaño Latent especializado para modelos
- ¡Ya no tienes que preocuparte por las resoluciones según si es SDXL o no!
```vba
result = OPTIMAL_LATENT("SDXL", 4, 3) ' Se ajusta automáticamente a 1152x896
RETURN1 = RESULT[0] '1152
RETURN2 = RESULT[1] '896
```
<img src="../img/OPTIMAL_LATENT.png" alt="Ejemplo de ajuste automático de resolución optimizada de modelo con la función OPTIMAL_LATENT" width="80%"><br>

**Simplemente pega en la ventana de script en la parte inferior del nodo y se convierte en un nodo profesional con funciones especiales**

---

## 📖 Documentación

Para documentación detallada, consulta lo siguiente:

- **[📖 Referencia del lenguaje de scripts](01_syntax_reference.md)** - Guía completa de gramática y estructuras de control
- **[🔧 Referencia de funciones integradas](00_index.md)** - Referencia completa de más de 100 funciones integradas
- **[🌟 Por favor apóyanos](CONTENTS.md)** - Ejemplos más prácticos y útiles, imágenes de flujos de trabajo abundantes, explicaciones detalladas

---

## u5 EasyScripter como solución

**Un nodo, infinitas posibilidades** - u5 EasyScripter es un motor de scripts de propósito general que funciona en Comfy UI:

- ✅ **Reemplaza más de 10 nodos dedicados**: procesamiento de texto, cálculos matemáticos, lógica condicional, generación aleatoria
- ✅ **Acelera el procesamiento por lotes**: barrido automático de parámetros, generación inteligente de variaciones
- ✅ **Mejora la ingeniería de prompts**: ajuste dinámico de pesos, modificaciones con ramificaciones condicionales, variaciones inteligentes
- ✅ **Optimiza los flujos de trabajo**: gráficos limpios, carga rápida, fácil de compartir
- ✅ **Escalable**: desde cálculos simples hasta algoritmos de automatización complejos
- ✅ **Guardia de ejecución concurrente**: procesamiento de cola seguro sin cuelgues incluso cuando se ejecutan múltiples nodos simultáneamente
- ✅ **Soporte multilingüe**: mensajes de error y salida de depuración en japonés e inglés

---

## ⚡ Inicio rápido

### Instalación

```bash
# Clonar en el directorio custom_nodes de ComfyUI
git clone https://github.com/u5dev/ComfyUI_u5_EasyScripter.git
```

### Tu primer flujo de trabajo inteligente
- Ajuste inteligente basado en las reglas de prompts que requiere el tipo de modelo

```vba

model_type = TXT1  ' Conectar nombre del modelo ("sdxl" o "Flux")
PRINT(model_type)  ' Confirmar tipo de modelo
base_prompt = "beautiful landscape"

SELECT CASE model_type
    CASE "sdxl"
        RETURN1 = "(" & base_prompt & ", ultra-detailed wide landscape, crisp daylight photography, shot on full-frame DSLR, high dynamic range, 8k uhd, professional photography:1.2)"
        PRINT(RETURN1)  ' Confirmar prompt SDXL
    CASE "flux"
        RETURN1 = "(" & base_prompt & "moody cinematic wide shot of a beautiful landscape at golden hour, dramatic backlight haze, soft volumetric light, cinematic lighting:1.1, subtle film grain)"
        PRINT(RETURN1)  ' Confirmar prompt Flux
    CASE ELSE
        RETURN1 = base_prompt & ", high quality"
        PRINT(RETURN1)  ' Confirmar prompt predeterminado
END SELECT
```
<img src="../img/FIRST_WORFLOW.png" alt="Ejemplo de flujo de trabajo de ajuste de prompts por tipo de modelo" width="50%">

---

## 💡 Uso básico

### Configuración del nodo

El **nodo EasyScripter** tiene la siguiente configuración:

#### Entradas
- `script`: Escribe un script estilo VBA (obligatorio)
- `VAL1_int`, `VAL1_float`: Entrada numérica 1 (se suma y está disponible como `VAL1`)
- `VAL2_int`, `VAL2_float`: Entrada numérica 2 (se suma y está disponible como `VAL2`)
- `TXT1`, `TXT2`: Entrada de texto
- `any_input`: Entrada tipo ANY (acepta MODEL, CLIP, VAE, etc.)

#### Salidas
- `RETURN1_int`, `RETURN1_float`, `RETURN1_text`: Valor de retorno principal (salida simultánea en 3 formatos)
- `RETURN2_int`, `RETURN2_float`, `RETURN2_text`: Valor de retorno secundario (salida simultánea en 3 formatos)
- `relay_output`: Salida de bypass completo de `any_input` (controlable con la variable RELAY_OUTPUT)

![Ejemplo de conexión básica del nodo EasyScripter](../img/SimpleConnection.png)

### Ejemplos simples
Copia y pega en el flujo de trabajo de arriba

#### Cálculo básico
```vba
' Suma dos valores y devuelve el resultado
result = VAL1 + VAL2
PRINT(result)  ' Confirmar resultado del cálculo
RETURN1 = result
```

#### Concatenación de cadenas
```vba
' Combina dos textos
combined = TXT1 & " " & TXT2
PRINT(combined)  ' Confirmar resultado de combinación
RETURN1 = combined
```

#### Ramificación condicional
```vba
' Cambia el mensaje según el valor
IF VAL1 > 10 THEN
    RETURN1 = "grande"
    PRINT(RETURN1)  ' Confirmar resultado de la ramificación
ELSE
    RETURN1 = "pequeño"
    PRINT(RETURN1)  ' Confirmar resultado de la ramificación
END IF
```

**Sentencias IF de una línea y EXIT** (v2.1.1 en adelante):
```vba
' Retorno temprano dentro de funciones
FUNCTION Validate(value)
    IF value < 0 THEN EXIT FUNCTION  ' Terminar inmediatamente si es negativo
    Validate = value * 2
END FUNCTION

' Salida temprana del bucle
FOR i = 1 TO 100
    IF i > 50 THEN EXIT FOR  ' Terminar bucle cuando supera 50
    sum = sum + i
NEXT

RETURN1 = sum
RETURN2 = i
```

#### Selección aleatoria
```vba
' Selección aleatoria de CSV (cuando se omite el índice)
styles = "realistic, anime, oil painting, watercolor"
selected = PICKCSV(styles)  ' Selección aleatoria
PRINT(selected)  ' Confirmar resultado de selección
RETURN1 = selected

' O especificar un índice específico (basado en 1)
' selected = PICKCSV(styles, 2)  ' Selecciona el segundo "anime"
' PRINT(selected)  ' "anime"
```

---

## 🛠️ Serie de cargadores u5

Grupo de nodos cargadores con función de salida de nombre de archivo para usar en combinación con EasyScripter:

- **u5 Checkpoint Loader** - MODEL, CLIP, VAE + salida de nombre de archivo
- **u5 LoRA Loader** - Aplicación de modelo + LoRA + salida de nombre de archivo
- **u5 VAE Loader** - VAE + salida de nombre de archivo
- **u5 ControlNet Loader** - ControlNet + salida de nombre de archivo
- **u5 CLIP Vision Loader** - CLIP Vision + salida de nombre de archivo
- **u5 Style Model Loader** - StyleModel + salida de nombre de archivo
- **u5 GLIGEN Loader** - GLIGEN + salida de nombre de archivo
- **u5 UNET Loader** - UNET + salida de nombre de archivo
- **u5 CLIP Loader** - CLIP + salida de nombre de archivo

Todos los cargadores u5 tienen las siguientes funciones comunes:
- Especificación de búsqueda de nombre de archivo mediante el campo `text_input` (coincidencia parcial) para cargar
- Salida del nombre de archivo cargado como texto mediante la salida `filename`

---

## 🔍 Solución de problemas

### El script da error
- Al usar la función PRINT para confirmar la salida de depuración, usa la forma de función con paréntesis `PRINT("LOG", valor)`
  - **Nota**: La forma de sentencia de VBA (`PRINT "LOG", valor`) no está soportada
- Verifica errores ortográficos de nombres de variables y mayúsculas/minúsculas

### No se encuentra la función
- Verifica la ortografía del nombre de la función
- Confirma el nombre correcto de la función en el [Índice de funciones integradas](00_index.md)

### El valor de retorno es diferente al esperado
- Al usar la función PRINT para confirmar valores intermedios, llámala también en forma con paréntesis (`PRINT("valor intermedio:", variable)`)
- Verifica si se necesita conversión de tipo (CINT, CDBL, CSTR)

### El aspecto es extraño
- Prueba guardar el flujo de trabajo y actualizar con F5

---

## 📜 Licencia

MIT License

Copyright (c) 2025 u5dev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 📝 Historial de actualizaciones

Para un historial detallado de versiones, consulta [CHANGELOG.md](CHANGELOG.md).

---

## 🙏 Agradecimientos

Agradecemos a toda la comunidad de ComfyUI.
