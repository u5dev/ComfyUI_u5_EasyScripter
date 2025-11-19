# 更新履歴 (CHANGELOG)

u5 EasyScripterの主要なバージョン更新履歴です。

---

## 📝 更新履歴


### v3.1.2 (2025-11-18) - ドキュメント体裁修正

#### Fixed
- **関数数クロスリファレンス修正**: docs/02_builtin_functions/00_index.mdの関数数を実際の実装数に合わせて修正
  - 数学関数: 24個 → 16個
  - CSV関数: 11個 → 9個
  - 配列関数: 7個 → 3個
  - モデル関数: 3個 → 1個
  - ユーティリティ関数: 21個 → 18個
  - ループ制御関数: 9個 → 1個
  - HTTP通信関数: 17個 → 9個
  - Python関数実行: 3個 → 4個
- **クイックリファレンステーブル修正**: 00_index.mdのクイックリファレンステーブルを修正
  - 数学関数テーブルから存在しない8関数（RND, RANDOMIZE, FIX, SGN, ASIN, ACOS, ATAN, ATAN2）を削除
  - CSVDIFF関数の引数を修正: CSVDIFF(csv1, csv2) → CSVDIFF(array_name, csv1, csv2)
  - PYDECODE関数をPython関数テーブルに追加
- **文字列関数数修正**: docs/02_builtin_functions/02_string_functions.mdの関数数を29個→28個に修正
- **目次アンカーリンク修正**: docs/01_syntax_reference.mdの目次アンカーリンクから冒頭のハイフンを削除（GitHubマークダウン仕様に準拠）

### v3.1.1 (2025-11-17) - 文字列関数ドキュメント追加

#### Added
- **文字列関数ドキュメント追加**: 7個の実装済み文字列関数のドキュメントを追加
  - **ESCAPEPATHSTR(path, [replacement])**: ファイルパスの禁則文字を置換または削除
  - **URLENCODE(text, [encoding])**: URLエンコード（パーセントエンコーディング）
  - **URLDECODE(text, [encoding])**: URLデコード
  - **PROPER(text)**: タイトルケースに変換（各単語の先頭を大文字化）
  - **CHR(code)**: 文字コード→文字変換（ASCII範囲）
  - **ASC(char)**: 文字→文字コード変換
  - **STR(value)**: 数値→文字列変換
  - ドキュメント: docs/02_builtin_functions/02_string_functions.md
  - 関数カウント: 21個 → 23個に修正

#### Changed
- **ビルトイン関数総数**: 135エントリ → 137エントリに更新
  - 135ユニーク関数（133関数 + 2エイリアス）
  - README.md、docs/02_builtin_functions/00_index.md を更新

### v3.1.0 (2025-11-17) - != 演算子サポート

#### Added
- **!= 演算子**: C言語スタイルの不等号演算子を追加
  - `<>` 演算子と完全に同じ動作（どちらも使用可能）
  - 実装: script_parser.py (TOKEN_PATTERNS配列に追加)
  - テスト: tests/test_neq_operator.py
  - ドキュメント: docs/01_syntax_reference.md

### v3.0.0 (2025-11-13) - Any_input入力ソケット関連強化ほか

### Added
- **IMAGETOBASE64関数**: IMAGE tensorまたは画像ファイルパスをBase64エンコード（またはdata URL形式）に変換する関数を追加
  - OpenAI等のVision API送信用データ生成に対応
  - IMAGE tensor（ComfyUIノード接続）およびファイルパス入力の両方に対応
  - リサイズ、JPEG圧縮（quality=85）、RGBA→RGB変換、Base64/data URL返却の機能を提供
  - 実装: functions/misc_functions.py (MiscFunctions.IMAGETOBASE64)
  - ドキュメント: docs/02_builtin_functions/09_utility_functions.md

- **IMAGETOBYTEARRAY関数**: IMAGE tensorまたは画像ファイルパスをJSON配列（またはバイト配列）に変換する関数を追加
  - Cloudflare Workers AI等のREST API送信用データ生成に対応
  - IMAGE tensor（ComfyUIノード接続）およびファイルパス入力の両方に対応
  - リサイズ、JPEG圧縮、RGBA→RGB変換、JSON配列/bytes型返却の機能を提供
  - 実装: functions/misc_functions.py (MiscFunctions.IMAGETOBYTEARRAY)
  - ドキュメント: docs/02_builtin_functions/09_utility_functions.md
- **FORMAT関数**: 数値・日時を指定フォーマットで整形する関数を追加（VBA互換）
  - VBA形式（"0", "0.0", "0.00", "#.##"）、Python format形式、日時strftime形式に対応
  - 実装: functions/misc_functions.py (MiscFunctions.FORMAT)
  - ドキュメント: docs/02_builtin_functions/07_type_functions.md

- **GETANYTYPE関数**: ANY型データの型名を判定する関数を追加
  - 基本型（int, float, string）、ComfyUI型（image, latent, model, vae, clip等）を判定
  - any_input入力ソケットから自動取得、または明示的にデータ指定可能
  - 実装: functions/misc_functions.py (MiscFunctions.GETANYTYPE)
  - ドキュメント: docs/02_builtin_functions/09_utility_functions.md

- **GETANYVALUEINT関数**: ANY型データから整数値を取得する関数を追加
  - any_input入力ソケットから自動取得、または明示的にデータ指定可能
  - 取得できない場合は0を返す
  - 実装: functions/misc_functions.py (MiscFunctions.GETANYVALUEINT)
  - ドキュメント: docs/02_builtin_functions/09_utility_functions.md

- **GETANYVALUEFLOAT関数**: ANY型データから浮動小数点値を取得する関数を追加
  - any_input入力ソケットから自動取得、または明示的にデータ指定可能
  - 取得できない場合は0.0を返す
  - 実装: functions/misc_functions.py (MiscFunctions.GETANYVALUEFLOAT)
  - ドキュメント: docs/02_builtin_functions/09_utility_functions.md

- **GETANYSTRING関数**: ANY型データから文字列を取得する関数を追加
  - any_input入力ソケットから自動取得、または明示的にデータ指定可能
  - 取得できない場合は空文字列を返す
  - 実装: functions/misc_functions.py (MiscFunctions.GETANYSTRING)
  - ドキュメント: docs/02_builtin_functions/09_utility_functions.md

- **GETANYWIDTH関数**: IMAGE/LATENT型データの幅（ピクセル数）を取得する関数を追加
  - any_input入力ソケットから自動取得、または明示的にデータ指定可能
  - IMAGE型・LATENT型の両方に対応
  - 実装: functions/misc_functions.py (MiscFunctions.GETANYWIDTH)

- **GETANYHEIGHT関数**: IMAGE/LATENT型データの高さ（ピクセル数）を取得する関数を追加
  - any_input入力ソケットから自動取得、または明示的にデータ指定可能
  - IMAGE型・LATENT型の両方に対応
  - 実装: functions/misc_functions.py (MiscFunctions.GETANYHEIGHT)

### Changed
- **LOOPSUBGRAPH順次実行保証**: イテレーションが並列実行ではなく順次実行されるようになりました
  - 各イテレーションは前イテレーションの完了を待機
  - NOW(), RND(), PRINT()等の関数が各イテレーションで再評価されることを保証
  - 内部実装: `_iteration_dependency`ダミー入力による依存関係チェーン（EasyScripterノードのみ）
  - 後方互換性: 既存ワークフロー影響なし（optional input）
  - パフォーマンス影響: 実行時間がイテレーション数に比例して増加
  - 実装: scripter_node.py (_duplicate_subgraph_iteration, _build_loop_subgraph, INPUT_TYPES, _execute_script_impl)

### Fixed
- **LOOPSUBGRAPH反復回数バグ修正**: 指定回数より1回少なく実行されるバグを修正
  - 問題: `LOOPSUBGRAPH(5)`が4回しか実行されていなかった
  - 原因: `range(1, total_count)`が誤って使用されていた（range(1,5)=[1,2,3,4]）
  - 修正: `range(total_count)`に変更（range(5)=[0,1,2,3,4]）
  - 実装: scripter_node.py L645

- **LOOPSUBGRAPH依存関係追加ロジック修正**: 標準ComfyUIノードへの誤った依存関係追加を修正
  - 問題: `TypeError: Int.execute() got an unexpected keyword argument '_iteration_dependency'`
  - 原因: PrimitiveInt等の標準ComfyUIノードに`_iteration_dependency`入力を追加していた
  - 修正: EasyScripterノード（`class_type=="comfyUI_u5_easyscripter"`）にのみ依存関係を追加
  - 実装: scripter_node.py L542-549

- **execute_scriptメソッドシグネチャ修正**: `_iteration_dependency`引数欠落バグを修正
  - 問題: `TypeError: ComfyUI_u5_EasyScripterNode.execute_script() got an unexpected keyword argument '_iteration_dependency'`
  - 原因: 公開メソッド`execute_script`に`_iteration_dependency`引数を追加し忘れ（内部メソッド`_execute_script_impl`にのみ追加）
  - 修正: `execute_script`シグネチャに`_iteration_dependency=None`を追加、`enqueue_and_wait`呼び出しで引数を渡す
  - 実装: scripter_node.py L89-92, L140

- **LOOPSUBGRAPHオリジナルノード削除不備**: 指定回数より1回多く実行されるバグを修正
  - 問題: `LOOPSUBGRAPH(5)`が6回実行される（オリジナルノード + 複製5回）
  - 原因: expandで複製ノードを追加するが、オリジナルのサブグラフノードが削除されていなかった
  - 症状: 後段のノードで過去のタイムスタンプ（前回実行のキャッシュ）が出力される
  - 修正: `remove`キーでオリジナルノードIDを明示的に削除
  - 実装: scripter_node.py L621, L643-645, L683

- **LOOPSUBGRAPH順次実行バグ修正**: イテレーション間で同じタイムスタンプで実行されるバグを修正
  - 問題: `LOOPSUBGRAPH(5)`で複数イテレーションが同じ秒に実行される（2個目と3個目等）
  - 原因:
    - `_duplicate_subgraph_iteration`が単に最後に処理したノードIDを返していた
    - 実際のグラフ構造上の最終ノード（tail）を返していなかった
    - 結果、次イテレーションの依存関係が正しく設定されず並列実行された
  - 修正:
    - オリジナルサブグラフの最終ノード（tail）を検出する`_find_subgraph_tail_node`メソッドを追加
    - `_duplicate_subgraph_iteration`に`original_tail_node_id`引数を追加
    - オリジナルtailに基づいて複製版のtailを正確に計算（`{original_tail}_loop_{iteration}`）
    - iteration 1からtotal_countまでの複製のみ作成、オリジナルノードを1回目として保持
  - 結果: オリジナル（1回目）→ 複製4回（2-5回目）が完全に順次実行される
  - 実装: scripter_node.py L565-617（`_find_subgraph_tail_node`追加）, L455,466,555-563（`_duplicate_subgraph_iteration`修正）, L708-710,729（オリジナルtail検出と引数渡し）

- **CDATE関数**: 日付文字列を日付型に変換する関数を追加（VBA互換）
  - 柔軟なフォーマット対応:
    - 完全な日時: `"2025/11/05 15:39:49"` → `2025/11/05 15:39:49`
    - 日付のみ: `"2025/11/05"` → `2025/11/05 00:00:00`
    - 年月のみ: `"2025/11"` → `2025/11/01 00:00:00`
    - 年のみ: `"2025"` → `2025/01/01 00:00:00`
    - 時刻の部分補完も対応
  - 区切り文字の柔軟性: `/`, `-`, `:`, 空白の混在を許容
  - 実装ファイル: `functions/date_functions.py`
  - ドキュメント: `docs/02_builtin_functions/03_datetime_functions.md`に詳細追加
  - ビルトイン関数総数: 日時関数 14 → 15個

### v2.9.0 (2025-10-29) - 製品名表記統一と多言語対応強化


- **多言語対応の完全実装**: 全システムメッセージを多言語対応
  - 対応言語: 日本語、英語
  - locales.pyに121個のメッセージキー追加（既存57個 + 新規64個）
  - ハードコードされた日本語メッセージを全て除去
  - 対象モジュール:
    - scripter_node.py: 全27箇所のハードコード日本語を多言語化
    - script_execution_queue.py: 全16箇所のハードコード日本語を多言語化
    - functions/loop_functions.py: 全8箇所のハードコード日本語を多言語化
    - functions/misc_functions.py: 全13箇所のハードコード日本語を多言語化（OUTPUT/INPUT/ISFILEEXIST関数）
  - locale引数を全モジュールで統一的に伝播:
    - scripter_node → script_execution_queue
    - scripter_node → script_engine → loop_functions
    - scripter_node → script_engine → misc_functions
  - ComfyUIのコンソール出力も完全に多言語対応
  - テスト: 全34テストケース成功（tests/test_scripter_node_localization.py）


- **SLEEP関数**: 処理を一時停止するユーティリティ関数を追加
  - 機能: 指定したミリ秒だけ処理を一時停止（スリープ）
  - パラメータ: `milliseconds`（float、オプション、デフォルト: 10ms）
  - 戻り値: なし（内部的には0.0を返す）
  - 主な用途:
    - WHILE()ループの速度制御（CPU使用率低減）
    - 処理待ち合わせ
    - デバッグ用の一時停止
  - ComfyUI統合:
    - ComfyUIのスレッドベースキューイング制御（ScriptExecutionQueue）と協調動作
    - time.sleep()による同期的ブロッキング実行
    - 複数EasyScripterノード同時実行時の安全性はScriptExecutionQueueが保証
  - 実装ファイル: `functions/misc_functions.py`（VRAMFREE関数の後）
  - テスト: 全10テストケース成功（tests/test_sleep_function.py）
  - ドキュメント: `docs/02_builtin_functions/09_utility_functions.md`に詳細追加
  - ビルトイン関数総数: 133 → 134エントリ（132ユニーク関数、2エイリアス含む）

- **VRAMFREE関数**: VRAMとRAMを解放するユーティリティ関数を追加
  - 機能: モデルアンロード、キャッシュクリア、ガベージコレクションを実行
  - パラメータ: `min_free_vram_gb`（float、オプション）で実行閾値を指定可能
  - 戻り値: dict形式で実行結果の詳細情報を返却
    - `success`: 実行成功フラグ（bool）
    - `freed_vram_gb`: 解放されたVRAM量（float）
    - `freed_ram_gb`: 解放されたRAM量（float）
    - `actions_performed`: 実行されたアクションリスト（list）
  - ⚠️ WARNING: デリケートな操作のため、使用には注意が必要
  - 実装ファイル: `functions/misc_functions.py`
  - テスト: 全テストケース成功（tests/test_vramfree.py）
  - ドキュメント: `docs/02_builtin_functions/09_utility_functions.md`に詳細追加

- **ISFILEEXIST関数**: ファイル存在チェックと拡張情報取得機能を追加
  - 基本機能: ComfyUI出力フォルダ内のファイル存在チェック
  - 拡張機能: 4つのモード対応
    - `flg=""` (デフォルト): 存在チェックのみ（"TRUE"/"FALSE"）
    - `flg="NNNN"`: 連番ファイルの最大番号検索（例: `output_0003.png`）
    - `flg="PIXEL"`: 画像サイズ取得（"[width, height]"形式）
    - `flg="SIZE"`: ファイルサイズ取得（バイト数）
  - セキュリティ: 絶対パス・UNCパス拒否（相対パスのみ許可）
  - 対象ディレクトリ: ComfyUI環境では`ComfyUI/output/`配下、テスト環境ではカレントディレクトリ配下
  - 画像フォーマット対応: PNG, JPEG, JPG, BMP, WEBP
  - 戻り値: すべて文字列型（str）、エラー時は"FALSE"を返す
  - 実装ファイル: `functions/misc_functions.py`
  - テスト: 全14テストケース成功（tests/test_isfileexist.py）
  - ドキュメント: `docs/02_builtin_functions/09_utility_functions.md`に詳細追加
  - ビルトイン関数総数: 131 → 132エントリ（130ユニーク関数、2エイリアス含む）


- **RELAY_OUTPUT変数**: スクリプト内で`RELAY_OUTPUT`変数に値を代入することで、relay_output出力ソケット（ANY型）の値を制御可能になりました
  - 用途: INPUT関数で読み込んだ画像（torch.Tensor）等のANY型データを後続ノードに渡す
  - 後方互換性: RELAY_OUTPUT未使用時は従来通りany_input入力をパススルー
  - 実装: script_engine.py, scripter_node.py
  - Tier 3機能: 実装完了、テスト完了（PASS）
  - ドキュメント:
    - `docs/01_syntax_reference.md`: 予約変数セクションにRELAY_OUTPUT変数説明を追加
    - `docs/02_builtin_functions/09_utility_functions.md`: INPUT関数セクションにRELAY_OUTPUT連携例を追加

- **INPUT関数**: ファイル読み込み機能を追加（v2.2.0で追加）
  - ComfyUI出力フォルダからファイルを読み込む
  - テキスト、JSON（数値/配列）、画像（torch.Tensor）、バイナリデータの自動型判定
  - OUTPUT関数の対称関数として実装
  - セキュリティ機能: 絶対パス・UNCパス拒否（相対パスのみ許可）
  - 読み込み元: ComfyUI環境では`ComfyUI/output/`配下、テスト環境ではカレントディレクトリ配下
  - エラーハンドリング: ファイルが見つからない場合は警告PRINTしてNoneを返す
  - 対応型:
    - テキストファイル (.txt, .md) → str型
    - JSON数値 → float型
    - JSON配列 → list型
    - 画像ファイル (.png, .jpg等) → torch.Tensor型（ComfyUI互換）
    - その他 → bytes型（バイナリ）
  - Tier 1機能（テキスト/数値/配列）: テスト完了（PASS）
  - Tier 2機能（画像）: 実装済み、テストは未実施
  - Tier 3機能（Latent/RELAY_OUTPUT）: 将来拡張として未実装

- **ドキュメント更新**:
  - `docs/02_builtin_functions/09_utility_functions.md`: INPUT関数の詳細ドキュメント追加
  - `docs/02_builtin_functions/00_index.md`: ユーティリティ関数数を6→7個に更新、全128エントリ（126ユニーク関数、2エイリアス含む）
  - `docs/00_documentation_index.md`: 全131エントリに更新、ファイル入出力セクション追加
  - `README.md`: ビルトイン関数総数を131エントリ（129ユニーク関数、2エイリアス含む）に更新


- **OUTPUT関数**: ファイル出力機能を追加
  - テキスト、数値、配列、画像（torch.Tensor）、バイナリデータの出力に対応
  - NEWモード（重複回避、`_0001`, `_0002`...自動付与）とADDモード（追記）をサポート
  - 予約変数（TXT1, TXT2, ANY_INPUT）からの直接出力に対応
  - セキュリティ機能: 絶対パス・UNCパス拒否（相対パスのみ許可）
  - サブディレクトリの自動再帰作成
  - 拡張子自動補完（`.txt`、`.png`等）
  - 出力先: ComfyUI環境では`ComfyUI/output/`配下、テスト環境ではカレントディレクトリ配下

- **ドキュメント更新**:
  - `docs/02_builtin_functions/09_utility_functions.md`: OUTPUT関数の詳細ドキュメント追加
  - `docs/02_builtin_functions/00_index.md`: ユーティリティ関数数を5→6個に更新、全127エントリ（125ユニーク関数、2エイリアス含む）
  - `README.md`: ビルトイン関数総数を130エントリ（128ユニーク関数、2エイリアス含む）に更新

### v2.8.2 (2025-10-27) - 不要関数削除（MSGBOX, INPUTBOX, LBOUND）

- **削除関数**:
  - **MSGBOX**: ComfyUIワークフロー環境ではダイアログ表示が不適切なため削除（PRINTで代替可能）
  - **INPUTBOX**: ComfyUIヘッドレス環境では入力ダイアログ表示が不可能なため削除
  - **LBOUND**: EasyScripterの配列はゼロベース固定（常に0を返す）のため不要と判断し削除

- **影響箇所**:
  - `builtin_functions.py`: BUILTIN_FUNCTIONS辞書、is_builtin_function()、get_function_usage()から削除
  - `functions/base_functions.py`: MSGBOX関数削除
  - `functions/misc_functions.py`: INPUTBOX関数、LBOUND関数削除
  - `tests/audit_06_array_functions.py`: LBOUND関連テスト3件削除、test_example_aggregate内のLBOUND使用を0に置換
  - `README.md`: 配列関数（4→3）、ユーティリティ関数（7→5）のカウント更新
  - `docs/02_builtin_functions/00_index.md`: 全126エントリに更新（-3）
  - `docs/02_builtin_functions/06_array_functions.md`: LBOUNDセクション削除、サンプルコード内LBOUND使用を0に置換
  - `docs/02_builtin_functions/09_utility_functions.md`: MSGBOX、INPUTBOXセクション削除
  - 多言語版README（docs/zh/README.md、docs/en/README.md）: カウント更新

- **後方互換性**:
  - **破壊的変更**: 上記3関数を使用している既存スクリプトは動作しなくなります
  - **推奨代替手段**:
    - MSGBOX → PRINT
    - INPUTBOX → VAL1, VAL2, TXT1, TXT2（ノード入力）
    - LBOUND → 0（固定値）またはFOR I = 0 TO UBOUND(arr[])

### v2.8.1 (2025-10-27) - EXIT文と1行IF文サポート追加(EXIT文のみ)

- **新機能**:
  - EXIT文のサポート追加
    - `EXIT FUNCTION`: 関数から早期リターン
    - `EXIT FOR`: FORループから早期終了
    - `EXIT WHILE`: WHILEループから早期終了
  - 1行IF文のサポート追加（EXIT文との組み合わせ限定）
    - 例: `IF value < 0 THEN EXIT FUNCTION`
    - 複雑な条件式もサポート: `IF x < 0 AND y < 0 THEN EXIT FUNCTION`

- **仕様変更**:
  - 関数の戻り値初期化: `0` → `""`（空文字列）
    - EXIT FUNCTION呼び出し時の未設定戻り値が空文字列となるように修正
    - EasyScripter仕様書に準拠

- **テスト追加**:
  - `tests/test_exit_basic.py`: EXIT文基本動作テスト（10テストケース）
  - `tests/test_one_line_if_exit.py`: 1行IF+EXITエッジケーステスト（8テストケース）

- **後方互換性**:
  - 既存の複数行IF文は完全に後方互換性を保持
  - 既存の全テストケース（36ファイル中27ファイル）がパス、リグレッションなし

### v2.7.9 (2025-10-22) - 全ドキュメント期待値監査プロジェクト完了

### v2.7.8 (2025-10-22) - Python関数ドキュメント期待値監査

### v2.7.7 (2025-10-22) - モデル関数ドキュメント期待値監査

### v2.7.6 (2025-10-22) - 型関数ドキュメント期待値監査

### v2.7.5 (2025-10-22) - CSV関数ドキュメント期待値監査

### v2.7.4 (2025-10-22) - ドキュメント未代入変数監査プロジェクト

### v2.7.3 (2025-10-22) - ドキュメント変数命名規則完全統一プロジェクト

### v2.7.2 (2025-10-22)
- **ドキュメント構造リファクタリング**: 情報一元化と二重管理の解消
  - **関数数表記の統一**: 全ドキュメントで「129エントリ（127ユニーク関数、2エイリアス含む）」に統一
    - 修正対象: README.md, docs/00_documentation_index.md, docs/02_builtin_functions/00_index.md, docs/01_syntax_reference.md
    - 多言語版も更新: docs/en/README.md, docs/zh/README.md
  - **Single Source of Truth確立**: docs/02_builtin_functions/00_index.md を唯一の完全リファレンス索引に指定
    - docs/00_documentation_index.md のビルトイン関数セクションを簡潔化し、詳細索引へ委譲
    - 12カテゴリの個別リストを削除し、統計情報のみ記載
  - **統計情報テーブル強化**: 詳細な関数数内訳と備考を追加
    - 各カテゴリの登録エントリ数を明記
    - エイリアスと独立実装の区別を明確化
  - **クロスリファレンス検証**: 全ドキュメント間で関数数記載の整合性を確認・修正

### v2.7.1 (2025-10-22)
- **ドキュメント構造整理**: カテゴリ順序の統一と重複コンテンツの解消
  - ビルトイン関数カテゴリ一覧の順序を全ドキュメント間で統一（正規順序: 1-12）
    - 修正対象: README.md, docs/00_documentation_index.md, docs/02_builtin_functions/00_index.md
  - docs/00_documentation_index.md を簡潔な索引に再構成（詳細はREADME.md参照へ統合）
  - Python関数実行カテゴリの関数数を正確化（1個→4個）
    - PYEXEC, PYLIST, PYENCODE, PYDECODE の4関数を正確にカウント
  - 全ドキュメントでカテゴリ数「12個」に統一
  - クロスリファレンスの正確性を検証・修正

### v2.7.0 (2025-10-15)
- **Python関数実行機能を追加**: PYEXEC()関数で標準/ユーザーライブラリの関数が実行可能に
  - 新機能: `PYEXEC(func_path, [arg1], [arg2], ...)`関数を実装
  - 対応ライブラリ:
    - Python標準ライブラリ: math, random, json, datetime, base64等
    - ユーザーインストール済みライブラリ: numpy, pandas, requests, hashlib等（軽量データ処理）
  - セキュリティ: ブラックリスト方式（危険なモジュールのみブロック）
    - ブロック対象: os, sys, subprocess, eval, exec, compile, pickle, shelve, code, pdb
  - 型変換仕様:
    - None → 0.0, bool → 1.0/0.0, int → float
    - list/tuple → CSV文字列, dict → JSON文字列
    - numpy.ndarray → CSV文字列, pandas.DataFrame → JSON文字列
  - 制限事項:
    - 引数は最大10個まで
    - 戻り値サイズは最大1MB
    - リスト・配列要素数は最大10000個
    - **注意**: 画像データ（cv2.imread等）は数十万要素となるため制限超過エラー
  - **重要**: Windowsファイルパスは必ず `\\` (ダブルバックスラッシュ) を使用してください
    - ❌ 誤り: `"C:\test.csv"` → `\t` がタブ文字に変換されパス破損
    - ✅ 正解: `"C:\\test.csv"` または `"C:/test.csv"`
  - 実装詳細:
    - `functions/python_functions.py`: PythonFunctionsクラス実装
    - `builtin_functions.py`: PYEXEC関数をビルトイン関数に統合
    - TDD準拠: 実装前にテストコード作成（tests/test_pyexec_standalone.py, test_pyexec_via_engine.py）
  - テスト: 全10テストケース成功（ScriptEngine経由での動作確認完了）
  - ドキュメント: docs/02_builtin_functions/12_python_functions.md作成
  - ビルトイン関数数: 138 → 139エントリ（1関数追加）

### v2.6.5 (2025-10-14)
- **UI改善**: ログエリアの初期状態、高さ、配置位置を調整
  - 変更内容:
    - ノード初回ロード時にログエリアが閉じた状態でロードされるように修正
    - `UI_CONFIG.logDisplay.defaultState`を`EXPANDED`（展開）から`COLLAPSED`（閉じた状態）に変更
    - ログエリアの高さを全体的に2倍に拡大
      - 閉じた状態: 40px → 80px（2倍）
      - 開いた状態: 100px → 200px（2倍）
      - 最大高さ: 150px → 300px（2倍）
    - ログエリアとスクリプトエリアの間のスペースを20px追加
      - `UI_CONFIG.widgets.spacing`を10px→30pxに変更（+20pxスペース追加）
  - 効果:
    - 初回ロード時の画面スペースを効率的に利用
    - ログエリアが広くなり、より多くの出力内容を確認可能
    - 閉じた状態でも2行程度のログが表示可能
    - ログエリアとスクリプトエリアの間にゆとりができ、視認性が向上
    - スクリプト編集エリアが広く使える状態で開始
    - ユーザーはクリックで必要に応じてログエリアを展開可能
  - 実装ファイル:
    - `web/comfyui_u5_easyscripter.js`: defaultState修正（line 822）、高さ設定2倍化（line 788-794）
    - `web/comfyui_u5_easyscripter.js`: spacing変更（line 796: 10→30）
  - 後方互換性:
    - 既存ワークフローの折りたたみ状態は保存値を優先（ワークフローJSON内のlogDisplayStateプロパティ）
    - 新規ノードのみデフォルトが閉じた状態に変更
    - 既存ワークフローもスペース拡大の恩恵を受ける

### v2.6.4 (2025-10-14)
- **スクリプト構文拡張**: インラインコメント機能を追加
  - 新機能: ステートメント後方に`'`でコメントを記述可能
    - 例: `PRINT(VAL1) 'これはコメント`
    - 例: `RETURN1 = VAL1 + VAL2 '合計を計算`
  - 実装方法:
    - 文字列リテラル内の`'`は保護される（インラインコメントとして解釈されない）
    - 文字列リテラル外の`'`以降が行末までコメントとして除去される
    - 行頭コメントの動作は変更なし（既存機能を100%保持）
  - 実装ファイル:
    - `script_parser.py`: tokenizeメソッドにインラインコメント処理ロジックを追加
    - `tests/test_inline_comment.py`: 8パターンのテストケースを作成（全て成功）
  - 効果:
    - スクリプトの可読性が向上（コードと説明を同じ行に記述可能）
    - VBAライクな記述スタイルをさらに再現
    - 既存スクリプトとの100%後方互換性
  - TDD準拠: テストファースト開発方式で実装（実装前にテストコード作成・失敗確認→実装→成功確認）

### v2.6.3 (2025-10-14)
- **UI改善**: ログエリア折りたたみ機能とテキスト可読性向上
  - 新機能:
    - ログエリアをクリックで1行表示⇄全行表示を切り替え可能
    - 折りたたみ状態はワークフロー保存時に保持（セッション永続化）
    - 折りたたみ時にスクリプトエリアのY座標を自動調整
    - 視覚的インジケータ（▶/▼アイコン）で折りたたみ状態を表示
  - 可読性向上:
    - スクリプトエリア: フォントサイズ 13px→14px、行間 1.5→1.6
    - 出力エリア: 背景色とテキスト色のコントラスト向上
    - モノスペースフォント適用で読みやすさを改善
  - 実装詳細:
    - `web/comfyui_u5_easyscripter.js`: 折りたたみ機能実装（setupLogToggle関数追加）
    - `web/comfyui_u5_easyscripter.js`: レイアウト再計算関数追加（updateLayoutForLogState関数）
    - `web/comfyui_u5_easyscripter.js`: setupResizeHandlerを折りたたみ状態対応に修正
    - `web/comfyui_u5_easyscripter.css`: 折りたたみUI用スタイル追加（.easyscripter-output-header等）
  - 効果:
    - ログ量が多い場合でも画面スペースを効率的に利用可能
    - スクリプト編集エリアが広く使える（ログ折りたたみ時）
    - テキストの読みやすさが大幅に向上
  - 互換性:
    - 既存ワークフローとの完全互換性（デフォルトは全行表示）
    - リサイズハンドラとの互換性維持
    - LOOP_SUBGRAPH()プレビューウィンドウとの互換性維持

### v2.6.2 (2025-10-14)
- **ノードカテゴリ階層を調整**: ComfyUIのノード追加メニュー構造を改善
  - 変更前: ノードを追加 > u5
  - 変更後: ノードを追加 > u5 > EasyScripter
  - 実装詳細:
    - `scripter_node.py`: CATEGORY定義を「u5」から「u5/EasyScripter」に変更
  - 効果:
    - u5カスタムノード群の階層的な整理
    - 将来的なu5シリーズノードの拡張性向上

### v2.6.1 (2025-10-14)
- **OPTIMAL_LATENT複数単語検索機能を追加**: モデル名検索がより柔軟に
  - 新機能: スペース区切りの複数単語によるAND検索
    - 単語ごとのマッチング: 全ての単語が含まれる必要あり
    - 数値バリエーション自動生成: "1.5" → ["1.5", "15"]も試行
    - 二桁数字の1の位省略: "2.0" → ["2.0", "20", "2"]も試行
    - 大文字小文字区別なし: "SD 1.5" = "sd 1.5" = "Sd 1.5"
  - 検索優先順位:
    1. スペース含む完全一致（例: "sd 1.5"というエイリアスがあればそれを優先）
    2. スペース除去後の従来検索（既存動作）
    3. 複数単語AND検索（新機能）
  - 使用例:
    ```vba
    ' 複数単語検索の例
    result = OPTIMAL_LATENT("sd 1.5", 512, 512)        ' SD1.5を識別
    result = OPTIMAL_LATENT("stable diffusion 1.5", 512, 512)  ' SD1.5を識別
    result = OPTIMAL_LATENT("sdxl turbo", 1024, 1024)  ' SDXLを識別
    result = OPTIMAL_LATENT("SD 2.0", 768, 768)        ' SD2.0を識別
    ```
  - 実装詳細:
    - `functions/model_functions.py`: `generate_numeric_variations()`関数追加（数値バリエーション生成）
    - `functions/model_functions.py`: `identify_model_multiword()`関数追加（複数単語AND検索）
    - `functions/model_functions.py`: `identify_model()`関数を拡張（完全一致→従来検索→複数単語検索）
    - `script_engine.py`: OPTIMAL_LATENT関数をengine-aware functionsに追加
  - テスト: tests/test_optimal_latent_multiword.pyに18パターンのテストケースを追加（全成功）
  - 後方互換性: 100%保持（既存の単一単語検索は完全に動作）


### v2.6.0 (2025-10-14)
- **HTTP/HTTPS通信機能を追加**: 外部RestAPIとの通信が可能に
  - 新機能: HTTP通信ビルトイン関数（7関数）を実装
    - `HTTPGET(url, [headers])`: HTTP GETリクエスト送信
    - `HTTPPOST(url, body, [headers])`: HTTP POSTリクエスト送信
    - `HTTPPUT(url, body, [headers])`: HTTP PUTリクエスト送信
    - `HTTPDELETE(url, [headers])`: HTTP DELETEリクエスト送信
    - `HTTPJSON(url, method, [json_body], [headers])`: JSON形式通信（自動Content-Type設定）
    - `HTTPSTATUS()`: 最後のHTTPリクエストのステータスコード取得
    - `HTTPHEADERS()`: 最後のHTTPレスポンスヘッダー取得（JSON形式）
  - 実装詳細:
    - `functions/http_functions.py`: HttpFunctionsクラス実装（urllib使用）
    - `builtin_functions.py`: HTTP関数をビルトイン関数に統合
    - TDD準拠: 実装前にテストコード作成（tests/test_http_functions.py）
  - 用途:
    - 外部API連携（天気API、翻訳API等）
    - Webhook通知
    - RESTful API利用
    - JSONデータ取得・送信
  - テスト: 全9テストケースが成功（JSONPlaceholder公開APIを使用）
  - ビルトイン関数数: 131 → 138エントリ（7関数追加）

### v2.5.6 (2025-10-14)
- **ドキュメント監査**: README.mdの正確性とHTML/Markdown整合性を検証
  - 監査内容:
    - ビルトイン関数のI/Oルール、引数ルール、出力ルール正確性の検証（95個の関数 + 36個のエイリアス）
    - 使用例コードの公式ルール適合性チェック（予約変数、引数型、関数形式）
    - HTML/Markdownの整合性チェック（リンク切れ、見出しレベル、内容重複）
  - 修正内容:
    - PICKCSV関数: 2引数対応（インデックス指定）を明示（README.md line 126-132）
    - PRINT関数: 括弧付き関数形式のみサポート、VBAステートメント形式未サポートを明示（README.md line 194-195, 203）
    - 整数除算演算子: ドキュメント表記（`\\`）と実装（`\`）の一致を確認済み
  - 検証結果:
    - ✅ 全95個のビルトイン関数のI/Oルール正確性確認完了
    - ✅ 全使用例コードが公式ルール（予約変数、引数型）に適合
    - ✅ リンク切れ0件、見出しレベル整合性確認
  - 影響ファイル:
    - `README.md`: PICKCSV関数2引数サンプル追加、PRINT関数形式明示
  - ドキュメント整合性: 100%（実装とドキュメントの完全一致を確認）

### v2.5.5 (2025-10-13)
- **UI修正**: widgets_values配列の順序不整合問題を解決
  - 問題:
    - UI変更後、ログウィンドウの内容がスクリプトとして解釈され、`無効な文字: '警'`エラーが発生していた
    - ループ実行の複製ノードでのみエラーが発生（元のノードでは正常）
  - 原因分析（「推論のはしご」フレームワークによる調査）:
    - JavaScriptでのwidgets配列順序変更: `[script, output]` → `[output, script]`
    - ComfyUIのwidgets_values配列構築: widgets配列の順序に従って `[outputの値, scriptの値]`
    - INPUT_TYPESとの不一致: `[script]`のみ定義 → script引数に`widgets_values[0]`（= outputの値、つまりログ）を誤って渡す
  - 修正内容:
    - `scripter_node.py`: INPUT_TYPESに`output`を追加（1番目の位置）
    - `scripter_node.py`: execute_scriptシグネチャに`output`引数を追加（読み取り専用、無視される）
    - `web/comfyui_u5_easyscripter.js`: 動的なoutputウィジェット作成を削除（INPUT_TYPESで定義されるため）
    - `web/comfyui_u5_easyscripter.js`: reorderWidgets関数を削除（不要になったため）
    - `web/comfyui_u5_easyscripter.js`: configureOutputWidgetを修正（INPUT_TYPESで定義されたoutputウィジェットにスタイルを適用）
  - 効果:
    - widgets_values配列の順序が`[output, script]`でINPUT_TYPES定義と一致
    - scriptに正しいスクリプトコードが渡される（ログメッセージではなく）
    - ループ実行でもエラーが発生しなくなる
  - 実装方法:
    - INPUT_TYPESの定義順とwidgets配列の順序を一致させることで、widgets_values配列の順序整合性を保証
    - ComfyUIの内部ロジック（widgets配列の順序でwidgets_values配列を構築）を正しく利用
  - 実装ファイル:
    - `scripter_node.py`: INPUT_TYPES修正、execute_scriptシグネチャ修正
    - `web/comfyui_u5_easyscripter.js`: 動的ウィジェット作成削除、reorderWidgets削除、configureOutputWidget修正

### v2.5.4 (2025-10-13)
- **UI改善**: ScriptWidgetの手動resize自由度を向上
  - 問題:
    - ノードを拡大すると、scriptWidgetのminHeightが動的に増加し、ユーザーが一定以上縮められなくなっていた
    - 例: ノード600px→800px拡大時、minHeight 325px→525pxに増加し、525px以下に縮められない
  - 原因:
    - setupResizeHandler内で、ノードリサイズ時に毎回minHeightを再計算・更新していた
    - 「LOOP未使用時は残りスペース全体を使用」という設計意図の副作用
  - 修正内容:
    - ユーザー手動resize検知メカニズムを実装（MutationObserverによるstyle.height監視）
    - setupResizeHandler内でminHeight更新を条件付きに変更
    - ユーザーが手動resizeした場合、minHeight更新をスキップ
    - LOOP使用時（プレビューウィンドウあり）は常にminHeight更新（v2.5.3の動作を維持）
  - 効果:
    - ユーザーがtextareaを手動resizeした後、ノードを拡大してもminHeightが固定される
    - 縮小の下限が初期値（例: 282px）で固定され、自由に縮められる
    - maxHeightは常に更新されるため、拡大方向の自由度も確保
    - LOOP使用時の動作は変更なし（v2.5.3の修正を維持）
  - 実装方法:
    - onNodeCreated: `_user_manually_resized_script`フラグ初期化
    - configureScriptWidget: MutationObserverでstyle.height変更を監視
    - setupResizeHandler: `!_user_manually_resized_script || _has_preview_widgets`条件でminHeight更新
  - 実装ファイル:
    - `web/comfyui_u5_easyscripter.js`: 初期化フラグ追加、MutationObserver実装、条件付きminHeight更新

### v2.5.3 (2025-10-13)
- **UI改善**: LOOP_SUBGRAPH()実行時のプレビューウィンドウ重複問題を解決
  - 問題:
    - LOOP_SUBGRAPH()実行後、プレビューウィンドウが追加されると、既存のscriptWidgetと重なって表示されていた
    - JS側がプレビューウィンドウ追加を検知できず、レイアウト再計算が行われなかった
  - 原因分析（「推論のはしご」フレームワークによる調査）:
    - ComfyUIにはウィジェット追加専用のイベントハンドラーが存在しない
    - onExecuted時点で既にnode.widgets配列にプレビューウィンドウが追加されているが、JS側は未検知
    - scriptWidgetの最小高さ180pxが固定で、プレビューウィンドウの追加スペースがなかった
  - 修正内容:
    - scriptWidget最小高さを180px→50pxに変更（ユーザー手動調整可能）
    - onExecuted内にウィジェット数監視機能を追加
    - setupResizeHandler内にプレビューウィンドウ対応ロジックを追加
    - 検知時に自動的にレイアウト再計算をトリガー
  - 効果:
    - LOOP未使用時: 既存レイアウト品質維持（scriptWidgetが残りスペース全体を使用）
    - LOOP実行時: プレビューウィンドウ追加を自動検知
    - LOOP実行時: scriptWidgetが50pxに縮小、プレビューウィンドウに十分なスペースを確保
    - LOOP実行時: ユーザーがscriptWidgetをtextarea resizeで手動調整可能
  - 実装方法:
    - ComfyUI→JSのイベントフローを完全追跡（LOOP_SUBGRAPH実行→サブグラフ複製→プレビュー追加→onExecuted）
    - onExecuted内でnode.widgets.lengthを監視（期待値2個 vs 実際）
    - プレビューウィンドウ検知時、_has_preview_widgetsフラグをtrueに設定
    - setupResizeHandler内で条件分岐（プレビューあり: 50px固定、なし: 動的計算）
  - 実装ファイル:
    - `web/comfyui_u5_easyscripter.js`: UI_CONFIG修正、onNodeCreated初期化フラグ追加、onExecutedウィジェット監視追加、setupResizeHandlerプレビュー対応ロジック追加

### v2.5.2 (2025-10-13)
- **UI改善**: ノードリサイズ時のScriptWidget高さ計算ロジックを修正
  - 問題:
    - ノードを拡大すると、ScriptWidgetの高さ変化がノード変化より小さく、下辺の余白が増大していた
  - 原因分析（「推論のはしご」フレームワークによる調査）:
    - outputWidgetが固定高さの場合、scriptHeightは `availableHeight * 0.65` で計算されていた
    - 残りの `availableHeight * 0.35` 分のスペースが使われず、余白として残っていた
    - ノードを拡大するほど余白が増大する仕組みだった
  - 修正内容:
    - setupResizeHandler内のscriptHeight計算式を変更
    - `availableHeight * scriptAreaRatio` → `availableHeight - output.minHeight - spacing`
    - scriptWidgetが残りスペース全体を使用するよう修正
  - 効果:
    - ノードを拡大しても余白が発生しない（余白: 0px）
    - ScriptWidgetがノードサイズ変化に正確に追従
    - outputWidgetは固定高さ（100px）を維持
  - 実装方法:
    - ComfyUI→JSのイベントシーケンスを完全追跡
    - onResizeイベントフローと計算ロジックの解析
    - 根本原因の特定と修正案の検証
  - 実装ファイル:
    - `web/comfyui_u5_easyscripter.js`: setupResizeHandler内のscriptHeight計算式修正（line 299-302）

### v2.5.1 (2025-10-13)
- **UI改善**: ノードレイアウト設定を最適化
  - 改善内容:
    - ノード最小高さを実用的な値に修正（150px → 300px）
    - 未使用のinputSocketAreaRatioパラメータを削除（コードクリーンアップ）
    - computeSizeHeightの使用理由をコメントで明確化（保守性向上）
  - 効果:
    - ノードを縮小してもウィジェットが重ならない（最小300px）
    - コードの可読性と保守性が向上
  - 実装方法:
    - 「推論のはしご」フレームワークに基づく段階的実装
    - UI_CONFIG修正とドキュメントコメント追加
  - 実装ファイル:
    - `web/comfyui_u5_easyscripter.js`: UI_CONFIG修正とコメント追加

### v2.5.0 (2025-10-13)
- **コード品質向上**: JavaScript UIコードのリファクタリング実施
  - 改善内容:
    - デバッグログ制御機能を実装（UI_CONFIG.debug.enabledフラグで有効/無効切り替え）
    - debugLog()関数を追加し、全console.log呼び出しを置き換え（18箇所）
    - スタイル設定を共通化（applyWidgetStyles関数）
    - メッセージ処理を独立化（parseExecutionMessage関数）
    - onNodeCreatedメソッドを5つの小関数に分割（225行 → 42行）
  - 分割された関数:
    - configureScriptWidget(): スクリプトウィジェット設定
    - configureOutputWidget(): 出力ウィジェット設定
    - reorderWidgets(): ウィジェット順序変更
    - setupResizeHandler(): リサイズハンドラ設定
    - setupConfigureHandler(): 設定ハンドラ（遅延初期化）
  - 効果:
    - 可読性の大幅向上（関数の責任が明確化）
    - 保守性の向上（DRY原則適用、重複コード削減）
    - デバッグ効率の改善（ログの集中制御）
    - 機能追加の容易化（モジュール化による拡張性向上）
  - 破壊的変更: なし（既存機能を100%保持）
  - 実装ファイル:
    - `web/comfyui_u5_easyscripter.js`: 全体的なリファクタリング

### v2.4.2 (2025-10-13)
- **UI改善**: ノードレイアウトの動的計算機能を実装
  - 改善内容:
    - 入力ソケットエリア高さを実際のソケット数に基づいて動的計算
    - UI_CONFIG構造を改善: `headerSpace` → `inputSocketArea`に名称変更
    - ソケット関連定数を追加: `socketHeight: 20`, `socketSpacing: 5`, `nodeHeaderHeight: 30`
    - `calculateInputSocketAreaHeight()` 関数を新規実装
  - 効果:
    - 固定パーセント（20%）による非効率なレイアウトを解消
    - ソケット数（EasyScripterの場合7個）に応じた正確な高さ計算
    - より柔軟で保守性の高いUI実装
  - 実装ファイル:
    - `web/comfyui_u5_easyscripter.js`: 動的計算関数とUI_CONFIG更新、3箇所の計算ロジック改善

### v2.4.1 (2025-10-09)
- **LOOP_SUBGRAPH小数点文字列対応**: 引数に小数点を含む文字列を受け入れるように改善
  - 改善内容:
    - count引数の型変換を`int(count)`から`int(float(count))`に変更
    - 小数点文字列（例: "1.3", "99.9"）を受け入れ、切り捨てで整数化
    - 既存の整数・整数文字列の動作は完全保持（100%後方互換性）
  - 実装ファイル:
    - `functions/loop_functions.py`: builtin_loop_subgraph関数のcount変換ロジック修正
  - テスト: tests/test_loop_subgraph.pyに9パターンの小数点文字列テストを追加（全成功）
  - ドキュメント: docs/02_builtin_functions/10_loop_functions.mdに引数説明と使用例を追記

### v2.4.0 (2025-10-09)
- **LOOP_SUBGRAPH機能を大幅強化（v1.2）**: サブグラフの自動判定と収集機能を実装
  - 新機能:
    - EasyScripterに接続された後続ノード全体を自動的にサブグラフとして認識
    - サブグラフ全体を指定回数だけ複製し繰り返し実行
    - 接続なしの場合は自動的にループを無効化（エラーなし）
    - 後方互換性を完全維持（既存コードは変更不要）
  - 実装詳細:
    - `scripter_node.py`: サブグラフ検出・収集機能を追加
      - `_get_downstream_nodes()`: 出力スロットに接続された後続ノードを取得
      - `_is_subgraph()`: 後続ノードがサブグラフか判定
      - `_collect_subgraph_nodes()`: 開始ノードから到達可能な全ノードを再帰的に収集
      - `_build_loop_subgraph()`: サブグラフ複製とノード参照更新ロジックを完全実装
  - 動作:
    - チャネル（RETURN1/RETURN2/RELAY）に対応する出力スロットを特定
    - 後続ノードを検出し、サブグラフ判定を実行
    - サブグラフの場合: 全ノードを収集→反復回数分複製→ノードID更新（`{original_id}_loop_{iteration}`形式）
    - サブグラフでない場合: ループを無効化し通常出力を返却
  - テスト: tests/test_loop_subgraph.pyにサブグラフ検出テストを追加
  - ドキュメント: docs/02_builtin_functions/10_loop_functions.mdにv1.2改善点を追記

- **LOOP_SUBGRAPH複数チャネル対応（v1.3）**: 同じスクリプト内で異なるチャネルに個別にループ設定が可能に
  - 新機能:
    - 複数チャネルの個別設定: RETURN1, RETURN2, RELAYそれぞれに異なる繰り返し回数を設定可能
    - 同一サブグラフの統合実行: 複数チャネルが同じサブグラフに接続されている場合、回数を合計してシーケンシャルに実行
    - AUTOモードの拡張: `LOOP_SUBGRAPH(5, None)`で接続されている全チャネルに対してループ設定を適用
    - 後勝ち優先ルール: 同じチャネルへの複数回コールは、後から呼ばれた設定が優先される
    - 完全な後方互換性: 既存の単一チャネル動作は変更なし
  - 実装詳細:
    - `script_engine.py`: loop_config構造を単一辞書からチャネル別辞書に変更
    - `functions/loop_functions.py`: チャネル別設定保存と後勝ち優先ロジック実装
    - `scripter_node.py`: 5つの補助メソッドを追加
      - `_get_channel_slots()`: チャネル名から出力スロット番号への変換
      - `_get_channel_outputs()`: チャネルの出力値取得
      - `_expand_auto_config()`: AUTOモードの全接続チャネル展開
      - `_group_by_subgraph()`: サブグラフごとのチャネルグループ化
      - `_duplicate_subgraph_iteration()`: 1イテレーション分のサブグラフ複製
    - `_build_loop_subgraph()`: 複数チャネル統合実行ロジックを完全実装
  - テスト: tests/test_loop_subgraph.pyに複数チャネルテストケースを追加（全て成功）
  - ドキュメント: docs/02_builtin_functions/10_loop_functions.mdにv1.3改善点と実用例を追記

### v2.3.0 (2025-10-09)
- **サブグラフループ実行機能を追加**: LOOP_SUBGRAPH関数でN回繰り返し実行が可能に
  - 新機能: `LOOP_SUBGRAPH(count, channel)` 関数を実装
  - 対応チャネル: RETURN1, RETURN2, RELAY（ANY型出力）
  - 繰り返し回数: 1-100回の範囲で指定可能
  - 実装詳細:
    - `functions/loop_functions.py`: LOOP_SUBGRAPH関数実装
    - `script_engine.py`: loop_config管理とengine渡し機能追加
    - `builtin_functions.py`: 関数登録とspecial_functionsリスト追加
    - `scripter_node.py`: hidden inputs（unique_id, dynprompt）追加、サブグラフ検出ロジック実装
  - テスト: tests/test_loop_subgraph.pyで基本動作を検証済み

### v2.2.2 (2025-10-08)
- **CSVSORT関数シグネチャ修正**: delimiter引数を追加し、ドキュメントと実装を一致させた
  - 問題: `CSVSORT(tags, ",", FALSE)`呼び出しで「3引数与えられたが1-2引数しか受け付けない」エラー
  - 原因: 実装が`CSVSORT(csv_text, descending)`の2引数、ドキュメントが`CSVSORT(csv_text, [delimiter], [descending])`の3引数で不一致
  - 修正: 実装に`delimiter`引数を追加し、`CSVSORT(csv_text, delimiter=",", descending=False)`に変更
  - 影響ファイル:
    - `functions/csv_functions.py`: CsvFunctions.CSVSORTメソッド修正
    - `Release/functions/csv_functions.py`: 同上
    - `docs/02_builtin_functions/04_csv_functions.md`: シグネチャとサンプル更新
    - 後方互換性: `CSVSORT("a,b,c")`の1引数呼び出しも継続動作（delimiter=","がデフォルト）
  - 新機能: セミコロン等のカスタム区切り文字対応（例: `CSVSORT("z;a;m", ";")`）

### v2.2.1 (2025-10-08)
- **整数除算演算子(\)の実装完了**: VBA準拠の整数除算演算子が正常に動作
  - script_parser.py: INTDIVトークンパターン追加（`r'^\\'`）
  - script_parser.py: parse_multiplicationメソッドにINTDIV処理追加
  - script_engine.py: evaluate_binary_opに整数除算ロジック追加（`int(left_num // right_num)`）
  - ドキュメント: docs/01_syntax_reference.md:154に既存記載を確認

- **FORMAT関数バグ修正**: VBA形式の簡易指定（"0.0"等）が正しく動作するよう実装順序を修正
  - 問題: `FORMAT(1.2, "0.0")`が`"1e+00"`（科学的記数法）を返していた
  - 原因: Python標準`format(value, format_string)`が先に試行されていた
  - 修正: VBA形式の簡易指定（"0", "0.0", "0.00"）を最優先でチェックするよう順序変更
  - 影響ファイル: `functions/misc_functions.py`のFORMATメソッド
  - 検証: ScriptEngine経由での動作確認完了（RESULT1が正しく"1.2"を返すことを確認）

### v2.2.0 (2025-10-08)
- **hot fix**:
  - 軽微なバグフィックス

### v2.1.1 (2025-10-06)
- **文字エンコーディング修正**: 日本語文字列の文字化け問題を解決
  - script_parser.py: unicode_escapeデコードを削除し、明示的なエスケープシーケンス（\n, \t, \r, \\）のみを置換
  - scripter_node.py: RETURN値に明示的なUTF-8エンコーディング保証を追加
  - PRINT出力とノード間文字列受け渡しの両方で日本語が正しく表示されるように修正

### v2.1.0 (2025-10-06)
- **関数修正**: CSVSORT, CSVCOUNT, ARRAY関数の引数仕様を修正

### v2.0.0 (2025-10-03)
- ドキュメント体系を完全リニューアル
- README.mdを簡潔化し、詳細ドキュメントを分離

### v1.5.0 (2025-10-02)
- OPTIMAL_LATENT関数を追加（30+モデル対応）
- u5ローダーシリーズを実装（9種類）
- ANY型入力とrelay_output機能を追加

### v1.0.0
- 初回リリース
- VBAスタイルスクリプト実行エンジン
- 基本的なビルトイン関数実装
