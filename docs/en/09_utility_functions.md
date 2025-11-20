# Utility Functions Reference

[← Back to Built-in Functions Index](00_index.md)

Utility functions are a set of convenient functions that support script development, including debug output, type detection, and input processing.

---

## Output Functions

### PRINT(message, ...)

**Description**: Outputs values to text area (for debugging)

**Arguments**:
- message - Value to output (multiple values can be specified)

**Return Value**: None (appended to PRINT variable)

**Example**:
```vba
' Track variable values
value = VAL1 * 2
PRINT("value after multiplication: " & value)

' Loop progress
FOR i = 1 TO 10
    PRINT("Loop iteration: " & i)
    ' Processing...
NEXT

' Check conditionals
condition = VAL1 > 100
IF condition THEN
    PRINT("Condition was TRUE")
ELSE
    PRINT("Condition was FALSE")
END IF

' Output multiple values simultaneously
PRINT("VAL1:", VAL1, "VAL2:", VAL2)
result = VAL1 + VAL2
PRINT("Calculation result:", result)
```

**Note**:
- Content output by PRINT function is displayed in text area below the node
- Useful for checking variable values during debugging

---

### OUTPUT(arg, [path], [flg])

**Description**: Outputs text, numbers, arrays, images, binary data to file

**Arguments**:
- arg (Any) - Value to output (string, number, array, torch.Tensor, bytes)
- path (str, optional) - Output path (relative path, default="")
- flg (str, optional) - Operation mode ("NEW"=new/avoid duplicates, "ADD"=append, default="NEW")

**Return Value**: str - Absolute path of output file (empty string on failure)

**Features**:
1. **Text output**: Outputs strings, numbers, arrays as text files
2. **Image output**: Outputs torch.Tensor (ComfyUI image data) as PNG/JPEG etc.
3. **Binary output**: Outputs bytes type data as binary files
4. **NEW mode**: Automatically appends `_0001`, `_0002`... on duplicates
5. **ADD mode**: Appends to existing file
6. **Security**: Rejects absolute paths/UNC paths (allows relative paths only)
7. **Subdirectories**: Automatic recursive creation
8. **Extension auto-completion**: `.txt` (text), `.png` (image)

**Reserved Variable Support**:
- `OUTPUT("TXT1", "output.txt")` → Outputs TXT1 input socket value
- Supports TXT1, TXT2, ANY_INPUT

**Example**:
```vba
' Text output
path = OUTPUT("Hello World", "output.txt", "NEW")
PRINT("Output to: " & path)

' Numeric output
path = OUTPUT(12345, "number.txt")
PRINT("Output to: " & path)

' Array output
ARR = ARRAY("apple", "banana", "cherry")
path = OUTPUT(ARR, "fruits.txt")
PRINT("Output to: " & path)

' Output from reserved variable
path = OUTPUT("TXT1", "user_input.txt")
PRINT("TXT1 value output: " & path)

' Append mode
path1 = OUTPUT("First Line", "log.txt", "NEW")
PRINT("New creation: " & path1)
path2 = OUTPUT("Second Line", "log.txt", "ADD")
PRINT("Appended: " & path2)

' Subdirectory creation
path = OUTPUT("data", "subdir/data.txt")
PRINT("Created with subdirectory: " & path)

' Duplicate avoidance
path1 = OUTPUT("content", "file.txt", "NEW")
PRINT("1st time: " & path1)  ' file.txt
path2 = OUTPUT("content", "file.txt", "NEW")
PRINT("2nd time: " & path2)  ' file_0001.txt
```

**Security Restrictions**:
- Absolute paths (`C:\...`, `/...`) rejected
- UNC paths (`\\server\...`) rejected
- Relative paths only allowed

**Output Directory**:
- ComfyUI environment: Under `ComfyUI/output/`
- Test environment: Under current directory

---

### INPUT(path)

**Description**: Reads file from ComfyUI output folder (symmetric function to OUTPUT)

**Arguments**:
- path (str, required) - Relative path from ComfyUI output folder
  - Absolute paths (`C:\...`, `/...`) prohibited
  - UNC paths (`\\server\...`) prohibited
  - Relative paths only allowed

**Return Value**: Dynamic type (automatically determined by file format)
- Text files (`.txt`, `.md`) → str type
- JSON numbers → float type
- JSON arrays → list type
- Image files (`.png`, `.jpg`, `.jpeg`, `.bmp`, `.webp`) → torch.Tensor type (ComfyUI compatible)
- Others → bytes type (binary)

**Features**:
1. **Automatic type detection**: Reads with optimal type according to file format
2. **Image data support**: torch.Tensor format can be directly connected to ComfyUI image nodes
3. **JSON support**: Automatic parsing of numeric/array JSON
4. **Security**: Rejects absolute paths/UNC paths (allows relative paths only)
5. **Error handling**: Warns and returns None if file not found

**Source Directory**:
- ComfyUI environment: Under `ComfyUI/output/`
- Test environment: Under current directory

**Example**:
```vba
' Read text file
prompt = INPUT("prompts/positive.txt")
PRINT("Loaded prompt: " & prompt)
RETURN1 = prompt

' Read JSON array
dataArray = INPUT("data_array.json")
PRINT("Array element count: " & (UBOUND(dataArray[]) + 1))

' Read image (torch.Tensor format)
refImage = INPUT("reference_images/style_sample.png")
' refImage can be directly connected to ComfyUI image input nodes

' Read from subdirectory
configText = INPUT("configs/model_settings.txt")
PRINT("Config content: " & configText)
```

**Security Restrictions**:
- Absolute paths (`C:\...`, `/...`) rejected
- UNC paths (`\\server\...`) rejected
- Relative paths only allowed

#### Coordination between INPUT Function and RELAY_OUTPUT

To pass images or data loaded with INPUT function to subsequent nodes, use RELAY_OUTPUT variable.

```vba
' Read prompt from text file and pass to subsequent CLIPTextEncode
PROMPT_TEXT = INPUT("prompts/positive.txt")
RELAY_OUTPUT = PROMPT_TEXT

' Or read image file and pass to subsequent LoadImage
IMG1 = INPUT("reference_images/base.png")
RELAY_OUTPUT = IMG1
```

**RETURN1/RETURN2 vs RELAY_OUTPUT**:
- RETURN1/RETURN2: Primitive types only (INT, FLOAT, STRING)
- RELAY_OUTPUT: Supports ANY type (objects like torch.Tensor, list, dict)

**Note**:
- If file does not exist, warns with PRINT message and returns None
- Reading large files (images etc.) may take time

---

### ISFILEEXIST(path, [flg])

**Description**: File existence check and extended information retrieval in ComfyUI output folder

**Arguments**:
- path (str, required) - Relative path from ComfyUI output folder
  - Absolute paths (`C:\...`, `/...`) prohibited
  - UNC paths (`\\server\...`) prohibited
  - Relative paths only allowed
- flg (str, optional) - Option flag (default: "")
  - `""` (default): Existence check only
  - `"NNNN"`: Search for maximum numbered _NNNN file path
  - `"PIXEL"`: Get image size (width/height)
  - `"SIZE"`: Get file size (bytes)

**Return Value**: Dynamic type (varies according to flg)
- **flg=""**: `"TRUE"` or `"FALSE"` (str type)
- **flg="NNNN"**: Maximum numbered file path (relative path, str type), `"FALSE"` if not exists
- **flg="PIXEL"**: `"[width, height]"` format array string (str type), `"FALSE"` if not image/not exists
- **flg="SIZE"**: File size in bytes (str type), `"FALSE"` if not exists

**Features**:
1. **Existence check**: Check file presence
2. **_NNNN search**: Search maximum number in sequential files (e.g. `output_0003.png`)
3. **Image size retrieval**: Get resolution of PNG/JPEG/WEBP image files
4. **File size retrieval**: Get file size in bytes
5. **Security**: Rejects absolute paths/UNC paths (allows relative paths only)

**Target Directory**:
- ComfyUI environment: Under `ComfyUI/output/`
- Test environment: Under current directory

**Example**:
```vba
' Basic existence check
exists = ISFILEEXIST("output.txt")
PRINT("exists = " & exists)
IF exists = "TRUE" THEN
    PRINT("File exists")
ELSE
    PRINT("File does not exist")
END IF

' Search for maximum numbered _NNNN file
latestFile = ISFILEEXIST("ComfyUI_00001_.png", "NNNN")
PRINT("latestFile = " & latestFile)
IF latestFile <> "FALSE" THEN
    PRINT("Latest file: " & latestFile)
    ' e.g. "ComfyUI_00005_.png"
ELSE
    PRINT("No matching files")
END IF

' Get image size
imageSize = ISFILEEXIST("sample_image.png", "PIXEL")
PRINT("imageSize = " & imageSize)
IF imageSize <> "FALSE" THEN
    PRINT("Image size: " & imageSize)
    ' e.g. "[512, 768]"
ELSE
    PRINT("Not an image file")
END IF

' Get file size
fileSize = ISFILEEXIST("data.txt", "SIZE")
PRINT("fileSize = " & fileSize)
IF fileSize <> "FALSE" THEN
    PRINT("File size: " & fileSize & " bytes")
ELSE
    PRINT("File not found")
END IF
```

**Security Restrictions**:
- Absolute paths (`C:\...`, `/...`) rejected
- UNC paths (`\\server\...`) rejected
- Relative paths only allowed

**_NNNN Search Specification**:
- File name pattern: `{base}_{number}.{ext}` format
- Numbers are 4-digit zero-padded (e.g. `_0001`, `_0002`)
- Returns maximum numbered file path
- `"FALSE"` if no matching files exist

**Image Size Retrieval Supported Formats**:
- PNG, JPEG, JPG, BMP, WEBP
- `"FALSE"` if not image file

**Note**:
- All return values are string type (str)
- Even in modes other than existence check, returns `"FALSE"` on error
- Image size is `"[width, height]"` format string (not array type)

---

### VRAMFREE([min_free_vram_gb])

**Description**: Function to free VRAM and RAM. Executes model unloading, cache clearing, and garbage collection.

**⚠️ WARNING**: Model unloading is a delicate operation. Depending on execution timing, it may cause unexpected behavior during workflow execution. Use with caution.

**Syntax**:
```vba
result = VRAMFREE(min_free_vram_gb)
```

**Parameters**:
- `min_free_vram_gb` (float, optional): Execution threshold (in GB)
  - If current free VRAM is above this value, processing is skipped
  - Default: 0.0 (always execute)

**Return Value**:
dict (detailed execution result information)
- `success`: Execution success flag (bool)
- `message`: Execution result message (str)
- `freed_vram_gb`: VRAM amount freed (float)
- `freed_ram_gb`: RAM amount freed (float)
- `initial_status`: Memory state before execution (dict)
- `final_status`: Memory state after execution (dict)
- `actions_performed`: List of actions performed (list)

**Usage Example**:
```vba
' Always execute (no threshold)
result = VRAMFREE(0.0)
PRINT("VRAM freed: " & result["freed_vram_gb"] & " GB")

' Execute only when free VRAM is less than 2GB
result = VRAMFREE(2.0)
IF result["success"] = TRUE THEN
    PRINT("Cleanup completed")
ELSE
    PRINT("Cleanup failed")
END IF
```

**Execution Details**:
1. Get initial memory state
2. Threshold check (skip determination)
3. Unload ComfyUI models
4. Clear ComfyUI soft cache
5. Clear PyTorch GPU cache
6. Python garbage collection (GC)
7. Set flag to ComfyUI prompt_queue
8. Monitor asynchronous flush (3 seconds)
9. Calculate memory freed

**Notes**:
- Outside ComfyUI environment, available features are limited (limited mode)
- In non-CUDA environments, VRAM information may not be retrievable
- Due to asynchronous processing, memory may be freed with slight delay after execution completion

---

### SLEEP([milliseconds])

**Description**: Pauses processing for specified milliseconds (sleep). Used for WHILE() loop speed control and processing synchronization.

**Arguments**:
- milliseconds (FLOAT, optional): Sleep time (milliseconds), default: 10ms

**Return Value**: None (internally returns 0.0)

**Syntax**:
```vba
SLEEP(milliseconds)
```

**Usage Example**:
```vba
' Default 10ms sleep
SLEEP()

' 0.5 second sleep
SLEEP(500)

' WHILE() loop speed control (reduce CPU usage)
VAL1 = 0
WHILE VAL1 < 100
    VAL1 = VAL1 + 1
    SLEEP(100)  ' Wait 100ms
WEND
PRINT("Loop complete: " & VAL1)
RETURN1 = VAL1

' Processing synchronization
PRINT("Processing started")
result = VAL1 * 2
SLEEP(1000)  ' Wait 1 second
PRINT("Processing complete: " & result)
RETURN1 = result
```

**Main Uses**:
1. **WHILE() loop speed control**: Reduce CPU usage and lighten system load
2. **Processing synchronization**: Wait for external system response or intentional delay processing
3. **Debugging**: Temporary pause to observe processing flow

**ComfyUI Integration**:
- Cooperates with ComfyUI thread-based queuing control (ScriptExecutionQueue)
- Synchronous blocking execution using time.sleep()
- ScriptExecutionQueue guarantees safety during simultaneous execution of multiple EasyScripter nodes

**Notes**:
- SLEEP() blocks current thread (other processing does not execute)
- Does not use asynchronous processing (asyncio) (ComfyUI is not event-loop driven)
- Long sleep increases overall workflow execution time

---

## Image Processing Functions

### IMAGETOBYTEARRAY(image_input, [max_size], [format], [return_format])

**Description**: Receives IMAGE tensor or image file path, resizes/compresses and converts to byte array or JSON array. Mainly used as data for REST API transmission.

**Arguments**:
- image_input (str | torch.Tensor, required) - Image source
  - String: Image file path (e.g. `"C:/path/to/image.png"`)
  - torch.Tensor: ComfyUI IMAGE format `[batch, height, width, channels]`
- max_size (int, optional) - Maximum size after resize (long side, pixels), default: 336
- format (str, optional) - Output image format ("PNG", "JPEG" etc.), default: "PNG"
- return_format (str, optional) - Return format ("bytes" or "json"), default: "bytes"

**Return Value**: Dynamic type (varies according to return_format)
- **return_format="bytes"**: bytes type (raw binary data)
- **return_format="json"**: str type (JSON array format string, e.g. `"[137, 80, 78, 71, ...]"`)

**Features**:
1. **IMAGE tensor support**: Can directly receive IMAGE type from ComfyUI nodes
2. **File path support**: Traditional image file path specification also possible
3. **Automatic resize**: Resizes to specified size while maintaining aspect ratio
4. **JPEG compression**: Compresses at quality=50 when format="JPEG" specified (reduces file size)
5. **RGBA→RGB conversion**: Automatically converts transparent background to white background during JPEG output
6. **JSON array conversion**: Integer array format directly usable in Cloudflare API etc.

**Encoding Specification**:
- Not Base64
- Not MIME encoding
- return_format="bytes": Returns raw binary data as bytes type
- return_format="json": Returns JSON string of integer array [0-255]
- JSON array format directly usable in Cloudflare API

**Example**:
```vba
' File path input (traditional method)
json_array = IMAGETOBYTEARRAY("C:/path/to/image.png", 336, "JPEG", "json")
PRINT("JSON array length: " & LEN(json_array))

' IMAGE tensor input (from ComfyUI node connection)
' VAL1 receives IMAGE type from LoadImage node etc.
json_array = IMAGETOBYTEARRAY(VAL1, 336, "JPEG", "json")
RETURN1 = json_array

' Cloudflare Workers AI Image-to-Text API transmission example
```

**Security Restrictions**:
None (FileNotFoundError if file does not exist when file path specified)

**Error Handling**:
- FileNotFoundError: Image file does not exist (string input)
- RuntimeError: PIL (Pillow) not installed, image processing error
- ValueError: Invalid return_format or invalid image size
- TypeError: Invalid input type (not str/torch.Tensor)

**Notes**:
- PIL (Pillow) library required (`pip install Pillow`)
- PyTorch required when handling torch.Tensor (usually pre-installed in ComfyUI environment)
- JPEG format compressed at quality=50, prioritizes file size over image quality
- JSON conversion of large images (4K etc.) without resizing may create huge JSON strings

---

### IMAGETOBASE64(image_input, [max_size], [format], [return_format])

**Description**: Receives IMAGE tensor or image file path, resizes/compresses and converts to Base64 encoding or data URL format. Mainly used as data for REST API transmission.

**Arguments**:
- image_input (str | torch.Tensor, required) - Image source
  - String: Image file path (e.g. `"C:/path/to/image.png"`)
  - torch.Tensor: ComfyUI IMAGE format `[batch, height, width, channels]`
- max_size (int, optional) - Maximum size after resize (long side, pixels), default: 512
- format (str, optional) - Output image format ("PNG", "JPEG" etc.), default: "PNG"
- return_format (str, optional) - Return format ("base64" or "data_url"), default: "base64"

**Return Value**: str type (varies according to return_format)
- **return_format="base64"**: Base64 encoded string (e.g. `"iVBORw0KGgoAAAANSUhEUgAA..."`)
- **return_format="data_url"**: data URL format string (e.g. `"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."`)

**Features**:
1. **IMAGE tensor support**: Can directly receive IMAGE type from ComfyUI nodes
2. **File path support**: Traditional image file path specification also possible
3. **Automatic resize**: Resizes to specified size while maintaining aspect ratio
4. **JPEG compression**: Compresses at quality=85 when format="JPEG" specified (balance of quality and size)
5. **RGBA→RGB conversion**: Automatically converts transparent background to white background during JPEG output
6. **Base64 encoding**: Standard Base64 encoding, also supports data URL format

**Encoding Specification**:
- Standard Base64 encoding
- return_format="base64": Returns Base64 string only
- return_format="data_url": Returns data URL format (`"data:image/png;base64,..."`)
- Directly usable in Vision API

**Example**:
```vba
' File path input (Base64 string)
base64_str = IMAGETOBASE64("C:/path/to/image.png", 512, "PNG", "base64")
PRINT("Base64 length: " & LEN(base64_str))

' IMAGE tensor input (data URL format)
' ANY_INPUT receives IMAGE type from LoadImage node etc.
data_url = IMAGETOBASE64(ANY_INPUT, 512, "PNG", "data_url")
RETURN1 = data_url
```

---

## Image/Latent Data Retrieval Functions

### GETANYWIDTH([any_data])

**Description**: Gets width (pixels) of IMAGE/LATENT type data

**Arguments**:
- any_data (torch.Tensor, optional) - IMAGE/LATENT data
  - If omitted, automatically uses any_input input socket data

**Return Value**: float - Width (pixels, 0.0 if cannot retrieve)

**Supported Formats**:
- IMAGE type: torch.Tensor format `[batch, height, width, channels]`
- LATENT type: torch.Tensor format `[batch, channels, height, width]`

**Example**:
```vba
' Auto-retrieve from any_input input socket
width = GETANYWIDTH()
PRINT("Width: " & width)
RETURN1 = width

' Explicitly specify data
imageData = INPUT("sample.png")
w = GETANYWIDTH(imageData)
PRINT("Image width: " & w)
```

---

### GETANYHEIGHT([any_data])

**Description**: Gets height (pixels) of IMAGE/LATENT type data

**Arguments**:
- any_data (torch.Tensor, optional) - IMAGE/LATENT data
  - If omitted, automatically uses any_input input socket data

**Return Value**: float - Height (pixels, 0.0 if cannot retrieve)

**Supported Formats**:
- IMAGE type: torch.Tensor format `[batch, height, width, channels]`
- LATENT type: torch.Tensor format `[batch, channels, height, width]`

**Example**:
```vba
' Auto-retrieve from any_input input socket
height = GETANYHEIGHT()
PRINT("Height: " & height)
RETURN2 = height

' Conditional branching according to resolution
w = GETANYWIDTH()
h = GETANYHEIGHT()
IF w >= 1024 AND h >= 1024 THEN
    PRINT("High resolution image")
    scale = 1.0
ELSE
    PRINT("Standard resolution image")
    scale = 2.0
END IF
RETURN1 = scale
```

---

### GETANYTYPE([any_data])

**Description**: Determines type name of ANY type data

**Arguments**:
- any_data (Any, optional) - Data for type detection
  - If omitted, automatically uses any_input input socket data

**Return Value**: str - Type name
- "int", "float", "string" - Basic types
- "image", "latent" - Image/Latent
- "model", "vae", "clip" - ComfyUI model types
- "conditioning", "control_net", "clip_vision", "style_model", "gligen", "lora" - ComfyUI specific types
- "none" - None value
- "unknown" - Cannot determine

**Example**:
```vba
' Auto-detect from any_input input socket
type_name = GETANYTYPE()
PRINT("Type: " & type_name)

SELECT CASE type_name
    CASE "image"
        w = GETANYWIDTH()
        h = GETANYHEIGHT()
        PRINT("IMAGE type: " & w & "x" & h)
    CASE "latent"
        PRINT("LATENT type")
    CASE "model"
        PRINT("MODEL type")
    CASE "string"
        PRINT("STRING type")
    CASE ELSE
        PRINT("Other type: " & type_name)
END SELECT
```

---

### GETANYVALUEINT([any_data])

**Description**: Get integer value from ANY type data

**Arguments**:
- any_data (Any, optional) - Data
  - If no argument, automatically uses data from any_input input socket

**Return Value**: int - Integer value (returns 0 if cannot retrieve)

**Example**:
```vba
' Get integer value from any_input input socket
int_value = GETANYVALUEINT()
PRINT("Integer value: " & int_value)
RETURN1 = int_value
```

---

### GETANYVALUEFLOAT([any_data])

**Description**: Get floating point value from ANY type data

**Arguments**:
- any_data (Any, optional) - Data
  - If no argument, automatically uses data from any_input input socket

**Return Value**: float - Floating point value (returns 0.0 if cannot retrieve)

**Example**:
```vba
' Get floating point value from any_input input socket
float_value = GETANYVALUEFLOAT()
PRINT("Float value: " & float_value)
RETURN1 = float_value
```

---

### GETANYSTRING([any_data])

**Description**: Get string from ANY type data

**Arguments**:
- any_data (Any, optional) - Data
  - If no argument, automatically uses data from any_input input socket

**Return Value**: str - String (returns empty string if cannot retrieve)

**Example**:
```vba
' Get string from any_input input socket
str_value = GETANYSTRING()
PRINT("String: " & str_value)
RETURN1 = str_value
```

---

## Type Detection Functions

### ISNUMERIC(value)

**Description**: Determines if value is numeric

**Arguments**:
- value - Value to check

**Return Value**: 1 (numeric) or 0 (non-numeric)

**Example**:
```vba
result = ISNUMERIC("123")      ' 1
PRINT("ISNUMERIC('123') = " & result)
result = ISNUMERIC("12.34")    ' 1
PRINT("ISNUMERIC('12.34') = " & result)
result = ISNUMERIC("abc")      ' 0
PRINT("ISNUMERIC('abc') = " & result)
result = ISNUMERIC("")         ' 0
PRINT("ISNUMERIC('') = " & result)

' Practical example: Input value validation
IF ISNUMERIC(TXT1) THEN
    value = CDBL(TXT1)
    PRINT("Process as number: " & value)
ELSE
    PRINT("Error: Not a number")
END IF
```

---

### ISDATE(value)

**Description**: Determines if value can be parsed as a date

**Arguments**:
- value - Value to check

**Return Value**: 1 (date) or 0 (non-date)

**Example**:
```vba
result = ISDATE("2024-01-15")     ' 1
PRINT("ISDATE('2024-01-15') = " & result)
result = ISDATE("2024/01/15")     ' 1
PRINT("ISDATE('2024/01/15') = " & result)
result = ISDATE("15:30:00")       ' 1 (time can also be detected)
PRINT("ISDATE('15:30:00') = " & result)
result = ISDATE("hello")          ' 0
PRINT("ISDATE('hello') = " & result)

' Practical example: Date validation
IF ISDATE(TXT1) THEN
    dateVal = DATEVALUE(TXT1)
    PRINT("Processing as date: " & dateVal)
ELSE
    PRINT("Error: Not in date format")
END IF
```

**Supported Formats**:
- `YYYY/MM/DD HH:MM:SS`
- `YYYY/MM/DD`
- `YYYY-MM-DD HH:MM:SS`
- `YYYY-MM-DD`
- `MM/DD/YYYY`
- `DD/MM/YYYY`
- `HH:MM:SS`
- `HH:MM`

---

### ISARRAY(variable_name)

**Description**: Determines if variable is an array

**Arguments**:
- variable_name - Variable name (string) or array variable reference (ARR[] notation)

**Return Value**: 1 (array) or 0 (non-array)

**Example**:
```vba
REDIM arr, 10
result = ISARRAY(arr[])      ' 1 (array reference)
PRINT("ISARRAY(arr[]) = " & result)
result = ISARRAY("arr")      ' 1 (array name string)
PRINT("ISARRAY('arr') = " & result)
result = ISARRAY("VAL1")     ' 0 (regular variable)
PRINT("ISARRAY('VAL1') = " & result)

' Practical example: Variable type checking
REDIM myData, 5
myData[0] = "a"
myData[1] = "b"
IF ISARRAY(myData[]) THEN
    PRINT("It's an array. Element count: " & (UBOUND(myData[]) + 1))
ELSE
    PRINT("Not an array")
END IF
```

**Note**:
- Pass array name as string or array variable reference with ARR[] notation

---

### TYPE(value)

**Description**: Returns variable type as string

**Arguments**:
- value - Value to check type

**Return Value**: Type name ("NUMBER", "STRING", "BOOLEAN", "ARRAY", "NULL", "OBJECT")

**Example**:
```vba
typeName = TYPE(123)           ' "NUMBER"
PRINT("TYPE(123) = " & typeName)
typeName = TYPE("hello")       ' "STRING"
PRINT("TYPE('hello') = " & typeName)
typeName = TYPE(1 > 0)         ' "NUMBER"
PRINT("TYPE(1 > 0) = " & typeName)

REDIM arr, 5
typeName = TYPE(arr[])         ' "OBJECT"
PRINT("TYPE(arr[]) = " & typeName)

' Practical example: Generic type processing
myValue = VAL1
dataType = TYPE(myValue)
PRINT("TYPE(myValue) = " & dataType)
SELECT CASE dataType
    CASE "NUMBER"
        PRINT("Number: " & myValue)
    CASE "STRING"
        PRINT("String: " & myValue)
    CASE "ARRAY"
        PRINT("Array (element count: " & (UBOUND(myValue[]) + 1) & ")")
    CASE "NULL"
        PRINT("No value")
END SELECT
```

---

## Practical Examples

### Debug Output Utilization

```vba
' Check values at each processing stage
originalValue = VAL1
PRINT("Original value: " & originalValue)

processedValue = originalValue * 2
PRINT("After doubling: " & processedValue)

finalValue = processedValue + 10
PRINT("Final value: " & finalValue)

RETURN1 = finalValue
PRINT("Assigned to RETURN1: " & RETURN1)
```

### Input Value Validation

```vba
' Check if numeric then process
IF ISNUMERIC(TXT1) THEN
    number = CDBL(TXT1)
    PRINT("Converted TXT1 to number: " & number)
    result = number * VAL1
    PRINT("Calculation result: " & result)
    RETURN1 = result
    PRINT("Assigned to RETURN1: " & RETURN1)
ELSE
    PRINT("Error: TXT1 is not a number")
    RETURN1 = 0
    PRINT("Assigned default value to RETURN1: " & RETURN1)
END IF
```

### Processing Branch According to Type

```vba
' Change processing according to data type
myData = VAL1
dataType = TYPE(myData)
PRINT("TYPE(myData) = " & dataType)

IF dataType = "NUMBER" THEN
    result = myData * 2
    PRINT("Numeric processing: " & result)
ELSEIF dataType = "STRING" THEN
    result = UCASE(myData)
    PRINT("String processing: " & result)
ELSEIF dataType = "ARRAY" THEN
    count = UBOUND(myData[]) + 1
    PRINT("Array processing: element count=" & count)
    FOR i = 0 TO UBOUND(myData[])
        PRINT("  [" & i & "] = " & myData[i])
    NEXT
ELSE
    PRINT("Unsupported type: " & dataType)
END IF
```

---

[← Back to Built-in Functions Index](00_index.md)
