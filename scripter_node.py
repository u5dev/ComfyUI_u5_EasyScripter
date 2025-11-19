"""
ComfyUI U5 EasyScripter Node Implementation - 型安全版
Executes VBA-style scripts in ComfyUI
"""

from .locales import get_message, detect_locale_from_language_code
from comfy.comfy_types import IO

try:
    from .script_engine import ScriptEngine
    from .script_execution_queue import get_execution_queue
except ImportError:
    from script_engine import ScriptEngine
    from script_execution_queue import get_execution_queue

class ComfyUI_u5_EasyScripterNode:
    """ComfyUI U5 EasyScripter - Node that executes VBA-style scripts"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # 出力表示欄（読み取り専用、上部に表示）
                "output": ("STRING", {
                    "multiline": True,
                    "default": "",
                }),
                # スクリプト欄（下部に表示）
                "script": ("STRING", {
                    "multiline": True,
                    "default": "' EasyScripter Sample Script\n' 2つの数値入力を使った計算例\nRETURN1 = VAL1 + VAL2\nPRINT(\"Result:\", RETURN1)",
                }),
            },
            "optional": {
                # 入力ソケットを上部に配置（接続専用、入力フィールドなし）
                "VAL1_int": ("INT", {"forceInput": True}),
                "VAL1_float": ("FLOAT", {"forceInput": True}),
                "VAL2_int": ("INT", {"forceInput": True}),
                "VAL2_float": ("FLOAT", {"forceInput": True}),
                "TXT1": ("STRING", {"forceInput": True}),
                "TXT2": ("STRING", {"forceInput": True}),
                # ANY型入力（完全Bypass用）
                "any_input": (IO.ANY, {"forceInput": True}),
            },
            "hidden": {
                # サブグラフループ実行用の隠し入力
                "unique_id": "UNIQUE_ID",
                "dynprompt": "DYNPROMPT",
                "_iteration_dependency": None
            }
        }


    @classmethod
    def IS_CHANGED(cls, script, **kwargs):
        """スクリプト実行を毎回強制（キャッシュ無効化）
        
        ComfyUIはIS_CHANGEDメソッドの戻り値が変わるとノードを再実行します。
        time.time()を含めることで、毎回異なる値を返し、常に再実行されます。
        
        Args:
            script: スクリプト内容
            **kwargs: 追加パラメータ（unique_id等）
            
        Returns:
            str: 毎回異なるハッシュ値（キャッシュ無効化のため）
        """
        import hashlib
        import time
        
        # スクリプト内容 + 現在時刻でハッシュ生成（毎回異なる値）
        unique_id = kwargs.get('unique_id', '')
        content = f"{script}_{unique_id}_{time.time()}"
        hash_value = hashlib.md5(content.encode()).hexdigest()

        # デバッグログ（get_messageは6行目でグローバルインポート済み）
        locale = 'ja'  # デフォルトロケール
        print(get_message('scripter_node_is_changed', locale, hash_value[:8] + "...", unique_id))

        return hash_value

    RETURN_TYPES = ("INT", "FLOAT", "STRING", "INT", "FLOAT", "STRING", IO.ANY)
    RETURN_NAMES = ("RETURN1_int", "RETURN1_float", "RETURN1_text", "RETURN2_int", "RETURN2_float", "RETURN2_text", "relay_output")
    FUNCTION = "execute_script"
    CATEGORY = "u5/EasyScripter"
    OUTPUT_NODE = True  # UIへの出力を有効化

    def execute_script(self, output, script, VAL1_int=None, VAL1_float=None,
                      VAL2_int=None, VAL2_float=None, TXT1=None, TXT2=None, any_input=None,
                      _iteration_dependency=None,
                      unique_id=None, dynprompt=None):
        """Execute the VBA-style script (並行実行ガード付き)

        このメソッドは並行実行制御のラッパーです。
        実際の処理は _execute_script_impl() で実行されます。
        """

        # ========================================
        # DIAG-1: 実行回数カウンターとライフサイクル追跡
        # ========================================
        import time
        ComfyUI_u5_EasyScripterNode._execution_counter += 1
        current_time = time.time()
        time_since_last = 0
        if ComfyUI_u5_EasyScripterNode._last_execution_time:
            time_since_last = current_time - ComfyUI_u5_EasyScripterNode._last_execution_time
        ComfyUI_u5_EasyScripterNode._last_execution_time = current_time
        
        script_hash = hash(script) if script else 0
        locale = 'ja'  # デフォルトロケール
        print(get_message('scripter_node_diag_execution_counter', locale,
                         ComfyUI_u5_EasyScripterNode._execution_counter,
                         time_since_last,
                         unique_id,
                         script_hash))

        # キューイング制御を取得
        exec_queue = get_execution_queue(locale=locale)

        # タスクIDを生成（デバッグ用）
        task_id = f"easyscripter_{unique_id}" if unique_id else "easyscripter_unknown"

        # キューに追加し、順次実行（タイムアウト120秒）
        try:
            print(get_message('scripter_node_task_sent', locale, task_id))
            result = exec_queue.enqueue_and_wait(
                self._execute_script_impl,
                task_id=task_id,
                timeout=120.0,  # 2分タイムアウト
                output=output,
                script=script,
                VAL1_int=VAL1_int,
                VAL1_float=VAL1_float,
                VAL2_int=VAL2_int,
                VAL2_float=VAL2_float,
                TXT1=TXT1,
                TXT2=TXT2,
                any_input=any_input,
                _iteration_dependency=_iteration_dependency,
                unique_id=unique_id,
                dynprompt=dynprompt
            )
            return result
        except TimeoutError as e:
            print(get_message('scripter_node_timeout', locale, task_id, e))
            # タイムアウト時のフォールバック結果
            return {
                "ui": {"text": [get_message('scripter_node_timeout_error', locale, e)]},
                "result": (0, 0.0, "TIMEOUT", 0, 0.0, "TIMEOUT", None)
            }
        except Exception as e:
            print(get_message('scripter_node_queue_error', locale, task_id, e))
            import traceback
            traceback.print_exc()
            # エラー時のフォールバック結果
            return {
                "ui": {"text": [get_message('scripter_node_queue_error_result', locale, e)]},
                "result": (0, 0.0, "ERROR", 0, 0.0, "ERROR", None)
            }

    def _execute_script_impl(self, output, script, VAL1_int=None, VAL1_float=None,
                            VAL2_int=None, VAL2_float=None, TXT1=None, TXT2=None, any_input=None,
                            _iteration_dependency=None,
                            unique_id=None, dynprompt=None):
        """Execute the VBA-style script (内部実装)

        この関数は ScriptExecutionQueue のワーカースレッドから呼び出されます。
        """

        # output引数は無視（読み取り専用のため、widgets_values配列の順序整合性のためだけに存在）

        # デフォルトで日本語を使用
        locale = 'ja'

        # 【DEBUG】ノードID確認
        print(get_message('scripter_node_debug_execute_called', locale, unique_id, type(unique_id).__name__))

        # デバッグ用：受信値をそのまま表示
        print(get_message('executing_script', locale))
        print(get_message('received_values', locale, VAL1_int, VAL1_float, VAL2_int, VAL2_float))
        print(get_message('received_texts', locale, TXT1, TXT2))

        # 入力値の統合処理 - VAL1とVAL2をint値とfloat値で合算
        # ComfyUIでは未接続でもデフォルト値が入るため、両方の値を加算

        # VAL1の処理 (int + float の合算)
        val1_int = VAL1_int if VAL1_int is not None else 0
        val1_float = VAL1_float if VAL1_float is not None else 0.0
        val1 = float(val1_int) + float(val1_float)

        # VAL2の処理 (int + float の合算)
        val2_int = VAL2_int if VAL2_int is not None else 0
        val2_float = VAL2_float if VAL2_float is not None else 0.0
        val2 = float(val2_int) + float(val2_float)

        # TXT1とTXT2の処理
        text_input1 = str(TXT1) if TXT1 else ""
        text_input2 = str(TXT2) if TXT2 else ""

        print(get_message('resolved_values', locale, val1, val2, text_input1, text_input2))

        # ========================================
        # DIAG-4: ScriptEngine状態確認（生成前）
        # ========================================
        print(get_message('scripter_node_diag_impl_start', locale, unique_id))

        # Initialize script engine with locale
        engine = ScriptEngine(locale=locale)

        # ========================================
        # DIAG-4: ScriptEngine状態確認（生成後）
        # ========================================
        print(get_message('scripter_node_diag_engine_created', locale,
                         id(engine),
                         engine.return1_assigned,
                         engine.return2_assigned,
                         engine.loop_config,
                         len(engine.variables)))

        engine.return1_assigned = False
        engine.return2_assigned = False
        # RETURN1とRETURNの両方を初期化（後方互換性）
        engine.variables["RETURN1"] = 0.0
        engine.variables["RETURN"] = 0.0  # 後方互換性のためのRETURN1のエイリアス
        engine.variables["RETURN2"] = 0.0

        # Set initial variables（VAL1, VAL2を正式名称として使用）
        engine.set_variable("VAL1", val1)
        engine.set_variable("VAL2", val2)
        engine.set_variable("VAL_1", val1)  # 後方互換性
        engine.set_variable("VAL_2", val2)  # 後方互換性
        engine.set_variable("TXT1", text_input1)
        engine.set_variable("TXT2", text_input2)
        engine.set_variable("PRINT", "")
        # ANY型入力を変数スコープに登録
        engine.set_variable("any_input", any_input)

        # RETURNとRETURN1を同期させるための処理を追加
        # ユーザーがRETURNに代入した値をRETURN1にも反映する

        # Execute script
        script_has_body = bool(script and script.strip())
        script_executed = False

        if not script_has_body:
            warning_msg = get_message('warning_no_script', locale)
            engine.set_variable("PRINT", warning_msg)
            engine.add_to_print_stack(warning_msg)
            engine.variables["RETURN1"] = 0.0
            engine.variables["RETURN"] = 0.0  # 後方互換性
        else:
            try:
                engine.execute(script)
                script_executed = True
                print(get_message('script_executed', locale))

                # RETURNに値が代入された場合、RETURN1に同期
                if engine.return1_assigned:
                    return_val = engine.get_variable("RETURN", None)
                    if return_val is not None:
                        engine.set_variable("RETURN1", return_val)
            except Exception as e:
                error_msg = f"{type(e).__name__}: {str(e)}"
                print(get_message('script_error', locale) + f" {error_msg}")
                import traceback
                traceback.print_exc()
                engine.add_to_print_stack(get_message('error_prefix', locale) + f" {error_msg}")
                engine.variables["RETURN1"] = 0.0
            engine.variables["RETURN"] = 0.0  # 後方互換性

        # Get results
        # RETURN1の値を取得（RETURNからも取得して後方互換性を保つ）
        return1_value = engine.get_variable("RETURN1", engine.get_variable("RETURN", 0.0))
        return2_value = engine.get_variable("RETURN2", 0.0)

        # RETURN1が代入されていない場合の警告
        if script_has_body and script_executed and not engine.return1_assigned:
            warning_msg = get_message('warning_return1_not_assigned', locale)
            engine.add_to_print_stack(warning_msg)

        # RETURN2が代入されていない場合の警告
        if script_has_body and script_executed and not engine.return2_assigned:
            warning_msg = get_message('warning_return2_not_assigned', locale)
            engine.add_to_print_stack(warning_msg)
        print_lines = engine.get_print_output()  # PRINT関数の出力を取得
        print_output = "\n".join(print_lines) if print_lines else ""

        print(get_message('results', locale, return1_value, len(print_lines)))

        # Type conversion for RETURN1 outputs
        if isinstance(return1_value, str):
            int_output1 = 0
            float_output1 = 0.0
            # 明示的にUTF-8文字列として扱う（Windows環境での文字化け対策）
            text_output1 = return1_value.encode('utf-8', errors='replace').decode('utf-8')
        else:
            try:
                float_output1 = float(return1_value)
                int_output1 = int(float_output1)
                text_output1 = str(float_output1)
            except:
                int_output1 = 0
                float_output1 = 0.0
                text_output1 = "0"

        # Type conversion for RETURN2 outputs
        if isinstance(return2_value, str):
            int_output2 = 0
            float_output2 = 0.0
            # 明示的にUTF-8文字列として扱う（Windows環境での文字化け対策）
            text_output2 = return2_value.encode('utf-8', errors='replace').decode('utf-8')
        else:
            try:
                float_output2 = float(return2_value)
                int_output2 = int(float_output2)
                text_output2 = str(float_output2)
            except:
                int_output2 = 0
                float_output2 = 0.0
                text_output2 = "0"

        # Console output
        if print_output:
            print(get_message('output_header', locale))
            for line in print_lines:
                print(f"  {line}")

        print(get_message('scripter_node_final_result_line1', locale, int_output1, float_output1, text_output1))
        print(get_message('scripter_node_final_result_line2', locale, int_output2, float_output2, text_output2))

        # ANY型出力（Tier 3実装: RELAY_OUTPUT変数対応）
        if engine.relay_output_assigned:
            # スクリプトでRELAY_OUTPUTが代入された場合
            relay_output = engine.relay_output_value
            print(get_message('scripter_node_relay_output_assigned', locale, type(relay_output).__name__))
        else:
            # RELAY_OUTPUT未使用時は従来通りany_inputをパススルー
            relay_output = any_input
            print(get_message('scripter_node_relay_output_passthrough', locale, type(relay_output).__name__))

        # UI表示用テキストを作成
        ui_display_lines = []
        if print_lines:
            ui_display_lines.extend(print_lines)  # PRINT関数の出力行を追加
        ui_display_lines.append(f"[Result] RETURN1: INT={int_output1}, FLOAT={float_output1:.2f}, TEXT={text_output1}")
        ui_display_lines.append(f"[Result] RETURN2: INT={int_output2}, FLOAT={float_output2:.2f}, TEXT={text_output2}")

        # サブグラフループ検出（修正版：チャネルベースのloop_config構造に対応）
        if engine.loop_config:  # チャネル設定が存在すればTrue
            print(get_message('scripter_node_loop_detected', locale, engine.loop_config))
            # サブグラフを構築して返す
            subgraph = self._build_loop_subgraph(
                engine=engine,
                unique_id=unique_id,
                dynprompt=dynprompt,
                return1_outputs=(int_output1, float_output1, text_output1),
                return2_outputs=(int_output2, float_output2, text_output2),
                relay_output=relay_output,
                ui_display_lines=ui_display_lines,
                locale=locale
            )
            return subgraph

        # 【LOOP_SUBGRAPH UI修正】複製ノードの場合はUI出力を抑制
        # unique_idに":"（ComfyUI内部展開）または"_loop_"が含まれている場合は複製ノード
        is_loop_duplicate = unique_id and (":" in str(unique_id) or "_loop_" in str(unique_id))

        # 【DEBUG】UI出力判定ログ
        print(get_message('scripter_node_debug_ui_decision', locale, unique_id, is_loop_duplicate))
        print(get_message('scripter_node_debug_ui_lines', locale, len(ui_display_lines), ui_display_lines))

        if is_loop_duplicate:
            # 複製ノードはUI出力なし（resultのみ返す）
            print(get_message('scripter_node_debug_suppress_ui', locale, unique_id))
            return {
                "result": (int_output1, float_output1, text_output1, int_output2, float_output2, text_output2, relay_output)
            }
        else:
            # 元のノードのみUIを表示
            print(get_message('scripter_node_debug_output_ui', locale, unique_id))
            return {
                "ui": {
                    "text": ui_display_lines  # 配列形式
                },
                "result": (int_output1, float_output1, text_output1, int_output2, float_output2, text_output2, relay_output)  # タプル形式
            }


    def _get_channel_slots(self, channel):
        """チャネルに対応する出力スロット番号を返す"""
        if channel == "RETURN1":
            return [0, 1, 2]  # int, float, text
        elif channel == "RETURN2":
            return [3, 4, 5]  # int, float, text
        elif channel == "RELAY":
            return [6]  # any
        else:
            return []
    
    def _get_channel_outputs(self, channel, return1_outputs, return2_outputs, relay_output):
        """チャネルに対応する出力値を返す"""
        if channel == "RETURN1":
            return return1_outputs
        elif channel == "RETURN2":
            return return2_outputs
        elif channel == "RELAY":
            return (relay_output,)
        else:
            return (0, 0.0, "")
    
    def _expand_auto_config(self, engine, dynprompt, unique_id, locale='ja'):
        """AUTO設定を接続されている全チャネルに展開"""
        if "_AUTO_" not in engine.loop_config:
            return

        auto_config = engine.loop_config.pop("_AUTO_")
        count = auto_config["count"]

        # 各チャネルの接続をチェック
        for channel in ["RETURN1", "RETURN2", "RELAY"]:
            channel_slots = self._get_channel_slots(channel)
            downstream = self._get_downstream_nodes(dynprompt, unique_id, channel_slots)

            if downstream:  # 接続がある
                engine.loop_config[channel] = {
                    "enabled": True,
                    "count": count,
                    "current_iteration": 0
                }
                print(get_message('scripter_node_loop_auto_applied', locale, channel, count))
    
    def _group_by_subgraph(self, channel_subgraphs):
        """サブグラフの同一性でチャネルをグループ化
        
        Returns:
            dict: {subgraph_key: {channel: channel_data}}
        """
        groups = {}
        
        for channel, ch_data in channel_subgraphs.items():
            # サブグラフのノードIDセットをキーとして使用
            subgraph_key = frozenset(ch_data["subgraph"].keys())
            
            if subgraph_key not in groups:
                groups[subgraph_key] = {}
            
            groups[subgraph_key][channel] = ch_data
        
        return groups
    
    def _duplicate_subgraph_iteration(self, subgraph_nodes, iteration, unique_id, 
                                      outputs, current_channel, channel_slots,
                                      previous_iteration_tail_node=None,
                                      original_tail_node_id=None):
        """1イテレーション分のサブグラフノードを複製
        
        Args:
            subgraph_nodes (dict): 複製元のサブグラフノード群
            iteration (int): 現在のイテレーション番号
            unique_id (str): EasyScripterノードのID
            outputs (tuple): チャネルの出力値
            current_channel (str): 現在のチャネル名
            channel_slots (list): チャネルのスロット番号リスト
            previous_iteration_tail_node (str): 前イテレーションの最終ノードID（順次実行保証用）
            original_tail_node_id (str): オリジナルサブグラフの最終ノードID（tail検出用）
        
        Returns:
            tuple: (expanded_nodes, tail_node_id)
                - expanded_nodes (dict): 複製されたノード群 {node_id: node_info}
                - tail_node_id (str): サブグラフの最終ノードID（次イテレーション用）
        """
        expanded_nodes = {}
        first_node_id = None
        
        for original_node_id, original_node_info in subgraph_nodes.items():
            # 【FIX】すべてのiterationで_loop_Xサフィックスを使用（DuplicateNodeError回避）
            # ComfyUIのexpandは新規ノード追加のみ許可、既存ノード修正は不可
            new_node_id = f"{original_node_id}_loop_{iteration}"
            
            # ノード情報を複製
            new_node = {
                "inputs": {},
                "class_type": original_node_info.get("class_type", ""),
                "is_changed": [str(iteration)]  # 各イテレーションで異なる値
            }
            
            # 入力を複製し、参照を更新
            original_inputs = original_node_info.get("inputs", {})
            for input_name, input_value in original_inputs.items():
                # リンク形式の入力を処理
                if isinstance(input_value, list) and len(input_value) == 2:
                    source_node_id, source_slot = input_value

                    # EasyScripterノードからの入力の場合
                    if source_node_id == unique_id:
                        # チャネルのスロット範囲内かチェック
                        if source_slot in channel_slots:
                            # チャネル別の出力値を直接設定
                            slot_index = channel_slots.index(source_slot)
                            if slot_index < len(outputs):
                                new_node["inputs"][input_name] = outputs[slot_index]
                            else:
                                new_node["inputs"][input_name] = input_value
                        else:
                            new_node["inputs"][input_name] = input_value

                    # サブグラフ内の他のノードからの入力の場合
                    elif source_node_id in subgraph_nodes:
                        # 同じイテレーション内の複製ノードを参照（常に_loop_Xサフィックス）
                        ref_node_id = f"{source_node_id}_loop_{iteration}"
                        new_node["inputs"][input_name] = [ref_node_id, source_slot]

                    # サブグラフ外のノードからの入力（そのまま維持）
                    else:
                        new_node["inputs"][input_name] = input_value

                # 値形式の入力（そのまま複製）
                else:
                    new_node["inputs"][input_name] = input_value

            # 【CACHE FIX】全ノードのwidget入力にiteration番号を注入（キャッシュ回避）
            # ComfyUIはinputsのシグネチャでキャッシュキーを生成するため、
            # 各イテレーションでinputs値を変更することでキャッシュミスを強制する
            for input_name, input_value in new_node["inputs"].items():
                # リンク入力（[node_id, slot]形式）はスキップ
                if isinstance(input_value, list):
                    continue

                # widget値（固定値）のみ処理
                if isinstance(input_value, int):
                    # INT入力：iteration番号を加算
                    modified_value = input_value + iteration
                    new_node["inputs"][input_name] = modified_value

                elif isinstance(input_value, float):
                    # FLOAT入力：微小値を加算（精度を保ちつつ変化させる）
                    modified_value = input_value + (iteration * 0.000001)
                    new_node["inputs"][input_name] = modified_value

                # STRING入力はそのまま（"randomize"などの文字列は変更不要）

            # 【NEW】前イテレーションの最終ノードへの依存関係を追加（順次実行強制）
            # EasyScripterノードにのみ追加（標準ComfyUIノードは_iteration_dependency入力を持たない）
            if previous_iteration_tail_node and new_node.get("class_type") == "comfyUI_u5_easyscripter":
                # ダミー入力を追加（ComfyUIに依存関係を認識させる）
                # このノードは previous_iteration_tail_node の完了後にのみ実行される
                new_node["inputs"]["_iteration_dependency"] = [previous_iteration_tail_node, 0]

                # 最初のEasyScripterノードを記録
                if first_node_id is None:
                    first_node_id = new_node_id

            expanded_nodes[new_node_id] = new_node
        
        # 【FIX 2025-11-06】オリジナルサブグラフのtailノードIDから複製版のtail IDを生成
        # 単に最後に処理したノードではなく、実際のグラフ構造上の最終ノードを返す
        if original_tail_node_id:
            tail_node_id = f"{original_tail_node_id}_loop_{iteration}"
        else:
            # フォールバック: original_tail_node_idが未指定の場合は最後のノード
            tail_node_id = new_node_id
        
        return expanded_nodes, tail_node_id

    def _find_subgraph_tail_node(self, subgraph_nodes, dynprompt):
        """サブグラフの最終ノード（tail）を検出
        
        サブグラフ内のノードで、他のサブグラフノードに出力していないノードを探す。
        複数ある場合は、最初に見つかったものを返す。
        
        Args:
            subgraph_nodes: サブグラフノード辞書 {node_id: node_data}
            dynprompt: 動的プロンプトオブジェクト
            
        Returns:
            str: 最終ノードID（見つからない場合はNone）
        """
        subgraph_node_ids = set(subgraph_nodes.keys())
        
        # 各ノードの出力先を調査
        for node_id in subgraph_node_ids:
            node = dynprompt.get_node(node_id)
            if not node:
                continue
                
            # このノードの出力が他のサブグラフノードに接続されているか確認
            has_internal_output = False
            
            # すべてのノードをスキャンして、このノードを入力として参照しているものを探す
            for other_id in subgraph_node_ids:
                if other_id == node_id:
                    continue
                    
                other_node = dynprompt.get_node(other_id)
                if not other_node:
                    continue
                    
                # other_nodeの入力にnode_idが含まれているか確認
                inputs = other_node.get("inputs", {})
                for input_value in inputs.values():
                    # 入力が[node_id, slot]形式の参照の場合
                    if isinstance(input_value, list) and len(input_value) == 2:
                        if str(input_value[0]) == str(node_id):
                            has_internal_output = True
                            break
                            
                if has_internal_output:
                    break
            
            # サブグラフ内部に出力していないノード = tail候補
            if not has_internal_output:
                return node_id
        
        # 見つからない場合は最初のノードを返す（フォールバック）
        return list(subgraph_node_ids)[0] if subgraph_node_ids else None

    def _build_loop_subgraph(self, engine, unique_id, dynprompt,
                             return1_outputs, return2_outputs, relay_output, ui_display_lines, locale='ja'):
        """複数チャネル統合サブグラフループ構築

        複数チャネルのLOOP_SUBGRAPH設定を統合し、シーケンシャルに実行します。
        同じサブグラフに複数チャネルが接続されている場合、回数を合計して実行します。
        """

        # Step 1: AUTO設定を展開（接続先を自動検出して各チャネルに展開）
        self._expand_auto_config(engine, dynprompt, unique_id, locale)
        
        # loop_configが空の場合、ループなしで通常出力
        if not engine.loop_config:
            return {
                "ui": {"text": ui_display_lines},
                "result": (return1_outputs[0], return1_outputs[1], return1_outputs[2],
                          *return2_outputs, relay_output)
            }
        
        # Step 2: 各チャネルのサブグラフ情報を収集
        channel_subgraphs = {}
        
        for channel, config in engine.loop_config.items():
            if not config.get("enabled", False):
                continue
            
            # チャネルのスロットと出力値を取得
            slots = self._get_channel_slots(channel)
            outputs = self._get_channel_outputs(channel, return1_outputs, return2_outputs, relay_output)
            
            # 後続ノードを取得
            downstream = self._get_downstream_nodes(dynprompt, unique_id, slots)

            if not downstream:
                print(get_message('scripter_node_loop_skip_no_connection', locale, channel))
                continue
            
            # サブグラフ全体を収集
            subgraph = self._collect_subgraph_nodes(dynprompt, downstream)
            
            channel_subgraphs[channel] = {
                "count": config["count"],
                "slots": slots,
                "downstream": downstream,
                "subgraph": subgraph,
                "outputs": outputs
            }
        
        # サブグラフ接続がない場合、ループなしで通常出力
        if not channel_subgraphs:
            print(get_message('scripter_node_loop_warning_no_connections', locale))
            return {
                "ui": {"text": ui_display_lines + [get_message('scripter_node_loop_warning_no_connections_disabled', locale)]},
                "result": (return1_outputs[0], return1_outputs[1], return1_outputs[2],
                          *return2_outputs, relay_output)
            }
        
        # Step 3: サブグラフの同一性でグループ化
        subgraph_groups = self._group_by_subgraph(channel_subgraphs)
        
        # Step 4: 各グループで統合実行
        all_expanded_nodes = {}
        all_removed_nodes = []  # オリジナルノードID収集（remove用、現在は使用しない）
        ui_messages = []

        for subgraph_key, channels in subgraph_groups.items():
            # 合計回数を計算
            total_count = sum(ch_data["count"] for ch_data in channels.values())
            
            # チャネル別イテレーション範囲を決定
            iteration_ranges = {}  # {channel: (start, end)}
            current_iter = 0
            
            # チャネルを順序付け（RETURN1 → RETURN2 → RELAY）
            channel_order = ["RETURN1", "RETURN2", "RELAY"]
            ordered_channels = {ch: channels[ch] for ch in channel_order if ch in channels}
            
            for channel, ch_data in ordered_channels.items():
                iteration_ranges[channel] = (current_iter, current_iter + ch_data["count"])
                current_iter += ch_data["count"]
            
            # サブグラフノード（全チャネルで同一）
            subgraph_nodes = list(channels.values())[0]["subgraph"]

            # 【FIX 2025-11-06】オリジナルノードは削除しない（1回目の実行として保持）
            # iteration 1からtotal_countまでの複製を作成
            # オリジナル（1回目）+ 複製（2-5回目）= 合計total_count回実行
            # all_removed_nodes.extend(list(subgraph_nodes.keys()))  # ← 削除（オリジナル保持）

            # 【NEW】前イテレーションの最終ノードを追跡（順次実行保証）
            # オリジナルサブグラフの最終ノード（tail）を検出し、iteration 1の依存関係として設定
            original_tail_node = self._find_subgraph_tail_node(subgraph_nodes, dynprompt)
            previous_tail_node = original_tail_node

            # 【FIX 2025-11-06】iteration 1からtotal_countまで生成（複製部分のみ）
            # オリジナルノードが1回目の実行、iteration 1,2,3,4が2-5回目の実行
            # range(1, total_count) = [1,2,3,4] for total_count=5
            for iteration in range(1, total_count):
                # このiterationがどのチャネルに属するか判定
                current_channel = None
                for channel, (start, end) in iteration_ranges.items():
                    if start <= iteration < end:
                        current_channel = channel
                        break

                # チャネル別の出力値とスロットを使用してノード複製
                ch_data = channel_subgraphs[current_channel]
                expanded, tail_node = self._duplicate_subgraph_iteration(
                    subgraph_nodes, iteration, unique_id,
                    ch_data["outputs"], current_channel, ch_data["slots"],
                    previous_iteration_tail_node=previous_tail_node,  # ← 依存関係渡す
                    original_tail_node_id=original_tail_node  # ← tail検出用
                )
                all_expanded_nodes.update(expanded)
                previous_tail_node = tail_node  # ← 次イテレーション用に保存
            
            # UIメッセージ生成
            channel_details = ", ".join(
                f"{ch}:{data['count']}回" for ch, data in ordered_channels.items()
            )
            ui_messages.append(
                f"[LOOP] サブグラフ統合: {total_count}回実行 ({channel_details}、{len(subgraph_nodes)}ノード)"
            )

        return {
            "ui": {"text": ui_display_lines + ui_messages},
            "result": (return1_outputs[0], return1_outputs[1], return1_outputs[2],
                      *return2_outputs, relay_output),
            "expand": all_expanded_nodes,
            "remove": all_removed_nodes  # 空リスト（オリジナルノード削除なし）
        }

    def _has_connections(self, dynprompt, unique_id, output_slots):
        """
        指定された出力スロットが後続ノードに接続されているか確認
        
        Args:
            dynprompt: ComfyUIのDynamicPromptオブジェクト
            unique_id: 現在のノードID
            output_slots: チェック対象の出力スロット番号リスト
        
        Returns:
            bool: いずれかのスロットに接続があればTrue
        """
        if dynprompt is None or unique_id is None:
            return False
        
        try:
            # 全ノードをスキャンして、現在のノードを参照しているものを探す
            all_node_ids = dynprompt.all_node_ids()
            
            for node_id in all_node_ids:
                if node_id == unique_id:
                    continue  # 自分自身はスキップ
                
                try:
                    node_info = dynprompt.get_node(node_id)
                    inputs = node_info.get("inputs", {})
                    
                    # このノードの各入力をチェック
                    for input_name, input_value in inputs.items():
                        # リンク形式：[source_node_id, source_slot]
                        if isinstance(input_value, list) and len(input_value) == 2:
                            source_node_id, source_slot = input_value
                            
                            # 現在のノードへの接続かチェック
                            if source_node_id == unique_id and source_slot in output_slots:
                                return True
                
                except Exception as e:
                    # 個別ノードのエラーは無視して続行
                    continue
            
            return False

        except Exception as e:
            locale = 'ja'  # デフォルトロケール
            print(get_message('scripter_node_loop_connection_check_error', locale, e))
            return False
    
    def _auto_select_channel_simple(self, unique_id, dynprompt):
        """
        dynpromptから接続情報を取得し、チャネルを自動選択
        
        優先順位: RETURN1 → RETURN2 → RELAY
        
        Args:
            unique_id: 現在のノードID
            dynprompt: ComfyUIのDynamicPromptオブジェクト
        
        Returns:
            str: 選択されたチャネル ("RETURN1", "RETURN2", "RELAY")
            None: 有効な接続がない場合
        """
        if dynprompt is None or unique_id is None:
            return None
        
        try:
            # 出力スロットマッピング
            # RETURN1: slots 0,1,2 (int, float, text)
            # RETURN2: slots 3,4,5 (int, float, text)
            # RELAY: slot 6 (any)
            
            # 優先順位1: RETURN1の接続をチェック
            if self._has_connections(dynprompt, unique_id, [0, 1, 2]):
                return "RETURN1"
            
            # 優先順位2: RETURN2の接続をチェック
            if self._has_connections(dynprompt, unique_id, [3, 4, 5]):
                return "RETURN2"
            
            # 優先順位3: RELAYの接続をチェック
            if self._has_connections(dynprompt, unique_id, [6]):
                return "RELAY"
            
            return None

        except Exception as e:
            locale = 'ja'  # デフォルトロケール
            print(get_message('scripter_node_loop_auto_select_error', locale, e))
            return None

    def _get_downstream_nodes(self, dynprompt, unique_id, channel_slots):
        """
        指定チャネルの出力スロットに接続された後続ノードを取得
        
        Args:
            dynprompt: ComfyUIのDynamicPromptオブジェクト
            unique_id: 現在のノードID
            channel_slots: チャネルの出力スロット番号リスト
        
        Returns:
            list: 後続ノード情報のリスト [{"id": node_id, "info": node_info}, ...]
        """
        downstream_nodes = []
        
        if dynprompt is None or unique_id is None:
            return downstream_nodes
        
        try:
            all_node_ids = dynprompt.all_node_ids()
            
            for node_id in all_node_ids:
                if node_id == unique_id:
                    continue  # 自分自身はスキップ
                
                try:
                    node_info = dynprompt.get_node(node_id)
                    inputs = node_info.get("inputs", {})
                    
                    # このノードの各入力をチェック
                    for input_name, input_value in inputs.items():
                        # リンク形式：[source_node_id, source_slot]
                        if isinstance(input_value, list) and len(input_value) == 2:
                            source_node_id, source_slot = input_value
                            
                            # 現在のノードへの接続かチェック
                            if source_node_id == unique_id and source_slot in channel_slots:
                                downstream_nodes.append({
                                    "id": node_id,
                                    "info": node_info,
                                    "connected_slot": source_slot,
                                    "connected_input": input_name
                                })
                                break  # 同じノードを重複して追加しない
                
                except Exception as e:
                    # 個別ノードのエラーは無視して続行
                    continue
            
            return downstream_nodes

        except Exception as e:
            locale = 'ja'  # デフォルトロケール
            print(get_message('scripter_node_loop_successor_error', locale, e))
            return []
    
    def _is_subgraph(self, downstream_nodes):
        """
        後続ノードがサブグラフか判定
        
        Args:
            downstream_nodes: _get_downstream_nodesで取得したノードリスト
        
        Returns:
            bool: サブグラフの場合True、通常ノードの場合False
        """
        # 判定基準:
        # - 複数ノードに接続 → サブグラフ
        # - 1つ以上のノードに接続 → サブグラフ（現在の実装では1ノードでもサブグラフとして扱う）
        # - 接続なし → False
        
        return len(downstream_nodes) > 0
    
    def _collect_subgraph_nodes(self, dynprompt, start_nodes):
        """
        開始ノードから到達可能な全ノードを再帰的に収集（サブグラフ全体を取得）
        
        Args:
            dynprompt: ComfyUIのDynamicPromptオブジェクト
            start_nodes: 開始ノード情報のリスト（_get_downstream_nodesの戻り値形式）
        
        Returns:
            dict: {node_id: node_info} の辞書
        """
        collected = {}
        visited = set()
        
        def traverse(node_id):
            """ノードを再帰的に辿る"""
            if node_id in visited:
                return
            
            visited.add(node_id)
            
            try:
                node_info = dynprompt.get_node(node_id)
                collected[node_id] = node_info
                
                # このノードの全出力に接続されたノードを探す
                all_node_ids = dynprompt.all_node_ids()
                
                for next_node_id in all_node_ids:
                    if next_node_id in visited:
                        continue
                    
                    try:
                        next_node_info = dynprompt.get_node(next_node_id)
                        inputs = next_node_info.get("inputs", {})
                        
                        # next_nodeがcurrent_nodeの出力を参照しているかチェック
                        for input_value in inputs.values():
                            if isinstance(input_value, list) and len(input_value) == 2:
                                source_node_id, _ = input_value
                                if source_node_id == node_id:
                                    # 接続発見 → 再帰的に辿る
                                    traverse(next_node_id)
                                    break
                    
                    except Exception:
                        continue

            except Exception as e:
                locale = 'ja'  # デフォルトロケール
                print(get_message('scripter_node_loop_node_collection_error', locale, node_id, e))
        
        # 開始ノードから辿り始める
        for start_node in start_nodes:
            traverse(start_node["id"])
        
        return collected

    def _find_sequential_node(self, subgraph_nodes):
        """サブグラフ内のSequential系ノードを検出
        
        Args:
            subgraph_nodes (dict): サブグラフノード群
            
        Returns:
            str or None: Sequential系ノードのID（見つからない場合None）
        """
        # Sequential系class_typeリスト
        sequential_types = [
            "SequentialCheckpointLoader",
            "SequentialLoraLoader", 
            "SequentialVAELoader",
            "SequentialControlNetLoader",
            "SequentialCLIPVisionLoader",
            "SequentialGLIGENLoader",
            "SequentialUNETLoader"
        ]
        
        for node_id, node_info in subgraph_nodes.items():
            class_type = node_info.get("class_type", "")
            if class_type in sequential_types:
                return node_id
        
        return None
    
    def _get_bypass_node_id(self, expanded_nodes, original_subgraph):
        """Bypass出力を持つノードのIDを取得
        
        Args:
            expanded_nodes (dict): 複製されたノード群
            original_subgraph (dict): 元のサブグラフ
            
        Returns:
            str or None: BypassノードID
        """
        # Sequential系ノードを探す（Bypass出力を持つ）
        sequential_node_id = self._find_sequential_node(original_subgraph)
        
        if sequential_node_id:
            # 複製されたノードIDを返す
            for node_id in expanded_nodes.keys():
                if node_id.startswith(f"{sequential_node_id}_loop_"):
                    return node_id
        
        return None

    # ========================================
    # 診断用クラス変数（DIAG-1: 実行回数追跡）
    # ========================================
    _execution_counter = 0
    _last_execution_time = None
