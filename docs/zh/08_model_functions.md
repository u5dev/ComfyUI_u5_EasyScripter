# 模型函数参考

[← 返回内置函数索引](00_index.md)

## 概述

模型函数提供自动判定ComfyUI中使用的各种生成模型最优分辨率的功能。根据模型名称和纵横比，自动计算该模型的最优Latent空间大小。

支持模型: Stable Diffusion 1.5/2.1/XL、SD3/3.5、FLUX.1、Hunyuan-DiT、Kandinsky、PixArt、Playground等（30种以上）

---

## 模型函数一览

### OPTIMAL_LATENT(model_hint, width, height)

**说明**: 根据模型名称和纵横比自动判定最优Latent大小

**参数**:
- model_hint - 模型名称提示（字符串）
  - 例: "SDXL", "SD 1.5", "Flux", "Hunyuan"
- width - 期望的宽度（整数）
- height - 期望的高度（整数）

**返回值**: 最优Latent大小的数组 [width, height]

**支持模型**: SD1.5, SD2.1, SDXL, SD3/3.5, Hunyuan-DiT, FLUX.1, Kandinsky, PixArt, Playground等（30+模型）

**示例**:
```vba
' 获取SDXL最优4:3分辨率
DIM result
result = OPTIMAL_LATENT("SDXL", 4, 3)
PRINT(result)  ' 确认中间结果
PRINT("Optimal Size: " & result(0) & "x" & result(1))
' 输出: "Model: SDXL 1.0 (base) | Optimal: 1152x896 (4:3)"
' 输出: "{0: 1152, 1: 896}"
' 输出: "Optimal Size: 1152x896"

' 获取Stable Diffusion 1.5的16:9
result = OPTIMAL_LATENT("SD 1.5", 16, 9)
PRINT(result)  ' 确认中间结果
PRINT(result(0) & "x" & result(1))
' 输出: "Model: blue_pencil（SD1.5） | Optimal: 704x384 (11:6)"
' 输出: "{0: 704, 1: 384}"
' 输出: "704x384"

' FLUX.1正方形
result = OPTIMAL_LATENT("Flux", 256, 256)
PRINT(result)  ' 确认中间结果
' 输出: "Model: FLUX.1 (dev/pro) | Optimal: 1024x1024 (1:1)"
' 输出: "{0: 1024, 1: 1024}"
```

---

## 更新模型数据

要添加新模型，请编辑`data/model_resolutions.csv`。

**CSV格式**:
```csv
model_key,model_display_name,aliases,version,width,height,aspect_ratio,description
new_model,New Model v1.0,newmodel|new,1.0,1024,1024,1:1,说明
```

**注意**: 重启ComfyUI后新数据将生效。

---

## 使用示例

### SDXL工作流中的最优分辨率判定

```vba
' 从用户输入分辨率自动计算SDXL最优分辨率
DIM user_width
DIM user_height
user_width = 1920  ' 全高清宽度
PRINT(user_width)  ' 确认中间结果
' 输出: "1920"
user_height = 1080 ' 全高清高度
PRINT(user_height)  ' 确认中间结果
' 输出: "1080"

DIM optimal
optimal = OPTIMAL_LATENT("SDXL", user_width, user_height)
PRINT(optimal)  ' 确认中间结果
' 输出: "Model: SDXL 1.0 (base) | Optimal: 1344x768 (16:9)"
' 输出: "{0: 1344, 1: 768}"

' 从optimal数组获取最优宽度和高度
DIM final_width
DIM final_height
final_width = optimal(0)
PRINT(final_width)  ' 确认中间结果
' 输出: "1344"
final_height = optimal(1)
PRINT(final_height)  ' 确认中间结果
' 输出: "768"

PRINT("Input: " & user_width & "x" & user_height)
PRINT("SDXL Optimal: " & final_width & "x" & final_height)
' 输出: "Input: 1920x1080"
' 输出: "SDXL Optimal: 1344x768"
```

### 支持多模型的通用脚本

```vba
' 仅更改模型名称即可获取各模型的最优分辨率
DIM model_name
DIM aspect_width
DIM aspect_height

model_name = "Flux"
PRINT(model_name)  ' 确认中间结果
' 输出: "Flux"
aspect_width = 1024
PRINT(aspect_width)  ' 确认中间结果
' 输出: "1024"
aspect_height = 1024
PRINT(aspect_height)  ' 确认中间结果
' 输出: "1024"

DIM result
result = OPTIMAL_LATENT(model_name, aspect_width, aspect_height)
PRINT(result)  ' 确认中间结果
' 输出: "Model: FLUX.1 (dev/pro) | Optimal: 1024x1024 (1:1)"
' 输出: "{0: 1024, 1: 1024}"
PRINT(model_name & " -> " & result(0) & "x" & result(1))
' 输出: "Flux -> 1024x1024"

' 更改为SD1.5
model_name = "SD 1.5"
PRINT(model_name)  ' 确认中间结果
' 输出: "SD 1.5"
result = OPTIMAL_LATENT(model_name, aspect_width, aspect_height)
PRINT(result)  ' 确认中间结果
' 输出: "Model: blue_pencil（SD1.5） | Optimal: 512x512 (1:1)"
' 输出: "{0: 512, 1: 512}"
PRINT(model_name & " -> " & result(0) & "x" & result(1))
' 输出: "SD 1.5 -> 512x512"
```

---

[← 返回内置函数索引](00_index.md)
