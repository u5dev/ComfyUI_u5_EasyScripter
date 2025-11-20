# Model Functions Reference

[← Back to Built-in Functions Index](00_index.md)

## Overview

Model functions provide automatic determination of optimal resolution for various generation models used in ComfyUI. Automatically calculates the optimal Latent space size for a model based on model name and aspect ratio.

Supported Models: Stable Diffusion 1.5/2.1/XL, SD3/3.5, FLUX.1, Hunyuan-DiT, Kandinsky, PixArt, Playground, etc. (30+ models)

---

## Model Function List

### OPTIMAL_LATENT(model_hint, width, height)

**Description**: Automatically determines optimal Latent size from model name and aspect ratio

**Arguments**:
- model_hint - Model name hint (string)
  - Examples: "SDXL", "SD 1.5", "Flux", "Hunyuan"
- width - Desired width (integer)
- height - Desired height (integer)

**Return Value**: Array of optimal Latent size [width, height]

**Supported Models**: SD1.5, SD2.1, SDXL, SD3/3.5, Hunyuan-DiT, FLUX.1, Kandinsky, PixArt, Playground, etc. (30+ models)

**Example**:
```vba
' Get optimal 4:3 resolution for SDXL
DIM result
result = OPTIMAL_LATENT("SDXL", 4, 3)
PRINT(result)  ' Intermediate result check
PRINT("Optimal Size: " & result(0) & "x" & result(1))
' Output: "Model: SDXL 1.0 (base) | Optimal: 1152x896 (4:3)"
' Output: "{0: 1152, 1: 896}"
' Output: "Optimal Size: 1152x896"

' Get 16:9 for Stable Diffusion 1.5
result = OPTIMAL_LATENT("SD 1.5", 16, 9)
PRINT(result)  ' Intermediate result check
PRINT(result(0) & "x" & result(1))
' Output: "Model: blue_pencil (SD1.5) | Optimal: 704x384 (11:6)"
' Output: "{0: 704, 1: 384}"
' Output: "704x384"

' Square for FLUX.1
result = OPTIMAL_LATENT("Flux", 256, 256)
PRINT(result)  ' Intermediate result check
' Output: "Model: FLUX.1 (dev/pro) | Optimal: 1024x1024 (1:1)"
' Output: "{0: 1024, 1: 1024}"
```

---

## Updating Model Data

To add new models, edit `data/model_resolutions.csv`.

**CSV Format**:
```csv
model_key,model_display_name,aliases,version,width,height,aspect_ratio,description
new_model,New Model v1.0,newmodel|new,1.0,1024,1024,1:1,Description
```

**Note**: New data is reflected after restarting ComfyUI.

---

## Usage Examples

### Optimal Resolution Determination in SDXL Workflow

```vba
' Automatically calculate optimal resolution for SDXL from user input resolution
DIM user_width
DIM user_height
user_width = 1920  ' Full HD width
PRINT(user_width)  ' Intermediate result check
' Output: "1920"
user_height = 1080 ' Full HD height
PRINT(user_height)  ' Intermediate result check
' Output: "1080"

DIM optimal
optimal = OPTIMAL_LATENT("SDXL", user_width, user_height)
PRINT(optimal)  ' Intermediate result check
' Output: "Model: SDXL 1.0 (base) | Optimal: 1344x768 (16:9)"
' Output: "{0: 1344, 1: 768}"

' Get optimal width and height from optimal array
DIM final_width
DIM final_height
final_width = optimal(0)
PRINT(final_width)  ' Intermediate result check
' Output: "1344"
final_height = optimal(1)
PRINT(final_height)  ' Intermediate result check
' Output: "768"

PRINT("Input: " & user_width & "x" & user_height)
PRINT("SDXL Optimal: " & final_width & "x" & final_height)
' Output: "Input: 1920x1080"
' Output: "SDXL Optimal: 1344x768"
```

### Generic Script Supporting Multiple Models

```vba
' Get optimal resolution for each model just by changing model name
DIM model_name
DIM aspect_width
DIM aspect_height

model_name = "Flux"
PRINT(model_name)  ' Intermediate result check
' Output: "Flux"
aspect_width = 1024
PRINT(aspect_width)  ' Intermediate result check
' Output: "1024"
aspect_height = 1024
PRINT(aspect_height)  ' Intermediate result check
' Output: "1024"

DIM result
result = OPTIMAL_LATENT(model_name, aspect_width, aspect_height)
PRINT(result)  ' Intermediate result check
' Output: "Model: FLUX.1 (dev/pro) | Optimal: 1024x1024 (1:1)"
' Output: "{0: 1024, 1: 1024}"
PRINT(model_name & " -> " & result(0) & "x" & result(1))
' Output: "Flux -> 1024x1024"

' Change to SD1.5
model_name = "SD 1.5"
PRINT(model_name)  ' Intermediate result check
' Output: "SD 1.5"
result = OPTIMAL_LATENT(model_name, aspect_width, aspect_height)
PRINT(result)  ' Intermediate result check
' Output: "Model: blue_pencil (SD1.5) | Optimal: 512x512 (1:1)"
' Output: "{0: 512, 1: 512}"
PRINT(model_name & " -> " & result(0) & "x" & result(1))
' Output: "SD 1.5 -> 512x512"
```

---

[← Back to Built-in Functions Index](00_index.md)
