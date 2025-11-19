"""
スクリプト実行エンジン
パースされたASTを実行する
"""

from typing import Any, Dict, Optional, Union, List
import itertools

try:
    from .script_parser import ScriptParser, ASTNode
    from .builtin_functions import (
        get_builtin_function,
        is_builtin_function,
        get_function_usage,
        BuiltinFunctions,
        BUILTIN_FUNCTIONS
    )
    from .locales import get_message
except ImportError:
    from script_parser import ScriptParser, ASTNode
    from builtin_functions import (
        get_builtin_function,
        is_builtin_function,
        get_function_usage,
        BuiltinFunctions,
        BUILTIN_FUNCTIONS
    )
    from locales import get_message


# ======================================================================
# EXIT statement exception classes
# ======================================================================

class ControlFlowExit(Exception):
    """
    制御フロー脱出の基底クラス
    Base class for control flow exit (EXIT FUNCTION/FOR/WHILE)
    """
    pass


class FunctionExit(ControlFlowExit):
    """
    EXIT FUNCTION用例外クラス
    Exception for EXIT FUNCTION statement
    """
    pass


class LoopExit(ControlFlowExit):
    """
    EXIT FOR / EXIT WHILE用例外クラス
    Exception for EXIT FOR and EXIT WHILE statements

    Attributes:
        loop_type: "FOR" or "WHILE"
    """
    def __init__(self, loop_type: str):
        self.loop_type = loop_type.upper()
        super().__init__()


# ======================================================================
# Script Engine
# ======================================================================

class ScriptEngine:
    """VBA風スクリプトの実行エンジン"""

    def __init__(self, locale: str = 'ja'):
        self.locale = locale  # デフォルトで日本語
        self.variables: Dict[str, Any] = {}
        self.arrays: Dict[str, Dict[int, Any]] = {}
        self.user_functions: Dict[str, Any] = {}  # ユーザー定義関数を保持
        self.call_stack: List[Dict[str, Any]] = []  # 関数呼び出しスタック
        self.max_call_depth = 100  # 最大呼び出し深度（無限再帰防止）
        self.parser = ScriptParser(locale=self.locale)
        self.print_stack: List[str] = []  # PRINT関数の出力スタック
        self.return1_assigned: bool = False  # RETURN1が代入されたか
        self.return2_assigned: bool = False  # RETURN2が代入されたか

        # RELAY_OUTPUT制御用フラグと値（Tier 3実装）
        self.relay_output_assigned: bool = False  # RELAY_OUTPUTが代入されたか
        self.relay_output_value: Any = None        # RELAY_OUTPUTの値

        # ループ制御設定（LOOP_SUBGRAPH用） - チャネル別辞書に変更
        # 構造: {"RETURN1": {"enabled": True, "count": 5}, "RETURN2": {...}, ...}
        self.loop_config: Dict[str, Dict[str, Any]] = {}

    def reset(self):
        """エンジンの状態をリセット"""
        self.variables.clear()
        self.arrays.clear()
        self.user_functions.clear()
        self.call_stack.clear()
        self.print_stack.clear()
        self.return1_assigned = False
        self.return2_assigned = False

    def set_variable(self, name: str, value: Any):
        """変数を設定（スコープ対応）"""
        name_upper = name.upper()

        # RETURNとRETURN1の両方でreturn1_assignedを設定（後方互換性）
        if name_upper in ('RETURN', 'RETURN1'):
            self.return1_assigned = True
            # RETURNに代入された値をRETURN1にも反映
            if name_upper == 'RETURN':
                self.variables['RETURN1'] = value
            # RETURN1に代入された値をRETURNにも反映
            elif name_upper == 'RETURN1':
                self.variables['RETURN'] = value
        elif name_upper == 'RETURN2':
            self.return2_assigned = True

        # 値がリストの場合は辞書型配列に変換
        if isinstance(value, list):
            array_dict = {i: v for i, v in enumerate(value)}
            # 現在のスコープを取得
            current_scope = self.get_current_scope()
            if current_scope:
                current_scope['arrays'][name_upper] = array_dict
            else:
                self.arrays[name_upper] = array_dict
            return

        # 値が配列オブジェクトの場合は配列として設定
        if isinstance(value, dict) and all(isinstance(k, int) for k in value.keys()):
            # 現在のスコープを取得
            current_scope = self.get_current_scope()
            if current_scope:
                current_scope['arrays'][name_upper] = value
            else:
                self.arrays[name_upper] = value
            return

        # 現在のスコープを取得
        current_scope = self.get_current_scope()
        if current_scope:
            # 関数内の場合、関数名への代入をチェック（戻り値設定）
            if name_upper == current_scope['function_name'].upper():
                current_scope['return_value'] = value
            # ローカルスコープに設定
            current_scope['variables'][name_upper] = value
        else:
            # グローバルスコープに設定
            self.variables[name_upper] = value

    def get_variable(self, name: str, default: Any = None) -> Any:
        """変数を取得（スコープ対応）"""
        name_upper = name.upper()

        # 特殊変数（RETURN, VAL1, VAL2, TXT1, TXT2）は常にグローバルスコープから取得
        # これにより、PRINT関数内で特殊変数を参照した際に正しい値が取得できる
        special_vars = ['RETURN', 'VAL1', 'VAL2', 'VAL_1', 'VAL_2', 'TXT1', 'TXT2']
        if name_upper in special_vars:
            value = self.variables.get(name_upper, default if default is not None else 0)
            return value

        # 現在のスコープから検索
        current_scope = self.get_current_scope()
        if current_scope:
            # ローカル変数をチェック
            if name_upper in current_scope['variables']:
                return current_scope['variables'][name_upper]
            # パラメータをチェック
            if name_upper in current_scope['parameters']:
                return current_scope['parameters'][name_upper]
            # 関数名（戻り値）をチェック
            if name_upper == current_scope['function_name'].upper():
                return current_scope.get('return_value', 0)

        # グローバル変数をチェック（関数内からもアクセス可能）
        return self.variables.get(name_upper, default)

    def get_print_output(self) -> List[str]:
        """PRINT関数の出力スタックを取得"""
        return self.print_stack

    def clear_print_stack(self):
        """PRINT関数の出力スタックをクリア"""
        self.print_stack.clear()

    def add_to_print_stack(self, message: str):
        """PRINT関数の出力をスタックに追加"""
        self.print_stack.append(message)

    def push_scope(self, function_name: str, parameters: Dict[str, Any], parameter_arrays: Dict[str, Dict] = None, array_mappings: Dict[str, str] = None):
        """新しいスコープをプッシュ"""
        if len(self.call_stack) >= self.max_call_depth:
            raise RuntimeError(get_message('error_max_call_depth', self.locale, self.max_call_depth))

        scope = {
            'function_name': function_name,
            'variables': {},
            'arrays': parameter_arrays.copy() if parameter_arrays else {},
            'parameters': parameters.copy(),
            'array_mappings': array_mappings.copy() if array_mappings else {},
            'return_value': ""  # EasyScripter仕様: 未設定の関数戻り値は空文字列
        }
        self.call_stack.append(scope)

    def pop_scope(self) -> Dict[str, Any]:
        """スコープをポップして戻り値を返す"""
        if self.call_stack:
            scope = self.call_stack.pop()

            # 配列パラメータの変更を元の配列に反映
            if 'array_mappings' in scope and scope['array_mappings']:
                for param_name, original_name in scope['array_mappings'].items():
                    if param_name in scope['arrays']:
                        # 関数内で変更された配列を元の配列に反映
                        original_name_upper = original_name.upper()

                        # 現在のスコープ(呼び出し元)を確認
                        parent_scope = self.get_current_scope()
                        if parent_scope and original_name_upper in parent_scope['arrays']:
                            # 親スコープの配列に反映
                            parent_scope['arrays'][original_name_upper].update(scope['arrays'][param_name])
                        elif original_name_upper in self.arrays:
                            # グローバル配列に反映
                            self.arrays[original_name_upper].update(scope['arrays'][param_name])
                        else:
                            # 配列が存在しない場合、新しく作成
                            if parent_scope:
                                parent_scope['arrays'][original_name_upper] = scope['arrays'][param_name].copy()
                            else:
                                self.arrays[original_name_upper] = scope['arrays'][param_name].copy()

            return scope.get('return_value', "")  # EasyScripter仕様: 未設定の関数戻り値は空文字列
        return ""  # EasyScripter仕様: 未設定の関数戻り値は空文字列

    def get_current_scope(self) -> Optional[Dict[str, Any]]:
        """現在のスコープを取得"""
        return self.call_stack[-1] if self.call_stack else None

    def get_array_ubound(self, array_name: str, dimension: int = 1) -> float:
        """
        配列の最大インデックスを取得（VBAのUBOUND相当）

        Args:
            array_name: 配列名
            dimension: 次元（1ベース）

        Returns:
            最大インデックス値（配列が存在しないまたは空の場合は-1）
        """
        array_name_upper = array_name.upper()

        # 現在のスコープから配列を検索
        current_scope = self.get_current_scope()
        array_dict = None
        if current_scope and array_name_upper in current_scope['arrays']:
            array_dict = current_scope['arrays'][array_name_upper]
        elif array_name_upper in self.arrays:
            array_dict = self.arrays[array_name_upper]

        if array_dict:
            if not array_dict:
                return -1.0  # 空配列

            # キーのタイプをチェック
            first_key = next(iter(array_dict.keys()))
            if isinstance(first_key, tuple):
                # 多次元配列
                if dimension > len(first_key):
                    return -1.0
                # 指定された次元の最大値を取得
                max_index = max(key[dimension - 1] for key in array_dict.keys())
                return float(max_index)
            else:
                # 1次元配列
                if dimension == 1:
                    return float(max(array_dict.keys()))
                else:
                    return -1.0
        return -1.0

    def get_array_lbound(self, array_name: str, dimension: int = 1) -> float:
        """
        配列の最小インデックスを取得（VBAのLBOUND相当）

        Args:
            array_name: 配列名
            dimension: 次元（1ベース）

        Returns:
            最小インデックス値（配列が存在しないまたは空の場合は0）
        """
        array_name_upper = array_name.upper()

        # 現在のスコープから配列を検索
        current_scope = self.get_current_scope()
        array_dict = None
        if current_scope and array_name_upper in current_scope['arrays']:
            array_dict = current_scope['arrays'][array_name_upper]
        elif array_name_upper in self.arrays:
            array_dict = self.arrays[array_name_upper]

        if array_dict:
            if not array_dict:
                return 0.0  # 空配列でも0を返す

            # キーのタイプをチェック
            first_key = next(iter(array_dict.keys()))
            if isinstance(first_key, tuple):
                # 多次元配列
                if dimension > len(first_key):
                    return 0.0
                # 指定された次元の最小値を取得（通常は0）
                min_index = min(key[dimension - 1] for key in array_dict.keys())
                return float(min_index)
            else:
                # 1次元配列
                if dimension == 1:
                    return float(min(array_dict.keys()))
                else:
                    return 0.0
        return 0.0

    def execute_split_function(self, array_name: str, text: Any, delimiter: Any) -> float:
        """SPLIT関数を実行"""
        array_name = str(array_name).upper()
        text = str(text) if text is not None else ""
        delimiter = str(delimiter) if delimiter is not None else ","

        # 現在のスコープを取得
        current_scope = self.get_current_scope()

        # 区切り文字で分割
        if delimiter == "":
            # 空の区切り文字の場合、文字単位で分割
            parts = list(text)
        else:
            # 通常の区切り文字で分割
            parts = text.split(delimiter)

        # 配列に格納（0ベースインデックス）
        if current_scope:
            # 関数内の場合、ローカルスコープに配列を作成
            current_scope['arrays'][array_name] = {}
            for i, part in enumerate(parts):
                current_scope['arrays'][array_name][i] = part
        else:
            # グローバルスコープに配列を作成
            self.arrays[array_name] = {}
            for i, part in enumerate(parts):
                self.arrays[array_name][i] = part

        # 要素数を返す
        return float(len(parts))

    def execute(self, script: str):
        """スクリプトを実行"""
        try:
            # スクリプト実行開始時に予約変数の初期値を保存（OUTPUT関数用）
            self._reserved_vars_initial = {
                'TXT1': self.variables.get('TXT1'),
                'TXT2': self.variables.get('TXT2'),
                'ANY_INPUT': self.variables.get('ANY_INPUT')
            }

            ast = self.parser.parse(script)
            for statement in ast:
                self.execute_statement(statement)
            # RETURNまたはRETURN_VALUEの値を返す
            return self.variables.get('RETURN', self.variables.get('RETURN_VALUE', None))
        except Exception as e:
            raise RuntimeError(get_message('error_script_execution', self.locale, str(e)))

    def execute_statement(self, node: ASTNode) -> Any:
        """ステートメントを実行"""
        if node.type == 'FUNCTION_DEF':
            # 関数定義を実行（登録）
            return self.execute_function_definition(node)

        elif node.type == 'ASSIGN':
            # 変数代入（スコープ対応）
            value = self.evaluate_expression(node.value)
            var_name = node.variable.upper()  # 変数名を大文字化

            # RELAY_OUTPUT変数への代入を検出（Tier 3実装）
            if var_name == "RELAY_OUTPUT":
                self.relay_output_assigned = True
                self.relay_output_value = value

            self.set_variable(node.variable, value)
            return value

        elif node.type == 'ASSIGN_ARRAY':
            # 配列代入（配列名も大文字小文字を区別しない）
            array_name = node.array.upper()
            index = int(self.evaluate_expression(node.index))
            value = self.evaluate_expression(node.value)

            # 現在のスコープを取得
            current_scope = self.get_current_scope()
            if current_scope:
                # 関数内の場合、ローカルスコープの配列に設定
                if array_name not in current_scope['arrays']:
                    current_scope['arrays'][array_name] = {}
                current_scope['arrays'][array_name][index] = value
            else:
                # グローバルスコープに設定
                if array_name not in self.arrays:
                    self.arrays[array_name] = {}
                self.arrays[array_name][index] = value
            return value

        elif node.type == 'ASSIGN_ARRAY_MULTI':
            # 多次元配列代入
            array_name = node.array.upper()
            indices = tuple(int(self.evaluate_expression(idx)) for idx in node.indices)
            value = self.evaluate_expression(node.value)

            # 現在のスコープを取得
            current_scope = self.get_current_scope()
            if current_scope:
                # 関数内の場合、ローカルスコープの配列に設定
                if array_name not in current_scope['arrays']:
                    current_scope['arrays'][array_name] = {}
                current_scope['arrays'][array_name][indices] = value
            else:
                # グローバルスコープに設定
                if array_name not in self.arrays:
                    self.arrays[array_name] = {}
                self.arrays[array_name][indices] = value
            return value

        elif node.type == 'SELECT_CASE':
            # SELECT CASE文
            return self.execute_select_case(node)

        elif node.type == 'IF':
            # IF文（ELSEIF対応）
            condition = self.evaluate_expression(node.condition)
            if self.is_true(condition):
                # IF条件が真の場合
                for stmt in node.then_branch:
                    self.execute_statement(stmt)
            else:
                # ELSEIF条件の順次評価
                executed = False
                if hasattr(node, 'elseif_branches') and node.elseif_branches:
                    for elseif_condition, elseif_statements in node.elseif_branches:
                        if self.is_true(self.evaluate_expression(elseif_condition)):
                            for stmt in elseif_statements:
                                self.execute_statement(stmt)
                            executed = True
                            break  # 最初に真になったELSEIF句のみ実行

                # ELSE句の実行（ELSEIF句が実行されなかった場合のみ）
                if not executed and node.else_branch:
                    for stmt in node.else_branch:
                        self.execute_statement(stmt)

        elif node.type == 'WHILE':
            # WHILE文
            try:
                while self.is_true(self.evaluate_expression(node.condition)):
                    for stmt in node.body:
                        self.execute_statement(stmt)
            except LoopExit as e:
                # EXIT WHILE処理
                if e.loop_type == 'WHILE':
                    pass  # ループを正常終了
                else:
                    # 他のループタイプ（FOR）のEXITは再スロー
                    raise

        elif node.type == 'FOR':
            # FOR文（ループ変数も大文字小文字を区別しない）
            var_name = node.variable.upper()
            start = self.evaluate_expression(node.start)
            end = self.evaluate_expression(node.end)
            step = self.evaluate_expression(node.step) if hasattr(node, 'step') else 1

            # 数値に変換
            start = self.to_number(start)
            end = self.to_number(end)
            step = self.to_number(step)

            # ループ実行
            current = start
            try:
                if step > 0:
                    while current <= end:
                        self.set_variable(var_name, current)
                        for stmt in node.body:
                            self.execute_statement(stmt)
                        current += step
                else:
                    while current >= end:
                        self.set_variable(var_name, current)
                        for stmt in node.body:
                            self.execute_statement(stmt)
                        current += step
            except LoopExit as e:
                # EXIT FOR処理
                if e.loop_type == 'FOR':
                    pass  # ループを正常終了
                else:
                    # 他のループタイプ（WHILE）のEXITは再スロー
                    raise

        elif node.type == 'dim':
            # DIM文（配列宣言）
            array_name = node.array_name.upper()
            if node.sizes:
                # 配列として宣言
                if len(node.sizes) == 1:
                    # 1次元配列
                    size = int(self.evaluate_expression(node.sizes[0]))
                    # 配列を初期化（0ベースインデックス）
                    scope = self.get_current_scope()
                    if scope:
                        scope['arrays'][array_name] = {i: 0 for i in range(size + 1)}
                    else:
                        self.arrays[array_name] = {i: 0 for i in range(size + 1)}
                else:
                    # 多次元配列
                    sizes = [int(self.evaluate_expression(s)) for s in node.sizes]
                    # 多次元配列を初期化
                    scope = self.get_current_scope()
                    array_dict = {}
                    # 全ての組み合わせのインデックスを作成
                    for indices in itertools.product(*[range(s+1) for s in sizes]):
                        # タプルをキーとして使用
                        array_dict[indices] = 0
                    if scope:
                        scope['arrays'][array_name] = array_dict
                    else:
                        self.arrays[array_name] = array_dict
            else:
                # 通常の変数として宣言
                self.set_variable(array_name, 0)
            return None

        elif node.type == 'REDIM_STMT':
            # REDIM文
            array_name = node.array_name.upper()
            new_size = int(self.evaluate_expression(node.size))
            preserve = False
            if node.preserve:
                preserve = self.is_true(self.evaluate_expression(node.preserve))
            self.execute_redim_function(array_name, new_size, preserve)
            return new_size

        elif node.type == 'ARRAY_STMT':
            # ARRAY文
            array_name = node.array_name.upper()
            values = []
            for value_node in node.values:
                values.append(self.evaluate_expression(value_node))
            self.execute_array_function_with_name(array_name, values)
            return len(values)

        elif node.type == 'SPLIT_STMT':
            # SPLIT文
            array_name = node.array_name.upper()
            text = str(self.evaluate_expression(node.text))
            delimiter = str(self.evaluate_expression(node.delimiter))
            return self.execute_split_function(array_name, text, delimiter)

        elif node.type == 'FUNCTION_CALL':
            # 関数呼び出し（ステートメントとしても扱う）
            return self.evaluate_expression(node)

        elif node.type == 'RETURN':
            # RETURN文の処理
            current_scope = self.get_current_scope()
            if current_scope:
                if hasattr(node, 'value') and node.value:
                    # RETURN value の形式
                    return_value = self.evaluate_expression(node.value)
                    current_scope['return_value'] = return_value
                    return return_value
                else:
                    # 単純なRETURN（戻り値なし）
                    current_scope['return_value'] = 0
                    return 0
            else:
                # グローバルスコープでのRETURN（RETURN変数として扱う）
                if hasattr(node, 'value') and node.value:
                    return_value = self.evaluate_expression(node.value)
                    self.variables['RETURN'] = return_value
                    return return_value
            return 0

        elif node.type == 'EXIT':
            # EXIT文の処理
            exit_type = node.exit_type.upper()  # "FUNCTION", "FOR", "WHILE"

            if exit_type == 'FUNCTION':
                raise FunctionExit()
            elif exit_type == 'FOR':
                raise LoopExit('FOR')
            elif exit_type == 'WHILE':
                raise LoopExit('WHILE')
            else:
                raise RuntimeError(f"不明なEXIT文タイプ: {exit_type}")

        else:
            # その他の式
            return self.evaluate_expression(node)

    def execute_function_definition(self, node: ASTNode):
        """関数定義を実行（登録）"""
        func_name = node.name.upper()

        # ビルトイン関数との名前衝突チェック
        if is_builtin_function(func_name):
            raise RuntimeError(get_message('error_function_conflict', self.locale, node.name))

        # 関数を辞書に登録
        self.user_functions[func_name] = node
        return None

    def execute_select_case(self, node: ASTNode) -> Any:
        """SELECT CASE文を実行"""
        # テスト式を評価
        test_value = self.evaluate_expression(node.test_expression)

        # 各Caseを順番に評価
        for case in node.cases:
            if self.match_case(test_value, case.conditions):
                # マッチしたCaseのステートメントを実行
                for stmt in case.statements:
                    self.execute_statement(stmt)
                return  # 最初にマッチしたCaseで終了

        # Case Elseの実行
        if node.else_case:
            for stmt in node.else_case:
                self.execute_statement(stmt)

    def match_case(self, test_value: Any, conditions: List[ASTNode]) -> bool:
        """Case条件のマッチング判定"""
        for condition in conditions:
            if self.match_single_condition(test_value, condition):
                return True  # いずれかの条件にマッチすればTrue
        return False

    def match_single_condition(self, test_value: Any, condition: ASTNode) -> bool:
        """単一のCase条件のマッチング判定"""
        if condition.type == 'CASE_VALUE':
            # 単一値の比較
            condition_value = self.evaluate_expression(condition.value)
            return self.compare_values(test_value, condition_value, 'EQ')

        elif condition.type == 'CASE_RANGE':
            # 範囲のチェック (start TO end)
            start_value = self.evaluate_expression(condition.start)
            end_value = self.evaluate_expression(condition.end)

            # 数値比較を試みる
            try:
                test_num = self.to_number(test_value)
                start_num = self.to_number(start_value)
                end_num = self.to_number(end_value)
                return start_num <= test_num <= end_num
            except:
                # 文字列比較
                test_str = str(test_value).upper()
                start_str = str(start_value).upper()
                end_str = str(end_value).upper()
                return start_str <= test_str <= end_str

        elif condition.type == 'CASE_IS':
            # Is演算子による比較
            compare_value = self.evaluate_expression(condition.value)
            return self.compare_values(test_value, compare_value, condition.operator)

        else:
            # その他の条件（式として評価）
            condition_value = self.evaluate_expression(condition)
            return self.compare_values(test_value, condition_value, 'EQ')

    def compare_values(self, left: Any, right: Any, operator: str) -> bool:
        """値を比較（大文字小文字を区別しない）"""
        # 両方が数値として有効な場合のみ数値比較
        left_is_numeric = False
        right_is_numeric = False

        try:
            # 数値型かチェック
            if isinstance(left, (int, float)):
                left_num = float(left)
                left_is_numeric = True
            elif isinstance(left, str) and left.replace('.', '', 1).replace('-', '', 1).isdigit():
                left_num = float(left)
                left_is_numeric = True
        except:
            pass

        try:
            if isinstance(right, (int, float)):
                right_num = float(right)
                right_is_numeric = True
            elif isinstance(right, str) and right.replace('.', '', 1).replace('-', '', 1).isdigit():
                right_num = float(right)
                right_is_numeric = True
        except:
            pass

        # 両方が数値の場合は数値比較
        if left_is_numeric and right_is_numeric:
            if operator == 'EQ':
                return left_num == right_num
            elif operator == 'NEQ':
                return left_num != right_num
            elif operator == 'LT':
                return left_num < right_num
            elif operator == 'GT':
                return left_num > right_num
            elif operator == 'LTE':
                return left_num <= right_num
            elif operator == 'GTE':
                return left_num >= right_num

        # それ以外は文字列比較（大文字小文字を区別しない）
        left_str = str(left).upper()
        right_str = str(right).upper()

        if operator == 'EQ':
            return left_str == right_str
        elif operator == 'NEQ':
            return left_str != right_str
        elif operator == 'LT':
            return left_str < right_str
        elif operator == 'GT':
            return left_str > right_str
        elif operator == 'LTE':
            return left_str <= right_str
        elif operator == 'GTE':
            return left_str >= right_str

        return False

    def execute_user_function(self, func_name: str, arguments: List[Any], arg_names: List[str] = None) -> Any:
        """ユーザー定義関数を実行"""
        func_name_upper = func_name.upper()
        func_def = self.user_functions[func_name_upper]

        # 必須パラメータの数をチェック
        required_params = [p for p in func_def.parameters if not hasattr(p, 'optional') or not p.optional]
        if len(arguments) < len(required_params):
            # パラメータ名のリストを作成
            param_names = [p.name for p in func_def.parameters]
            param_list = ", ".join(param_names) if param_names else ""

            error_msg = f"関数 {func_name}: 引数が不足しています（必要: {len(required_params)}, 実際: {len(arguments)}）"
            usage_msg = f"使用例: {func_name}({param_list})"
            raise RuntimeError(f"{error_msg}\n{usage_msg}")

        # パラメータの準備
        parameters = {}
        parameter_arrays = {}
        array_mappings = {}  # パラメータ名 -> 元の配列名のマッピング

        for i, param in enumerate(func_def.parameters):
            param_name = param.name.upper()
            if i < len(arguments):
                # 引数が提供されている場合
                arg_value = arguments[i]
                # 配列引数の場合、配列として設定
                if isinstance(arg_value, dict) and arg_names and i < len(arg_names) and arg_names[i]:
                    parameter_arrays[param_name] = arg_value.copy()  # コピーを作成
                    array_mappings[param_name] = arg_names[i]  # 元の配列名を記録
                    parameters[param_name] = 0  # 変数としても初期化
                else:
                    parameters[param_name] = arg_value
            elif hasattr(param, 'optional') and param.optional and hasattr(param, 'default_value') and param.default_value is not None:
                # オプション引数のデフォルト値を評価
                parameters[param_name] = self.evaluate_expression(param.default_value)
            else:
                # デフォルト値がない場合は0
                parameters[param_name] = 0

        # 新しいスコープでの実行（配列も渡す）
        self.push_scope(func_name_upper, parameters, parameter_arrays, array_mappings)

        try:
            # 関数本体を実行
            for statement in func_def.body:
                self.execute_statement(statement)
        except FunctionExit:
            # EXIT FUNCTION処理 - 早期リターン
            pass  # finally節で戻り値を返すので何もしない
        finally:
            # スコープをポップして戻り値を返す
            return_value = self.pop_scope()

        return return_value

    def evaluate_expression(self, node: Any) -> Any:
        """式を評価"""
        # ASTNodeでない場合(直接の値)
        if not isinstance(node, ASTNode):
            return node

        if node is None:
            return 0

        if node.type == 'LITERAL':
            return node.value

        elif node.type == 'VARIABLE':
            # 変数名を大文字に統一して取得(スコープ対応)
            return self.get_variable(node.name, 0)

        elif node.type == 'ARRAY_VAR':
            # 配列変数参照(ITEMS[]記法) - 配列オブジェクト自体を返す
            array_name = node.name.upper()

            # 現在のスコープから配列を検索
            current_scope = self.get_current_scope()
            if current_scope and array_name in current_scope['arrays']:
                return {'_array_ref': array_name, '_scope': 'local', '_data': current_scope['arrays'][array_name]}

            # グローバルスコープから検索
            if array_name in self.arrays:
                return {'_array_ref': array_name, '_scope': 'global', '_data': self.arrays[array_name]}

            # 配列が存在しない場合は空の配列オブジェクトを返す
            return {'_array_ref': array_name, '_scope': 'local' if current_scope else 'global', '_data': {}}

        elif node.type == 'ARRAY_ACCESS':
            # 配列名を大文字に統一
            array_name = node.array.upper()
            index = int(self.evaluate_expression(node.index))

            # 現在のスコープから配列を検索
            current_scope = self.get_current_scope()
            if current_scope and array_name in current_scope['arrays'] and index in current_scope['arrays'][array_name]:
                return current_scope['arrays'][array_name][index]

            # グローバルスコープから検索
            if array_name in self.arrays and index in self.arrays[array_name]:
                return self.arrays[array_name][index]
            return 0

        elif node.type == 'BINARY_OP':
            # 短絡評価対応: AND/OR演算子の場合は特別な処理
            # VBA準拠: 結果は数値(True=1.0, False=0.0)
            if node.operator == 'AND':
                left = self.evaluate_expression(node.left)
                if not self.is_true(left):
                    return 0.0  # 左が偽なら右を評価せずに0.0を返す
                right = self.evaluate_expression(node.right)
                return 1.0 if self.is_true(right) else 0.0
            elif node.operator == 'OR':
                left = self.evaluate_expression(node.left)
                if self.is_true(left):
                    return 1.0  # 左が真なら右を評価せずに1.0を返す
                right = self.evaluate_expression(node.right)
                return 1.0 if self.is_true(right) else 0.0
            else:
                # その他の演算子は通常の評価
                left = self.evaluate_expression(node.left)
                right = self.evaluate_expression(node.right)
                return self.evaluate_binary_op(node.operator, left, right)

        elif node.type == 'UNARY_OP':
            operand = self.evaluate_expression(node.operand)
            return self.evaluate_unary_op(node.operator, operand)

        elif node.type == 'FUNCTION_CALL':
            # 関数呼び出し
            func_name = node.name.upper()

            # 配列アクセスかどうかチェック(配列が定義されている場合)
            current_scope = self.get_current_scope()
            is_array = False
            if current_scope and func_name in current_scope['arrays']:
                is_array = True
            elif func_name in self.arrays:
                is_array = True

            # 配列アクセスとして処理
            if is_array:
                if len(node.arguments) == 1:
                    # 1次元配列アクセス
                    index = int(self.evaluate_expression(node.arguments[0]))
                    # 配列から値を取得
                    if current_scope and func_name in current_scope['arrays'] and index in current_scope['arrays'][func_name]:
                        return current_scope['arrays'][func_name][index]
                    elif func_name in self.arrays and index in self.arrays[func_name]:
                        return self.arrays[func_name][index]
                    else:
                        # インデックスが範囲外の場合は0を返す
                        return 0
                else:
                    # 多次元配列アクセス
                    indices = tuple(int(self.evaluate_expression(arg)) for arg in node.arguments)
                    # 配列から値を取得
                    if current_scope and func_name in current_scope['arrays'] and indices in current_scope['arrays'][func_name]:
                        return current_scope['arrays'][func_name][indices]
                    elif func_name in self.arrays and indices in self.arrays[func_name]:
                        return self.arrays[func_name][indices]
                    else:
                        # インデックスが範囲外の場合は0を返す
                        return 0

            # SPLIT関数の特別処理(第1引数は配列名として扱う)
            elif func_name == 'SPLIT' and len(node.arguments) >= 3:
                # 第1引数は配列変数参照または変数名として扱い、評価しない
                array_name_node = node.arguments[0]
                if hasattr(array_name_node, 'type'):
                    if array_name_node.type == 'ARRAY_VAR':
                        array_name = array_name_node.name
                    elif array_name_node.type == 'VARIABLE':
                        array_name = array_name_node.name
                    elif array_name_node.type == 'LITERAL' and hasattr(array_name_node, 'datatype') and array_name_node.datatype == 'STRING':
                        array_name = array_name_node.value
                    else:
                        array_name = str(self.evaluate_expression(array_name_node))
                else:
                    array_name = str(array_name_node)

                # 第2引数以降は通常通り評価
                text = self.evaluate_expression(node.arguments[1]) if len(node.arguments) > 1 else ""
                delimiter = self.evaluate_expression(node.arguments[2]) if len(node.arguments) > 2 else ","

                # SPLIT関数の実行
                return self.execute_split_function(array_name, text, delimiter)

            # 引数を評価
            args = []
            arg_names = []  # 配列名を追跡
            for arg in node.arguments:
                # 配列変数参照の場合(ITEMS[]記法)
                if isinstance(arg, ASTNode) and arg.type == 'ARRAY_VAR':
                    var_name = arg.name.upper()
                    arg_names.append(var_name)
                    # 配列の実体を引数として渡す
                    current_scope = self.get_current_scope()
                    if current_scope and var_name in current_scope['arrays']:
                        args.append(current_scope['arrays'][var_name])
                    elif var_name in self.arrays:
                        args.append(self.arrays[var_name])
                    else:
                        # 配列が存在しない場合は空の配列として渡す
                        args.append({})
                # 変数ノードの場合、配列かどうかをチェック(後方互換性用)
                elif isinstance(arg, ASTNode) and arg.type == 'VARIABLE':
                    var_name = arg.name.upper()
                    # 配列があるかチェック
                    current_scope = self.get_current_scope()
                    if current_scope and var_name in current_scope['arrays']:
                        # 関数スコープの配列として渡す
                        arg_names.append(var_name)
                        args.append(current_scope['arrays'][var_name])
                    elif var_name in self.arrays:
                        # グローバル配列として渡す
                        arg_names.append(var_name)
                        args.append(self.arrays[var_name])
                    else:
                        # 配列でない場合は通常の変数として評価
                        arg_names.append(None)
                        args.append(self.evaluate_expression(arg))
                else:
                    args.append(self.evaluate_expression(arg))
                    arg_names.append(None)

            # ユーザー定義関数を最優先でチェック
            if func_name in self.user_functions:
                return self.execute_user_function(func_name, args, arg_names)

            # PRINT関数の特殊処理
            elif func_name == 'PRINT':
                # 特殊フラグ "CLEAR" のチェック
                if len(args) == 1 and str(args[0]).upper() == "CLEAR":
                    self.clear_print_stack()
                    return ""

                # 引数を文字列に変換して連結(数値のフォーマットを改善)
                if args:
                    formatted_args = []
                    for arg in args:
                        if isinstance(arg, float) and arg.is_integer():
                            # 整数値の場合は .0 を表示しない
                            formatted_args.append(str(int(arg)))
                        else:
                            formatted_args.append(str(arg))
                    output = " ".join(formatted_args)
                else:
                    output = ""

                # スタックに追加
                self.add_to_print_stack(output)
                return output

            # OUTPUT関数の特殊処理（予約変数変換 + locale渡し）
            elif func_name == 'OUTPUT':
                # 第1引数が文字列リテラルで予約変数名の場合、実値に変換
                if len(args) > 0 and isinstance(args[0], str):
                    reserved_var = args[0].upper()
                    if reserved_var in ['TXT1', 'TXT2', 'ANY_INPUT']:
                        # スクリプト実行開始時の初期値を使用（スクリプト内での上書きを無視）
                        if hasattr(self, '_reserved_vars_initial') and reserved_var in self._reserved_vars_initial:
                            args[0] = self._reserved_vars_initial[reserved_var]
                        else:
                            # フォールバック: 現在の値を取得
                            args[0] = self.get_variable(reserved_var, args[0])

                # ビルトイン関数として実行（locale引数を追加）
                func = get_builtin_function(func_name)
                result = func(*args, locale=self.locale)
                return result

            # INPUT関数の特殊処理（locale渡し）
            elif func_name == 'INPUT':
                func = get_builtin_function(func_name)
                result = func(*args, locale=self.locale)
                return result

            # ISFILEEXIST関数の特殊処理（locale渡し）
            elif func_name == 'ISFILEEXIST':
                func = get_builtin_function(func_name)
                result = func(*args, locale=self.locale)
                return result

            # REDIM関数の特殊処理
            elif func_name == 'REDIM':
                if len(node.arguments) < 2:
                    raise RuntimeError(get_message('error_redim_needs_array', self.locale))

                # 第一引数は配列変数参照または変数名
                first_arg = node.arguments[0]
                if isinstance(first_arg, ASTNode) and first_arg.type == 'ARRAY_VAR':
                    array_name = first_arg.name.upper()
                elif isinstance(first_arg, ASTNode) and first_arg.type == 'VARIABLE':
                    array_name = first_arg.name.upper()
                else:
                    raise RuntimeError(get_message('error_redim_first_arg', self.locale))

                new_size = int(self.evaluate_expression(node.arguments[1]))
                preserve = False
                if len(node.arguments) > 2:
                    preserve_arg = self.evaluate_expression(node.arguments[2])
                    preserve = self.is_true(preserve_arg)

                self.execute_redim_function(array_name, new_size, preserve)
                return float(new_size)

            # ARRAY関数の特殊処理
            elif func_name == 'ARRAY':
                # すべての引数を値として評価(空配列も許可)
                values = []
                for arg in node.arguments:
                    values.append(self.evaluate_expression(arg))

                # 配列を作成して返す
                return self.execute_array_function(*values)

            # UBOUND/LBOUND関数の特殊処理
            elif func_name in ['UBOUND', 'LBOUND']:
                if len(node.arguments) == 0:
                    raise RuntimeError(get_message('error_array_function_needs_name', self.locale, func_name))

                # 第一引数が配列変数参照または変数ノードの場合、変数名を直接使用
                first_arg = node.arguments[0]
                if isinstance(first_arg, ASTNode) and first_arg.type == 'ARRAY_VAR':
                    array_name = first_arg.name
                elif isinstance(first_arg, ASTNode) and first_arg.type == 'VARIABLE':
                    array_name = first_arg.name
                else:
                    # 文字列リテラルの場合は評価結果を使用
                    array_name = str(self.evaluate_expression(first_arg))

                dimension = int(self.evaluate_expression(node.arguments[1])) if len(node.arguments) > 1 else 1

                if func_name == 'UBOUND':
                    return self.get_array_ubound(array_name, dimension)
                else:
                    return self.get_array_lbound(array_name, dimension)


            # ISARRAY関数の特殊処理
            elif func_name == 'ISARRAY':
                if len(args) == 0:
                    raise RuntimeError(get_message('error_isarray_needs_arg', self.locale))

                # 引数が配列かどうかを直接チェック
                arg = args[0]
                # 配列は辞書として格納されている
                if isinstance(arg, dict):
                    return 1.0
                elif isinstance(arg, list):
                    return 1.0
                elif isinstance(arg, str):
                    # 変数名が文字列で渡された場合
                    var_name = arg.upper()
                    if var_name in self.arrays and self.arrays[var_name]:
                        return 1.0
                return 0.0

            # JOIN関数の特殊処理
            elif func_name == 'JOIN':
                if len(node.arguments) == 0:
                    raise RuntimeError(get_message('error_join_needs_array', self.locale))

                # 第1引数は配列変数参照または変数名
                first_arg = node.arguments[0]
                if isinstance(first_arg, ASTNode) and first_arg.type == 'ARRAY_VAR':
                    array_name = first_arg.name.upper()
                elif isinstance(first_arg, ASTNode) and first_arg.type == 'VARIABLE':
                    array_name = first_arg.name.upper()
                else:
                    array_name = str(self.evaluate_expression(first_arg)).upper()

                # 残りの引数を評価
                args = []
                for i in range(1, len(node.arguments)):
                    args.append(self.evaluate_expression(node.arguments[i]))
                delimiter = str(args[0]) if len(args) > 0 else " "  # デフォルトは半角スペース
                unique_only = False
                if len(args) > 1:
                    # 第3引数で重複除外を指定(0以外の値でユニーク化)
                    try:
                        unique_val = float(args[1])
                        unique_only = unique_val != 0
                    except:
                        unique_only = False

                # 現在のスコープを取得
                current_scope = self.get_current_scope()
                array_dict = None

                # スコープから配列を検索
                if current_scope and array_name in current_scope['arrays']:
                    array_dict = current_scope['arrays'][array_name]
                elif array_name in self.arrays:
                    array_dict = self.arrays[array_name]

                # 配列が存在しない場合は空文字列を返す
                if not array_dict:
                    return ""

                # 配列要素を順番に取得
                sorted_keys = sorted(array_dict.keys())
                elements = []
                seen = set() if unique_only else None

                for key in sorted_keys:
                    value = array_dict[key]
                    # 数値の場合は整数かどうかチェック
                    if isinstance(value, float) and value.is_integer():
                        value_str = str(int(value))
                    else:
                        value_str = str(value)

                    # ユニークモードの場合は重複チェック
                    if unique_only:
                        value_upper = value_str.upper()
                        if value_upper not in seen:
                            seen.add(value_upper)
                            elements.append(value_str)
                    else:
                        elements.append(value_str)

                # 区切り文字で結合
                return delimiter.join(elements)

            # CSVDIFF関数の特殊処理
            elif func_name == 'CSVDIFF':
                if len(node.arguments) < 3:
                    raise RuntimeError(get_message('error_csvdiff_args', self.locale))

                # 第1引数は配列変数参照または変数名
                first_arg = node.arguments[0]
                if isinstance(first_arg, ASTNode) and first_arg.type == 'ARRAY_VAR':
                    array_name = first_arg.name.upper()
                elif isinstance(first_arg, ASTNode) and first_arg.type == 'VARIABLE':
                    array_name = first_arg.name.upper()
                else:
                    array_name = str(self.evaluate_expression(first_arg)).upper()

                csv1 = str(self.evaluate_expression(node.arguments[1])) if len(node.arguments) > 1 else ""
                csv2 = str(self.evaluate_expression(node.arguments[2])) if len(node.arguments) > 2 else ""

                # CSVの差分を取得
                diff_elements = BuiltinFunctions.CSVDIFF(csv1, csv2)

                # 配列を初期化
                self.arrays[array_name] = {}

                # 差分要素を配列に格納
                for i, element in enumerate(diff_elements):
                    self.arrays[array_name][i] = element

                # 要素数を返す
                return float(len(diff_elements))

            # ビルトイン関数かどうかチェック
            elif is_builtin_function(func_name):
                func = get_builtin_function(func_name)
                try:
                    # Engine-aware functions (engine渡しが必要な関数)
                    if func_name in ['LOOP_SUBGRAPH', 'LOOPSUBGRAPH']:
                        # locale引数を追加で渡す
                        result = func(self, *args, locale=self.locale)
                    elif func_name in ['OPTIMAL_LATENT', 'OPTIMALLATENT']:
                        result = func(self, *args)
                    # ANY型関数は引数なしの場合、any_input変数を自動的に渡す
                    elif func_name in ['GETANYTYPE', 'GETANYWIDTH', 'GETANYHEIGHT',
                                     'GETANYVALUEINT', 'GETANYVALUEFLOAT', 'GETANYSTRING']:
                        if len(args) == 0:
                            # any_input変数を引数として渡す
                            any_data = self.get_variable('any_input', None)
                            result = func(any_data)
                        else:
                            # 引数が指定されている場合はそのまま渡す
                            result = func(*args)
                    # PYEXEC関数: 辞書型配列をPythonリストに変換
                    elif func_name == 'PYEXEC':
                        # 引数を変換（辞書型配列 → Pythonリスト）
                        converted_args = []
                        for arg in args:
                            if isinstance(arg, dict) and all(isinstance(k, int) for k in arg.keys()):
                                # 辞書型配列をPythonリストに変換
                                sorted_keys = sorted(arg.keys())
                                converted_args.append([arg[k] for k in sorted_keys])
                            else:
                                converted_args.append(arg)
                        result = func(*converted_args)
                    else:
                        # 通常のビルトイン関数
                        result = func(*args)
                    return result
                except TypeError as e:
                    # 引数エラーの可能性が高い
                    usage = get_function_usage(func_name)
                    error_msg = get_message('error_function_execution', self.locale, func_name, str(e))
                    if usage:
                        error_msg += f"\n使用例: {usage}"
                    raise RuntimeError(error_msg)
                except Exception as e:
                    raise RuntimeError(get_message('error_function_execution', self.locale, func_name, str(e)))
            else:
                # ビルトイン関数ではない場合、変数として扱う(引数がない場合のみ)
                if len(args) == 0:
                    # 関数内からアクセスの場合、ローカル変数をチェック
                    return self.get_variable(node.name, 0)
                else:
                    # 引数がある場合はエラーとして扱う
                    # 似た名前のビルトイン関数を提案
                    suggestions = []
                    func_name_upper = func_name.upper()

                    # よくある間違いをチェック
                    common_mistakes = {
                        'PRINT': get_message('hint_print_usage', self.locale),
                        'IF': get_message('hint_if_control', self.locale),
                        'VAR': get_message('hint_var_deprecated', self.locale)
                    }

                    if func_name_upper in common_mistakes:
                        raise RuntimeError(get_message('error_function_not_defined', self.locale, func_name) + "\n" + common_mistakes[func_name_upper])

                    # 似た名前の関数を検索
                    for builtin_func in BUILTIN_FUNCTIONS:
                        if builtin_func.startswith(func_name_upper[:2]):
                            usage = get_function_usage(builtin_func)
                            if usage:
                                suggestions.append(f"  {usage}")

                    error_msg = get_message('error_function_not_defined', self.locale, func_name)
                    if suggestions:
                        error_msg += "\n利用可能な類似関数:\n" + "\n".join(suggestions[:3])  # 最大3つまで表示
                    raise RuntimeError(error_msg)

        return 0

    def evaluate_binary_op(self, operator: str, left: Any, right: Any) -> Any:
        """二項演算子を評価"""
        # 文字列連結
        if operator == 'CONCAT':
            return self.format_for_string(left) + self.format_for_string(right)

        # 論理演算（VBA準拠: 結果は数値 True=1.0, False=0.0）
        if operator == 'AND':
            return 1.0 if (self.is_true(left) and self.is_true(right)) else 0.0
        elif operator == 'OR':
            return 1.0 if (self.is_true(left) or self.is_true(right)) else 0.0

        # 比較演算（VBA準拠: 結果は数値 True=1.0, False=0.0）
        # 文字列の場合は大文字小文字を区別しない
        elif operator == 'EQ':
            # 両方が文字列の場合、大文字小文字を区別しない比較
            if isinstance(left, str) and isinstance(right, str):
                return 1.0 if left.upper() == right.upper() else 0.0
            return 1.0 if left == right else 0.0
        elif operator == 'NEQ':
            # 両方が文字列の場合、大文字小文字を区別しない比較
            if isinstance(left, str) and isinstance(right, str):
                return 1.0 if left.upper() != right.upper() else 0.0
            return 1.0 if left != right else 0.0
        elif operator == 'LT':
            return 1.0 if self.to_number(left) < self.to_number(right) else 0.0
        elif operator == 'GT':
            return 1.0 if self.to_number(left) > self.to_number(right) else 0.0
        elif operator == 'LTE':
            return 1.0 if self.to_number(left) <= self.to_number(right) else 0.0
        elif operator == 'GTE':
            return 1.0 if self.to_number(left) >= self.to_number(right) else 0.0

        # 算術演算
        left_num = self.to_number(left)
        right_num = self.to_number(right)

        if operator == 'PLUS':
            return left_num + right_num
        elif operator == 'MINUS':
            return left_num - right_num
        elif operator == 'MULTIPLY':
            return left_num * right_num
        elif operator == 'DIVIDE':
            if right_num == 0:
                raise RuntimeError(get_message('error_zero_division', self.locale))
            return left_num / right_num
        elif operator == 'MOD':
            if right_num == 0:
                raise RuntimeError(get_message('error_zero_division_mod', self.locale))
            return left_num % right_num
        elif operator == 'INTDIV':
            if right_num == 0:
                raise RuntimeError(get_message('error_zero_division', self.locale))
            return int(left_num // right_num)
        elif operator == 'POWER':
            return left_num ** right_num

        return 0

    def evaluate_unary_op(self, operator: str, operand: Any) -> Any:
        """単項演算子を評価"""
        if operator == 'NOT':
            # VBA準拠: 結果は数値（True=1.0, False=0.0）
            return 1.0 if not self.is_true(operand) else 0.0
        elif operator == 'MINUS':
            return -self.to_number(operand)
        elif operator == 'PLUS':
            return self.to_number(operand)
        return operand

    def format_for_string(self, value: Any) -> str:
        """値を文字列連結用にフォーマット"""
        if isinstance(value, float):
            # 整数値の場合は.0を除去
            if value.is_integer():
                return str(int(value))
            else:
                return str(value)
        elif value is None:
            return ""
        else:
            return str(value)

    def is_true(self, value: Any) -> bool:
        """値を真偽値に変換
        
        文字列の場合、以下の特別なルールを適用:
        - "FALSE", "false", "False" → False
        - "0" → False
        - 空文字列 → False
        - その他の文字列 → True
        """
        if isinstance(value, bool):
            return value
        elif isinstance(value, (int, float)):
            return value != 0
        elif isinstance(value, str):
            # 特別な文字列の処理（大文字小文字を区別しない）
            upper_value = value.upper()
            if upper_value == "FALSE":
                return False
            elif upper_value == "0":
                return False
            # 空文字列はFalse
            elif len(value) == 0:
                return False
            # その他の文字列はTrue
            else:
                return True
        return False

    def to_number(self, value: Any) -> float:
        """値を数値に変換"""
        if isinstance(value, (int, float)):
            return float(value)
        elif isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                return 0.0
        elif isinstance(value, bool):
            return 1.0 if value else 0.0
        return 0.0

    def execute_redim_function(self, array_name: str, new_size: int, preserve: bool = False) -> float:
        """REDIM関数の実行"""
        array_name = array_name.upper()

        # 現在のスコープを取得
        current_scope = self.get_current_scope()

        # 既存の配列データを取得
        existing_data = {}
        if current_scope and array_name in current_scope['arrays']:
            existing_data = current_scope['arrays'][array_name].copy()
        elif array_name in self.arrays:
            existing_data = self.arrays[array_name].copy()

        # 新しい配列を作成
        new_array = {}

        # preserveがTrueの場合、既存のデータを保持
        if preserve and existing_data:
            for i in range(new_size):  # 0からnew_size-1まで
                if i in existing_data:
                    new_array[i] = existing_data[i]
                else:
                    new_array[i] = 0  # デフォルト値
        else:
            # preserveがFalseの場合、すべて0で初期化
            for i in range(new_size):  # 0からnew_size-1まで
                new_array[i] = 0

        # 配列を設定
        if current_scope:
            current_scope['arrays'][array_name] = new_array
        else:
            self.arrays[array_name] = new_array

        return float(new_size)

    def execute_array_function(self, *values) -> Dict[int, Any]:
        """ARRAY関数の実行 - 値のリストから配列を作成"""
        new_array = {}
        for i, value in enumerate(values):
            new_array[i] = value
        return new_array

    def execute_array_function_with_name(self, array_name: str, values: List[Any]) -> float:
        """ARRAY関数の実行 - 指定した配列名に値のリストから配列を作成"""
        array_name = array_name.upper()

        # 現在のスコープを取得
        current_scope = self.get_current_scope()

        # 新しい配列を作成
        new_array = {}
        for i, value in enumerate(values):
            new_array[i] = value

        # 配列を設定
        if current_scope:
            current_scope['arrays'][array_name] = new_array
        else:
            self.arrays[array_name] = new_array

        return float(len(values))