# Change Log (CHANGELOG)

**Languages**: [日本語](../CHANGELOG.md) | [English](CHANGELOG.md)

Major version update history for u5 EasyScripter.

---

## 📝 Update History


### v3.1.2 (2025-11-18) - Documentation Format Corrections

#### Fixed
- **Function Count Cross-Reference Corrections**: Fixed function counts in docs/02_builtin_functions/00_index.md to match actual implementation counts
  - Math Functions: 24 → 16
  - CSV Functions: 11 → 9
  - Array Functions: 7 → 3
  - Model Functions: 3 → 1
  - Utility Functions: 21 → 18
  - Loop Control Functions: 9 → 1
  - HTTP Communication Functions: 17 → 9
  - Python Function Execution: 3 → 4
- **Quick Reference Table Corrections**: Fixed quick reference table in 00_index.md
  - Removed 8 non-existent math functions from table (RND, RANDOMIZE, FIX, SGN, ASIN, ACOS, ATAN, ATAN2)
  - Fixed CSVDIFF function arguments: CSVDIFF(csv1, csv2) → CSVDIFF(array_name, csv1, csv2)
  - Added PYDECODE function to Python function table
- **String Function Count Correction**: Fixed function count in docs/02_builtin_functions/02_string_functions.md from 29 → 28
- **Table of Contents Anchor Link Correction**: Removed leading hyphens from TOC anchor links in docs/01_syntax_reference.md (GitHub Markdown spec compliance)

### v3.1.1 (2025-11-17) - String Function Documentation Added

#### Added
- **String Function Documentation Added**: Added documentation for 7 implemented string functions
  - **ESCAPEPATHSTR(path, [replacement])**: Replace or remove forbidden characters in file paths
  - **URLENCODE(text, [encoding])**: URL encoding (percent encoding)
  - **URLDECODE(text, [encoding])**: URL decoding
  - **PROPER(text)**: Convert to title case (capitalize first letter of each word)
  - **CHR(code)**: Character code → character conversion (ASCII range)
  - **ASC(char)**: Character → character code conversion
  - **STR(value)**: Number → string conversion
  - Documentation: docs/02_builtin_functions/02_string_functions.md
  - Function count: 21 → 23

#### Changed
- **Total Built-in Functions**: 135 entries → 137 entries
  - 135 unique functions (133 functions + 2 aliases)
  - Updated README.md, docs/02_builtin_functions/00_index.md

### v3.1.0 (2025-11-17) - != Operator Support

#### Added
- **!= Operator**: Added C-style inequality operator
  - Identical behavior to `<>` operator (both can be used)
  - Implementation: script_parser.py (added to TOKEN_PATTERNS array)
  - Test: tests/test_neq_operator.py
  - Documentation: docs/01_syntax_reference.md

### v3.0.0 (2025-11-13) - Any_input Input Socket Enhancements and More

### Added
- **IMAGETOBASE64 Function**: Added function to convert IMAGE tensor or image file path to Base64 encoding (or data URL format)
  - Supports OpenAI Vision API data generation
  - Supports both IMAGE tensor (ComfyUI node connection) and file path input
  - Provides resize, JPEG compression (quality=85), RGBA→RGB conversion, Base64/data URL return functionality
  - Implementation: functions/misc_functions.py (MiscFunctions.IMAGETOBASE64)
  - Documentation: docs/02_builtin_functions/09_utility_functions.md

- **IMAGETOBYTEARRAY Function**: Added function to convert IMAGE tensor or image file path to JSON array (or byte array)
  - Supports Cloudflare Workers AI REST API data generation
  - Supports both IMAGE tensor (ComfyUI node connection) and file path input
  - Provides resize, JPEG compression, RGBA→RGB conversion, JSON array/bytes type return functionality
  - Implementation: functions/misc_functions.py (MiscFunctions.IMAGETOBYTEARRAY)
  - Documentation: docs/02_builtin_functions/09_utility_functions.md
- **FORMAT Function**: Added function to format numbers and datetime with specified format (VBA compatible)
  - Supports VBA format ("0", "0.0", "0.00", "#.##"), Python format format, datetime strftime format
  - Implementation: functions/misc_functions.py (MiscFunctions.FORMAT)
  - Documentation: docs/02_builtin_functions/07_type_functions.md

- **GETANYTYPE Function**: Added function to determine type name of ANY type data
  - Determines basic types (int, float, string), ComfyUI types (image, latent, model, vae, clip, etc.)
  - Auto-fetch from any_input input socket, or explicitly specify data
  - Implementation: functions/misc_functions.py (MiscFunctions.GETANYTYPE)
  - Documentation: docs/02_builtin_functions/09_utility_functions.md

- **GETANYVALUEINT Function**: Added function to get integer value from ANY type data
  - Auto-fetch from any_input input socket, or explicitly specify data
  - Returns 0 if cannot get value
  - Implementation: functions/misc_functions.py (MiscFunctions.GETANYVALUEINT)
  - Documentation: docs/02_builtin_functions/09_utility_functions.md

- **GETANYVALUEFLOAT Function**: Added function to get float value from ANY type data
  - Auto-fetch from any_input input socket, or explicitly specify data
  - Returns 0.0 if cannot get value
  - Implementation: functions/misc_functions.py (MiscFunctions.GETANYVALUEFLOAT)
  - Documentation: docs/02_builtin_functions/09_utility_functions.md

- **GETANYSTRING Function**: Added function to get string from ANY type data
  - Auto-fetch from any_input input socket, or explicitly specify data
  - Returns empty string if cannot get value
  - Implementation: functions/misc_functions.py (MiscFunctions.GETANYSTRING)
  - Documentation: docs/02_builtin_functions/09_utility_functions.md

- **GETANYWIDTH Function**: Added function to get width (pixels) of IMAGE/LATENT type data
  - Auto-fetch from any_input input socket, or explicitly specify data
  - Supports both IMAGE and LATENT types
  - Implementation: functions/misc_functions.py (MiscFunctions.GETANYWIDTH)

- **GETANYHEIGHT Function**: Added function to get height (pixels) of IMAGE/LATENT type data
  - Auto-fetch from any_input input socket, or explicitly specify data
  - Supports both IMAGE and LATENT types
  - Implementation: functions/misc_functions.py (MiscFunctions.GETANYHEIGHT)

### Changed
- **LOOPSUBGRAPH Sequential Execution Guarantee**: Iterations are now executed sequentially instead of in parallel
  - Each iteration waits for previous iteration completion
  - Guarantees re-evaluation of NOW(), RND(), PRINT() functions at each iteration
  - Internal implementation: `_iteration_dependency` dummy input dependency chain (EasyScripter nodes only)
  - Backward compatibility: No impact on existing workflows (optional input)
  - Performance impact: Execution time increases proportionally to iteration count
  - Implementation: scripter_node.py (_duplicate_subgraph_iteration, _build_loop_subgraph, INPUT_TYPES, _execute_script_impl)

### Fixed
- **LOOPSUBGRAPH Iteration Count Bug Fix**: Fixed bug where executes one time less than specified count
  - Issue: `LOOPSUBGRAPH(5)` only executed 4 times
  - Cause: `range(1, total_count)` was incorrectly used (range(1,5)=[1,2,3,4])
  - Fix: Changed to `range(total_count)` (range(5)=[0,1,2,3,4])
  - Implementation: scripter_node.py L645

- **LOOPSUBGRAPH Dependency Addition Logic Fix**: Fixed incorrect dependency addition to standard ComfyUI nodes
  - Issue: `TypeError: Int.execute() got an unexpected keyword argument '_iteration_dependency'`
  - Cause: Added `_iteration_dependency` input to standard ComfyUI nodes like PrimitiveInt
  - Fix: Only add dependency to EasyScripter nodes (`class_type=="comfyUI_u5_easyscripter"`)
  - Implementation: scripter_node.py L542-549

- **execute_script Method Signature Fix**: Fixed bug with missing `_iteration_dependency` argument
  - Issue: `TypeError: ComfyUI_u5_EasyScripterNode.execute_script() got an unexpected keyword argument '_iteration_dependency'`
  - Cause: Forgot to add `_iteration_dependency` argument to public method `execute_script` (only added to internal method `_execute_script_impl`)
  - Fix: Added `_iteration_dependency=None` to `execute_script` signature, pass argument in `enqueue_and_wait` call
  - Implementation: scripter_node.py L89-92, L140

- **LOOPSUBGRAPH Original Node Deletion Issue**: Fixed bug where executes one time more than specified count
  - Issue: `LOOPSUBGRAPH(5)` executes 6 times (original node + 5 duplicates)
  - Cause: expand added duplicate nodes but didn't delete original subgraph node
  - Symptom: Downstream nodes output old timestamp (previous execution cache)
  - Fix: Explicitly delete original node ID with `remove` key
  - Implementation: scripter_node.py L621, L643-645, L683

- **LOOPSUBGRAPH Sequential Execution Bug Fix**: Fixed bug where multiple iterations execute at same timestamp
  - Issue: `LOOPSUBGRAPH(5)` has multiple iterations executing at same second (2nd and 3rd, etc.)
  - Cause:
    - `_duplicate_subgraph_iteration` simply returned last processed node ID
    - Didn't return actual graph structure tail node
    - Result: Next iteration dependency not set correctly, executed in parallel
  - Fix:
    - Added `_find_subgraph_tail_node` method to detect original subgraph tail node
    - Added `original_tail_node_id` argument to `_duplicate_subgraph_iteration`
    - Accurately calculate duplicate version tail based on original tail (`{original_tail}_loop_{iteration}`)
    - Only create duplicates from iteration 1 to total_count, keep original node as 1st iteration
  - Result: Original (1st) → 4 duplicates (2nd-5th) execute completely sequentially
  - Implementation: scripter_node.py L565-617 (`_find_subgraph_tail_node` added), L455,466,555-563 (`_duplicate_subgraph_iteration` fix), L708-710,729 (original tail detection and argument passing)

- **CDATE Function**: Added function to convert date string to date type (VBA compatible)
  - Flexible format support:
    - Full datetime: `"2025/11/05 15:39:49"` → `2025/11/05 15:39:49`
    - Date only: `"2025/11/05"` → `2025/11/05 00:00:00`
    - Year-month only: `"2025/11"` → `2025/11/01 00:00:00`
    - Year only: `"2025"` → `2025/01/01 00:00:00`
    - Time partial completion also supported
  - Delimiter flexibility: Allows mixing of `/`, `-`, `:`, space
  - Implementation file: `functions/date_functions.py`
  - Documentation: Details added to `docs/02_builtin_functions/03_datetime_functions.md`
  - Total built-in functions: Datetime functions 14 → 15

### v2.9.0 (2025-10-29) - Product Name Unification and Multilingual Support Enhancement


- **Complete Multilingual Support Implementation**: All system messages now multilingual
  - Supported languages: Japanese, English
  - Added 121 message keys to locales.py (existing 57 + new 64)
  - Removed all hardcoded Japanese messages
  - Target modules:
    - scripter_node.py: Multilingualized all 27 hardcoded Japanese locations
    - script_execution_queue.py: Multilingualized all 16 hardcoded Japanese locations
    - functions/loop_functions.py: Multilingualized all 8 hardcoded Japanese locations
    - functions/misc_functions.py: Multilingualized all 13 hardcoded Japanese locations (OUTPUT/INPUT/ISFILEEXIST functions)
  - Unified locale argument propagation across all modules:
    - scripter_node → script_execution_queue
    - scripter_node → script_engine → loop_functions
    - scripter_node → script_engine → misc_functions
  - ComfyUI console output also fully multilingual
  - Test: All 34 test cases succeeded (tests/test_scripter_node_localization.py)


- **SLEEP Function**: Added utility function to temporarily pause processing
  - Function: Temporarily pause (sleep) processing for specified milliseconds
  - Parameter: `milliseconds` (float, optional, default: 10ms)
  - Return value: None (internally returns 0.0)
  - Main uses:
    - WHILE() loop speed control (reduce CPU usage)
    - Processing synchronization
    - Debug pause
  - ComfyUI integration:
    - Cooperative operation with ComfyUI's thread-based queuing control (ScriptExecutionQueue)
    - Synchronous blocking execution with time.sleep()
    - ScriptExecutionQueue guarantees safety when executing multiple EasyScripter nodes simultaneously
  - Implementation file: `functions/misc_functions.py` (after VRAMFREE function)
  - Test: All 10 test cases succeeded (tests/test_sleep_function.py)
  - Documentation: Details added to `docs/02_builtin_functions/09_utility_functions.md`
  - Total built-in functions: 133 → 134 entries (132 unique functions, including 2 aliases)

- **VRAMFREE Function**: Added utility function to free VRAM and RAM
  - Function: Execute model unload, cache clear, garbage collection
  - Parameter: `min_free_vram_gb` (float, optional) to specify execution threshold
  - Return value: Returns detailed information of execution result in dict format
    - `success`: Execution success flag (bool)
    - `freed_vram_gb`: Amount of VRAM freed (float)
    - `freed_ram_gb`: Amount of RAM freed (float)
    - `actions_performed`: List of actions performed (list)
  - ⚠️ WARNING: Delicate operation, use with caution
  - Implementation file: `functions/misc_functions.py`
  - Test: All test cases succeeded (tests/test_vramfree.py)
  - Documentation: Details added to `docs/02_builtin_functions/09_utility_functions.md`

- **ISFILEEXIST Function**: Added file existence check and extended information retrieval functionality
  - Basic function: File existence check in ComfyUI output folder
  - Extended function: 4 mode support
    - `flg=""` (default): Existence check only ("TRUE"/"FALSE")
    - `flg="NNNN"`: Search maximum number of sequential files (e.g., `output_0003.png`)
    - `flg="PIXEL"`: Get image size ("[width, height]" format)
    - `flg="SIZE"`: Get file size (bytes)
  - Security: Reject absolute path/UNC path (only relative path allowed)
  - Target directory: `ComfyUI/output/` in ComfyUI environment, current directory in test environment
  - Image format support: PNG, JPEG, JPG, BMP, WEBP
  - Return value: All string type (str), returns "FALSE" on error
  - Implementation file: `functions/misc_functions.py`
  - Test: All 14 test cases succeeded (tests/test_isfileexist.py)
  - Documentation: Details added to `docs/02_builtin_functions/09_utility_functions.md`
  - Total built-in functions: 131 → 132 entries (130 unique functions, including 2 aliases)


- **RELAY_OUTPUT Variable**: Can now control relay_output output socket (ANY type) value by assigning to `RELAY_OUTPUT` variable in script
  - Use: Pass ANY type data like images (torch.Tensor) loaded with INPUT function to subsequent nodes
  - Backward compatibility: When RELAY_OUTPUT not used, passes through any_input input as before
  - Implementation: script_engine.py, scripter_node.py
  - Tier 3 feature: Implementation complete, test complete (PASS)
  - Documentation:
    - `docs/01_syntax_reference.md`: Added RELAY_OUTPUT variable description to reserved variables section
    - `docs/02_builtin_functions/09_utility_functions.md`: Added RELAY_OUTPUT integration example to INPUT function section

- **INPUT Function**: Added file read functionality (added in v2.2.0)
  - Read files from ComfyUI output folder
  - Automatic type detection for text, JSON (numeric/array), images (torch.Tensor), binary data
  - Implemented as symmetric function to OUTPUT function
  - Security feature: Reject absolute path/UNC path (only relative path allowed)
  - Read source: `ComfyUI/output/` in ComfyUI environment, current directory in test environment
  - Error handling: Print warning and return None if file not found
  - Supported types:
    - Text files (.txt, .md) → str type
    - JSON numeric → float type
    - JSON array → list type
    - Image files (.png, .jpg, etc.) → torch.Tensor type (ComfyUI compatible)
    - Others → bytes type (binary)
  - Tier 1 features (text/numeric/array): Test complete (PASS)
  - Tier 2 features (images): Implemented, test not performed
  - Tier 3 features (Latent/RELAY_OUTPUT): Not implemented as future extension

- **Documentation Updates**:
  - `docs/02_builtin_functions/09_utility_functions.md`: Added detailed INPUT function documentation
  - `docs/02_builtin_functions/00_index.md`: Updated utility function count from 6 → 7, total 128 entries (126 unique functions, including 2 aliases)
  - `docs/00_documentation_index.md`: Updated to total 131 entries, added file I/O section
  - `README.md`: Updated total built-in functions to 131 entries (129 unique functions, including 2 aliases)


- **OUTPUT Function**: Added file output functionality
  - Supports text, numeric, array, image (torch.Tensor), binary data output
  - Supports NEW mode (duplication avoidance, automatic `_0001`, `_0002`... suffix) and ADD mode (append)
  - Supports direct output from reserved variables (TXT1, TXT2, ANY_INPUT)
  - Security feature: Reject absolute path/UNC path (only relative path allowed)
  - Automatic recursive subdirectory creation
  - Automatic extension completion (`.txt`, `.png`, etc.)
  - Output destination: `ComfyUI/output/` in ComfyUI environment, current directory in test environment

- **Documentation Updates**:
  - `docs/02_builtin_functions/09_utility_functions.md`: Added detailed OUTPUT function documentation
  - `docs/02_builtin_functions/00_index.md`: Updated utility function count from 5 → 6, total 127 entries (125 unique functions, including 2 aliases)
  - `README.md`: Updated total built-in functions to 130 entries (128 unique functions, including 2 aliases)

### v2.8.2 (2025-10-27) - Unnecessary Function Deletion (MSGBOX, INPUTBOX, LBOUND)

- **Deleted Functions**:
  - **MSGBOX**: Deleted as dialog display inappropriate in ComfyUI workflow environment (can substitute with PRINT)
  - **INPUTBOX**: Deleted as input dialog display impossible in ComfyUI headless environment
  - **LBOUND**: Deleted as unnecessary since EasyScripter arrays are zero-based fixed (always returns 0)

- **Affected Locations**:
  - `builtin_functions.py`: Deleted from BUILTIN_FUNCTIONS dictionary, is_builtin_function(), get_function_usage()
  - `functions/base_functions.py`: Deleted MSGBOX function
  - `functions/misc_functions.py`: Deleted INPUTBOX function, LBOUND function
  - `tests/audit_06_array_functions.py`: Deleted 3 LBOUND-related tests, replaced LBOUND usage in test_example_aggregate with 0
  - `README.md`: Updated array functions (4→3), utility functions (7→5) counts
  - `docs/02_builtin_functions/00_index.md`: Updated to total 126 entries (-3)
  - `docs/02_builtin_functions/06_array_functions.md`: Deleted LBOUND section, replaced LBOUND usage in sample code with 0
  - `docs/02_builtin_functions/09_utility_functions.md`: Deleted MSGBOX, INPUTBOX sections
  - Multilingual README (docs/zh/README.md, docs/en/README.md): Updated counts

- **Backward Compatibility**:
  - **Breaking Change**: Existing scripts using these 3 functions will stop working
  - **Recommended Alternatives**:
    - MSGBOX → PRINT
    - INPUTBOX → VAL1, VAL2, TXT1, TXT2 (node inputs)
    - LBOUND → 0 (fixed value) or FOR I = 0 TO UBOUND(arr[])

### v2.8.1 (2025-10-27) - EXIT Statement and One-line IF Statement Support Added (EXIT Statement Only)

- **New Features**:
  - Added EXIT statement support
    - `EXIT FUNCTION`: Early return from function
    - `EXIT FOR`: Early exit from FOR loop
    - `EXIT WHILE`: Early exit from WHILE loop
  - Added one-line IF statement support (limited to combination with EXIT statement)
    - Example: `IF value < 0 THEN EXIT FUNCTION`
    - Complex conditional expressions also supported: `IF x < 0 AND y < 0 THEN EXIT FUNCTION`

- **Specification Changes**:
  - Function return value initialization: `0` → `""` (empty string)
    - Modified so unset return value when calling EXIT FUNCTION becomes empty string
    - Complies with EasyScripter specification

- **Tests Added**:
  - `tests/test_exit_basic.py`: EXIT statement basic operation test (10 test cases)
  - `tests/test_one_line_if_exit.py`: One-line IF+EXIT edge case test (8 test cases)

- **Backward Compatibility**:
  - Existing multi-line IF statements completely maintain backward compatibility
  - All existing test cases (27 out of 36 files) passed, no regression

### v2.7.9 (2025-10-22) - All Documentation Expected Value Audit Project Complete

### v2.7.8 (2025-10-22) - Python Function Documentation Expected Value Audit

### v2.7.7 (2025-10-22) - Model Function Documentation Expected Value Audit

### v2.7.6 (2025-10-22) - Type Function Documentation Expected Value Audit

### v2.7.5 (2025-10-22) - CSV Function Documentation Expected Value Audit

### v2.7.4 (2025-10-22) - Documentation Unassigned Variable Audit Project

### v2.7.3 (2025-10-22) - Documentation Variable Naming Convention Complete Unification Project

### v2.7.2 (2025-10-22)
- **Documentation Structure Refactoring**: Information centralization and elimination of duplicate management
  - **Function Count Notation Unification**: Unified to "129 entries (127 unique functions, including 2 aliases)" across all documentation
    - Correction target: README.md, docs/00_documentation_index.md, docs/02_builtin_functions/00_index.md, docs/01_syntax_reference.md
    - Also updated multilingual versions: docs/en/README.md, docs/zh/README.md
  - **Single Source of Truth Establishment**: Designated docs/02_builtin_functions/00_index.md as only complete reference index
    - Simplified built-in function section of docs/00_documentation_index.md, delegated to detailed index
    - Deleted 12 category individual lists, only recorded statistical information
  - **Statistical Information Table Enhancement**: Added detailed function count breakdown and notes
    - Clearly stated registered entry count for each category
    - Clarified distinction between aliases and independent implementations
  - **Cross-Reference Verification**: Confirmed and corrected function count consistency across all documentation

### v2.7.1 (2025-10-22)
- **Documentation Structure Organization**: Unification of category order and elimination of duplicate content
  - Unified built-in function category list order across all documentation (canonical order: 1-12)
    - Correction target: README.md, docs/00_documentation_index.md, docs/02_builtin_functions/00_index.md
  - Reconstructed docs/00_documentation_index.md as concise index (consolidated details to README.md reference)
  - Corrected Python function execution category function count (1 → 4)
    - Accurately counted 4 functions: PYEXEC, PYLIST, PYENCODE, PYDECODE
  - Unified category count to "12" across all documentation
  - Verified and corrected cross-reference accuracy

### v2.7.0 (2025-10-15)
- **Python Function Execution Feature Added**: Can execute standard/user library functions with PYEXEC() function
  - New feature: Implemented `PYEXEC(func_path, [arg1], [arg2], ...)` function
  - Supported libraries:
    - Python standard library: math, random, json, datetime, base64, etc.
    - User-installed libraries: numpy, pandas, requests, hashlib, etc. (lightweight data processing)
  - Security: Blacklist approach (only block dangerous modules)
    - Blocked: os, sys, subprocess, eval, exec, compile, pickle, shelve, code, pdb
  - Type conversion specification:
    - None → 0.0, bool → 1.0/0.0, int → float
    - list/tuple → CSV string, dict → JSON string
    - numpy.ndarray → CSV string, pandas.DataFrame → JSON string
  - Limitations:
    - Maximum 10 arguments
    - Maximum return value size 1MB
    - Maximum list/array elements 10000
    - **Note**: Image data (cv2.imread, etc.) has hundreds of thousands of elements, causing limit exceeded error
  - **Important**: Windows file paths must use `\\` (double backslash)
    - ❌ Wrong: `"C:\test.csv"` → `\t` converted to tab character, path corrupted
    - ✅ Correct: `"C:\\test.csv"` or `"C:/test.csv"`
  - Implementation details:
    - `functions/python_functions.py`: PythonFunctions class implementation
    - `builtin_functions.py`: Integrated PYEXEC function into built-in functions
    - TDD compliance: Created test code before implementation (tests/test_pyexec_standalone.py, test_pyexec_via_engine.py)
  - Test: All 10 test cases succeeded (operation confirmed via ScriptEngine)
  - Documentation: Created docs/02_builtin_functions/12_python_functions.md
  - Built-in function count: 138 → 139 entries (1 function added)

### v2.6.5 (2025-10-14)
- **UI Improvement**: Adjusted log area initial state, height, placement position
  - Changes:
    - Modified to load with log area closed on node initial load
    - Changed `UI_CONFIG.logDisplay.defaultState` from `EXPANDED` (expanded) to `COLLAPSED` (closed)
    - Doubled log area height overall
      - Closed state: 40px → 80px (2x)
      - Open state: 100px → 200px (2x)
      - Maximum height: 150px → 300px (2x)
    - Added 20px space between log area and script area
      - Changed `UI_CONFIG.widgets.spacing` from 10px → 30px (+20px space added)
  - Effects:
    - Efficient use of screen space on initial load
    - Log area wider, can confirm more output content
    - Can display about 2 lines of log even in closed state
    - Space between log area and script area creates margin, improved visibility
    - Script editing area starts widely available
    - User can expand log area by clicking as needed
  - Implementation files:
    - `web/comfyui_u5_easyscripter.js`: Fixed defaultState (line 822), doubled height settings (line 788-794)
    - `web/comfyui_u5_easyscripter.js`: Changed spacing (line 796: 10→30)
  - Backward compatibility:
    - Existing workflow collapse state prioritizes saved value (logDisplayState property in workflow JSON)
    - Only new nodes default to closed state
    - Existing workflows also benefit from increased space

### v2.6.4 (2025-10-14)
- **Script Syntax Extension**: Added inline comment functionality
  - New feature: Can write comments with `'` after statements
    - Example: `PRINT(VAL1) 'This is a comment`
    - Example: `RETURN1 = VAL1 + VAL2 'Calculate sum`
  - Implementation method:
    - `'` inside string literals protected (not interpreted as inline comment)
    - `'` outside string literals onwards to line end removed as comment
    - Line-leading comment behavior unchanged (existing functionality 100% retained)
  - Implementation files:
    - `script_parser.py`: Added inline comment processing logic to tokenize method
    - `tests/test_inline_comment.py`: Created 8 pattern test cases (all succeeded)
  - Effects:
    - Improved script readability (can write code and description on same line)
    - Further reproduces VBA-like writing style
    - 100% backward compatibility with existing scripts
  - TDD compliance: Test-first development method implementation (create test code before implementation, confirm failure → implement → confirm success)

### v2.6.3 (2025-10-14)
- **UI Improvement**: Log area collapse functionality and text readability improvement
  - New features:
    - Can toggle log area 1-line display ⇄ all-line display by clicking
    - Collapse state saved when saving workflow (session persistence)
    - Automatically adjust script area Y coordinate when collapsed
    - Visual indicator (▶/▼ icon) shows collapse state
  - Readability improvement:
    - Script area: Font size 13px→14px, line height 1.5→1.6
    - Output area: Improved background color and text color contrast
    - Improved readability with monospace font
  - Implementation details:
    - `web/comfyui_u5_easyscripter.js`: Implemented collapse functionality (added setupLogToggle function)
    - `web/comfyui_u5_easyscripter.js`: Added layout recalculation function (updateLayoutForLogState function)
    - `web/comfyui_u5_easyscripter.js`: Modified setupResizeHandler for collapse state support
    - `web/comfyui_u5_easyscripter.css`: Added collapse UI styles (.easyscripter-output-header, etc.)
  - Effects:
    - Can efficiently use screen space even with large log volume
    - Script editing area widely available (when log collapsed)
    - Greatly improved text readability
  - Compatibility:
    - Complete compatibility with existing workflows (default all-line display)
    - Maintained compatibility with resize handler
    - Maintained compatibility with LOOP_SUBGRAPH() preview window

### v2.6.2 (2025-10-14)
- **Adjusted Node Category Hierarchy**: Improved ComfyUI's add node menu structure
  - Before: Add Node > u5
  - After: Add Node > u5 > EasyScripter
  - Implementation details:
    - `scripter_node.py`: Changed CATEGORY definition from "u5" to "u5/EasyScripter"
  - Effects:
    - Hierarchical organization of u5 custom node group
    - Improved expandability of future u5 series nodes

### v2.6.1 (2025-10-14)
- **OPTIMAL_LATENT Multiple Word Search Feature Added**: Model name search more flexible
  - New feature: AND search with space-separated multiple words
    - Word-by-word matching: All words must be included
    - Automatic numeric variation generation: "1.5" → also tries ["1.5", "15"]
    - Two-digit number ones place omission: "2.0" → also tries ["2.0", "20", "2"]
    - Case insensitive: "SD 1.5" = "sd 1.5" = "Sd 1.5"
  - Search priority:
    1. Exact match with space (e.g., prioritize alias "sd 1.5" if exists)
    2. Traditional search after removing space (existing behavior)
    3. Multiple word AND search (new feature)
  - Usage examples:
    ```vba
    ' Multiple word search examples
    result = OPTIMAL_LATENT("sd 1.5", 512, 512)        ' Identifies SD1.5
    result = OPTIMAL_LATENT("stable diffusion 1.5", 512, 512)  ' Identifies SD1.5
    result = OPTIMAL_LATENT("sdxl turbo", 1024, 1024)  ' Identifies SDXL
    result = OPTIMAL_LATENT("SD 2.0", 768, 768)        ' Identifies SD2.0
    ```
  - Implementation details:
    - `functions/model_functions.py`: Added `generate_numeric_variations()` function (numeric variation generation)
    - `functions/model_functions.py`: Added `identify_model_multiword()` function (multiple word AND search)
    - `functions/model_functions.py`: Extended `identify_model()` function (exact match → traditional search → multiple word search)
    - `script_engine.py`: Added OPTIMAL_LATENT function to engine-aware functions
  - Test: Added 18 pattern test cases to tests/test_optimal_latent_multiword.py (all succeeded)
  - Backward compatibility: 100% maintained (existing single word search completely works)


### v2.6.0 (2025-10-14)
- **HTTP/HTTPS Communication Feature Added**: Communication with external Rest APIs now possible
  - New feature: Implemented HTTP communication built-in functions (7 functions)
    - `HTTPGET(url, [headers])`: Send HTTP GET request
    - `HTTPPOST(url, body, [headers])`: Send HTTP POST request
    - `HTTPPUT(url, body, [headers])`: Send HTTP PUT request
    - `HTTPDELETE(url, [headers])`: Send HTTP DELETE request
    - `HTTPJSON(url, method, [json_body], [headers])`: JSON format communication (automatic Content-Type setting)
    - `HTTPSTATUS()`: Get last HTTP request status code
    - `HTTPHEADERS()`: Get last HTTP response headers (JSON format)
  - Implementation details:
    - `functions/http_functions.py`: HttpFunctions class implementation (using urllib)
    - `builtin_functions.py`: Integrated HTTP functions into built-in functions
    - TDD compliance: Created test code before implementation (tests/test_http_functions.py)
  - Uses:
    - External API integration (weather API, translation API, etc.)
    - Webhook notification
    - RESTful API usage
    - JSON data get/send
  - Test: All 9 test cases succeeded (using JSONPlaceholder public API)
  - Built-in function count: 131 → 138 entries (7 functions added)

### v2.5.6 (2025-10-14)
- **Documentation Audit**: Verified README.md accuracy and HTML/Markdown consistency
  - Audit content:
    - Verified built-in function I/O rules, argument rules, output rules accuracy (95 functions + 36 aliases)
    - Checked usage example code compliance with official rules (reserved variables, argument types, function format)
    - HTML/Markdown consistency check (broken links, heading levels, content duplication)
  - Corrections:
    - PICKCSV function: Clarified 2-argument support (index specification) (README.md line 126-132)
    - PRINT function: Clarified only parenthesized function format supported, VBA statement format not supported (README.md line 194-195, 203)
    - Integer division operator: Confirmed documentation notation (`\\`) matches implementation (`\`)
  - Verification results:
    - ✅ Confirmed I/O rule accuracy for all 95 built-in functions
    - ✅ All usage example code complies with official rules (reserved variables, argument types)
    - ✅ 0 broken links, confirmed heading level consistency
  - Affected files:
    - `README.md`: Added PICKCSV function 2-argument sample, clarified PRINT function format
  - Documentation consistency: 100% (confirmed complete match between implementation and documentation)

### v2.5.5 (2025-10-13)
- **UI Fix**: Resolved widgets_values array order inconsistency issue
  - Issue:
    - After UI change, log window content interpreted as script, causing `Invalid character: '警'` error
    - Error only occurred in loop execution duplicate nodes (original node normal)
  - Cause analysis ("Ladder of Inference" framework investigation):
    - JavaScript widgets array order change: `[script, output]` → `[output, script]`
    - ComfyUI widgets_values array construction: `[output value, script value]` according to widgets array order
    - INPUT_TYPES mismatch: Only `[script]` defined → incorrectly passed `widgets_values[0]` (= output value, i.e., log) to script argument
  - Corrections:
    - `scripter_node.py`: Added `output` to INPUT_TYPES (1st position)
    - `scripter_node.py`: Added `output` argument to execute_script signature (read-only, ignored)
    - `web/comfyui_u5_easyscripter.js`: Deleted dynamic output widget creation (defined by INPUT_TYPES)
    - `web/comfyui_u5_easyscripter.js`: Deleted reorderWidgets function (no longer needed)
    - `web/comfyui_u5_easyscripter.js`: Modified configureOutputWidget (apply style to output widget defined by INPUT_TYPES)
  - Effects:
    - widgets_values array order `[output, script]` matches INPUT_TYPES definition
    - script receives correct script code (not log message)
    - No error occurs in loop execution
  - Implementation method:
    - Guarantee widgets_values array order consistency by matching INPUT_TYPES definition order with widgets array order
    - Correctly utilize ComfyUI internal logic (construct widgets_values array in widgets array order)
  - Implementation files:
    - `scripter_node.py`: Modified INPUT_TYPES, modified execute_script signature
    - `web/comfyui_u5_easyscripter.js`: Deleted dynamic widget creation, deleted reorderWidgets, modified configureOutputWidget

### v2.5.4 (2025-10-13)
- **UI Improvement**: Improved ScriptWidget manual resize freedom
  - Issue:
    - When enlarging node, scriptWidget minHeight dynamically increased, user couldn't shrink below certain point
    - Example: When node enlarged 600px→800px, minHeight increased 325px→525px, couldn't shrink below 525px
  - Cause:
    - In setupResizeHandler, recalculated and updated minHeight every time node resized
    - Side effect of "Use entire remaining space when LOOP not used" design intent
  - Corrections:
    - Implemented user manual resize detection mechanism (MutationObserver monitoring style.height)
    - Changed minHeight update in setupResizeHandler to conditional
    - When user manually resizes, skip minHeight update
    - When LOOP used (preview window present), always update minHeight (maintain v2.5.3 behavior)
  - Effects:
    - After user manually resizes textarea, minHeight fixed even when enlarging node
    - Shrink lower limit fixed at initial value (e.g., 282px), can freely shrink
    - maxHeight always updated, so expansion direction freedom also secured
    - LOOP usage behavior unchanged (maintained v2.5.3 fix)
  - Implementation method:
    - onNodeCreated: Initialize `_user_manually_resized_script` flag
    - configureScriptWidget: Monitor style.height changes with MutationObserver
    - setupResizeHandler: Update minHeight with `!_user_manually_resized_script || _has_preview_widgets` condition
  - Implementation files:
    - `web/comfyui_u5_easyscripter.js`: Added initialization flag, implemented MutationObserver, conditional minHeight update

### v2.5.3 (2025-10-13)
- **UI Improvement**: Resolved preview window overlap issue when executing LOOP_SUBGRAPH()
  - Issue:
    - After LOOP_SUBGRAPH() execution, when preview window added, displayed overlapping with existing scriptWidget
    - JS side couldn't detect preview window addition, layout recalculation not performed
  - Cause analysis ("Ladder of Inference" framework investigation):
    - ComfyUI has no event handler dedicated to widget addition
    - Preview window already added to node.widgets array at onExecuted timing, but JS side not detected
    - scriptWidget minimum height 180px fixed, no space for preview window addition
  - Corrections:
    - Changed scriptWidget minimum height from 180px → 50px (user manually adjustable)
    - Added widget count monitoring functionality in onExecuted
    - Added preview window support logic in setupResizeHandler
    - Automatically trigger layout recalculation when detected
  - Effects:
    - LOOP not used: Maintain existing layout quality (scriptWidget uses entire remaining space)
    - LOOP execution: Automatically detect preview window addition
    - LOOP execution: scriptWidget shrinks to 50px, secures sufficient space for preview window
    - LOOP execution: User can manually adjust scriptWidget with textarea resize
  - Implementation method:
    - Completely tracked ComfyUI→JS event flow (LOOP_SUBGRAPH execution → subgraph duplication → preview addition → onExecuted)
    - Monitored node.widgets.length in onExecuted (expected 2 vs actual)
    - When preview window detected, set _has_preview_widgets flag to true
    - Conditional branch in setupResizeHandler (preview present: 50px fixed, none: dynamic calculation)
  - Implementation files:
    - `web/comfyui_u5_easyscripter.js`: Modified UI_CONFIG, added onNodeCreated initialization flag, added onExecuted widget monitoring, added setupResizeHandler preview support logic

### v2.5.2 (2025-10-13)
- **UI Improvement**: Fixed ScriptWidget height calculation logic when node resizing
  - Issue:
    - When enlarging node, ScriptWidget height change smaller than node change, bottom margin increased
  - Cause analysis ("Ladder of Inference" framework investigation):
    - When outputWidget fixed height, scriptHeight calculated with `availableHeight * 0.65`
    - Remaining `availableHeight * 0.35` space unused, left as margin
    - Mechanism where margin increased as node enlarged
  - Corrections:
    - Changed scriptHeight calculation formula in setupResizeHandler
    - `availableHeight * scriptAreaRatio` → `availableHeight - output.minHeight - spacing`
    - Modified scriptWidget to use entire remaining space
  - Effects:
    - No margin generated even when enlarging node (margin: 0px)
    - ScriptWidget accurately follows node size changes
    - outputWidget maintains fixed height (100px)
  - Implementation method:
    - Completely tracked ComfyUI→JS event sequence
    - Analyzed onResize event flow and calculation logic
    - Identified root cause and verified fix plan
  - Implementation files:
    - `web/comfyui_u5_easyscripter.js`: Modified scriptHeight calculation formula in setupResizeHandler (line 299-302)

### v2.5.1 (2025-10-13)
- **UI Improvement**: Optimized node layout settings
  - Improvements:
    - Modified node minimum height to practical value (150px → 300px)
    - Deleted unused inputSocketAreaRatio parameter (code cleanup)
    - Clarified computeSizeHeight usage reason in comments (maintainability improvement)
  - Effects:
    - Widgets don't overlap even when shrinking node (minimum 300px)
    - Improved code readability and maintainability
  - Implementation method:
    - Staged implementation based on "Ladder of Inference" framework
    - Modified UI_CONFIG and added documentation comments
  - Implementation files:
    - `web/comfyui_u5_easyscripter.js`: Modified UI_CONFIG and added comments

### v2.5.0 (2025-10-13)
- **Code Quality Improvement**: Performed JavaScript UI code refactoring
  - Improvements:
    - Implemented debug log control functionality (enable/disable toggle with UI_CONFIG.debug.enabled flag)
    - Added debugLog() function, replaced all console.log calls (18 locations)
    - Standardized style settings (applyWidgetStyles function)
    - Isolated message processing (parseExecutionMessage function)
    - Split onNodeCreated method into 5 small functions (225 lines → 42 lines)
  - Split functions:
    - configureScriptWidget(): Script widget settings
    - configureOutputWidget(): Output widget settings
    - reorderWidgets(): Widget order change
    - setupResizeHandler(): Resize handler settings
    - setupConfigureHandler(): Configuration handler (delayed initialization)
  - Effects:
    - Greatly improved readability (clarified function responsibilities)
    - Improved maintainability (applied DRY principle, reduced duplicate code)
    - Improved debugging efficiency (centralized log control)
    - Facilitated feature addition (improved expandability through modularization)
  - Breaking changes: None (maintained 100% existing functionality)
  - Implementation files:
    - `web/comfyui_u5_easyscripter.js`: Overall refactoring

### v2.4.2 (2025-10-13)
- **UI Improvement**: Implemented node layout dynamic calculation functionality
  - Improvements:
    - Dynamically calculate input socket area height based on actual socket count
    - Improved UI_CONFIG structure: Renamed `headerSpace` → `inputSocketArea`
    - Added socket-related constants: `socketHeight: 20`, `socketSpacing: 5`, `nodeHeaderHeight: 30`
    - Newly implemented `calculateInputSocketAreaHeight()` function
  - Effects:
    - Eliminated inefficient layout from fixed percent (20%)
    - Accurate height calculation according to socket count (7 for EasyScripter)
    - More flexible and maintainable UI implementation
  - Implementation files:
    - `web/comfyui_u5_easyscripter.js`: Dynamic calculation function and UI_CONFIG update, improved 3-location calculation logic

### v2.4.1 (2025-10-09)
- **LOOP_SUBGRAPH Decimal String Support**: Improved to accept strings containing decimal points in arguments
  - Improvements:
    - Changed count argument type conversion from `int(count)` to `int(float(count))`
    - Accept decimal strings (e.g., "1.3", "99.9"), truncate to integer
    - Completely maintained existing integer/integer string behavior (100% backward compatibility)
  - Implementation files:
    - `functions/loop_functions.py`: Modified builtin_loop_subgraph function count conversion logic
  - Test: Added 9 pattern decimal string tests to tests/test_loop_subgraph.py (all succeeded)
  - Documentation: Added argument description and usage examples to docs/02_builtin_functions/10_loop_functions.md

### v2.4.0 (2025-10-09)
- **LOOP_SUBGRAPH Major Enhancement (v1.2)**: Implemented subgraph automatic detection and collection functionality
  - New features:
    - Automatically recognize all subsequent nodes connected to EasyScripter as subgraph
    - Duplicate entire subgraph specified number of times for repeated execution
    - Automatically disable loop if no connection (no error)
    - Completely maintain backward compatibility (existing code requires no changes)
  - Implementation details:
    - `scripter_node.py`: Added subgraph detection/collection functionality
      - `_get_downstream_nodes()`: Get subsequent nodes connected to output slot
      - `_is_subgraph()`: Determine if subsequent node is subgraph
      - `_collect_subgraph_nodes()`: Recursively collect all nodes reachable from start node
      - `_build_loop_subgraph()`: Completely implemented subgraph duplication and node reference update logic
  - Behavior:
    - Identify output slot corresponding to channel (RETURN1/RETURN2/RELAY)
    - Detect subsequent nodes, perform subgraph determination
    - If subgraph: Collect all nodes → duplicate for iteration count → update node ID (`{original_id}_loop_{iteration}` format)
    - If not subgraph: Disable loop and return normal output
  - Test: Added subgraph detection test to tests/test_loop_subgraph.py
  - Documentation: Added v1.2 improvements to docs/02_builtin_functions/10_loop_functions.md

- **LOOP_SUBGRAPH Multiple Channel Support (v1.3)**: Individual loop settings for different channels in same script now possible
  - New features:
    - Individual settings for multiple channels: Can set different repeat counts for RETURN1, RETURN2, RELAY
    - Integrated execution of same subgraph: When multiple channels connected to same subgraph, sum counts and execute sequentially
    - AUTO mode extension: `LOOP_SUBGRAPH(5, None)` applies loop settings to all connected channels
    - Last-wins priority rule: When same channel called multiple times, later called setting prioritized
    - Complete backward compatibility: Existing single channel behavior unchanged
  - Implementation details:
    - `script_engine.py`: Changed loop_config structure from single dictionary to channel-specific dictionary
    - `functions/loop_functions.py`: Implemented channel-specific setting storage and last-wins priority logic
    - `scripter_node.py`: Added 5 helper methods
      - `_get_channel_slots()`: Convert channel name to output slot number
      - `_get_channel_outputs()`: Get channel output values
      - `_expand_auto_config()`: Expand all connected channels in AUTO mode
      - `_group_by_subgraph()`: Group channels by subgraph
      - `_duplicate_subgraph_iteration()`: Duplicate subgraph for 1 iteration
    - `_build_loop_subgraph()`: Completely implemented multiple channel integrated execution logic
  - Test: Added multiple channel test cases to tests/test_loop_subgraph.py (all succeeded)
  - Documentation: Added v1.3 improvements and practical examples to docs/02_builtin_functions/10_loop_functions.md

### v2.3.0 (2025-10-09)
- **Subgraph Loop Execution Feature Added**: N-times repeated execution possible with LOOP_SUBGRAPH function
  - New feature: Implemented `LOOP_SUBGRAPH(count, channel)` function
  - Supported channels: RETURN1, RETURN2, RELAY (ANY type output)
  - Repeat count: Can specify in range 1-100 times
  - Implementation details:
    - `functions/loop_functions.py`: Implemented LOOP_SUBGRAPH function
    - `script_engine.py`: Added loop_config management and engine passing functionality
    - `builtin_functions.py`: Added function registration and special_functions list
    - `scripter_node.py`: Added hidden inputs (unique_id, dynprompt), implemented subgraph detection logic
  - Test: Verified basic operation with tests/test_loop_subgraph.py

### v2.2.2 (2025-10-08)
- **CSVSORT Function Signature Fix**: Added delimiter argument to match documentation and implementation
  - Issue: `CSVSORT(tags, ",", FALSE)` call error "Given 3 arguments but only accepts 1-2 arguments"
  - Cause: Implementation `CSVSORT(csv_text, descending)` 2 arguments, documentation `CSVSORT(csv_text, [delimiter], [descending])` 3 arguments mismatch
  - Fix: Added `delimiter` argument to implementation, changed to `CSVSORT(csv_text, delimiter=",", descending=False)`
  - Affected files:
    - `functions/csv_functions.py`: Modified CsvFunctions.CSVSORT method
    - `Release/functions/csv_functions.py`: Same as above
    - `docs/02_builtin_functions/04_csv_functions.md`: Updated signature and sample
    - Backward compatibility: 1-argument call `CSVSORT("a,b,c")` continues to work (delimiter="," is default)
  - New feature: Custom delimiter support like semicolon (e.g., `CSVSORT("z;a;m", ";")`)

### v2.2.1 (2025-10-08)
- **Integer Division Operator (\) Implementation Complete**: VBA-compliant integer division operator working normally
  - script_parser.py: Added INTDIV token pattern (`r'^\\'`)
  - script_parser.py: Added INTDIV processing to parse_multiplication method
  - script_engine.py: Added integer division logic to evaluate_binary_op (`int(left_num // right_num)`)
  - Documentation: Confirmed existing description in docs/01_syntax_reference.md:154

- **FORMAT Function Bug Fix**: Modified implementation order so VBA format simple specifications ("0.0", etc.) work correctly
  - Issue: `FORMAT(1.2, "0.0")` returned `"1e+00"` (scientific notation)
  - Cause: Python standard `format(value, format_string)` tried first
  - Fix: Changed order to check VBA format simple specifications ("0", "0.0", "0.00") with highest priority
  - Affected files: FORMAT method in `functions/misc_functions.py`
  - Verification: Confirmed operation via ScriptEngine (confirmed RESULT1 correctly returns "1.2")

### v2.2.0 (2025-10-08)
- **hot fix**:
  - Minor bug fixes

### v2.1.1 (2025-10-06)
- **Character Encoding Fix**: Resolved Japanese string mojibake issue
  - script_parser.py: Removed unicode_escape decode, only replace explicit escape sequences (\n, \t, \r, \\)
  - scripter_node.py: Added explicit UTF-8 encoding guarantee to RETURN values
  - Modified so Japanese displays correctly in both PRINT output and node-to-node string passing

### v2.1.0 (2025-10-06)
- **Function Corrections**: Fixed argument specifications for CSVSORT, CSVCOUNT, ARRAY functions

### v2.0.0 (2025-10-03)
- Complete documentation system renewal
- Simplified README.md, separated detailed documentation

### v1.5.0 (2025-10-02)
- Added OPTIMAL_LATENT function (30+ model support)
- Implemented u5 loader series (9 types)
- Added ANY type input and relay_output functionality

### v1.0.0
- Initial release
- VBA-style script execution engine
- Basic built-in function implementation

---

[← Back to Main Documentation](README.md)
