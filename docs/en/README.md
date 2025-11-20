# u5 EasyScripter Node

**Languages**: [日本語](../../README.md) | [English](README.md) | [中文](../zh/README.md) | [Español](../es/README.md) | [Français](../fr/README.md) | [Deutsch](../de/README.md)

---

## What is this?
- A custom node that allows you to **run simple VBA-like scripts** on ComfyUI
- Supports conditional branching, prompt generation, loops, external API calls, and various built-in functions
- **Almost all functions come with copy-paste ready samples**, so no programming experience required
- Also includes enhanced built-in versions of sequential nodes and memory release tools published elsewhere

```
Created because standard nodes and individual nodes made configurations cumbersome and fine-grained control difficult
```

---

## Recommended Features & Use Cases
 - Simply drag and drop workflow screenshot images into ComfyUI and use them immediately

### Automatically create various variations
- Tired of thinking up prompts every time. Just quickly generate a batch like a slideshow!
```vba
' Base prompt + randomly switch expressions and poses each time to create prompts
' → "base prompt" & "," & RNDCSV("pose candidate CSV") & "," & RNDCSV("expression candidate CSV")

RETURN1 = "woman, a girl, nurse, with a bandage, pale skin, green eyes, pink hair, blunt bangs,upper body, full body shot, masterpiece, best quality, high quality," & RNDCSV("looking at viewer, looking away, looking back, wink, making a peace sign, making a heart with hands, making a thumbs up, waving at the camera") & "," & RNDCSV("blush, smiling, embarrassed, sleepy, serious expression, fear")
```
<img src="../img/AUTO_SLIDESHOW.png" alt="Example of prompt generation script in EasyScripter node" width="80%"><br>
  ↓<br>
  Just paste one line<br>
  ↓<br>
<img src="../img/SLIDES.png" alt="Slideshow of automatically generated variation images" width="100%">

### Automatically adjust model-specific Latent (latent) size in one shot
- Tired of "what resolution for SDXL" every time!
```vba
result = OPTIMAL_LATENT("SDXL", 4, 3) ' Automatically adjusted to 1152x896
RETURN1 = RESULT[0] '1152
RETURN2 = RESULT[1] '896
```
<img src="../img/OPTIMAL_LATENT.png" alt="Example of automatic model-optimized resolution adjustment with OPTIMAL_LATENT function" width="80%"><br>



**Just paste into the script window at the bottom of the node and it instantly becomes a professional node with special features**

---




## 📖 Documentation

See the following for detailed documentation:


- **[📖 Scripting Language Reference](01_syntax_reference.md)** - Complete guide to grammar and control structures
- **[🔧 Built-in Functions Reference](00_index.md)** - Complete reference for 100+ built-in functions
- **[🌟 Please Support Us](CONTENTS.md)** - More practical and useful examples, abundant workflow images, detailed explanations


---

## u5 EasyScripter Solutions

**One Node, Infinite Possibilities** - u5 EasyScripter is a general-purpose scripting engine running on ComfyUI:

- ✅ **Replaces 10+ dedicated nodes**: Text processing, math calculations, conditional logic, random generation
- ✅ **Accelerates batch processing**: Automatic parameter sweeps, intelligent variation generation
- ✅ **Enhances prompt engineering**: Dynamic weight adjustment, conditional modifications, smart variations
- ✅ **Streamlines workflows**: Clean graphs, fast loading, easy sharing
- ✅ **Scalable**: From simple calculations to complex automation algorithms
- ✅ **Concurrent execution guard**: Safe queuing without hangs even with simultaneous multi-node execution
- ✅ **Multilingual support**: Error messages and debug output in Japanese and English



---

## ⚡ Quick Start

### Installation

```bash
# Clone into ComfyUI's custom_nodes directory
git clone https://github.com/u5dev/ComfyUI_u5_EasyScripter.git
```

### Your First Smart Workflow
- Intelligent adjustments based on prompt rules required by model type

```vba

model_type = TXT1  ' Connect model name ("sdxl" or "Flux")
PRINT(model_type)  ' Confirm model type
base_prompt = "beautiful landscape"

SELECT CASE model_type
    CASE "sdxl"
        RETURN1 = "(" & base_prompt & ", ultra-detailed wide landscape, crisp daylight photography, shot on full-frame DSLR, high dynamic range, 8k uhd, professional photography:1.2)"
        PRINT(RETURN1)  ' Confirm SDXL prompt
    CASE "flux"
        RETURN1 = "(" & base_prompt & "moody cinematic wide shot of a beautiful landscape at golden hour, dramatic backlight haze, soft volumetric light, cinematic lighting:1.1, subtle film grain)"
        PRINT(RETURN1)  ' Confirm Flux prompt
    CASE ELSE
        RETURN1 = base_prompt & ", high quality"
        PRINT(RETURN1)  ' Confirm default prompt
END SELECT
```
<img src="../img/FIRST_WORFLOW.png" alt="Example workflow for model type-specific prompt adjustment" width="50%">


---

## 💡 Basic Usage

### Node Configuration

**EasyScripter Node** has the following configuration:

#### Inputs
- `script`: Write VBA-style script (required)
- `VAL1_int`, `VAL1_float`: Numeric input 1 (summed and available as `VAL1`)
- `VAL2_int`, `VAL2_float`: Numeric input 2 (summed and available as `VAL2`)
- `TXT1`, `TXT2`: Text inputs
- `any_input`: ANY type input (accepts MODEL, CLIP, VAE, etc.)

#### Outputs
- `RETURN1_int`, `RETURN1_float`, `RETURN1_text`: Main return value (output in 3 formats simultaneously)
- `RETURN2_int`, `RETURN2_float`, `RETURN2_text`: Sub return value (output in 3 formats simultaneously)
- `relay_output`: Complete bypass output of `any_input` (controllable with RELAY_OUTPUT variable)


![Basic connection example of EasyScripter node](../img/SimpleConnection.png)



### Simple Examples
Copy and paste into the workflow above

#### Basic Calculation
```vba
' Add two values and return
result = VAL1 + VAL2
PRINT(result)  ' Confirm calculation result
RETURN1 = result
```

#### String Concatenation
```vba
' Combine two texts
combined = TXT1 & " " & TXT2
PRINT(combined)  ' Confirm concatenation result
RETURN1 = combined
```

#### Conditional Branching
```vba
' Change message based on value
IF VAL1 > 10 THEN
    RETURN1 = "Large"
    PRINT(RETURN1)  ' Confirm branch result
ELSE
    RETURN1 = "Small"
    PRINT(RETURN1)  ' Confirm branch result
END IF
```

**One-line IF statements and EXIT statements** (v2.1.1+):
```vba
' Early return within a function
FUNCTION Validate(value)
    IF value < 0 THEN EXIT FUNCTION  ' Exit immediately if negative
    Validate = value * 2
END FUNCTION

' Early loop exit
FOR i = 1 TO 100
    IF i > 50 THEN EXIT FOR  ' Exit loop when exceeds 50
    sum = sum + i
NEXT


RETURN1 = sum
RETURN2 = i
```

#### Random Selection
```vba
' Random selection from CSV (when index is omitted)
styles = "realistic, anime, oil painting, watercolor"
selected = PICKCSV(styles)  ' Random selection
PRINT(selected)  ' Confirm selection result
RETURN1 = selected

' Or specify a specific index (1-based)
' selected = PICKCSV(styles, 2)  ' Select 2nd "anime"
' PRINT(selected)  ' "anime"
```

---

## 🛠️ u5 Loader Series

Loader node series with filename output, to be used with EasyScripter:

- **u5 Checkpoint Loader** - MODEL, CLIP, VAE + filename output
- **u5 LoRA Loader** - Model + LoRA application + filename output
- **u5 VAE Loader** - VAE + filename output
- **u5 ControlNet Loader** - ControlNet + filename output
- **u5 CLIP Vision Loader** - CLIP Vision + filename output
- **u5 Style Model Loader** - StyleModel + filename output
- **u5 GLIGEN Loader** - GLIGEN + filename output
- **u5 UNET Loader** - UNET + filename output
- **u5 CLIP Loader** - CLIP + filename output

All u5 loaders have the following common features:
- Filename search specification by `text_input` field (partial match) for loading
- Output loaded filename as text via `filename` output


---


## 🔍 Troubleshooting

### Script errors
- For debug output with PRINT function, use function form with parentheses `PRINT("LOG", value)`
  - **Note**: VBA statement form (`PRINT "LOG", value`) is not supported
- Check variable name spelling and case

### Function not found
- Check function name spelling
- Verify correct function name in [Built-in Function Index](00_index.md)

### Return value differs from expectation
- For checking intermediate values with PRINT function, also use form with parentheses (`PRINT("Intermediate value:", variable)`)
- Check if type conversion (CINT, CDBL, CSTR) is needed

### Display looks strange
 - Try saving the workflow and refreshing with F5

---

## 📜 License

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

## 📝 Update History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

---

## 🙏 Acknowledgments

Thanks to everyone in the ComfyUI community.

