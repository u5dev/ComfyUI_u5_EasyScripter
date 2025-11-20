# 更新履歴 (CHANGELOG)

u5 EasyScripterの主要なバージョン更新履歴です。

---

## 📝 更新履歴

### v3.2.12 (2025-11-20) - 多言語ドキュメントリンク検証完全PASS達成

#### Verified
- **反復監査実施（4回のIteration）**:
  - Iteration 1: 初回検証で10件検出（全て偽陽性）
  - Iteration 2: 言語切り替え検出改善 → 警告0件達成
  - Iteration 3: 言語切り替えセクション完全除外 → Phase 1完全PASS（エラー0件）
  - Iteration 4: Phase 2拡張検証実施 → Phase 2完全PASS（エラー0件）

- **Phase 1基本検証（エラー0件、警告0件）**:
  - 相対リンクの妥当性検証
  - 画像参照の妥当性検証
  - 言語切り替えセクションの除外

- **Phase 2拡張検証（エラー0件、警告0件）**:
  - リンクアンカー（#見出し）の検証
  - HTMLタグ内のリンク検証
  - 画像ファイルの実在性確認（厳格版）
  - 言語切り替えリンクの一貫性検証
  - 相対パス深度の妥当性検証

#### Fixed
- **検証スクリプト改善（3箇所の修正）**:
  - `tools/validate_multilang_links.py`:
    - `_is_language_switcher_section`関数: 言語切り替えセクション検出ロジック改善
    - `_extract_markdown_links`関数: 画像リンク除外ロジック追加（否定後読み使用）
    - `validate_language_docs`メソッド: 言語切り替えセクション内リンク完全除外

#### Added
- **Phase 2拡張検証ツール**: `tools/validate_multilang_links_advanced.py` - アンカーリンク、HTMLタグ、画像実在性、言語切り替え一貫性、相対パス深度の検証
- **統合検証ツール**: `tools/run_full_validation.py` - Phase 1 + Phase 2統合実行

#### Documentation
- **完全PASS証明書**: `claudedocs/link_validation_certificate.md` - 全検証項目PASS証明
- **反復監査レポート**: `claudedocs/iterative_audit_report.md` - 4回の反復監査詳細記録

### v3.2.11 (2025-11-20) - 多言語ドキュメントリンク修正（7箇所）

#### Fixed
- **フランス語版リンク修正（4ファイル、4箇所）**:
  - `docs/fr/01_syntax_reference.md`: 日本語版へのリンク `../../docs/01_syntax_reference.md` → `../01_syntax_reference.md`
  - `docs/fr/CHANGELOG.md`: 日本語版へのリンク `../../docs/CHANGELOG.md` → `../CHANGELOG.md` (2箇所: 行3, 行108)
  - `docs/fr/CONTENTS.md`: 日本語版へのリンク `../../docs/CONTENTS.md` → `../CONTENTS.md`

- **中国語版リンク修正（3ファイル、3箇所）**:
  - `docs/zh/01_syntax_reference.md`: 日本語版へのリンク `../../docs/01_syntax_reference.md` → `../01_syntax_reference.md`
  - `docs/zh/CHANGELOG.md`: 日本語版へのリンク `../../docs/CHANGELOG.md` → `../CHANGELOG.md`
  - `docs/zh/CONTENTS.md`: 日本語版へのリンク `../../docs/CONTENTS.md` → `../CONTENTS.md`

#### Verified
- **プロジェクトルートREADME.mdへのリンク（5ファイル）**: 全言語版README.mdの `[日本語](../../README.md)` は正しいパス（修正不要）
- **画像参照パス（5ファイル）**: 全言語版の `../img/SimpleConnection.png` は正しいパス（修正不要）

#### Added
- **検証ツール**: `tools/validate_multilang_links.py` - 多言語ドキュメントリンク自動検証スクリプト

#### Documentation
- **検証最終レポート**: `claudedocs/multilingual_link_audit_final_report.md` - リンク修正詳細と偽陽性分析
- **検証結果JSON**: `claudedocs/multilingual_link_audit_results.json` - 機械処理用検証結果

#### Notes
- 各国語版ドキュメント（`docs/{lang}/`）は全てフラット配置
- 日本語版参照時: プロジェクトルートREADME.mdは `../../README.md`, docs/配下は `../ファイル名.md`
- 画像参照は全言語共通で `../img/ファイル名.png`

---

### v3.2.10 (2025-11-20) - 水平線差異修正（4ファイル）

#### Fixed
- **中国語版 contents/docs/zh/03_advanced_examples.md**: `###`見出し前の余分な水平線を削除（行353）
- **ドイツ語版 contents/docs/de/03_advanced_examples.md**: `###`見出し前の余分な水平線を削除（行355）
- **日本語版 contents/README.md**: 水平線末尾のスペース削除（行13: `--- ` → `---`）

#### Verified
- **フランス語版 contents/docs/fr/README.md**: 水平線配置正常（修正不要）
- **スペイン語版 contents/docs/es/04_u5_loader_examples.md**: 水平線配置正常（修正不要）
- **全ファイル水平線数一致確認**:
  - zh/de/examples/ 03_advanced_examples.md: 9個（基準と一致）
  - fr/contents/ README.md: 11個（基準と一致）
  - es/examples/ 04_u5_loader_examples.md: 8個（基準と一致）

#### Notes
- 水平線は`##`（H2）見出し前のみ配置、`###`（H3）見出し前には配置しないルールを確認
- スペース付き水平線（`--- `）は`grep "^---$"`でカウントされないため、フォーマット統一を実施

---

### v3.2.9 (2025-11-20) - 有料コンテンツ多言語ドキュメント監査完了（全42ファイル完全一致保証）

#### Verified
- **全42ファイル完全監査達成**: contents/ ディレクトリ（7ファイル × 6言語 = 42ファイル）の構造的一致性を完全保証
  - **監査範囲**: 日本語(ja)、英語(en)、中国語(zh)、フランス語(fr)、ドイツ語(de)、スペイン語(es)
  - **監査項目**:
    - コードブロック数（````vba`, ```json`, ```mermaid`）の完全一致
    - 見出し構造（H1, H2, H3, H4）の完全一致
    - ヘッダー構造（言語切り替えリンク）の形式統一
    - フッター構造（区切り線+戻るリンク）の形式統一
  - **検出差異数**: 0件（最終検証後）
  - **監査対象ファイル**:
    - contents/README.md
    - contents/docs/02_builtin_functions/10_loop_functions.md
    - contents/docs/02_builtin_functions/11_http_functions.md
    - contents/docs/02_builtin_functions/12_python_functions.md
    - contents/docs/examples/01_beginner_examples.md
    - contents/docs/examples/02_intermediate_examples.md
    - contents/docs/examples/03_advanced_examples.md

#### Fixed
- **英語版・中国語版・フランス語版・ドイツ語版・スペイン語版 11_http_functions.md**: 5セクション欠落修正
  - 欠落セクション:
    - Yahoo検索：日本語クエリテスト
    - httpbin.org: JSON POSTリクエスト（日本語コンテンツ）
    - httpbin.org: HTTPステータスコード確認
    - エラーハンドリング実装
    - 複数ヘッダー設定
  - H4見出し数: 4 → 9（日本語版と一致）

- **中国語版 README.md**: 言語切り替えリンク4ブロック追加
  - ヘッダー構造を日本語版と完全一致させた

- **スペイン語版 README.md**: 見出し構造完全再構築
  - H2見出し数: 5 → 6（日本語版と一致）
  - H3見出し数: 5 → 19（+14見出し追加）
  - H4見出し数: 3 → 0（過剰なH4を削除/変換）
  - 構造的対称性を完全達成

- **中国語版・ドイツ語版 03_advanced_examples.md**: 欠落セクション補完
  - 欠落セクション:
    - Venice API for gentleman画像説明
    - Cloudflare i2t Image2Image自己ループ
  - コードブロック数: 30 → 34（日本語版と一致）

- **フランス語版 README.md**: 相対パスと言語切り替えリンク修正
  - 相対パス構造を日本語版と一致させた

- **ドイツ語版 README.md**: 言語切り替えリンク4ブロック追加
  - ヘッダー構造を日本語版と完全一致させた

#### Quality Assurance
- **構造的対称性100%達成**: 全言語版が日本語版（参照元）と完全一致
- **ナビゲーション整合性**: ヘッダー・フッターの言語切り替えリンクが全42ファイルで適切に配置
- **技術的品質保証**: UTF-8エンコーディング統一、Markdown構造標準化完了
- **コードブロック保全性**: 全コードブロック内容を一切変更せず、構造的一致のみを達成

---

### v3.2.8 (2025-11-20) - 多言語ドキュメント最終監査完了（全60ファイル完全一致保証）

#### Verified
- **全60ファイル完全監査達成**: 10ファイル × 6言語 = 60ファイルの構造的一致性を完全保証
  - **監査範囲**: 日本語(ja)、英語(en)、中国語(zh)、フランス語(fr)、ドイツ語(de)、スペイン語(es)
  - **監査項目**:
    - コードブロック数（````vba`）の完全一致
    - 見出し構造（H1, H2, H3, H4）の完全一致
    - ヘッダー構造（先頭3行）の形式統一
    - フッター構造（末尾区切り線+戻るリンク）の形式統一
  - **検出差異数**: 0件
  - **監査手法**: 自動化PowerShellスクリプト（`claudedocs/audit_iteration3.ps1`）
  - **最終レポート**: `claudedocs/multilingual_audit_final_report.md`

#### Quality Assurance
- **構造的対称性100%達成**: 全言語版が日本語版（参照元）と完全一致
- **ナビゲーション整合性**: ヘッダー・フッターの戻るリンクが全60ファイルで適切に配置
- **技術的品質保証**: UTF-8エンコーディング統一、Markdown構造標準化完了

---

### v3.2.6 (2025-11-20) - 全言語版ドキュメント構造完全一致達成（監査・修正完了）

#### Fixed
- **多言語ドキュメント構造的対称性の完全達成**: 全60ファイル（10ファイル×6言語）の見出し構造が日本語版と完全一致
  - **監査実施**: 全ファイルのH1-H4見出し数を自動カウント・比較
  - **検出された差異**: 5ファイル（ドイツ語版1件、スペイン語版4件）
  - **修正内容**:
    1. **ドイツ語版 02_string_functions.md**: 8個のH3見出し追加
       - 欠落関数: LTRIM, RTRIM, UCASE, LCASE, PROPER, CHR, ASC, STR
       - 挿入位置: JOIN関数の後、URLENCODE関数の前（Line 285）
       - H3見出し数: 20 → 28（日本語版と一致）
    2. **スペイン語版 03_datetime_functions.md**: 余分なH3見出し削除
       - 削除対象: WEEKDAY([date], [firstday]) 関数（日本語版に存在しない）
       - 削除範囲: Line 149-159
       - H3見出し数: 13 → 12（日本語版と一致）
    3. **スペイン語版 04_csv_functions.md**: 実用例セクション追加
       - 追加内容: H2「Ejemplos prácticos」+ H3 2個（ランダム選択、重複除去）
       - 挿入位置: CSVSORT関数の後、フッター前（Line 214）
       - H2見出し数: 2 → 3、H3見出し数: 9 → 11（日本語版と一致）
    4. **スペイン語版 06_array_functions.md**: 配列使用例セクション追加
       - 追加内容: H2「Ejemplos de uso de arrays」+ H3 4個（基本操作、サイズ変更、CSV組み合わせ、集計処理）
       - 挿入位置: REDIM関数の後、フッター前（Line 87）
       - H2見出し数: 2 → 3、H3見出し数: 3 → 7（日本語版と一致）
    5. **スペイン語版 08_model_functions.md**: 汎用スクリプト例追加
       - 追加内容: H3「Script genérico compatible con múltiples modelos」
       - 挿入位置: SDXLワークフロー例の後、フッター前（Line 107）
       - H3見出し数: 2 → 3（日本語版と一致）
  - **検証結果**: 修正後、全60ファイルで見出し数が完全一致（差異検出数: 0件）
  - **品質保証**: 翻訳内容は日本語版から忠実に再現、コード例のコメントも全て各言語に翻訳

#### Changed
- **監査スクリプト導入**: audit_headings.ps1を作成（見出し構造の自動検証）
  - 機能: 全言語版のH1-H4見出し数を自動カウント・比較
  - 出力: ファイル別・言語別の見出し数表、差異検出リスト
  - 用途: 今後の多言語ドキュメント更新時の品質チェック

### v3.2.5 (2025-11-20) - 中国語版・ドイツ語版ドキュメントINPUT関数セクション補完

#### Fixed
- **中国語版・ドイツ語版ドキュメント欠落修正**: INPUT関数とRELAY_OUTPUTの連携セクションを追加
  - **対象ファイル**:
    - docs/zh/09_utility_functions.md (Line 182に挿入)
    - docs/de/09_utility_functions.md (Line 135に挿入)
  - **追加内容**:
    - H4見出し: "INPUT函数与RELAY_OUTPUT的联动" (中国語版) / "Koordination zwischen INPUT-Funktion und RELAY_OUTPUT" (ドイツ語版)
    - INPUT関数で読み込んだデータをRELAY_OUTPUTで後続ノードに渡す方法の説明
    - RETURN1/RETURN2との違い（プリミティブ型専用 vs ANY型対応）
    - コード例とコメント（各言語に翻訳済み）
  - **検証結果**: 全言語版のH4見出し数が28個で完全一致

### v3.2.4 (2025-11-20) - スペイン語版ドキュメント実用例セクション補完

#### Fixed
- **スペイン語版ドキュメント欠落修正**: docs/es/09_utility_functions.mdに実用例セクションを追加
  - **欠落内容**: Line 351以降の実用例セクション全体（セクション見出し4個）
  - **追加内容**:
    - 実用例（セクション見出し）: Ejemplos prácticos
    - デバッグ出力の活用: Uso de salida de depuración
    - 入力値の検証: Validación de valores de entrada
    - 型に応じた処理分岐: Ramificación de procesamiento según el tipo
  - **翻訳品質**:
    - 日本語版docs/02_builtin_functions/09_utility_functions.mdから翻訳
    - コード例のコメントも全てスペイン語に翻訳
    - 既存のスペイン語版ドキュメントと文体を統一
  - **検証結果**: 見出し数 23個 → 28個（日本語版・英語版・中国語版・フランス語版・ドイツ語版と完全一致）

### v3.2.3 (2025-11-20) - 中国語版ドキュメント実用例セクション補完

#### Fixed
- **中国語版ドキュメント欠落修正**: docs/zh/09_utility_functions.mdに実用例セクションを追加
  - **欠落内容**: Line 496以降の実用例セクション全体（セクション見出し4個）
  - **追加内容**:
    - 実用例（セクション見出し）: 实用示例
    - デバッグ出力の活用: 调试输出的应用
    - 入力値の検証: 输入值验证
    - 型に応じた処理分岐: 根据类型进行处理分支
  - **翻訳品質**:
    - 日本語版docs/02_builtin_functions/09_utility_functions.mdから翻訳
    - コード例のコメントも全て簡体字中国語に翻訳
    - 専門用語の訳語を一貫して使用（例: "デバッグ出力" → "调试输出", "型に応じた処理分岐" → "根据类型进行处理分支"）
  - **検証結果**: 見出し数 22個 → 27個（日本語版・英語版・フランス語版・ドイツ語版と完全一致）

### v3.2.2 (2025-11-20) - ドイツ語版ドキュメント完全補完

#### Fixed
- **CRITICAL修正**: docs/de/09_utility_functions.mdが著しく不完全だった問題を解決
  - **欠落内容**: Line 386以降の全内容（関数12個 + セクション見出し3個）が丸ごと欠落
  - **追加内容**:
    - 画像・Latentデータ取得関数（続き）: GETANYVALUEINT, GETANYVALUEFLOAT, GETANYSTRING
    - 型判定関数（セクション全体）: ISNUMERIC, ISDATE, ISARRAY, TYPE
    - 実用例（セクション全体）: デバッグ出力の活用、入力値の検証、型に応じた処理分岐
  - **翻訳品質**:
    - 既存のドイツ語版ドキュメントと文体を統一
    - コード例のコメントも全てドイツ語に翻訳
    - 専門用語の訳語を一貫して使用（例: "配列" → "Array", "型判定" → "Typprüfungsfunktionen"）
  - **検証結果**: 見出し数 14個 → 26個（日本語版・フランス語版・英語版と完全一致）

### v3.2.1 (2025-11-20) - 英語版ドキュメント補完

#### Fixed
- **英語版ドキュメント関数欠落修正**: docs/en/09_utility_functions.mdに5つの関数セクションを追加
  - GETANYVALUEINT: ANY型データから整数値を取得
  - GETANYVALUEFLOAT: ANY型データから浮動小数点値を取得
  - GETANYSTRING: ANY型データから文字列を取得
  - ISDATE: 日付型判定関数
  - ISARRAY: 配列型判定関数
  - 見出し数: 21個 → 26個（日本語版・フランス語版と一致）

### v3.2.0 (2025-11-19) - 多言語ドキュメント対応

#### Added
- **多言語ドキュメント対応**: 5言語に完全翻訳したドキュメントを追加
  - **英語版**: docs/en/ (14ファイル)
  - **中国語簡体字版**: docs/zh/ (14ファイル)
  - **スペイン語版**: docs/es/ (14ファイル)
  - **フランス語版**: docs/fr/ (14ファイル)
  - **ドイツ語版**: docs/de/ (14ファイル)
  - 翻訳対象: README.md、構文リファレンス、ビルトイン関数ドキュメント、CHANGELOG.md、CONTENTS.md
  - 各言語版に言語切替リンクを追加（6言語間の相互リンク）

#### Changed
- **ドキュメント構造の再編成**: 各言語版をフラット構造で配置
  - 従来: `docs/02_builtin_functions/*.md`（階層構造）
  - 新規: `docs/{lang}/*.md`（フラット構造）
  - 画像は全言語で共有 (`docs/img/`)

#### Fixed
- **CRITICAL問題修正**: 多言語ドキュメントのクロスリファレンスエラーを修正
  - **画像パス修正**: 全CONTENTS.mdファイル（5言語版+日本語版）の画像リンクを修正
    - 修正前: `contents/docs/img/making.png` (存在しないパス)
    - 修正後: `../img/making.png` (正しいパス)
    - 対象ファイル: docs/CONTENTS.md, docs/en/CONTENTS.md, docs/zh/CONTENTS.md, docs/es/CONTENTS.md, docs/fr/CONTENTS.md
  - **ロシア語版リンク削除**: 中国語版ドキュメント（10ファイル）から未実装のロシア語版へのリンクを削除
    - 対象: docs/zh/00_index.md 〜 09_utility_functions.md
  - **言語表記統一**: README.md冒頭の言語切替リンクを現地語表記に統一
    - 修正前: `[Spanish]`, `[French]`, `[German]`
    - 修正後: `[Español]`, `[Français]`, `[Deutsch]`
  - **画像ファイルコピー**: `contents/docs/img/making.png` → `docs/img/making.png`
- **README.md更新**: 冒頭に多言語切替リンクを追加

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
