# 实用工具函数参考

[← 返回内置函数索引](00_index.md)

实用工具函数是辅助脚本开发的便捷函数群，提供调试输出、类型判定、输入处理等功能。

---

## 输出函数

### PRINT(message, ...)

**说明**: 将值输出到文本区域（用于调试）

**参数**:
- message - 输出的值（可指定多个）

**返回值**: 无（追加到PRINT变量）

**示例**:
```vba
' 跟踪变量值
value = VAL1 * 2
PRINT("value after multiplication: " & value)

' 循环进度
FOR i = 1 TO 10
    PRINT("Loop iteration: " & i)
    ' 处理...
NEXT

' 确认条件分支
condition = VAL1 > 100
IF condition THEN
    PRINT("Condition was TRUE")
ELSE
    PRINT("Condition was FALSE")
END IF

' 同时输出多个值
PRINT("VAL1:", VAL1, "VAL2:", VAL2)
result = VAL1 + VAL2
PRINT("计算结果:", result)
```

**注意**:
- PRINT函数输出的内容显示在节点下部的文本区域
- 方便在调试时确认变量值

---

### OUTPUT(arg, [path], [flg])

**说明**: 将文本、数值、数组、图像、二进制数据输出到文件

**参数**:
- arg (Any) - 输出的值（字符串、数值、数组、torch.Tensor、bytes）
- path (str, optional) - 输出路径（相对路径，默认=""）
- flg (str, optional) - 动作模式（"NEW"=新建/避免重复，"ADD"=追加，默认="NEW"）

**返回值**: str - 输出文件的绝对路径（失败时为空字符串）

**功能**:
1. **文本输出**: 将字符串、数值、数组输出为文本文件
2. **图像输出**: 将torch.Tensor（ComfyUI图像数据）输出为PNG/JPEG等
3. **二进制输出**: 将bytes型数据输出为二进制文件
4. **NEW模式**: 重复时自动添加`_0001`, `_0002`...
5. **ADD模式**: 追加到现有文件
6. **安全性**: 拒绝绝对路径·UNC路径（仅允许相对路径）
7. **子目录**: 自动递归创建
8. **扩展名自动补全**: `.txt`（文本）、`.png`（图像）

**保留变量对应**:
- `OUTPUT("TXT1", "output.txt")` → 输出输入接口TXT1的值
- 对应TXT1, TXT2, ANY_INPUT

**示例**:
```vba
' 文本输出
path = OUTPUT("Hello World", "output.txt", "NEW")
PRINT("输出路径: " & path)

' 数值输出
path = OUTPUT(12345, "number.txt")
PRINT("输出路径: " & path)

' 数组输出
ARR = ARRAY("apple", "banana", "cherry")
path = OUTPUT(ARR, "fruits.txt")
PRINT("输出路径: " & path)

' 从保留变量输出
path = OUTPUT("TXT1", "user_input.txt")
PRINT("输出TXT1的值: " & path)

' 追加模式
path1 = OUTPUT("First Line", "log.txt", "NEW")
PRINT("新建: " & path1)
path2 = OUTPUT("Second Line", "log.txt", "ADD")
PRINT("追加: " & path2)

' 创建子目录
path = OUTPUT("data", "subdir/data.txt")
PRINT("包含子目录创建: " & path)

' 避免重复
path1 = OUTPUT("content", "file.txt", "NEW")
PRINT("第1次: " & path1)  ' file.txt
path2 = OUTPUT("content", "file.txt", "NEW")
PRINT("第2次: " & path2)  ' file_0001.txt
```

**安全限制**:
- 拒绝绝对路径（`C:\...`, `/...`）
- 拒绝UNC路径（`\\server\...`）
- 仅允许相对路径

**输出目录**:
- ComfyUI环境: `ComfyUI/output/` 下
- 测试环境: 当前目录下

---

### INPUT(path)

**说明**: 从ComfyUI输出文件夹读取文件（OUTPUT函数的对称函数）

**参数**:
- path (str, 必须) - ComfyUI输出文件夹的相对路径
  - 禁止绝对路径（`C:\...`, `/...`）
  - 禁止UNC路径（`\\server\...`）
  - 仅允许相对路径

**返回值**: 动态类型（根据文件格式自动判定）
- 文本文件 (`.txt`, `.md`) → str型
- JSON数值 → float型
- JSON数组 → list型
- 图像文件 (`.png`, `.jpg`, `.jpeg`, `.bmp`, `.webp`) → torch.Tensor型（ComfyUI兼容）
- 其他 → bytes型（二进制）

**功能**:
1. **自动类型判定**: 根据文件格式以最优类型读取
2. **图像数据对应**: 以torch.Tensor格式可直接连接到ComfyUI图像节点
3. **JSON支持**: 自动解析数值·数组的JSON
4. **安全性**: 拒绝绝对路径·UNC路径（仅允许相对路径）
5. **错误处理**: 文件未找到时警告PRINT并返回None

**读取源目录**:
- ComfyUI环境: `ComfyUI/output/` 下
- 测试环境: 当前目录下

**示例**:
```vba
' 读取文本文件
prompt = INPUT("prompts/positive.txt")
PRINT("读取的提示词: " & prompt)
RETURN1 = prompt

' 读取JSON数组
dataArray = INPUT("data_array.json")
PRINT("数组元素数: " & (UBOUND(dataArray[]) + 1))

' 读取图像（torch.Tensor格式）
refImage = INPUT("reference_images/style_sample.png")
' refImage可直接连接到ComfyUI的图像输入节点

' 从子目录读取
configText = INPUT("configs/model_settings.txt")
PRINT("设置内容: " & configText)
```

**安全限制**:
- 拒绝绝对路径（`C:\...`, `/...`）
- 拒绝UNC路径（`\\server\...`）
- 仅允许相对路径

**与OUTPUT函数的对称性**:
- OUTPUT: 数据 → 保存文件
- INPUT: 读取文件 → 数据
- 两函数都仅允许相对路径，拒绝绝对路径·UNC路径

#### INPUT函数与RELAY_OUTPUT的联动

要将INPUT函数读取的图像或数据传递给后续节点，请使用RELAY_OUTPUT变量。

```vba
' 从文本文件读取提示词并传递给后续的CLIPTextEncode
PROMPT_TEXT = INPUT("prompts/positive.txt")
RELAY_OUTPUT = PROMPT_TEXT

' 或读取图像文件并传递给后续的LoadImage
IMG1 = INPUT("reference_images/base.png")
RELAY_OUTPUT = IMG1
```

**RETURN1/RETURN2 vs RELAY_OUTPUT**:
- RETURN1/RETURN2: 仅限原始类型 (INT, FLOAT, STRING)
- RELAY_OUTPUT: 支持ANY类型 (torch.Tensor, list, dict等对象也可以)

**注意**:
- 如果文件不存在，将通过PRINT显示警告消息并返回None
- 读取大文件(图像等)可能需要一些时间

---

### ISFILEEXIST(path, [flg])

**说明**: 文件存在检查和扩展信息获取（_NNNN搜索、图像大小、文件大小）

**参数**:
- path (str, 必须) - 检查的文件路径（相对路径）
- flg (str, optional) - 动作标志（默认=""）
  - `"SEARCH_NNNN"`: 搜索`filename_0001.ext`形式的文件
  - `"SIZE"`: 返回图像大小和文件大小

**返回值**:
- flg=""（默认）: int - 1（存在）/ 0（不存在）
- flg="SEARCH_NNNN": str - 找到的文件路径（未找到时空字符串）
- flg="SIZE": dict - 图像和文件信息

**功能**:
1. **基本存在检查**: 检查文件是否存在
2. **_NNNN搜索**: 搜索带序号的文件
3. **图像大小获取**: 获取图像宽度/高度
4. **文件大小获取**: 获取文件大小（字节）
5. **安全性**: 仅允许相对路径

**示例**:
```vba
' 基本存在检查
exists = ISFILEEXIST("output.txt")
IF exists = 1 THEN
    PRINT("文件存在")
ELSE
    PRINT("文件不存在")
END IF

' _NNNN搜索
foundPath = ISFILEEXIST("image.png", "SEARCH_NNNN")
IF foundPath <> "" THEN
    PRINT("找到: " & foundPath)
ELSE
    PRINT("未找到")
END IF

' 图像大小获取
info = ISFILEEXIST("sample.png", "SIZE")
PRINT("宽度: " & info["width"])
PRINT("高度: " & info["height"])
PRINT("文件大小: " & info["file_size"] & " bytes")
```

---

### VRAMFREE([min_free_vram_gb])

**说明**: 释放VRAM和RAM的函数。执行模型卸载、缓存清除、垃圾回收。

**⚠️ WARNING**: 模型卸载是一项敏感操作。根据执行时机，可能会在工作流执行期间引起意外行为。使用时请充分注意。

**语法**:
```vba
result = VRAMFREE(min_free_vram_gb)
```

**参数**:
- `min_free_vram_gb` (float, 可选): 执行阈值（GB单位）
  - 如果当前空闲VRAM大于或等于此值，则跳过处理
  - 默认值: 0.0（始终执行）

**返回值**:
dict（执行结果的详细信息）
- `success`: 执行成功标志（bool）
- `message`: 执行结果消息（str）
- `freed_vram_gb`: 已释放VRAM量（float）
- `freed_ram_gb`: 已释放RAM量（float）
- `initial_status`: 执行前的内存状态（dict）
- `final_status`: 执行后的内存状态（dict）
- `actions_performed`: 已执行操作的列表（list）

**使用示例**:
```vba
' 始终执行（无阈值）
result = VRAMFREE(0.0)
PRINT("VRAM freed: " & result["freed_vram_gb"] & " GB")

' 仅在空闲VRAM低于2GB时执行
result = VRAMFREE(2.0)
IF result["success"] = TRUE THEN
    PRINT("Cleanup completed")
ELSE
    PRINT("Cleanup failed")
END IF
```

**执行内容**:
1. 获取初始内存状态
2. 阈值检查（跳过判定）
3. 卸载ComfyUI模型
4. 清除ComfyUI软缓存
5. 清除PyTorch GPU缓存
6. Python垃圾回收（GC）
7. 向ComfyUI prompt_queue设置标志
8. 监视异步刷新（3秒）
9. 计算内存释放量

**注意事项**:
- 在ComfyUI环境外，可用功能受限（limited mode）
- 在不支持CUDA的环境中，可能无法获取VRAM信息
- 由于异步处理，执行完成后可能会有轻微延迟才能释放内存

---

### SLEEP([milliseconds])

**说明**: 暂停处理指定毫秒（睡眠）。用于WHILE()循环的速度控制和处理等待同步。

**参数**:
- milliseconds (FLOAT, 可选): 睡眠时间（毫秒），默认: 10ms

**返回值**: 无（内部返回0.0）

**语法**:
```vba
SLEEP(milliseconds)
```

**使用示例**:
```vba
' 默认10ms睡眠
SLEEP()

' 0.5秒睡眠
SLEEP(500)

' WHILE()循环的速度控制（降低CPU使用率）
VAL1 = 0
WHILE VAL1 < 100
    VAL1 = VAL1 + 1
    SLEEP(100)  ' 等待100ms
WEND
PRINT("循环完成: " & VAL1)
RETURN1 = VAL1

' 处理等待同步
PRINT("处理开始")
result = VAL1 * 2
SLEEP(1000)  ' 等待1秒
PRINT("处理完成: " & result)
RETURN1 = result
```

**主要用途**:
1. **WHILE()循环的速度控制**: 降低CPU使用率，减轻系统负载
2. **处理等待同步**: 等待外部系统响应或有意延迟处理
3. **调试**: 为观察处理流程而暂停

**ComfyUI集成**:
- 与ComfyUI的基于线程的排队控制（ScriptExecutionQueue）协同工作
- 通过time.sleep()进行同步阻塞执行
- ScriptExecutionQueue保证多个EasyScripter节点同时执行时的安全性

**注意事项**:
- SLEEP()会阻塞当前线程（不执行其他处理）
- 不使用异步处理（asyncio）（ComfyUI不是事件循环驱动）
- 长时间睡眠会增加整个工作流的执行时间

---

## 图像处理函数

### IMAGETOBYTEARRAY(image_input, [max_size], [format], [return_format])

**说明**: 将IMAGE/文件路径转换为图像JSON数组

**参数**:
- image_input - 图像数据或文件路径
- max_size (int, optional) - 最大尺寸（默认=512）
- format (str, optional) - 图像格式（默认="PNG"）
- return_format (str, optional) - 返回格式（默认="json"）

**返回值**: JSON数组字符串或Python列表

**示例**:
```vba
jsonArray = IMAGETOBYTEARRAY("sample.png", 512, "PNG", "json")
PRINT(jsonArray)
```

---

### IMAGETOBASE64(image_input, [max_size], [format], [return_format])

**说明**: 将IMAGE/文件路径转换为Base64编码（用于Vision API）

**参数**:
- image_input - 图像数据或文件路径
- max_size (int, optional) - 最大尺寸（默认=512）
- format (str, optional) - 图像格式（默认="PNG"）
- return_format (str, optional) - 返回格式（默认="base64"）

**返回值**: Base64编码字符串或数据URI

**示例**:
```vba
base64str = IMAGETOBASE64("sample.png", 512, "PNG", "base64")
PRINT(base64str)
```

---

## ANY型数据获取函数

### GETANYWIDTH([any_data])

**说明**: 获取IMAGE/LATENT型数据的宽度（像素数）

**参数**:
- any_data (optional) - ANY型数据（省略时使用ANY_INPUT）

**返回值**: int - 宽度（像素）

**示例**:
```vba
width = GETANYWIDTH()
PRINT("宽度: " & width)
```

---

### GETANYHEIGHT([any_data])

**说明**: 获取IMAGE/LATENT型数据的高度（像素数）

**参数**:
- any_data (optional) - ANY型数据（省略时使用ANY_INPUT）

**返回值**: int - 高度（像素）

**示例**:
```vba
height = GETANYHEIGHT()
PRINT("高度: " & height)
```

---

### GETANYTYPE([any_data])

**说明**: 判定ANY型数据的类型名

**参数**:
- any_data (optional) - ANY型数据（省略时使用ANY_INPUT）

**返回值**: str - 类型名（"IMAGE", "LATENT", "MASK", "STRING", "INT", "FLOAT", "UNKNOWN"等）

**示例**:
```vba
dataType = GETANYTYPE()
PRINT("数据类型: " & dataType)
```

---

### GETANYVALUEINT([any_data])

**说明**: 从ANY型数据获取整数值

**参数**:
- any_data (optional) - ANY型数据（省略时使用ANY_INPUT）

**返回值**: int - 整数值

**示例**:
```vba
intValue = GETANYVALUEINT()
PRINT("整数值: " & intValue)
```

---

### GETANYVALUEFLOAT([any_data])

**说明**: 从ANY型数据获取浮点数值

**参数**:
- any_data (optional) - ANY型数据（省略时使用ANY_INPUT）

**返回值**: float - 浮点数值

**示例**:
```vba
floatValue = GETANYVALUEFLOAT()
PRINT("浮点数值: " & floatValue)
```

---

### GETANYSTRING([any_data])

**说明**: 从ANY型数据获取字符串

**参数**:
- any_data (optional) - ANY型数据（省略时使用ANY_INPUT）

**返回值**: str - 字符串

**示例**:
```vba
strValue = GETANYSTRING()
PRINT("字符串值: " & strValue)
```

---

## 类型判定函数

### ISNUMERIC(value)

**说明**: 判断值是否为数值

**参数**:
- value - 检查的值

**返回值**: 1（数值）或0

**示例**:
```vba
result = ISNUMERIC("123")
PRINT(result)  ' 1
```

---

### ISDATE(value)

**说明**: 判断值是否可解析为日期

**参数**:
- value - 检查的值

**返回值**: 1（日期）或0

**示例**:
```vba
result = ISDATE("2024-01-15")
PRINT(result)  ' 1
```

---

### ISARRAY(variable_name)

**说明**: 判断变量是否为数组

**参数**:
- variable_name - 变量名（字符串）或数组变量引用

**返回值**: 1（数组）或0

**示例**:
```vba
REDIM ARR, 10
result = ISARRAY(ARR[])
PRINT(result)  ' 1
```

---

### TYPE(value)

**说明**: 以字符串形式返回变量类型

**参数**:
- value - 检查的值

**返回值**: str - 类型名

**示例**:
```vba
typeStr = TYPE(123)
PRINT(typeStr)  ' "int"
```

---

## 实用示例

### 调试输出的应用

```vba
' 确认处理的各个阶段的值
originalValue = VAL1
PRINT("原始值: " & originalValue)

processedValue = originalValue * 2
PRINT("2倍后: " & processedValue)

finalValue = processedValue + 10
PRINT("最终值: " & finalValue)

RETURN1 = finalValue
PRINT("赋值给RETURN1: " & RETURN1)
```

### 输入值验证

```vba
' 检查是否为数值后再处理
IF ISNUMERIC(TXT1) THEN
    number = CDBL(TXT1)
    PRINT("将TXT1转换为数值: " & number)
    result = number * VAL1
    PRINT("计算结果: " & result)
    RETURN1 = result
    PRINT("赋值给RETURN1: " & RETURN1)
ELSE
    PRINT("错误: TXT1不是数值")
    RETURN1 = 0
    PRINT("将默认值赋给RETURN1: " & RETURN1)
END IF
```

### 根据类型进行处理分支

```vba
' 根据数据类型改变处理
myData = VAL1
dataType = TYPE(myData)
PRINT("TYPE(myData) = " & dataType)

IF dataType = "NUMBER" THEN
    result = myData * 2
    PRINT("数值处理: " & result)
ELSEIF dataType = "STRING" THEN
    result = UCASE(myData)
    PRINT("字符串处理: " & result)
ELSEIF dataType = "ARRAY" THEN
    count = UBOUND(myData[]) + 1
    PRINT("数组处理: 元素数=" & count)
    FOR i = 0 TO UBOUND(myData[])
        PRINT("  [" & i & "] = " & myData[i])
    NEXT
ELSE
    PRINT("不支持的类型: " & dataType)
END IF
```

---

[← 返回内置函数索引](00_index.md)
