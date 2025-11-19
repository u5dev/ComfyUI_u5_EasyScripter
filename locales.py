# -*- coding: utf-8 -*-
"""
多言語サポート用のメッセージ定義
Localization messages for EasyScripter
"""

# 言語別メッセージ定義
MESSAGES = {
    'en': {
        # EasyScripter Node messages
        'warning_no_script': '[Warning] No script provided',
        'warning_return_not_assigned': '[Warning] RETURN was not assigned; defaulting to 0',  # 後方互換性用
        'warning_return1_not_assigned': '[Warning] RETURN1 was not assigned; defaulting to 0',
        'warning_return2_not_assigned': '[Warning] RETURN2 was not assigned; defaulting to 0',
        'error_prefix': '[Error]',
        'executing_script': '[EasyScripter] Executing Script',
        'script_executed': '[EasyScripter] Script executed successfully',
        'script_error': '[EasyScripter Error] Script execution failed:',
        'results': '[EasyScripter] Results: RETURN={0}, PRINT lines={1}',
        'output_header': '[EasyScripter Output]:',
        'final_result': '[EasyScripter Final]: INT={0}, FLOAT={1:.2f}, STRING={2}',
        'received_values': '[EasyScripter] Received: VAL1_int={0}, VAL1_float={1}, VAL2_int={2}, VAL2_float={3}',
        'received_texts': '[EasyScripter] Received: TXT1={0}, TXT2={1}',
        'resolved_values': '[EasyScripter] Resolved: VAL1={0}, VAL2={1}, TXT1={2}, TXT2={3}',

        # Script Engine messages
        'error_zero_division': 'Division by zero error',
        'error_zero_division_mod': 'Division by zero error (MOD operation)',
        'error_max_call_depth': 'Maximum call depth {0} exceeded (possible infinite recursion)',
        'error_script_execution': 'Script execution error: {0}',
        'error_function_conflict': "Function name '{0}' conflicts with built-in function",
        'error_function_execution': "Function {0} execution error: {1}",
        'error_function_not_defined': "Error: Function '{0}' is not defined.",
        'error_redim_needs_array': 'REDIM function requires array variable and new size',
        'error_redim_first_arg': 'First argument of REDIM must be an array variable',
        'error_isarray_needs_arg': 'ISARRAY function requires an argument',
        'error_join_needs_array': 'JOIN function requires array name',
        'error_csvdiff_args': 'CSVDIFF function requires array name, CSV1, and CSV2',
        'error_array_function_needs_name': '{0} function requires array name',

        # Script Parser messages
        'error_invalid_char': "Invalid character: '{0}' at line {1}, position {2}",
        'error_if_needs_endif': 'IF statement requires ENDIF',
        'error_one_line_if_exit_only': 'One-line IF statement only supports EXIT statements: {0}',
        'error_dim_needs_paren': 'DIM statement needs ) at line {0}',
        'error_dim_needs_bracket': 'DIM statement needs ] at line {0}',
        'error_redim_needs_paren': 'REDIM statement needs ) at line {0}',
        'error_redim_multidim': 'Multi-dimensional REDIM is not implemented at line {0}',
        'error_redim_needs_name': 'REDIM requires array name',
        'error_redim_invalid_syntax': 'Invalid REDIM syntax. Use REDIM array[size] or REDIM array, size',
        'error_array_needs_name': 'ARRAY requires array name',
        'error_split_needs_name': 'SPLIT requires array name',
        'error_reserved_keyword': "'{0}' is a reserved keyword and cannot be used as a variable name",
        'warning_space_before_paren': "Warning: Space between function name '{0}' and parenthesis.",
        'suggestion_no_space': "Suggestion: Write '{0}(' without space.",

        # Built-in function error messages
        'error_sqrt_negative': 'SQRT: Cannot calculate square root of negative number',
        'error_log_invalid_arg': 'LOG: Invalid argument',
        'error_log_invalid_base': 'LOG: Invalid base',
        'error_asin_range': 'ASIN: Argument must be between -1 and 1',
        'error_acos_range': 'ACOS: Argument must be between -1 and 1',
        'error_log10_positive': 'LOG10: Argument must be positive',

        # Special function hints
        'hint_print_usage': 'PRINT is a special function. Use PRINT = "message" format',
        'hint_msgbox': 'MSGBOX is an alias for PRINT. Use MSGBOX("message")',
        'hint_redim': 'REDIM resizes arrays. Use REDIM array, size',
        'hint_isarray': 'ISARRAY checks if variable is array. Use ISARRAY(variable)',
        'hint_inputbox': 'INPUTBOX is not available in batch processing (returns empty)',
        'hint_msgbox_usage': 'MSGBOX is an alias for PRINT. Use MSGBOX("message")',
        'hint_redim_usage': 'REDIM resizes arrays. Use REDIM array, size',
        'hint_isarray_usage': 'ISARRAY checks if variable is array. Use ISARRAY(variable)',
        'hint_inputbox_usage': 'INPUTBOX is not available in batch processing (returns empty)',
        'hint_if_control': 'IF is a control statement. Use IIF for conditional function',
        'hint_var_deprecated': 'VAR array is deprecated. Use ARR[] format for arrays',

        # Scripter Node diagnostic and loop messages
        'scripter_node_diag_execution_counter': '[DIAG-1] execute_script called #{0}, {1:.2f}s since last call, unique_id={2}, script_hash={3}',
        'scripter_node_task_sent': '[EasyScripter] Task sent: {0}',
        'scripter_node_timeout': '[EasyScripter] Timeout: {0} - {1}',
        'scripter_node_timeout_error': '[ERROR] Task timeout: {0}',
        'scripter_node_queue_error': '[EasyScripter] Queueing error: {0} - {1}',
        'scripter_node_queue_error_result': '[ERROR] Queueing error: {0}',
        'scripter_node_debug_execute_called': '[DEBUG] execute_script called: unique_id={0}, type={1}',
        'scripter_node_diag_impl_start': '[DIAG-4] _execute_script_impl started: unique_id={0}',
        'scripter_node_diag_engine_created': '[DIAG-4] ScriptEngine created: id={0}, return1_assigned={1}, return2_assigned={2}, loop_config={3}, variables_count={4}',
        'scripter_node_final_result_line1': '[comfyUI_u5_easyscripter Final Result]: RETURN1: INT={0}, FLOAT={1:.2f}, TEXT={2}',
        'scripter_node_final_result_line2': '                                  RETURN2: INT={0}, FLOAT={1:.2f}, TEXT={2}',
        'scripter_node_relay_output_assigned': '[RELAY_OUTPUT] Using script-assigned value: type={0}',
        'scripter_node_relay_output_passthrough': '[RELAY_OUTPUT] Passthrough any_input: type={0}',
        'scripter_node_loop_detected': '[LOOP_SUBGRAPH] Loop execution detected: {0}',
        'scripter_node_debug_ui_decision': '[DEBUG] UI output decision: unique_id={0}, is_loop_duplicate={1}',
        'scripter_node_debug_ui_lines': '[DEBUG] ui_display_lines length={0}, content={1}',
        'scripter_node_debug_suppress_ui': '[DEBUG] Suppressing UI output for loop duplicate node: {0}',
        'scripter_node_debug_output_ui': '[DEBUG] Outputting UI for original node: {0}',
        'scripter_node_loop_auto_applied': '[LOOP_AUTO] Loop config applied to {0}: {1} iterations',
        'scripter_node_loop_skip_no_connection': '[LOOP] {0}: No connection, skipping',
        'scripter_node_loop_warning_no_connections': '[LOOP] Warning: No channel is connected to downstream nodes',
        'scripter_node_loop_warning_no_connections_disabled': '[LOOP] Warning: No connection, loop disabled',
        'scripter_node_loop_connection_check_error': '[LOOP_SUBGRAPH] Connection check error: {0}',
        'scripter_node_loop_auto_select_error': '[LOOP_SUBGRAPH] Auto-select error: {0}',
        'scripter_node_loop_successor_error': '[LOOP_SUBGRAPH] Downstream node retrieval error: {0}',
        'scripter_node_loop_node_collection_error': '[LOOP_SUBGRAPH] Node collection error ({0}): {1}',
        'scripter_node_is_changed': '[IS_CHANGED] hash={0}, unique_id={1}',

        # Loop function messages
        'loop_arg_reorder_detected': '[LOOP_SUBGRAPH] Argument reordering detected: count={0}, channel={1}',
        'loop_engine_required': 'LOOP_SUBGRAPH: engine is required (internal error)',
        'loop_count_must_be_integer': 'LOOP_SUBGRAPH: count must be an integer (specified value: {0})',
        'loop_count_clamped_to_min': '[LOOP_SUBGRAPH] Warning: count={0} is out of range. Adjusted to 1',
        'loop_count_clamped_to_max': '[LOOP_SUBGRAPH] Warning: count={0} is out of range. Adjusted to 100',
        'loop_invalid_channel': 'LOOP_SUBGRAPH: channel must be one of {0} (specified value: {1})',
        'loop_set_auto_channel': '[LOOP_SUBGRAPH] Set to repeat {0} times (auto-channel selection: applies to all connected channels)',
        'loop_set_specific_channel': '[LOOP_SUBGRAPH] Set {0} to repeat {1} times',

        # OUTPUT function messages
        'output_warning_absolute_path': '[WARNING] OUTPUT: Absolute path or UNC path is not allowed: {0}',
        'output_error_file_write': '[ERROR] OUTPUT: File output error: {0}',

        # INPUT function messages
        'input_warning_absolute_path': '[WARNING] INPUT: Absolute path is not allowed: {0}',
        'input_warning_unc_path': '[WARNING] INPUT: UNC path is not allowed: {0}',
        'input_warning_file_not_found': '[WARNING] INPUT: File not found: {0}',
        'input_error_file_read': '[ERROR] INPUT: File read error: {0}',
        'input_error_pil_not_installed': 'PIL/Pillow is not installed. PIL is required for image loading.',

        # ISFILEEXIST function messages
        'isfileexist_warning_absolute_path': '[WARNING] ISFILEEXIST: Absolute path is not allowed: {0}',
        'isfileexist_warning_unc_path': '[WARNING] ISFILEEXIST: UNC path is not allowed: {0}',
        'isfileexist_error_size': '[ERROR] ISFILEEXIST: File size retrieval error: {0}',
        'isfileexist_warning_unknown_flag': '[WARNING] ISFILEEXIST: Unknown flag \'{0}\', using default behavior',
        'isfileexist_warning_pil_not_installed': '[WARNING] ISFILEEXIST: PIL/Pillow is not installed. PIL is required for PIXEL retrieval.',
        'isfileexist_error_image_load': '[ERROR] ISFILEEXIST: Image loading error: {0}',
    },

    'ja': {
        # EasyScripter Node messages
        'warning_no_script': '[警告] スクリプトが提供されていません',
        'warning_return_not_assigned': '[警告] RETURNが代入されていません。デフォルトの0を使用します',  # 後方互換性用
        'warning_return1_not_assigned': '[警告] RETURN1が代入されていません。デフォルトの0を使用します',
        'warning_return2_not_assigned': '[警告] RETURN2が代入されていません。デフォルトの0を使用します',
        'error_prefix': '[エラー]',
        'executing_script': '[EasyScripter] スクリプトを実行中',
        'script_executed': '[EasyScripter] スクリプトが正常に実行されました',
        'script_error': '[EasyScripter エラー] スクリプトの実行に失敗しました:',
        'results': '[EasyScripter] 結果: RETURN={0}, PRINT行数={1}',
        'output_header': '[EasyScripter 出力]:',
        'final_result': '[EasyScripter 最終結果]: INT={0}, FLOAT={1:.2f}, STRING={2}',
        'received_values': '[EasyScripter] 受信値: VAL1_int={0}, VAL1_float={1}, VAL2_int={2}, VAL2_float={3}',
        'received_texts': '[EasyScripter] 受信テキスト: TXT1={0}, TXT2={1}',
        'resolved_values': '[EasyScripter] 解決値: VAL1={0}, VAL2={1}, TXT1={2}, TXT2={3}',

        # Script Engine messages
        'error_zero_division': 'ゼロ除算エラー',
        'error_zero_division_mod': 'ゼロ除算エラー（MOD演算）',
        'error_max_call_depth': '最大呼び出し深度 {0} を超えました（無限再帰の可能性）',
        'error_script_execution': 'スクリプト実行エラー: {0}',
        'error_function_conflict': "関数名 '{0}' はビルトイン関数と競合します",
        'error_function_execution': "関数 {0} の実行エラー: {1}",
        'error_function_not_defined': "エラー: '{0}'という関数は定義されていません。",
        'error_redim_needs_array': 'REDIM関数には配列変数と新しいサイズが必要です',
        'error_redim_first_arg': 'REDIM関数の第1引数は配列変数である必要があります',
        'error_isarray_needs_arg': 'ISARRAY関数には引数が必要です',
        'error_join_needs_array': 'JOIN関数には配列名が必要です',
        'error_csvdiff_args': 'CSVDIFF関数には配列名、CSV1、CSV2が必要です',
        'error_array_function_needs_name': '{0}関数には配列名が必要です',

        # Script Parser messages
        'error_invalid_char': "無効な文字: '{0}' at line {1}, position {2}",
        'error_if_needs_endif': 'IF文にはENDIFが必要です',
        'error_one_line_if_exit_only': '1行IF文ではEXIT文のみサポートされています: {0}',
        'error_dim_needs_paren': 'DIM文で ) が必要です at line {0}',
        'error_dim_needs_bracket': 'DIM文で ] が必要です at line {0}',
        'error_redim_needs_paren': 'REDIM文で ) が必要です at line {0}',
        'error_redim_multidim': '多次元配列のREDIMは未実装です at line {0}',
        'error_redim_needs_name': 'REDIMの後には配列名が必要です',
        'error_redim_invalid_syntax': 'REDIM構文が無効です。REDIM array[size] または REDIM array, size を使用してください',
        'error_array_needs_name': 'ARRAYの後には配列名が必要です',
        'error_split_needs_name': 'SPLITの後には配列名が必要です',
        'error_reserved_keyword': "'{0}' は予約語のため変数名として使用できません",
        'warning_space_before_paren': "警告: '{0} ('のように関数名と括弧の間に空白があります。",
        'suggestion_no_space': "推奨: '{0}(' のように空白なしで記述してください。",

        # Built-in function error messages
        'error_sqrt_negative': 'SQRT: 負の値の平方根は計算できません',
        'error_log_invalid_arg': 'LOG: 不正な引数',
        'error_log_invalid_base': 'LOG: 不正な底',
        'error_asin_range': 'ASIN: 引数は-1から1の間でなければなりません',
        'error_acos_range': 'ACOS: 引数は-1から1の間でなければなりません',
        'error_log10_positive': 'LOG10: 引数は正の数でなければなりません',

        # Special function hints
        'hint_print_usage': 'PRINTは特殊な関数です。PRINT = "メッセージ" の形式で使用してください',
        'hint_msgbox': 'MSGBOXはPRINTのエイリアスです。MSGBOX("メッセージ")を使用してください',
        'hint_redim': 'REDIMは配列をリサイズします。REDIM array, size を使用してください',
        'hint_isarray': 'ISARRAYは変数が配列かチェックします。ISARRAY(variable)を使用してください',
        'hint_inputbox': 'INPUTBOXはバッチ処理では利用できません（空文字を返します）',
        'hint_msgbox_usage': 'MSGBOXはPRINTのエイリアスです。MSGBOX("メッセージ")を使用してください',
        'hint_redim_usage': 'REDIMは配列をリサイズします。REDIM array, size を使用してください',
        'hint_isarray_usage': 'ISARRAYは変数が配列かチェックします。ISARRAY(variable)を使用してください',
        'hint_inputbox_usage': 'INPUTBOXはバッチ処理では利用できません（空文字を返します）',
        'hint_if_control': 'IFは制御文です。条件関数が必要な場合は IIF を使用してください',
        'hint_var_deprecated': 'VAR配列は廃止されました。ARR[] の形式で配列を使用してください',

        # Scripter Node diagnostic and loop messages
        'scripter_node_diag_execution_counter': '[DIAG-1] execute_script 呼び出し #{0}, 前回から {1:.2f}秒経過, unique_id={2}, script_hash={3}',
        'scripter_node_task_sent': '[EasyScripter] タスク送信: {0}',
        'scripter_node_timeout': '[EasyScripter] タイムアウト: {0} - {1}',
        'scripter_node_timeout_error': '[エラー] タスクがタイムアウトしました: {0}',
        'scripter_node_queue_error': '[EasyScripter] キューイングエラー: {0} - {1}',
        'scripter_node_queue_error_result': '[エラー] キューイングエラー: {0}',
        'scripter_node_debug_execute_called': '[DEBUG] execute_script called: unique_id={0}, type={1}',
        'scripter_node_diag_impl_start': '[DIAG-4] _execute_script_impl 開始: unique_id={0}',
        'scripter_node_diag_engine_created': '[DIAG-4] ScriptEngine生成完了: id={0}, return1_assigned={1}, return2_assigned={2}, loop_config={3}, variables_count={4}',
        'scripter_node_final_result_line1': '[comfyUI_u5_easyscripter 最終結果]: RETURN1: INT={0}, FLOAT={1:.2f}, TEXT={2}',
        'scripter_node_final_result_line2': '                                  RETURN2: INT={0}, FLOAT={1:.2f}, TEXT={2}',
        'scripter_node_relay_output_assigned': '[RELAY_OUTPUT] スクリプト代入値を使用: type={0}',
        'scripter_node_relay_output_passthrough': '[RELAY_OUTPUT] any_inputをパススルー: type={0}',
        'scripter_node_loop_detected': '[LOOP_SUBGRAPH] ループ実行を検出: {0}',
        'scripter_node_debug_ui_decision': '[DEBUG] UI output decision: unique_id={0}, is_loop_duplicate={1}',
        'scripter_node_debug_ui_lines': '[DEBUG] ui_display_lines length={0}, content={1}',
        'scripter_node_debug_suppress_ui': '[DEBUG] Suppressing UI output for loop duplicate node: {0}',
        'scripter_node_debug_output_ui': '[DEBUG] Outputting UI for original node: {0}',
        'scripter_node_loop_auto_applied': '[LOOP_AUTO] {0}に{1}回ループ設定を適用',
        'scripter_node_loop_skip_no_connection': '[LOOP] {0}: 接続なし、スキップ',
        'scripter_node_loop_warning_no_connections': '[LOOP] 警告: どのチャネルも後続ノードに接続されていません',
        'scripter_node_loop_warning_no_connections_disabled': '[LOOP] 警告: 接続なし、ループ無効化',
        'scripter_node_loop_connection_check_error': '[LOOP_SUBGRAPH] 接続チェックエラー: {0}',
        'scripter_node_loop_auto_select_error': '[LOOP_SUBGRAPH] 自動選択エラー: {0}',
        'scripter_node_loop_successor_error': '[LOOP_SUBGRAPH] 後続ノード取得エラー: {0}',
        'scripter_node_loop_node_collection_error': '[LOOP_SUBGRAPH] ノード収集エラー ({0}): {1}',
        'scripter_node_is_changed': '[IS_CHANGED] hash={0}, unique_id={1}',

        # Loop function messages
        'loop_arg_reorder_detected': '[LOOP_SUBGRAPH] 引数再配置検出: count={0}, channel={1}',
        'loop_engine_required': 'LOOP_SUBGRAPH: engineが必要です(内部エラー)',
        'loop_count_must_be_integer': 'LOOP_SUBGRAPH: countは整数である必要があります(指定値: {0})',
        'loop_count_clamped_to_min': '[LOOP_SUBGRAPH] 警告: count={0}は範囲外です。1に調整されました',
        'loop_count_clamped_to_max': '[LOOP_SUBGRAPH] 警告: count={0}は範囲外です。100に調整されました',
        'loop_invalid_channel': 'LOOP_SUBGRAPH: channelは{0}のいずれかである必要があります(指定値: {1})',
        'loop_set_auto_channel': '[LOOP_SUBGRAPH] {0}回繰り返し実行に設定しました(自動チャネル選択: 接続されている全チャネルに適用)',
        'loop_set_specific_channel': '[LOOP_SUBGRAPH] {0}を{1}回繰り返し実行に設定しました',

        # OUTPUT function messages
        'output_warning_absolute_path': '[WARNING] OUTPUT: 絶対パス・UNCパスは使用できません: {0}',
        'output_error_file_write': '[ERROR] OUTPUT: ファイル出力エラー: {0}',

        # INPUT function messages
        'input_warning_absolute_path': '[WARNING] INPUT: 絶対パスは使用できません: {0}',
        'input_warning_unc_path': '[WARNING] INPUT: UNCパスは使用できません: {0}',
        'input_warning_file_not_found': '[WARNING] INPUT: ファイルが見つかりません: {0}',
        'input_error_file_read': '[ERROR] INPUT: ファイル読み込みエラー: {0}',
        'input_error_pil_not_installed': 'PIL/Pillowがインストールされていません。画像読み込みにはPILが必要です。',

        # ISFILEEXIST function messages
        'isfileexist_warning_absolute_path': '[WARNING] ISFILEEXIST: 絶対パスは使用できません: {0}',
        'isfileexist_warning_unc_path': '[WARNING] ISFILEEXIST: UNCパスは使用できません: {0}',
        'isfileexist_error_size': '[ERROR] ISFILEEXIST: ファイルサイズ取得エラー: {0}',
        'isfileexist_warning_unknown_flag': '[WARNING] ISFILEEXIST: 不明なフラグ \'{0}\'、デフォルト動作します',
        'isfileexist_warning_pil_not_installed': '[WARNING] ISFILEEXIST: PIL/Pillowがインストールされていません。PIXEL取得には PIL が必要です。',
        'isfileexist_error_image_load': '[ERROR] ISFILEEXIST: 画像読み込みエラー: {0}',
    }
}


def get_message(key: str, locale: str = 'en', *args) -> str:
    """
    指定されたロケールでメッセージを取得

    Args:
        key: メッセージキー
        locale: ロケール ('en' または 'ja')
        *args: フォーマット用の引数

    Returns:
        ローカライズされたメッセージ
    """
    # ロケールが見つからない場合は英語にフォールバック
    if locale not in MESSAGES:
        locale = 'en'

    messages = MESSAGES[locale]

    # メッセージキーが見つからない場合は英語を試す
    message = messages.get(key)
    if message is None:
        message = MESSAGES['en'].get(key, key)

    # フォーマット引数がある場合は適用
    if args:
        try:
            return message.format(*args)
        except:
            return message

    return message


# Script Execution Queue messages
QUEUE_MESSAGES = {
    'en': {
        # Initialization
        'queue_initialized': '[ScriptExecutionQueue] Initialized: Worker thread started',
        
        # Worker thread
        'queue_worker_started': '[ScriptExecutionQueue] Worker thread started',
        'queue_worker_stopped': '[ScriptExecutionQueue] Worker thread stopped',
        'queue_worker_fatal_error': '[ScriptExecutionQueue] Worker thread fatal error: {0}',
        
        # Task execution
        'queue_task_enqueued': '[ScriptExecutionQueue] Task enqueued: {0} (queue size: {1})',
        'queue_task_started': '[ScriptExecutionQueue] Task execution started: {0}',
        'queue_task_completed': '[ScriptExecutionQueue] Task completed: {0} ({1:.2f}s)',
        'queue_task_error': '[ScriptExecutionQueue] Task error: {0} - {1}',
        'queue_task_timeout': 'Task {0} timed out ({1}s)',
        
        # Diagnostics DIAG-2
        'queue_diag2_enqueue_call': '[DIAG-2] enqueue_and_wait called: task_id={0}, worker_alive={1}, queue_size={2}, _running={3}',
        'queue_diag2_worker_stopped': '[DIAG-2] Warning: Worker thread stopped! _running={0}, worker_thread={1}',
        
        # Diagnostics DIAG-3
        'queue_diag3_waiting': '[DIAG-3] Waiting: task_id={0}, elapsed={1:.1f}s, completed={2}, current_task={3}, queue_size={4}',
        'queue_diag3_timeout': '[DIAG-3] Timeout: task_id={0}, elapsed={1:.1f}s, worker_alive={2}, queue_size={3}, current_task={4}',
        
        # Shutdown
        'queue_shutdown_request': '[ScriptExecutionQueue] Shutdown requested',
        'queue_shutdown_complete': '[ScriptExecutionQueue] Shutdown complete',
        
        # Errors
        'queue_error_singleton': 'ScriptExecutionQueue is a singleton. Use get_instance().',
    },
    
    'ja': {
        # Initialization
        'queue_initialized': '[ScriptExecutionQueue] 初期化完了: ワーカースレッド起動',
        
        # Worker thread
        'queue_worker_started': '[ScriptExecutionQueue] ワーカースレッド開始',
        'queue_worker_stopped': '[ScriptExecutionQueue] ワーカースレッド終了',
        'queue_worker_fatal_error': '[ScriptExecutionQueue] ワーカースレッド致命的エラー: {0}',
        
        # Task execution
        'queue_task_enqueued': '[ScriptExecutionQueue] タスク追加: {0} (キュー長: {1})',
        'queue_task_started': '[ScriptExecutionQueue] タスク実行開始: {0}',
        'queue_task_completed': '[ScriptExecutionQueue] タスク完了: {0} ({1:.2f}秒)',
        'queue_task_error': '[ScriptExecutionQueue] タスクエラー: {0} - {1}',
        'queue_task_timeout': 'タスク {0} がタイムアウトしました（{1}秒）',
        
        # Diagnostics DIAG-2
        'queue_diag2_enqueue_call': '[DIAG-2] enqueue_and_wait 呼び出し: task_id={0}, worker_alive={1}, queue_size={2}, _running={3}',
        'queue_diag2_worker_stopped': '[DIAG-2] ワーカースレッド停止検出！ _running={0}, worker_thread={1}',
        
        # Diagnostics DIAG-3
        'queue_diag3_waiting': '[DIAG-3] 待機中: task_id={0}, elapsed={1:.1f}s, completed={2}, current_task={3}, queue_size={4}',
        'queue_diag3_timeout': '[DIAG-3] タイムアウト: task_id={0}, elapsed={1:.1f}s, worker_alive={2}, queue_size={3}, current_task={4}',
        
        # Shutdown
        'queue_shutdown_request': '[ScriptExecutionQueue] シャットダウン要求',
        'queue_shutdown_complete': '[ScriptExecutionQueue] シャットダウン完了',
        
        # Errors
        'queue_error_singleton': 'ScriptExecutionQueue はシングルトンです。get_instance() を使用してください。',
    }
}

# Merge QUEUE_MESSAGES into main MESSAGES dictionary
for lang in QUEUE_MESSAGES:
    if lang in MESSAGES:
        MESSAGES[lang].update(QUEUE_MESSAGES[lang])
    else:
        MESSAGES[lang] = QUEUE_MESSAGES[lang]


def detect_locale_from_language_code(language_code: str) -> str:
    """
    言語コードからロケールを判定

    Args:
        language_code: ブラウザの言語コード（例: 'ja-JP', 'en-US'）

    Returns:
        'ja' または 'en'
    """
    if language_code and language_code.lower().startswith('ja'):
        return 'ja'
    return 'en'