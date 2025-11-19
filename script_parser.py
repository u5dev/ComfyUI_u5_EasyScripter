"""
VBA風スクリプトパーサー
トークナイズとAST構築を行う
"""

# バージョン情報（Raw文字列リテラル対応版）
PARSER_VERSION = "2.1.0-raw-string-support"
PARSER_BUILD_DATE = "2025-01-21"

import re
from typing import List, Any, Optional, Union

try:
    from .locales import get_message
except ImportError:
    from locales import get_message

class Token:
    """トークンクラス"""
    def __init__(self, type_: str, value: Any, line: int = 0, is_end_of_line: bool = False):
        self.type = type_
        self.value = value
        self.line = line
        self.is_end_of_line = is_end_of_line  # 行末トークンかどうか（1行IF判定用）

class ASTNode:
    """Abstract Syntax Tree ノード"""
    def __init__(self, type_: str, **kwargs):
        self.type = type_
        for key, value in kwargs.items():
            setattr(self, key, value)

class ScriptParser:
    """VBA風スクリプトのパーサー"""

    # トークンパターン
    TOKEN_PATTERNS = [
        # Raw文字列リテラル（エスケープ処理を最小限にする）
        # VBA式""のみサポート: 文字列内の"を表す
        # バックスラッシュは通常文字として扱う（エスケープ処理なし）
        (r'^r"((?:[^"]|"")*)"', 'RAW_STRING'),
        # 文字列リテラルを先に判定（コメントより優先）
        # VBA式の"" エスケープをサポート: "" は " を表す
        (r'^"((?:[^"]|"")*)"', 'STRING'),
        (r"^'([^']*)'", 'STRING'),
        # その後でコメントを判定
        (r'^\s*\'\s+.*$', 'COMMENT'),  # ' の後にスペースがある場合のみコメント
        (r'^REM\b', 'COMMENT'),
        # 配列操作キーワード
        (r'^DIM\b', 'DIM'),
        (r'^REDIM\b', 'REDIM'),
        (r'^ARRAY\b', 'ARRAY_FUNC'),
        (r'^SPLIT\b', 'SPLIT_FUNC'),
        # 関数定義関連
        (r'^FUNCTION\b', 'FUNCTION_DEF'),
        (r'^END\s+FUNCTION\b', 'END_FUNCTION'),
        (r'^BYVAL\b', 'BYVAL'),
        (r'^BYREF\b', 'BYREF'),
        (r'^OPTIONAL\b', 'OPTIONAL'),
        (r'^AS\b', 'AS'),
        # 制御構造
        (r'^SELECT\s+CASE\b', 'SELECT_CASE'),
        (r'^END\s+SELECT\b', 'END_SELECT'),
        (r'^CASE\s+ELSE\b', 'CASE_ELSE'),
        (r'^CASE\b', 'CASE'),
        (r'^IS\b', 'IS'),
        (r'^IF\b', 'IF'),
        (r'^THEN\b', 'THEN'),
        (r'^ELSE\b', 'ELSE'),
        (r'^ELSEIF\b', 'ELSEIF'),
        (r'^ENDIF\b', 'ENDIF'),
        (r'^END\s+IF\b', 'ENDIF'),
        (r'^WHILE\b', 'WHILE'),
        (r'^END\s+WHILE\b', 'END_WHILE'),
        (r'^WEND\b', 'WEND'),
        (r'^DO\b', 'DO'),
        (r'^LOOP\b', 'LOOP'),
        (r'^FOR\b', 'FOR'),
        (r'^TO\b', 'TO'),
        (r'^STEP\b', 'STEP'),
        (r'^NEXT\b', 'NEXT'),
        (r'^RETURN\b', 'RETURN'),
        # EXIT statements (order matters: specific before general)
        (r'^EXIT\s+FUNCTION\b', 'EXIT_FUNCTION'),
        (r'^EXIT\s+FOR\b', 'EXIT_FOR'),
        (r'^EXIT\s+WHILE\b', 'EXIT_WHILE'),
        (r'^AND\b', 'AND'),
        (r'^OR\b', 'OR'),
        (r'^NOT\b', 'NOT'),
        (r'^MOD\b', 'MOD'),
        (r'^&', 'CONCAT'),
        (r'^<=', 'LTE'),
        (r'^>=', 'GTE'),
        (r'^!=', 'NEQ'),  # C言語スタイルの不等号演算子
        (r'^<>', 'NEQ'),
        (r'^<', 'LT'),
        (r'^>', 'GT'),
        (r'^=', 'EQ'),
        (r'^\+', 'PLUS'),
        (r'^-', 'MINUS'),
        (r'^\*', 'MULTIPLY'),
        (r'^\\', 'INTDIV'),  # 整数除算（DIVIDEより先にマッチさせる）
        (r'^/', 'DIVIDE'),
        (r'^\^', 'POWER'),
        (r'^\(', 'LPAREN'),
        (r'^\)', 'RPAREN'),
        (r'^\[', 'LBRACKET'),  # 配列アクセス用の左括弧
        (r'^\]', 'RBRACKET'),  # 配列アクセス用の右括弧
        (r'^,', 'COMMA'),
        # ブールリテラル
        (r'^True\b', 'BOOL'),
        (r'^False\b', 'BOOL'),
        (r'^[0-9]+\.[0-9]+', 'FLOAT'),
        (r'^[0-9]+', 'INT'),
        (r'^[A-Za-z_][A-Za-z0-9_]*\[\]', 'ARRAY_VAR'),  # 配列変数参照（[]記法）
        (r'^[A-Za-z_][A-Za-z0-9_]*\(', 'FUNCTION'),  # 関数呼び出し
        (r'^[A-Za-z_][A-Za-z0-9_]*', 'IDENTIFIER'),  # 通常の識別子（配列アクセスは後で判定）
    ]

    def __init__(self, locale: str = 'ja'):
        self.locale = locale  # デフォルトで日本語
        self.tokens = []
        self.current = 0
        # バージョン情報をコンソールに出力
        print(f"[ScriptParser] Version: {PARSER_VERSION} (Build: {PARSER_BUILD_DATE})")

    def tokenize(self, script: str) -> List[Token]:
        """スクリプトをトークンに分解"""
        tokens = []
        lines = script.split('\n')

        for line_num, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            # コメント行はスキップ
            # VBAスタイルのコメント: ' の後にスペースがあるか、= が含まれない行の場合
            if line.startswith("'") and ('=' not in line or line.startswith("' ")):
                continue
            if line.upper().startswith("REM "):
                continue

            # インラインコメント処理: 文字列リテラル外の ' 以降を除去
            # 文字列リテラル内の ' は保護する必要がある
            processed_line = ""
            in_string = False
            escape_next = False
            i = 0

            while i < len(line):
                char = line[i]

                # エスケープ処理
                if escape_next:
                    processed_line += char
                    escape_next = False
                    i += 1
                    continue

                if char == '\\':
                    processed_line += char
                    escape_next = True
                    i += 1
                    continue

                # ダブルクォート処理
                if char == '"':
                    in_string = not in_string
                    processed_line += char
                    i += 1
                    continue

                # インラインコメント検出（文字列外のみ）
                if char == "'" and not in_string:
                    # ここから行末までコメント
                    break

                processed_line += char
                i += 1

            # 処理後の行が空になった場合はスキップ
            line = processed_line.strip()
            if not line:
                continue

            # この行の開始トークンインデックスを記録
            line_start_token_idx = len(tokens)

            pos = 0
            while pos < len(line):
                # 空白をスキップ
                while pos < len(line) and line[pos] in ' \t':
                    pos += 1
                if pos >= len(line):
                    break

                # トークンマッチング
                matched = False
                for pattern, token_type in self.TOKEN_PATTERNS:
                    regex = re.compile(pattern, re.IGNORECASE)
                    match = regex.match(line[pos:])
                    if match:
                        value = match.group(0)
                        # Raw文字列リテラルの場合、エスケープ処理を最小限にする
                        if token_type == 'RAW_STRING':
                            # グループ1が存在すれば（括弧でキャプチャされた部分）それを使用
                            original_value = match.group(0)
                            value = match.group(1) if match.groups() else value[2:-1]  # r"..." の r" と " を除去
                            # Raw文字列ではVBA式エスケープ（""）のみ処理
                            value = value.replace('""', '"')
                            print(f"[ScriptParser] RAW_STRING: '{original_value}' -> '{value}'")
                            # その他のエスケープシーケンス（\n, \t等）は処理しない
                        # 通常の文字列リテラルの場合、引用符を除去
                        elif token_type == 'STRING':
                            # グループ1が存在すれば（括弧でキャプチャされた部分）それを使用
                            original_value = match.group(0)
                            value = match.group(1) if match.groups() else value[1:-1]
                            print(f"[ScriptParser] STRING matched: '{original_value}' -> group(1)='{match.group(1) if match.groups() else 'N/A'}'")
                            # エスケープシーケンスを処理
                            # VBAでは "" はダブルクォート、その他の\はそのまま（正規表現用）
                            value = value.replace('""', '"')
                            print(f"[ScriptParser] STRING after VBA escape: '{value}'")
                            # 明示的なエスケープシーケンスのみ置換（日本語文字列の文字化け対策）
                            # unicode_escapeは日本語などマルチバイト文字で文字化けを引き起こすため使用しない
                            # CRITICAL: \\ を先に処理しないと、\\n や \\t が誤って変換される
                            value = value.replace('\\\\', '\x00')  # 一時的にヌル文字に置き換え
                            value = value.replace('\\n', '\n')
                            value = value.replace('\\t', '\t')
                            value = value.replace('\\r', '\r')
                            value = value.replace('\x00', '\\')
                        # 関数呼び出しの場合、名前と括弧を分離
                        elif token_type == 'FUNCTION':
                            value = value[:-1]  # 括弧を除去
                        # 配列変数参照の場合、名前と括弧を分離
                        elif token_type == 'ARRAY_VAR':
                            value = value[:-2]  # []を除去
                        # 配列アクセスの場合、名前と括弧を分離
                        elif token_type == 'ARRAY':
                            value = value[:-1]  # 括弧を除去
                        # 数値の場合、適切な型に変換
                        elif token_type == 'INT':
                            value = int(value)
                        elif token_type == 'FLOAT':
                            value = float(value)

                        tokens.append(Token(token_type, value, line_num))
                        pos += len(match.group(0))
                        matched = True
                        break

                if not matched:
                    # マッチしなかった文字に対してエラーを発生
                    char = line[pos]
                    if char not in ' \t\n\r':  # 空白文字以外で無効な文字
                        raise SyntaxError(get_message('error_invalid_char', self.locale, char, line_num, pos))
                    pos += 1

            # この行の最後のトークンに is_end_of_line=True を設定
            if len(tokens) > line_start_token_idx:
                tokens[-1].is_end_of_line = True

        return tokens

    def parse(self, script: str) -> List[ASTNode]:
        """スクリプトをパースしてASTを構築"""
        self.tokens = self.tokenize(script)
        self.current = 0
        statements = []

        while not self.is_at_end():
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)

        return statements

    def parse_statement(self) -> Optional[ASTNode]:
        """ステートメントをパース"""
        if self.is_at_end():
            return None

        # 🚨 予約語チェック（代入文として使おうとしている場合）
        # IF, FOR, STEP等の予約語を変数名として使うことを禁止
        RESERVED_KEYWORDS = [
            'IF', 'THEN', 'ELSE', 'ELSEIF', 'ENDIF', 'END',
            'FOR', 'TO', 'STEP', 'NEXT',
            'DIM', 'REDIM',
            'SELECT', 'CASE',
            'FUNCTION', 'SUB'
        ]
        
        if self.current < len(self.tokens):
            token = self.peek()
            # 次のトークンが '=' の場合、変数代入として使おうとしている
            if token.type in RESERVED_KEYWORDS:
                next_pos = self.current + 1
                if next_pos < len(self.tokens) and self.tokens[next_pos].type == 'EQ':
                    from locales import get_message
                    raise SyntaxError(get_message('error_reserved_keyword', self.locale, token.value))

        # FUNCTION定義
        if self.check('FUNCTION_DEF'):
            return self.parse_function_definition()

        # SELECT CASE文
        if self.check('SELECT_CASE'):
            return self.parse_select_case_statement()

        # IF文（IF関数ではない場合）
        if self.check('IF') and not self.peek_ahead('LPAREN'):
            return self.parse_if_statement()

        # WHILE文
        if self.check('WHILE'):
            return self.parse_while_statement()

        # FOR文
        if self.check('FOR'):
            return self.parse_for_statement()

        # DIM文
        if self.check('DIM'):
            return self.parse_dim_statement()

        # REDIM文
        if self.check('REDIM'):
            return self.parse_redim_statement()

        # ARRAY文
        if self.check('ARRAY_FUNC'):
            return self.parse_array_statement()

        # SPLIT文
        if self.check('SPLIT_FUNC'):
            return self.parse_split_statement()

        # EXIT文 (EXIT FUNCTION / EXIT FOR / EXIT WHILE)
        if self.check_any(['EXIT_FUNCTION', 'EXIT_FOR', 'EXIT_WHILE']):
            return self.parse_exit_statement()

        # 代入文または式文（RETURN変数への代入も含む）
        # RETURN文は後で判定
        return self.parse_assignment_or_expression()

    def parse_if_statement(self) -> ASTNode:
        """IF文をパース（ELSEIF対応、1行IF対応）"""
        self.consume('IF')
        condition = self.parse_expression()
        self.consume('THEN')

        # 1行IF判定: THENトークンが行末にある場合は複数行IF
        then_token_idx = self.current - 1  # THENトークンの位置
        is_multiline_if = (then_token_idx >= 0 and then_token_idx < len(self.tokens) and 
                          self.tokens[then_token_idx].is_end_of_line)

        if is_multiline_if:
            # 【既存ロジック】複数行IF（変更なし）
            then_statements = []
            elseif_branches = []
            else_statements = []

            # THEN部分のステートメント
            while not self.check('ELSE') and not self.check('ELSEIF') and not self.check('ENDIF') and not self.is_at_end():
                stmt = self.parse_statement()
                if stmt:
                    then_statements.append(stmt)

            # ELSEIF部分の処理
            while self.check('ELSEIF'):
                self.advance()  # ELSEIF を消費
                elseif_condition = self.parse_expression()
                self.consume('THEN')

                elseif_statements = []
                while not self.check('ELSE') and not self.check('ELSEIF') and not self.check('ENDIF') and not self.is_at_end():
                    stmt = self.parse_statement()
                    if stmt:
                        elseif_statements.append(stmt)

                elseif_branches.append((elseif_condition, elseif_statements))

            # ELSE部分
            if self.check('ELSE'):
                self.advance()
                while not self.check('ENDIF') and not self.is_at_end():
                    stmt = self.parse_statement()
                    if stmt:
                        else_statements.append(stmt)

            # END IF
            if not self.check('ENDIF'):
                raise SyntaxError(get_message('error_if_needs_endif', self.locale))
            self.consume('ENDIF')

            return ASTNode('IF', condition=condition, then_branch=then_statements,
                          elseif_branches=elseif_branches, else_branch=else_statements)
        else:
            # 【新規ロジック】1行IF（EXIT文限定）
            stmt = self.parse_statement()

            # EXIT文以外はエラー
            if stmt.type != 'EXIT':
                raise SyntaxError(get_message('error_one_line_if_exit_only', self.locale, 
                                             f"1行IF文ではEXIT文のみサポートされています（{stmt.type}は使用できません）"))

            return ASTNode('IF', condition=condition, 
                          then_branch=[stmt], 
                          elseif_branches=[], 
                          else_branch=[])

    def parse_while_statement(self) -> ASTNode:
        """WHILE文をパース (WEND または END WHILE で終了)"""
        self.consume('WHILE')
        condition = self.parse_expression()

        body = []
        while not self.check('WEND') and not self.check('END_WHILE') and not self.is_at_end():
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)

        # WEND または END WHILE を受け付ける
        if self.check('END_WHILE'):
            self.consume('END_WHILE')
        else:
            self.consume('WEND')

        return ASTNode('WHILE', condition=condition, body=body)

    def parse_for_statement(self) -> ASTNode:
        """FOR文をパース（簡易版）"""
        self.consume('FOR')
        variable = self.consume('IDENTIFIER').value
        self.consume('EQ')
        start = self.parse_expression()
        self.consume('TO')
        end = self.parse_expression()

        step = 1
        if self.check('STEP'):
            self.advance()
            step = self.parse_expression()

        body = []
        while not self.check('NEXT') and not self.is_at_end():
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)

        self.consume('NEXT')

        return ASTNode('FOR', variable=variable, start=start, end=end, step=step, body=body)

    def parse_dim_statement(self) -> ASTNode:
        """DIM文をパース: DIM array(size) または DIM array(size1, size2)"""
        self.consume('DIM')

        # 配列名 - FUNCTIONトークンもサポート（ARR(のような場合）
        if self.check('FUNCTION'):
            # FUNCTIONトークンから配列名を取得（最後の(を除く）
            array_name = self.peek().value
            self.advance()  # FUNCTIONトークンを消費
            # この時点でLPARENは既に消費されている（FUNCTIONトークンに含まれる）

            sizes = []
            # サイズをパース
            if not self.check('RPAREN'):
                sizes.append(self.parse_expression())

                # 複数次元の場合
                while self.check('COMMA'):
                    self.advance()
                    sizes.append(self.parse_expression())

            # )を期待
            if not self.check('RPAREN'):
                raise SyntaxError(get_message('error_dim_needs_paren', self.locale, self.peek().line))
            self.advance()

            return ASTNode('dim', array_name=array_name, sizes=sizes)

        elif self.check('IDENTIFIER'):
            array_name = self.peek().value
            self.advance()

            # (または[を期待
            if self.check('LPAREN'):
                self.advance()  # (
                sizes = []

                # サイズをパース
                sizes.append(self.parse_expression())

                # 複数次元の場合
                while self.check('COMMA'):
                    self.advance()
                    sizes.append(self.parse_expression())

                # )を期待
                if not self.check('RPAREN'):
                    raise SyntaxError(get_message('error_dim_needs_paren', self.locale, self.peek().line))
                self.advance()

                return ASTNode('dim', array_name=array_name, sizes=sizes)
            elif self.check('LBRACKET'):
                self.advance()  # [
                sizes = []

                # 空の配列宣言の場合 DIM arr[]
                if not self.check('RBRACKET'):
                    # サイズをパース
                    sizes.append(self.parse_expression())

                    # 複数次元の場合
                    while self.check('COMMA'):
                        self.advance()
                        sizes.append(self.parse_expression())

                # ]を期待
                if not self.check('RBRACKET'):
                    raise SyntaxError(get_message('error_dim_needs_bracket', self.locale, self.peek().line))
                self.advance()

                return ASTNode('dim', array_name=array_name, sizes=sizes)
            else:
                # DIM var のような単純な変数宣言
                return ASTNode('dim', array_name=array_name, sizes=[])

    def parse_redim_statement(self) -> ASTNode:
        """REDIM文をパース: REDIM array[size] または REDIM array(size)"""
        self.consume('REDIM')

        # 配列変数 - FUNCTIONトークンもサポート（ARR(のような場合）
        if self.check('FUNCTION'):
            # FUNCTIONトークンから配列名を取得
            array_name = self.peek().value
            self.advance()  # FUNCTIONトークンを消費

            sizes = []
            # サイズをパース
            if not self.check('RPAREN'):
                sizes.append(self.parse_expression())

                # 複数次元の場合
                while self.check('COMMA'):
                    self.advance()
                    sizes.append(self.parse_expression())

            # )を期待
            if not self.check('RPAREN'):
                raise SyntaxError(get_message('error_redim_needs_paren', self.locale, self.peek().line))
            self.advance()

            # 単一次元の場合のみREDIMをサポート（現在の実装）
            if len(sizes) == 1:
                return ASTNode('REDIM_STMT', array_name=array_name, size=sizes[0], preserve=None)
            else:
                # 多次元REDIMは未実装
                raise SyntaxError(get_message('error_redim_multidim', self.locale, self.peek().line))

        elif self.check('ARRAY_VAR'):
            array_name = self.advance().value
        elif self.check('IDENTIFIER'):
            array_name = self.advance().value
            # REDIM array[size] 形式をチェック
            if self.check('LBRACKET'):
                self.advance()  # '['
                size = self.parse_expression()
                self.consume('RBRACKET')  # ']'
                return ASTNode('REDIM_STMT', array_name=array_name, size=size, preserve=None)
        else:
            raise SyntaxError(get_message('error_redim_needs_name', self.locale))

        # REDIM array, size 形式（既存の形式）
        if self.check('COMMA'):
            self.consume('COMMA')
            size = self.parse_expression()

            # オプション: PRESERVE
            preserve = None
            if self.check('COMMA'):
                self.advance()
                preserve = self.parse_expression()

            return ASTNode('REDIM_STMT', array_name=array_name, size=size, preserve=preserve)
        else:
            raise SyntaxError(get_message('error_redim_invalid_syntax', self.locale))

    def parse_array_statement(self) -> ASTNode:
        """ARRAY文をパース"""
        self.consume('ARRAY_FUNC')

        # 配列変数
        if self.check('ARRAY_VAR'):
            array_name = self.advance().value
        elif self.check('IDENTIFIER'):
            array_name = self.advance().value
        else:
            raise SyntaxError(get_message('error_array_needs_name', self.locale))

        self.consume('COMMA')

        # 値のリスト
        values = []
        values.append(self.parse_expression())

        while self.check('COMMA'):
            self.advance()
            values.append(self.parse_expression())

        return ASTNode('ARRAY_STMT', array_name=array_name, values=values)

    def parse_split_statement(self) -> ASTNode:
        """SPLIT文をパース"""
        self.consume('SPLIT_FUNC')

        # 配列変数
        if self.check('ARRAY_VAR'):
            array_name = self.advance().value
        elif self.check('IDENTIFIER'):
            array_name = self.advance().value
        else:
            raise SyntaxError(get_message('error_split_needs_name', self.locale))

        self.consume('COMMA')

        # テキスト
        text = self.parse_expression()

        self.consume('COMMA')

        # 区切り文字
        delimiter = self.parse_expression()

        return ASTNode('SPLIT_STMT', array_name=array_name, text=text, delimiter=delimiter)

    def parse_return_statement(self) -> ASTNode:
        """RETURN文をパース"""
        self.consume('RETURN')

        # RETURN値がある場合
        if not self.is_at_end() and not self.check_newline():
            value = self.parse_expression()
            return ASTNode('RETURN', value=value)
        else:
            # 単純なRETURN（値なし）
            return ASTNode('RETURN', value=None)

    def parse_exit_statement(self) -> ASTNode:
        """EXIT文をパース (EXIT FUNCTION / EXIT FOR / EXIT WHILE)"""
        # Consume EXIT_FUNCTION / EXIT_FOR / EXIT_WHILE token
        if self.check('EXIT_FUNCTION'):
            self.consume('EXIT_FUNCTION')
            return ASTNode('EXIT', exit_type='FUNCTION')
        elif self.check('EXIT_FOR'):
            self.consume('EXIT_FOR')
            return ASTNode('EXIT', exit_type='FOR')
        elif self.check('EXIT_WHILE'):
            self.consume('EXIT_WHILE')
            return ASTNode('EXIT', exit_type='WHILE')
        else:
            raise SyntaxError(f"Unexpected EXIT statement at position {self.current}")

    def check_newline(self) -> bool:
        """改行をチェック（簡易実装）"""
        # 現在のトークンが新しい文の開始である可能性が高いキーワードかチェック
        return (self.is_at_end() or
                self.check('IF') or self.check('FOR') or self.check('WHILE') or
                self.check('FUNCTION_DEF') or self.check('END_FUNCTION') or
                self.check('REDIM') or self.check('ARRAY_FUNC') or self.check('SPLIT_FUNC') or
                self.check('ENDIF') or self.check('NEXT') or self.check('WEND'))

    def parse_select_case_statement(self) -> ASTNode:
        """SELECT CASE文をパース"""
        self.consume('SELECT_CASE')
        test_expression = self.parse_expression()

        cases = []
        else_case = None

        while not self.check('END_SELECT') and not self.is_at_end():
            if self.check('CASE_ELSE'):
                # Case Else節
                self.advance()
                else_statements = []
                while not self.check('END_SELECT') and not self.check('CASE') and not self.is_at_end():
                    stmt = self.parse_statement()
                    if stmt:
                        else_statements.append(stmt)
                else_case = else_statements
            elif self.check('CASE'):
                # Case節
                self.advance()
                conditions = self.parse_case_conditions()
                statements = []
                while not self.check('CASE') and not self.check('CASE_ELSE') and not self.check('END_SELECT') and not self.is_at_end():
                    stmt = self.parse_statement()
                    if stmt:
                        statements.append(stmt)
                cases.append(ASTNode('CASE', conditions=conditions, statements=statements))
            else:
                # 予期しないトークンはスキップ
                self.advance()

        self.consume('END_SELECT')
        return ASTNode('SELECT_CASE', test_expression=test_expression, cases=cases, else_case=else_case)

    def parse_case_conditions(self) -> List[ASTNode]:
        """Case条件リストをパース（カンマ区切り）"""
        conditions = []
        conditions.append(self.parse_case_condition())

        while self.check('COMMA'):
            self.advance()
            conditions.append(self.parse_case_condition())

        return conditions

    def parse_case_condition(self) -> ASTNode:
        """個別のCase条件をパース"""
        # IS演算子による比較
        if self.check('IS'):
            self.advance()
            # 比較演算子を取得
            if self.check_any(['LT', 'GT', 'LTE', 'GTE', 'EQ', 'NEQ']):
                operator = self.advance().type
                value = self.parse_expression()
                return ASTNode('CASE_IS', operator=operator, value=value)
            else:
                # ISの後に比較演算子がない場合は、式として扱う
                return self.parse_expression()

        # 最初の式を取得
        expr1 = self.parse_expression()

        # TO演算子による範囲指定
        if self.check('TO'):
            self.advance()
            expr2 = self.parse_expression()
            return ASTNode('CASE_RANGE', start=expr1, end=expr2)

        # 単一値
        return ASTNode('CASE_VALUE', value=expr1)

    def parse_function_definition(self) -> ASTNode:
        """FUNCTION文をパース"""
        self.consume('FUNCTION_DEF')

        # 関数名はIDENTIFIERまたはFUNCTIONトークンの場合がある
        if self.check('FUNCTION'):
            # FUNCTIONトークンとして認識された場合（関数名の後に括弧が続く）
            func_name = self.advance().value
            self.consume('LPAREN')
        else:
            # 通常のIDENTIFIERの場合
            func_name = self.consume('IDENTIFIER').value
            self.consume('LPAREN')

        # パラメータリストのパース
        parameters = []
        if not self.check('RPAREN'):
            # 最初のパラメータ
            param = self.parse_parameter()
            parameters.append(param)

            # 追加のパラメータ
            while self.check('COMMA'):
                self.advance()
                param = self.parse_parameter()
                parameters.append(param)

        self.consume('RPAREN')

        # 戻り値型（オプション - 現時点では無視）
        return_type = None
        if self.check('AS'):
            self.advance()
            return_type = self.consume('IDENTIFIER').value

        # 関数本体
        body = []
        while not self.check('END_FUNCTION') and not self.is_at_end():
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)

        self.consume('END_FUNCTION')

        return ASTNode('FUNCTION_DEF',
                       name=func_name,
                       parameters=parameters,
                       body=body,
                       return_type=return_type)

    def parse_parameter(self) -> ASTNode:
        """パラメータをパース"""
        # Optional修飾子
        optional = False
        if self.check('OPTIONAL'):
            self.advance()
            optional = True

        # ByVal/ByRef修飾子（デフォルトはByVal）
        by_ref = False
        if self.check('BYVAL'):
            self.advance()
            by_ref = False
        elif self.check('BYREF'):
            self.advance()
            by_ref = True

        # パラメータ名
        param_name = self.consume('IDENTIFIER').value

        # 型（オプション）
        param_type = None
        if self.check('AS'):
            self.advance()
            param_type = self.consume('IDENTIFIER').value

        # デフォルト値（Optionalの場合）
        default_value = None
        if optional and self.check('EQ'):
            self.advance()
            default_value = self.parse_expression()

        return ASTNode('PARAMETER',
                       name=param_name,
                       by_ref=by_ref,
                       optional=optional,
                       default_value=default_value,
                       param_type=param_type)

    def parse_assignment_or_expression(self) -> ASTNode:
        """代入文または式文をパース"""
        # 配列変数参照の場合 (ITEMS[]記法)
        if self.check('ARRAY_VAR'):
            array_name = self.advance().value
            return ASTNode('ARRAY_VAR', name=array_name)

        # 配列アクセスの場合 ([]記法)
        elif self.check('ARRAY'):
            array_name = self.advance().value
            self.consume('LBRACKET')
            index = self.parse_expression()
            self.consume('RBRACKET')

            if self.check('EQ'):
                self.advance()
                value = self.parse_expression()
                return ASTNode('ASSIGN_ARRAY', array=array_name, index=index, value=value)
            else:
                return ASTNode('ARRAY_ACCESS', array=array_name, index=index)

        # RETURN文または変数（RETURNトークンの場合）
        elif self.check('RETURN'):
            # 次のトークンが'='かチェック
            saved_pos = self.current
            self.advance()  # RETURN を読み飛ばす
            if self.check('EQ'):
                # RETURN = value の代入文
                self.current = saved_pos  # 位置を戻す
                var_name = self.advance().value  # 'RETURN'
                self.advance()  # '='
                value = self.parse_expression()
                return ASTNode('ASSIGN', variable=var_name, value=value)
            else:
                # RETURN文（値あり/なし）
                self.current = saved_pos  # 位置を戻す
                return self.parse_return_statement()

        # 関数呼び出しまたは変数の場合
        elif self.check('IDENTIFIER') or self.check('FUNCTION'):
            token = self.peek()

            if self.check('FUNCTION'):
                # 関数呼び出し - または配列アクセス/代入
                func_name = self.advance().value
                # FUNCTIONトークンはLPARENを含まないので、明示的に消費する必要はない

                # 引数を取得
                args = []
                if not self.check('RPAREN'):
                    args.append(self.parse_expression())
                    while self.check('COMMA'):
                        self.advance()
                        args.append(self.parse_expression())

                self.consume('RPAREN')

                # 配列代入かどうかチェック（ARR(1) = value または MATRIX(1,1) = valueの形）
                if self.check('EQ'):
                    # 配列への代入として処理
                    self.advance()  # '='を消費
                    value = self.parse_expression()
                    if len(args) == 1:
                        # 1次元配列への代入
                        return ASTNode('ASSIGN_ARRAY', array=func_name, index=args[0], value=value)
                    else:
                        # 多次元配列への代入
                        return ASTNode('ASSIGN_ARRAY_MULTI', array=func_name, indices=args, value=value)
                else:
                    # 関数呼び出し
                    return ASTNode('FUNCTION_CALL', name=func_name, arguments=args)
            else:
                # 通常の変数または配列アクセス
                var_name = self.advance().value

                # IDENTIFIERの後に(が続く場合、ビルトイン関数かチェック
                if self.check('LPAREN'):
                    from builtin_functions import is_builtin_function
                    if is_builtin_function(var_name):
                        # ビルトイン関数として処理
                        print(get_message('warning_space_before_paren', self.locale, var_name))
                        print(get_message('suggestion_no_space', self.locale, var_name))
                        self.consume('LPAREN')

                        # 引数を取得
                        args = []
                        if not self.check('RPAREN'):
                            args.append(self.parse_expression())
                            while self.check('COMMA'):
                                self.advance()
                                args.append(self.parse_expression())

                        self.consume('RPAREN')
                        return ASTNode('FUNCTION_CALL', name=var_name.upper(), arguments=args)
                    else:
                        # 未定義の関数
                        raise SyntaxError(get_message('error_function_not_defined', self.locale, var_name))
                # 配列アクセスの場合
                elif self.check('LBRACKET'):
                    self.advance()  # '['
                    index = self.parse_expression()
                    self.consume('RBRACKET')  # ']'

                    if self.check('EQ'):
                        # 配列代入
                        self.advance()  # '='
                        value = self.parse_expression()
                        return ASTNode('ASSIGN_ARRAY', array=var_name, index=index, value=value)
                    else:
                        # 配列参照
                        return ASTNode('ARRAY_ACCESS', array=var_name, index=index)
                elif self.check('EQ'):
                    # 通常の変数代入
                    self.advance()
                    value = self.parse_expression()
                    return ASTNode('ASSIGN', variable=var_name, value=value)
                else:
                    # 変数参照
                    return ASTNode('VARIABLE', name=var_name)

        # その他の式
        return self.parse_expression()

    def parse_expression(self) -> ASTNode:
        """式をパース（論理演算）"""
        return self.parse_or()

    def parse_or(self) -> ASTNode:
        """OR演算をパース"""
        left = self.parse_and()

        while self.check('OR'):
            op = self.advance().type
            right = self.parse_and()
            left = ASTNode('BINARY_OP', operator=op, left=left, right=right)

        return left

    def parse_and(self) -> ASTNode:
        """AND演算をパース"""
        left = self.parse_not()

        while self.check('AND'):
            op = self.advance().type
            right = self.parse_not()
            left = ASTNode('BINARY_OP', operator=op, left=left, right=right)

        return left

    def parse_not(self) -> ASTNode:
        """NOT演算をパース"""
        if self.check('NOT'):
            self.advance()
            expr = self.parse_not()
            return ASTNode('UNARY_OP', operator='NOT', operand=expr)

        return self.parse_comparison()

    def parse_comparison(self) -> ASTNode:
        """比較演算をパース"""
        left = self.parse_concatenation()

        while self.check_any(['LT', 'GT', 'LTE', 'GTE', 'EQ', 'NEQ']):
            op = self.advance().type
            right = self.parse_concatenation()
            left = ASTNode('BINARY_OP', operator=op, left=left, right=right)

        return left

    def parse_concatenation(self) -> ASTNode:
        """文字列連結をパース"""
        left = self.parse_addition()

        while self.check('CONCAT'):
            op = self.advance().type
            right = self.parse_addition()
            left = ASTNode('BINARY_OP', operator=op, left=left, right=right)

        return left

    def parse_addition(self) -> ASTNode:
        """加減算をパース"""
        left = self.parse_multiplication()

        while self.check_any(['PLUS', 'MINUS']):
            op = self.advance().type
            right = self.parse_multiplication()
            left = ASTNode('BINARY_OP', operator=op, left=left, right=right)

        return left

    def parse_multiplication(self) -> ASTNode:
        """乗除算をパース"""
        left = self.parse_power()

        while self.check_any(['MULTIPLY', 'DIVIDE', 'MOD', 'INTDIV']):
            op = self.advance().type
            right = self.parse_power()
            left = ASTNode('BINARY_OP', operator=op, left=left, right=right)

        return left

    def parse_power(self) -> ASTNode:
        """べき乗をパース"""
        left = self.parse_unary()

        if self.check('POWER'):
            op = self.advance().type
            right = self.parse_power()  # 右結合
            return ASTNode('BINARY_OP', operator=op, left=left, right=right)

        return left

    def parse_unary(self) -> ASTNode:
        """単項演算をパース"""
        if self.check_any(['MINUS', 'PLUS']):
            op = self.advance().type
            expr = self.parse_unary()
            return ASTNode('UNARY_OP', operator=op, operand=expr)

        return self.parse_primary()

    def parse_primary(self) -> ASTNode:
        """基本要素をパース"""
        # 括弧
        if self.check('LPAREN'):
            self.advance()
            expr = self.parse_expression()
            self.consume('RPAREN')
            return expr

        # SPLIT関数呼び出し
        if self.check('SPLIT_FUNC'):
            self.advance()  # SPLIT_FUNC
            self.consume('LPAREN')

            # 引数を取得
            args = []
            if not self.check('RPAREN'):
                args.append(self.parse_expression())
                while self.check('COMMA'):
                    self.advance()
                    args.append(self.parse_expression())

            self.consume('RPAREN')
            return ASTNode('FUNCTION_CALL', name='SPLIT', arguments=args)

        # 配列変数参照 (ITEMS[]記法)
        if self.check('ARRAY_VAR'):
            array_name = self.advance().value
            return ASTNode('ARRAY_VAR', name=array_name)

        # 配列アクセス ([]記法)
        elif self.check('ARRAY'):
            array_name = self.advance().value
            self.consume('LBRACKET')
            index = self.parse_expression()
            self.consume('RBRACKET')
            return ASTNode('ARRAY_ACCESS', array=array_name, index=index)

        # IF関数呼び出し（IF文と区別するため特別扱い）
        if self.check('IF'):
            saved_pos = self.current
            func_name = self.advance().value

            if self.check('LPAREN'):
                # IF関数として処理
                self.consume('LPAREN')

                # 引数を取得
                args = []
                if not self.check('RPAREN'):
                    args.append(self.parse_expression())
                    while self.check('COMMA'):
                        self.advance()
                        args.append(self.parse_expression())

                self.consume('RPAREN')
                return ASTNode('FUNCTION_CALL', name=func_name.upper(), arguments=args)
            else:
                # IF文として処理するため位置を戻す
                self.current = saved_pos
                # IFはIF文として他の場所で処理されるため、ここでは処理しない

        # 関数呼び出し
        if self.check('FUNCTION'):
            func_name = self.advance().value
            self.consume('LPAREN')

            # 引数を取得
            args = []
            if not self.check('RPAREN'):
                args.append(self.parse_expression())
                while self.check('COMMA'):
                    self.advance()
                    args.append(self.parse_expression())

            self.consume('RPAREN')

            # 関数呼び出し
            return ASTNode('FUNCTION_CALL', name=func_name, arguments=args)

        # IDENTIFIERの後に(が続く場合（空白がある関数呼び出し）
        if self.check('IDENTIFIER'):
            saved_pos = self.current
            name = self.advance().value

            if self.check('LPAREN'):
                from builtin_functions import is_builtin_function
                if is_builtin_function(name):
                    # ビルトイン関数として処理
                    print(get_message('warning_space_before_paren', self.locale, name))
                    print(get_message('suggestion_no_space', self.locale, name))
                    self.consume('LPAREN')

                    # 引数を取得
                    args = []
                    if not self.check('RPAREN'):
                        args.append(self.parse_expression())
                        while self.check('COMMA'):
                            self.advance()
                            args.append(self.parse_expression())

                    self.consume('RPAREN')
                    return ASTNode('FUNCTION_CALL', name=name.upper(), arguments=args)
                else:
                    # ユーザー定義関数または未定義関数として処理
                    # ユーザーフレンドリーな警告を表示
                    print(get_message('warning_space_before_paren', self.locale, name))
                    print(get_message('suggestion_no_space', self.locale, name))
                    self.consume('LPAREN')

                    # 引数を取得
                    args = []
                    if not self.check('RPAREN'):
                        args.append(self.parse_expression())
                        while self.check('COMMA'):
                            self.advance()
                            args.append(self.parse_expression())

                    self.consume('RPAREN')
                    return ASTNode('FUNCTION_CALL', name=name, arguments=args)
            else:
                # 変数として処理
                self.current = saved_pos
                # パースを続ける

        # ARRAY関数呼び出し
        if self.check('ARRAY_FUNC'):
            func_name = self.advance().value
            self.consume('LPAREN')

            # 引数を取得
            args = []
            if not self.check('RPAREN'):
                args.append(self.parse_expression())
                while self.check('COMMA'):
                    self.advance()
                    args.append(self.parse_expression())

            self.consume('RPAREN')

            # ARRAY関数呼び出し
            return ASTNode('FUNCTION_CALL', name=func_name, arguments=args)

        # RETURNを変数として扱う特別処理
        # PRINT(RETURN) のような式内でRETURNを変数として参照できるようにする
        if self.check('RETURN'):
            # 次が'='でなければ変数参照として扱う
            saved_pos = self.current
            self.advance()  # RETURN を読む
            if not self.check('EQ'):  # '=' でない場合
                # RETURNを変数として扱う
                return ASTNode('VARIABLE', name='RETURN')
            else:
                # RETURN = の場合は元に戻して通常処理へ
                self.current = saved_pos
                # このケースは parse_assignment_or_expression で処理される

        # 変数または配列アクセス
        if self.check('IDENTIFIER'):
            var_name = self.advance().value

            # 配列アクセスかチェック
            if self.check('LBRACKET'):
                self.advance()  # '['
                index = self.parse_expression()
                self.consume('RBRACKET')  # ']'
                return ASTNode('ARRAY_ACCESS', array=var_name, index=index)
            else:
                return ASTNode('VARIABLE', name=var_name)

        # 文字列（通常文字列とRaw文字列の両方）
        if self.check('STRING') or self.check('RAW_STRING'):
            return ASTNode('LITERAL', value=self.advance().value, datatype='STRING')

        # 数値
        if self.check('INT'):
            val = self.advance().value
            return ASTNode('LITERAL', value=float(val), datatype='NUMBER')

        if self.check('FLOAT'):
            val = self.advance().value
            return ASTNode('LITERAL', value=float(val), datatype='NUMBER')

        # ブール値
        if self.check('BOOL'):
            val = self.advance().value
            bool_val = val.upper() == 'TRUE'
            return ASTNode('LITERAL', value=bool_val, datatype='BOOL')

        # エラー：予期しないトークン
        if not self.is_at_end():
            self.advance()  # スキップ

        return ASTNode('LITERAL', value=0, datatype='NUMBER')

    # ヘルパーメソッド
    def check(self, type_: str) -> bool:
        """現在のトークンが指定された型かチェック"""
        if self.is_at_end():
            return False
        return self.peek().type == type_

    def check_any(self, types: List[str]) -> bool:
        """現在のトークンが指定された型のいずれかかチェック"""
        return any(self.check(t) for t in types)

    def peek_ahead(self, token_type: str) -> bool:
        """次のトークン（現在の1つ先）が指定のタイプかチェック"""
        if self.current + 1 >= len(self.tokens):
            return False
        return self.tokens[self.current + 1].type == token_type

    def advance(self) -> Token:
        """次のトークンに進む"""
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        """トークンリストの末尾かチェック"""
        return self.current >= len(self.tokens)

    def peek(self) -> Token:
        """現在のトークンを返す"""
        if self.is_at_end():
            return Token('EOF', None)
        return self.tokens[self.current]

    def previous(self) -> Token:
        """前のトークンを返す"""
        return self.tokens[self.current - 1]

    def consume(self, type_: str) -> Token:
        """指定された型のトークンを消費"""
        if self.check(type_):
            return self.advance()
        # エラー処理（簡易版）
        return Token(type_, None)