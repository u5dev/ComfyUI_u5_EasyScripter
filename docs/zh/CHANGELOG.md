# 更新历史 (CHANGELOG)

[日本語](../CHANGELOG.md) | [English](../en/CHANGELOG.md) | [中文](../zh/CHANGELOG.md) | [Español](../es/CHANGELOG.md) | [Français](../fr/CHANGELOG.md) | [Deutsch](../de/CHANGELOG.md)

---

u5 EasyScripter的主要版本更新历史。

---

## 📝 更新历史


### v3.1.2 (2025-11-18) - 文档格式修正

#### Fixed
- **函数数量交叉引用修正**: 修正docs/02_builtin_functions/00_index.md中的函数数量以匹配实际实现数量
  - 数学函数: 24个 → 16个
  - CSV函数: 11个 → 9个
  - 数组函数: 7个 → 3个
  - 模型函数: 3个 → 1个
  - 实用函数: 21个 → 18个
  - 循环控制函数: 9个 → 1个
  - HTTP通信函数: 17个 → 9个
  - Python函数执行: 3个 → 4个
- **快速参考表修正**: 修正00_index.md的快速参考表
  - 从数学函数表中删除不存在的8个函数(RND, RANDOMIZE, FIX, SGN, ASIN, ACOS, ATAN, ATAN2)
  - 修正CSVDIFF函数参数: CSVDIFF(csv1, csv2) → CSVDIFF(array_name, csv1, csv2)
  - 将PYDECODE函数添加到Python函数表
- **字符串函数数修正**: 修正docs/02_builtin_functions/02_string_functions.md的函数数量29个→28个
- **目录锚点链接修正**: 从docs/01_syntax_reference.md的目录锚点链接中删除开头的连字符(符合GitHub Markdown规范)

### v3.1.1 (2025-11-17) - 字符串函数文档添加

#### Added
- **字符串函数文档添加**: 添加7个已实现字符串函数的文档
  - **ESCAPEPATHSTR(path, [replacement])**: 替换或删除文件路径的禁用字符
  - **URLENCODE(text, [encoding])**: URL编码(百分比编码)
  - **URLDECODE(text, [encoding])**: URL解码
  - **PROPER(text)**: 转换为标题大小写(每个单词首字母大写)
  - **CHR(code)**: 字符代码→字符转换(ASCII范围)
  - **ASC(char)**: 字符→字符代码转换
  - **STR(value)**: 数值→字符串转换
  - 文档: docs/02_builtin_functions/02_string_functions.md
  - 函数计数: 21个 → 23个修正

#### Changed
- **内置函数总数**: 135条目 → 137条目更新
  - 135个唯一函数(133个函数 + 2个别名)
  - 更新README.md、docs/02_builtin_functions/00_index.md

### v3.1.0 (2025-11-17) - != 运算符支持

#### Added
- **!= 运算符**: 添加C语言风格的不等运算符
  - 与`<>`运算符完全相同的行为(两者都可使用)
  - 实现: script_parser.py (添加到TOKEN_PATTERNS数组)
  - 测试: tests/test_neq_operator.py
  - 文档: docs/01_syntax_reference.md

### v3.0.0 (2025-11-13) - Any_input输入套接字相关增强等

### Added
- **IMAGETOBASE64函数**: 添加将IMAGE tensor或图像文件路径转换为Base64编码(或data URL格式)的函数
  - 支持OpenAI等Vision API发送数据生成
  - 支持IMAGE tensor(ComfyUI节点连接)和文件路径输入
  - 提供调整大小、JPEG压缩(quality=85)、RGBA→RGB转换、Base64/data URL返回功能
  - 实现: functions/misc_functions.py (MiscFunctions.IMAGETOBASE64)
  - 文档: docs/02_builtin_functions/09_utility_functions.md

- **IMAGETOBYTEARRAY函数**: 添加将IMAGE tensor或图像文件路径转换为JSON数组(或字节数组)的函数
  - 支持Cloudflare Workers AI等REST API发送数据生成
  - 支持IMAGE tensor(ComfyUI节点连接)和文件路径输入
  - 提供调整大小、JPEG压缩、RGBA→RGB转换、JSON数组/bytes类型返回功能
  - 实现: functions/misc_functions.py (MiscFunctions.IMAGETOBYTEARRAY)
  - 文档: docs/02_builtin_functions/09_utility_functions.md

- **FORMAT函数**: 添加按指定格式格式化数值・日期时间的函数(VBA兼容)
  - 支持VBA格式("0", "0.0", "0.00", "#.##")、Python format格式、日期时间strftime格式
  - 实现: functions/misc_functions.py (MiscFunctions.FORMAT)
  - 文档: docs/02_builtin_functions/07_type_functions.md

- **GETANYTYPE函数**: 添加判定ANY类型数据类型名称的函数
  - 判定基本类型(int, float, string)、ComfyUI类型(image, latent, model, vae, clip等)
  - 可从any_input输入套接字自动获取或明确指定数据
  - 实现: functions/misc_functions.py (MiscFunctions.GETANYTYPE)
  - 文档: docs/02_builtin_functions/09_utility_functions.md

- **GETANYVALUEINT函数**: 添加从ANY类型数据获取整数值的函数
  - 可从any_input输入套接字自动获取或明确指定数据
  - 无法获取时返回0
  - 实现: functions/misc_functions.py (MiscFunctions.GETANYVALUEINT)
  - 文档: docs/02_builtin_functions/09_utility_functions.md

- **GETANYVALUEFLOAT函数**: 添加从ANY类型数据获取浮点数值的函数
  - 可从any_input输入套接字自动获取或明确指定数据
  - 无法获取时返回0.0
  - 实现: functions/misc_functions.py (MiscFunctions.GETANYVALUEFLOAT)
  - 文档: docs/02_builtin_functions/09_utility_functions.md

- **GETANYSTRING函数**: 添加从ANY类型数据获取字符串的函数
  - 可从any_input输入套接字自动获取或明确指定数据
  - 无法获取时返回空字符串
  - 实现: functions/misc_functions.py (MiscFunctions.GETANYSTRING)
  - 文档: docs/02_builtin_functions/09_utility_functions.md

- **GETANYWIDTH函数**: 添加获取IMAGE/LATENT类型数据宽度(像素数)的函数
  - 可从any_input输入套接字自动获取或明确指定数据
  - 同时支持IMAGE类型・LATENT类型
  - 实现: functions/misc_functions.py (MiscFunctions.GETANYWIDTH)

- **GETANYHEIGHT函数**: 添加获取IMAGE/LATENT类型数据高度(像素数)的函数
  - 可从any_input输入套接字自动获取或明确指定数据
  - 同时支持IMAGE类型・LATENT类型
  - 实现: functions/misc_functions.py (MiscFunctions.GETANYHEIGHT)

### Changed
- **LOOPSUBGRAPH顺序执行保证**: 迭代改为顺序执行而非并行执行
  - 每个迭代等待前一迭代完成
  - 保证NOW()、RND()、PRINT()等函数在每个迭代中重新评估
  - 内部实现: 通过`_iteration_dependency`虚拟输入的依赖关系链(仅EasyScripter节点)
  - 向后兼容性: 不影响现有工作流(optional input)
  - 性能影响: 执行时间与迭代次数成正比增加
  - 实现: scripter_node.py (_duplicate_subgraph_iteration, _build_loop_subgraph, INPUT_TYPES, _execute_script_impl)

### Fixed
- **LOOPSUBGRAPH迭代次数bug修正**: 修正执行次数少于指定次数1次的bug
  - 问题: `LOOPSUBGRAPH(5)`只执行4次
  - 原因: 错误使用了`range(1, total_count)`(range(1,5)=[1,2,3,4])
  - 修正: 改为`range(total_count)`(range(5)=[0,1,2,3,4])
  - 实现: scripter_node.py L645

- **LOOPSUBGRAPH依赖关系添加逻辑修正**: 修正对标准ComfyUI节点的错误依赖关系添加
  - 问题: `TypeError: Int.execute() got an unexpected keyword argument '_iteration_dependency'`
  - 原因: 对PrimitiveInt等标准ComfyUI节点添加了`_iteration_dependency`输入
  - 修正: 仅对EasyScripter节点(`class_type=="comfyUI_u5_easyscripter"`)添加依赖关系
  - 实现: scripter_node.py L542-549

- **execute_script方法签名修正**: 修正`_iteration_dependency`参数缺失bug
  - 问题: `TypeError: ComfyUI_u5_EasyScripterNode.execute_script() got an unexpected keyword argument '_iteration_dependency'`
  - 原因: 公共方法`execute_script`忘记添加`_iteration_dependency`参数(仅添加到内部方法`_execute_script_impl`)
  - 修正: 在`execute_script`签名中添加`_iteration_dependency=None`,在`enqueue_and_wait`调用中传递参数
  - 实现: scripter_node.py L89-92, L140

- **LOOPSUBGRAPH原始节点删除不完整**: 修正执行次数多于指定次数1次的bug
  - 问题: `LOOPSUBGRAPH(5)`执行6次(原始节点 + 复制5次)
  - 原因: expand添加复制节点,但未删除原始子图节点
  - 症状: 后续节点输出过去的时间戳(上次执行的缓存)
  - 修正: 使用`remove`键明确删除原始节点ID
  - 实现: scripter_node.py L621, L643-645, L683

- **LOOPSUBGRAPH顺序执行bug修正**: 修正迭代间以相同时间戳执行的bug
  - 问题: `LOOPSUBGRAPH(5)`多个迭代在同一秒执行(第2个和第3个等)
  - 原因:
    - `_duplicate_subgraph_iteration`只返回最后处理的节点ID
    - 未返回实际图结构上的最终节点(tail)
    - 结果,下一迭代的依赖关系未正确设置导致并行执行
  - 修正:
    - 添加检测原始子图最终节点(tail)的`_find_subgraph_tail_node`方法
    - 为`_duplicate_subgraph_iteration`添加`original_tail_node_id`参数
    - 基于原始tail精确计算复制版tail(`{original_tail}_loop_{iteration}`)
    - 仅创建iteration 1到total_count的复制,保留原始节点作为第1次
  - 结果: 原始(第1次)→ 复制4次(第2-5次)完全顺序执行
  - 实现: scripter_node.py L565-617(`_find_subgraph_tail_node`添加), L455,466,555-563(`_duplicate_subgraph_iteration`修正), L708-710,729(原始tail检测和参数传递)

- **CDATE函数**: 添加将日期字符串转换为日期类型的函数(VBA兼容)
  - 灵活的格式支持:
    - 完整日期时间: `"2025/11/05 15:39:49"` → `2025/11/05 15:39:49`
    - 仅日期: `"2025/11/05"` → `2025/11/05 00:00:00`
    - 仅年月: `"2025/11"` → `2025/11/01 00:00:00`
    - 仅年: `"2025"` → `2025/01/01 00:00:00`
    - 也支持时间部分补全
  - 分隔符的灵活性: 允许`/`、`-`、`:`、空格混用
  - 实现文件: `functions/date_functions.py`
  - 文档: 在`docs/02_builtin_functions/03_datetime_functions.md`中添加详细信息
  - 内置函数总数: 日期时间函数 14 → 15个

### v2.9.0 (2025-10-29) - 产品名称表示统一和多语言支持增强


- **多语言支持的完整实现**: 所有系统消息支持多语言
  - 支持语言: 日语、英语
  - 在locales.py中添加121个消息键(既有57个 + 新增64个)
  - 删除所有硬编码的日语消息
  - 目标模块:
    - scripter_node.py: 将全部27处硬编码日语多语言化
    - script_execution_queue.py: 将全部16处硬编码日语多语言化
    - functions/loop_functions.py: 将全部8处硬编码日语多语言化
    - functions/misc_functions.py: 将全部13处硬编码日语多语言化(OUTPUT/INPUT/ISFILEEXIST函数)
  - 在所有模块中统一传播locale参数:
    - scripter_node → script_execution_queue
    - scripter_node → script_engine → loop_functions
    - scripter_node → script_engine → misc_functions
  - ComfyUI控制台输出也完全支持多语言
  - 测试: 全部34个测试用例成功(tests/test_scripter_node_localization.py)


- **SLEEP函数**: 添加暂停处理的实用函数
  - 功能: 暂停处理指定的毫秒数(sleep)
  - 参数: `milliseconds`(float、可选、默认: 10ms)
  - 返回值: 无(内部返回0.0)
  - 主要用途:
    - WHILE()循环的速度控制(降低CPU使用率)
    - 处理等待
    - 调试用暂停
  - ComfyUI集成:
    - 与ComfyUI的基于线程的排队控制(ScriptExecutionQueue)协同工作
    - 通过time.sleep()同步阻塞执行
    - ScriptExecutionQueue保证多个EasyScripter节点同时执行时的安全性
  - 实现文件: `functions/misc_functions.py`(VRAMFREE函数之后)
  - 测试: 全部10个测试用例成功(tests/test_sleep_function.py)
  - 文档: 在`docs/02_builtin_functions/09_utility_functions.md`中添加详细信息
  - 内置函数总数: 133 → 134条目(132个唯一函数,包含2个别名)

- **VRAMFREE函数**: 添加释放VRAM和RAM的实用函数
  - 功能: 执行模型卸载、缓存清除、垃圾收集
  - 参数: `min_free_vram_gb`(float、可选)可指定执行阈值
  - 返回值: 以dict格式返回执行结果的详细信息
    - `success`: 执行成功标志(bool)
    - `freed_vram_gb`: 已释放的VRAM量(float)
    - `freed_ram_gb`: 已释放的RAM量(float)
    - `actions_performed`: 已执行的操作列表(list)
  - ⚠️ WARNING: 因为是精密操作,使用时需要注意
  - 实现文件: `functions/misc_functions.py`
  - 测试: 所有测试用例成功(tests/test_vramfree.py)
  - 文档: 在`docs/02_builtin_functions/09_utility_functions.md`中添加详细信息

- **ISFILEEXIST函数**: 添加文件存在检查和扩展信息获取功能
  - 基本功能: 检查ComfyUI输出文件夹内的文件是否存在
  - 扩展功能: 支持4种模式
    - `flg=""` (默认): 仅存在检查("TRUE"/"FALSE")
    - `flg="NNNN"`: 搜索序号文件的最大编号(例: `output_0003.png`)
    - `flg="PIXEL"`: 获取图像大小("[width, height]"格式)
    - `flg="SIZE"`: 获取文件大小(字节数)
  - 安全性: 拒绝绝对路径・UNC路径(仅允许相对路径)
  - 目标目录: ComfyUI环境下为`ComfyUI/output/`下,测试环境下为当前目录下
  - 支持图像格式: PNG, JPEG, JPG, BMP, WEBP
  - 返回值: 全部为字符串类型(str),出错时返回"FALSE"
  - 实现文件: `functions/misc_functions.py`
  - 测试: 全部14个测试用例成功(tests/test_isfileexist.py)
  - 文档: 在`docs/02_builtin_functions/09_utility_functions.md`中添加详细信息
  - 内置函数总数: 131 → 132条目(130个唯一函数,包含2个别名)


- **RELAY_OUTPUT变量**: 现在可以在脚本内给`RELAY_OUTPUT`变量赋值来控制relay_output输出套接字(ANY类型)的值
  - 用途: 传递通过INPUT函数读取的图像(torch.Tensor)等ANY类型数据到后续节点
  - 向后兼容性: 未使用RELAY_OUTPUT时,按照传统方式直通any_input输入
  - 实现: script_engine.py, scripter_node.py
  - Tier 3功能: 实现完成,测试完成(PASS)
  - 文档:
    - `docs/01_syntax_reference.md`: 在保留变量部分添加RELAY_OUTPUT变量说明
    - `docs/02_builtin_functions/09_utility_functions.md`: 在INPUT函数部分添加RELAY_OUTPUT联动示例

- **INPUT函数**: 添加文件读取功能(v2.2.0添加)
  - 从ComfyUI输出文件夹读取文件
  - 自动判定文本、JSON(数值/数组)、图像(torch.Tensor)、二进制数据类型
  - 作为OUTPUT函数的对称函数实现
  - 安全功能: 拒绝绝对路径・UNC路径(仅允许相对路径)
  - 读取源: ComfyUI环境下为`ComfyUI/output/`下,测试环境下为当前目录下
  - 错误处理: 找不到文件时输出警告PRINT并返回None
  - 支持类型:
    - 文本文件 (.txt, .md) → str类型
    - JSON数值 → float类型
    - JSON数组 → list类型
    - 图像文件 (.png, .jpg等) → torch.Tensor类型(ComfyUI兼容)
    - 其他 → bytes类型(二进制)
  - Tier 1功能(文本/数值/数组): 测试完成(PASS)
  - Tier 2功能(图像): 已实现,测试未实施
  - Tier 3功能(Latent/RELAY_OUTPUT): 未实现,作为将来扩展

- **文档更新**:
  - `docs/02_builtin_functions/09_utility_functions.md`: 添加INPUT函数的详细文档
  - `docs/02_builtin_functions/00_index.md`: 更新实用函数数量6→7个,全128条目(126个唯一函数,包含2个别名)
  - `docs/00_documentation_index.md`: 更新到全131条目,添加文件输入输出部分
  - `README.md`: 更新内置函数总数到131条目(129个唯一函数,包含2个别名)


- **OUTPUT函数**: 添加文件输出功能
  - 支持输出文本、数值、数组、图像(torch.Tensor)、二进制数据
  - 支持NEW模式(避免重复,自动添加`_0001`、`_0002`...)和ADD模式(追加)
  - 支持从保留变量(TXT1、TXT2、ANY_INPUT)直接输出
  - 安全功能: 拒绝绝对路径・UNC路径(仅允许相对路径)
  - 自动递归创建子目录
  - 扩展名自动补全(`.txt`、`.png`等)
  - 输出目标: ComfyUI环境下为`ComfyUI/output/`下,测试环境下为当前目录下

- **文档更新**:
  - `docs/02_builtin_functions/09_utility_functions.md`: 添加OUTPUT函数的详细文档
  - `docs/02_builtin_functions/00_index.md`: 更新实用函数数量5→6个,全127条目(125个唯一函数,包含2个别名)
  - `README.md`: 更新内置函数总数到130条目(128个唯一函数,包含2个别名)

### v2.8.2 (2025-10-27) - 删除不需要的函数(MSGBOX, INPUTBOX, LBOUND)

- **删除的函数**:
  - **MSGBOX**: 因为在ComfyUI工作流环境中显示对话框不合适而删除(可用PRINT代替)
  - **INPUTBOX**: 因为在ComfyUI无头环境中无法显示输入对话框而删除
  - **LBOUND**: 因为EasyScripter的数组是零基固定(始终返回0)而判断为不需要删除

- **影响部分**:
  - `builtin_functions.py`: 从BUILTIN_FUNCTIONS字典、is_builtin_function()、get_function_usage()中删除
  - `functions/base_functions.py`: 删除MSGBOX函数
  - `functions/misc_functions.py`: 删除INPUTBOX函数、LBOUND函数
  - `tests/audit_06_array_functions.py`: 删除LBOUND相关测试3件,将test_example_aggregate内的LBOUND使用替换为0
  - `README.md`: 更新数组函数(4→3)、实用函数(7→5)的计数
  - `docs/02_builtin_functions/00_index.md`: 更新到全126条目(-3)
  - `docs/02_builtin_functions/06_array_functions.md`: 删除LBOUND部分,将示例代码内LBOUND使用替换为0
  - `docs/02_builtin_functions/09_utility_functions.md`: 删除MSGBOX、INPUTBOX部分
  - 多语言版README(docs/zh/README.md、docs/en/README.md): 更新计数

- **向后兼容性**:
  - **破坏性变更**: 使用上述3个函数的现有脚本将无法工作
  - **推荐替代方法**:
    - MSGBOX → PRINT
    - INPUTBOX → VAL1, VAL2, TXT1, TXT2(节点输入)
    - LBOUND → 0(固定值)或FOR I = 0 TO UBOUND(arr[])

### v2.8.1 (2025-10-27) - 添加EXIT语句和单行IF语句支持(仅EXIT语句)

- **新功能**:
  - 添加EXIT语句支持
    - `EXIT FUNCTION`: 从函数早期返回
    - `EXIT FOR`: 从FOR循环早期退出
    - `EXIT WHILE`: 从WHILE循环早期退出
  - 添加单行IF语句支持(限于与EXIT语句组合)
    - 示例: `IF value < 0 THEN EXIT FUNCTION`
    - 也支持复杂条件式: `IF x < 0 AND y < 0 THEN EXIT FUNCTION`

- **规格变更**:
  - 函数返回值初始化: `0` → `""`(空字符串)
    - 修正使调用EXIT FUNCTION时未设置的返回值成为空字符串
    - 符合EasyScripter规格书

- **添加测试**:
  - `tests/test_exit_basic.py`: EXIT语句基本动作测试(10个测试用例)
  - `tests/test_one_line_if_exit.py`: 单行IF+EXIT边缘情况测试(8个测试用例)

- **向后兼容性**:
  - 现有的多行IF语句完全保持向后兼容性
  - 现有的所有测试用例(36个文件中27个文件)通过,无回归

### v2.7.9 (2025-10-22) - 全文档期望值审计项目完成

### v2.7.8 (2025-10-22) - Python函数文档期望值审计

### v2.7.7 (2025-10-22) - 模型函数文档期望值审计

### v2.7.6 (2025-10-22) - 类型函数文档期望值审计

### v2.7.5 (2025-10-22) - CSV函数文档期望值审计

### v2.7.4 (2025-10-22) - 文档未赋值变量审计项目

### v2.7.3 (2025-10-22) - 文档变量命名规则完全统一项目

### v2.7.2 (2025-10-22)
- **文档结构重构**: 信息统一和消除双重管理
  - **函数数表示的统一**: 在所有文档中统一为"129条目(127个唯一函数,包含2个别名)"
    - 修正对象: README.md, docs/00_documentation_index.md, docs/02_builtin_functions/00_index.md, docs/01_syntax_reference.md
    - 多语言版也更新: docs/en/README.md, docs/zh/README.md
  - **确立Single Source of Truth**: 指定docs/02_builtin_functions/00_index.md为唯一的完整参考索引
    - 简化docs/00_documentation_index.md的内置函数部分,委托给详细索引
    - 删除12个类别的单独列表,仅记载统计信息
  - **强化统计信息表**: 添加详细的函数数明细和备注
    - 明记各类别的注册条目数
    - 明确别名和独立实现的区别
  - **交叉引用验证**: 确认并修正所有文档间函数数记载的一致性

### v2.7.1 (2025-10-22)
- **文档结构整理**: 统一类别顺序和消除重复内容
  - 统一所有文档间的内置函数类别列表顺序(正规顺序: 1-12)
    - 修正对象: README.md, docs/00_documentation_index.md, docs/02_builtin_functions/00_index.md
  - 将docs/00_documentation_index.md重构为简洁索引(详细内容统合到README.md参考)
  - 准确化Python函数执行类别的函数数(1个→4个)
    - 准确计数PYEXEC、PYLIST、PYENCODE、PYDECODE 4个函数
  - 在所有文档中统一类别数为"12个"
  - 验证并修正交叉引用的准确性

### v2.7.0 (2025-10-15)
- **添加Python函数执行功能**: 可通过PYEXEC()函数执行标准/用户库的函数
  - 新功能: 实现`PYEXEC(func_path, [arg1], [arg2], ...)`函数
  - 支持库:
    - Python标准库: math, random, json, datetime, base64等
    - 用户已安装库: numpy, pandas, requests, hashlib等(轻量数据处理)
  - 安全性: 黑名单方式(仅阻止危险模块)
    - 阻止对象: os, sys, subprocess, eval, exec, compile, pickle, shelve, code, pdb
  - 类型转换规格:
    - None → 0.0, bool → 1.0/0.0, int → float
    - list/tuple → CSV字符串, dict → JSON字符串
    - numpy.ndarray → CSV字符串, pandas.DataFrame → JSON字符串
  - 限制事项:
    - 参数最多10个
    - 返回值大小最大1MB
    - 列表・数组元素数最大10000个
    - **注意**: 图像数据(cv2.imread等)会有数十万元素因此会超过限制错误
  - **重要**: Windows文件路径必须使用 `\\` (双反斜杠)
    - ❌ 错误: `"C:\test.csv"` → `\t` 被转换为制表符导致路径破损
    - ✅ 正确: `"C:\\test.csv"` 或 `"C:/test.csv"`
  - 实现详细:
    - `functions/python_functions.py`: PythonFunctions类实现
    - `builtin_functions.py`: 将PYEXEC函数统合到内置函数
    - 符合TDD: 实现前创建测试代码(tests/test_pyexec_standalone.py, test_pyexec_via_engine.py)
  - 测试: 全10个测试用例成功(确认通过ScriptEngine的动作完成)
  - 文档: 创建docs/02_builtin_functions/12_python_functions.md
  - 内置函数数: 138 → 139条目(添加1个函数)

### v2.6.5 (2025-10-14)
- **UI改善**: 调整日志区域的初始状态、高度、配置位置
  - 变更内容:
    - 修正使节点首次加载时日志区域以关闭状态加载
    - 将`UI_CONFIG.logDisplay.defaultState`从`EXPANDED`(展开)改为`COLLAPSED`(关闭状态)
    - 将日志区域的高度整体扩大2倍
      - 关闭状态: 40px → 80px(2倍)
      - 打开状态: 100px → 200px(2倍)
      - 最大高度: 150px → 300px(2倍)
    - 在日志区域和脚本区域之间添加20px间距
      - 将`UI_CONFIG.widgets.spacing`从10px→30px变更(+20px间距添加)
  - 效果:
    - 首次加载时高效利用画面空间
    - 日志区域变宽,可确认更多输出内容
    - 关闭状态也可显示约2行日志
    - 日志区域和脚本区域之间有余裕,可见性提高
    - 脚本编辑区域以宽广状态开始
    - 用户可根据需要点击展开日志区域
  - 实现文件:
    - `web/comfyui_u5_easyscripter.js`: defaultState修正(line 822),高度设置2倍化(line 788-794)
    - `web/comfyui_u5_easyscripter.js`: spacing变更(line 796: 10→30)
  - 向后兼容性:
    - 现有工作流的折叠状态优先保存值(工作流JSON内的logDisplayState属性)
    - 仅新节点默认改为关闭状态
    - 现有工作流也受益于间距扩大

### v2.6.4 (2025-10-14)
- **脚本语法扩展**: 添加行内注释功能
  - 新功能: 可在语句后方用`'`记述注释
    - 示例: `PRINT(VAL1) '这是注释`
    - 示例: `RETURN1 = VAL1 + VAL2 '计算合计`
  - 实现方法:
    - 字符串文字内的`'`受保护(不解释为行内注释)
    - 字符串文字外的`'`之后到行末作为注释删除
    - 行首注释的动作无变更(100%保持既有功能)
  - 实现文件:
    - `script_parser.py`: 在tokenize方法中添加行内注释处理逻辑
    - `tests/test_inline_comment.py`: 创建8种模式的测试用例(全部成功)
  - 效果:
    - 脚本可读性提高(可在同一行记述代码和说明)
    - 进一步重现VBA式记述风格
    - 与既有脚本100%向后兼容
  - 符合TDD: 以测试优先开发方式实现(实现前创建测试代码・确认失败→实现→确认成功)

### v2.6.3 (2025-10-14)
- **UI改善**: 日志区域折叠功能和文本可读性提高
  - 新功能:
    - 可通过点击日志区域在1行显示⇄全行显示之间切换
    - 工作流保存时保持折叠状态(会话持久化)
    - 折叠时自动调整脚本区域的Y坐标
    - 用视觉指示器(▶/▼图标)显示折叠状态
  - 可读性提高:
    - 脚本区域: 字体大小 13px→14px,行间距 1.5→1.6
    - 输出区域: 背景色和文本色的对比度提高
    - 应用等宽字体提高可读性
  - 实现详细:
    - `web/comfyui_u5_easyscripter.js`: 实现折叠功能(添加setupLogToggle函数)
    - `web/comfyui_u5_easyscripter.js`: 添加布局重计算函数(updateLayoutForLogState函数)
    - `web/comfyui_u5_easyscripter.js`: 修正setupResizeHandler以对应折叠状态
    - `web/comfyui_u5_easyscripter.css`: 添加折叠UI用样式(.easyscripter-output-header等)
  - 效果:
    - 即使日志量多也可高效利用画面空间
    - 脚本编辑区域可广泛使用(日志折叠时)
    - 文本可读性大幅提高
  - 兼容性:
    - 与既有工作流完全兼容(默认为全行显示)
    - 维持与调整大小处理器的兼容性
    - 维持与LOOP_SUBGRAPH()预览窗口的兼容性

(由于长度限制,以下版本历史已省略部分详细内容)

### v2.6.2 (2025-10-14)
- 调整节点类别层次结构
  - 变更前: 添加节点 > u5
  - 变更后: 添加节点 > u5 > EasyScripter

### v2.6.1 (2025-10-14)
- OPTIMAL_LATENT多单词搜索功能

### v2.6.0 (2025-10-14)
- 添加HTTP/HTTPS通信功能

### v2.5.x系列 (2025-10-13~14)
- UI改善和JavaScript代码重构

### v2.4.x系列 (2025-10-09~13)
- LOOP_SUBGRAPH功能大幅增强

### v2.3.0 (2025-10-09)
- 添加子图循环执行功能

### v2.2.x系列 (2025-10-08)
- 各种函数修正和改善

### v2.1.x (2025-10-06)
- 字符编码修正

### v2.0.0 (2025-10-03)
- 文档体系完全更新
- 简化README.md,分离详细文档

### v1.5.0 (2025-10-02)
- 添加OPTIMAL_LATENT函数(支持30+模型)
- 实现u5加载器系列(9种)
- 添加ANY类型输入和relay_output功能

### v1.0.0
- 首次发布
- VBA风格脚本执行引擎
- 实现基本内置函数
