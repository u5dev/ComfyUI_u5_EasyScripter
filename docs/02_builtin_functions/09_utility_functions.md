# ユーティリティ関数リファレンス

[← ビルトイン関数索引に戻る](00_index.md)

ユーティリティ関数は、デバッグ出力、型判定、入力処理など、スクリプト開発を補助する便利な関数群です。

---

## 出力関数

### PRINT(message, ...)

**説明**: 値をテキストエリアに出力する（デバッグ用）

**引数**:
- message - 出力する値（複数指定可能）

**戻り値**: なし（PRINT変数に追記される）

**例**:
```vba
' 変数の値を追跡
value = VAL1 * 2
PRINT("value after multiplication: " & value)

' ループの進行状況
FOR i = 1 TO 10
    PRINT("Loop iteration: " & i)
    ' 処理...
NEXT

' 条件分岐の確認
condition = VAL1 > 100
IF condition THEN
    PRINT("Condition was TRUE")
ELSE
    PRINT("Condition was FALSE")
END IF

' 複数の値を同時に出力
PRINT("VAL1:", VAL1, "VAL2:", VAL2)
result = VAL1 + VAL2
PRINT("計算結果:", result)
```

**注意**:
- PRINT関数で出力された内容は、ノード下部のテキストエリアに表示されます
- デバッグ時の変数値確認に便利です

---

### OUTPUT(arg, [path], [flg])

**説明**: テキスト、数値、配列、画像、バイナリデータをファイルに出力する

**引数**:
- arg (Any) - 出力する値（文字列、数値、配列、torch.Tensor、bytes）
- path (str, optional) - 出力先パス（相対パス、デフォルト=""）
- flg (str, optional) - 動作モード（"NEW"=新規/重複回避、"ADD"=追記、デフォルト="NEW"）

**戻り値**: str - 出力したファイルの絶対パス（失敗時は空文字列）

**機能**:
1. **テキスト出力**: 文字列、数値、配列をテキストファイルとして出力
2. **画像出力**: torch.Tensor（ComfyUI画像データ）をPNG/JPEG等として出力
3. **バイナリ出力**: bytes型データをバイナリファイルとして出力
4. **NEWモード**: 重複時に`_0001`, `_0002`...を自動付与
5. **ADDモード**: 既存ファイルに追記
6. **セキュリティ**: 絶対パス・UNCパス拒否（相対パスのみ許可）
7. **サブディレクトリ**: 自動再帰作成
8. **拡張子自動補完**: `.txt`（テキスト）、`.png`（画像）

**予約変数対応**:
- `OUTPUT("TXT1", "output.txt")` → 入力ソケットTXT1の値を出力
- TXT1, TXT2, ANY_INPUT に対応

**例**:
```vba
' テキスト出力
path = OUTPUT("Hello World", "output.txt", "NEW")
PRINT("出力先: " & path)

' 数値出力
path = OUTPUT(12345, "number.txt")
PRINT("出力先: " & path)

' 配列出力
ARR = ARRAY("apple", "banana", "cherry")
path = OUTPUT(ARR, "fruits.txt")
PRINT("出力先: " & path)

' 予約変数からの出力
path = OUTPUT("TXT1", "user_input.txt")
PRINT("TXT1の値を出力: " & path)

' 追記モード
path1 = OUTPUT("First Line", "log.txt", "NEW")
PRINT("新規作成: " & path1)
path2 = OUTPUT("Second Line", "log.txt", "ADD")
PRINT("追記: " & path2)

' サブディレクトリ作成
path = OUTPUT("data", "subdir/data.txt")
PRINT("サブディレクトリ込みで作成: " & path)

' 重複回避
path1 = OUTPUT("content", "file.txt", "NEW")
PRINT("1回目: " & path1)  ' file.txt
path2 = OUTPUT("content", "file.txt", "NEW")
PRINT("2回目: " & path2)  ' file_0001.txt
```

**セキュリティ制限**:
- 絶対パス（`C:\...`, `/...`）は拒否
- UNCパス（`\\server\...`）は拒否
- 相対パスのみ許可

**出力先ディレクトリ**:
- ComfyUI環境: `ComfyUI/output/` 配下
- テスト環境: カレントディレクトリ配下

---

### INPUT(path)

**説明**: ComfyUI出力フォルダからファイルを読み込む（OUTPUT関数の対称関数）

**引数**:
- path (str, 必須) - ComfyUI出力フォルダからの相対パス
  - 絶対パス（`C:\...`, `/...`）は禁止
  - UNCパス（`\\server\...`）は禁止
  - 相対パスのみ許可

**戻り値**: 動的型（ファイル形式に応じて自動判定）
- テキストファイル (`.txt`, `.md`) → str型
- JSON数値 → float型
- JSON配列 → list型
- 画像ファイル (`.png`, `.jpg`, `.jpeg`, `.bmp`, `.webp`) → torch.Tensor型（ComfyUI互換）
- その他 → bytes型（バイナリ）

**機能**:
1. **自動型判定**: ファイル形式に応じて最適な型で読み込み
2. **画像データ対応**: torch.Tensor形式でComfyUI画像ノードに直接接続可能
3. **JSONサポート**: 数値・配列のJSON自動パース
4. **セキュリティ**: 絶対パス・UNCパス拒否（相対パスのみ許可）
5. **エラーハンドリング**: ファイルが見つからない場合は警告PRINTしてNoneを返す

**読み込み元ディレクトリ**:
- ComfyUI環境: `ComfyUI/output/` 配下
- テスト環境: カレントディレクトリ配下

**例**:
```vba
' テキストファイル読み込み
prompt = INPUT("prompts/positive.txt")
PRINT("読み込んだプロンプト: " & prompt)
RETURN1 = prompt

' JSON配列読み込み
dataArray = INPUT("data_array.json")
PRINT("配列要素数: " & (UBOUND(dataArray[]) + 1))

' 画像読み込み（torch.Tensor形式）
refImage = INPUT("reference_images/style_sample.png")
' refImageはComfyUIの画像入力ノードに直接接続可能

' サブディレクトリからの読み込み
configText = INPUT("configs/model_settings.txt")
PRINT("設定内容: " & configText)
```

**セキュリティ制限**:
- 絶対パス（`C:\...`, `/...`）は拒否
- UNCパス（`\\server\...`）は拒否
- 相対パスのみ許可

**出力元ディレクトリ**:
- ComfyUI環境: `ComfyUI/output/` 配下
- テスト環境: カレントディレクトリ配下

**OUTPUT関数との対称性**:
- OUTPUT: データ → ファイル保存
- INPUT: ファイル読み込み → データ
- 両関数とも相対パスのみ許可、絶対パス・UNCパス拒否

#### INPUT関数とRELAY_OUTPUTの連携

INPUT関数で読み込んだ画像やデータを後続ノードに渡すには、RELAY_OUTPUT変数を使用します。

```vba
' テキストファイルからプロンプトを読み込み、後続のCLIPTextEncodeに渡す
PROMPT_TEXT = INPUT("prompts/positive.txt")
RELAY_OUTPUT = PROMPT_TEXT

' または画像ファイルを読み込み、後続のLoadImageに渡す
IMG1 = INPUT("reference_images/base.png")
RELAY_OUTPUT = IMG1
```

**RETURN1/RETURN2 vs RELAY_OUTPUT**:
- RETURN1/RETURN2: プリミティブ型専用（INT, FLOAT, STRING）
- RELAY_OUTPUT: ANY型対応（torch.Tensor, list, dict等のオブジェクトも可）

**注意**:
- ファイルが存在しない場合、警告メッセージをPRINTしてNoneを返します
- 大きなファイル（画像等）の読み込みには時間がかかる場合があります

---

### ISFILEEXIST(path, [flg])

**説明**: ComfyUI出力フォルダ内のファイル存在チェックと拡張情報取得

**引数**:
- path (str, 必須) - ComfyUI出力フォルダからの相対パス
  - 絶対パス（`C:\...`, `/...`）は禁止
  - UNCパス（`\\server\...`）は禁止
  - 相対パスのみ許可
- flg (str, optional) - オプションフラグ（デフォルト: ""）
  - `""` (デフォルト): 存在チェックのみ
  - `"NNNN"`: 最大番号の_NNNNファイルパス検索
  - `"PIXEL"`: 画像サイズ（幅・高さ）取得
  - `"SIZE"`: ファイルサイズ（バイト）取得

**戻り値**: 動的型（flgに応じて変化）
- **flg=""**: `"TRUE"` または `"FALSE"` (str型)
- **flg="NNNN"**: 最大番号のファイルパス（相対パス、str型）、存在しない場合は `"FALSE"`
- **flg="PIXEL"**: `"[width, height]"` 形式の配列文字列（str型）、画像でない/存在しない場合は `"FALSE"`
- **flg="SIZE"**: ファイルサイズのバイト数（str型）、存在しない場合は `"FALSE"`

**機能**:
1. **存在チェック**: ファイルの有無を確認
2. **_NNNN検索**: 連番ファイルの最大番号を検索（例: `output_0003.png`）
3. **画像サイズ取得**: PNG/JPEG/WEBP等の画像ファイルの解像度を取得
4. **ファイルサイズ取得**: ファイルサイズをバイト単位で取得
5. **セキュリティ**: 絶対パス・UNCパス拒否（相対パスのみ許可）

**対象ディレクトリ**:
- ComfyUI環境: `ComfyUI/output/` 配下
- テスト環境: カレントディレクトリ配下

**例**:
```vba
' 基本的な存在チェック
exists = ISFILEEXIST("output.txt")
PRINT("exists = " & exists)
IF exists = "TRUE" THEN
    PRINT("ファイルは存在します")
ELSE
    PRINT("ファイルは存在しません")
END IF

' _NNNN付きファイルの最大番号検索
latestFile = ISFILEEXIST("ComfyUI_00001_.png", "NNNN")
PRINT("latestFile = " & latestFile)
IF latestFile <> "FALSE" THEN
    PRINT("最新ファイル: " & latestFile)
    ' 例: "ComfyUI_00005_.png"
ELSE
    PRINT("該当ファイルなし")
END IF

' 画像サイズ取得
imageSize = ISFILEEXIST("sample_image.png", "PIXEL")
PRINT("imageSize = " & imageSize)
IF imageSize <> "FALSE" THEN
    PRINT("画像サイズ: " & imageSize)
    ' 例: "[512, 768]"
ELSE
    PRINT("画像ファイルではありません")
END IF

' ファイルサイズ取得
fileSize = ISFILEEXIST("data.txt", "SIZE")
PRINT("fileSize = " & fileSize)
IF fileSize <> "FALSE" THEN
    PRINT("ファイルサイズ: " & fileSize & " bytes")
ELSE
    PRINT("ファイルが見つかりません")
END IF
```

**セキュリティ制限**:
- 絶対パス（`C:\...`, `/...`）は拒否
- UNCパス（`\\server\...`）は拒否
- 相対パスのみ許可

**_NNNN検索の仕様**:
- ファイル名パターン: `{base}_{number}.{ext}` 形式
- 番号は4桁ゼロパディング（例: `_0001`, `_0002`）
- 最大番号のファイルパスを返す
- 該当ファイルが存在しない場合は `"FALSE"`

**画像サイズ取得の対応フォーマット**:
- PNG, JPEG, JPG, BMP, WEBP
- 画像ファイルでない場合は `"FALSE"`

**注意**:
- すべての戻り値は文字列型（str）
- 存在チェック以外のモードでも、エラー時は `"FALSE"` を返す
- 画像サイズは `"[width, height]"` 形式の文字列（配列型ではない）

---

### VRAMFREE([min_free_vram_gb])

**説明**: VRAMとRAMを解放するための関数です。モデルのアンロード、キャッシュのクリア、ガベージコレクションを実行します。

**⚠️ WARNING**: モデルのアンロードはデリケートな操作です。実行タイミングによっては、ワークフロー実行中に予期しない動作を引き起こすリスクがあります。使用には十分注意してください。

**構文**:
```vba
result = VRAMFREE(min_free_vram_gb)
```

**パラメータ**:
- `min_free_vram_gb` (float, オプション): 実行閾値（GB単位）
  - 現在の空きVRAMがこの値以上の場合、処理をスキップします
  - デフォルト: 0.0（常に実行）

**戻り値**:
dict（実行結果の詳細情報）
- `success`: 実行成功フラグ（bool）
- `message`: 実行結果メッセージ（str）
- `freed_vram_gb`: 解放されたVRAM量（float）
- `freed_ram_gb`: 解放されたRAM量（float）
- `initial_status`: 実行前のメモリ状態（dict）
- `final_status`: 実行後のメモリ状態（dict）
- `actions_performed`: 実行されたアクションのリスト（list）

**使用例**:
```vba
' 常に実行（閾値なし）
result = VRAMFREE(0.0)
PRINT("VRAM freed: " & result["freed_vram_gb"] & " GB")

' 空きVRAMが2GB未満の場合のみ実行
result = VRAMFREE(2.0)
IF result["success"] = TRUE THEN
    PRINT("Cleanup completed")
ELSE
    PRINT("Cleanup failed")
END IF
```

**実行内容**:
1. 初期メモリ状態の取得
2. 閾値チェック（スキップ判定）
3. ComfyUI モデルのアンロード
4. ComfyUI ソフトキャッシュのクリア
5. PyTorch GPUキャッシュのクリア
6. Pythonガベージコレクション（GC）
7. ComfyUI prompt_queueへのフラグ設定
8. 非同期フラッシュの監視（3秒間）
9. メモリ解放量の計算

**注意事項**:
- ComfyUI環境外では、利用可能な機能が制限されます（limited mode）
- CUDA未対応環境では、VRAM情報が取得できない場合があります
- 非同期処理により、実行完了後も若干の遅延でメモリが解放される場合があります

---

### SLEEP([milliseconds])

**説明**: 指定したミリ秒だけ処理を一時停止します（スリープ）。WHILE()ループの速度制御や処理待ち合わせに使用します。

**引数**:
- milliseconds (FLOAT, オプション): スリープ時間（ミリ秒）、デフォルト: 10ms

**戻り値**: なし（内部的には0.0を返す）

**構文**:
```vba
SLEEP(milliseconds)
```

**使用例**:
```vba
' デフォルト10msスリープ
SLEEP()

' 0.5秒スリープ
SLEEP(500)

' WHILE()ループの速度制御（CPU使用率低減）
VAL1 = 0
WHILE VAL1 < 100
    VAL1 = VAL1 + 1
    SLEEP(100)  ' 100ms待機
WEND
PRINT("ループ完了: " & VAL1)
RETURN1 = VAL1

' 処理待ち合わせ
PRINT("処理開始")
result = VAL1 * 2
SLEEP(1000)  ' 1秒待機
PRINT("処理完了: " & result)
RETURN1 = result
```

**主な用途**:
1. **WHILE()ループの速度制御**: CPU使用率を低減し、システムへの負荷を軽減
2. **処理待ち合わせ**: 外部システムの応答待ちや、意図的な遅延処理
3. **デバッグ**: 処理の流れを観察するための一時停止

**ComfyUI統合**:
- ComfyUIのスレッドベースキューイング制御（ScriptExecutionQueue）と協調動作
- time.sleep()による同期的ブロッキング実行
- 複数EasyScripterノード同時実行時の安全性はScriptExecutionQueueが保証

**注意事項**:
- SLEEP()は現在のスレッドをブロックします（他の処理は実行されません）
- 非同期処理（asyncio）は使用していません（ComfyUIはイベントループ駆動ではない）
- 長時間のスリープはワークフロー全体の実行時間を増加させます

---

## 画像処理関数

### IMAGETOBYTEARRAY(image_input, [max_size], [format], [return_format])

**説明**: IMAGE tensorまたは画像ファイルパスを受け取り、リサイズ・圧縮してバイト配列またはJSON配列に変換します。主にREST APIへの送信用データとして使用します。

**引数**:
- image_input (str | torch.Tensor, 必須) - 画像ソース
  - 文字列: 画像ファイルパス（例: `"C:/path/to/image.png"`）
  - torch.Tensor: ComfyUI IMAGE形式 `[batch, height, width, channels]`
- max_size (int, オプション) - リサイズ後の最大サイズ（長辺、ピクセル）、デフォルト: 336
- format (str, オプション) - 出力画像フォーマット（"PNG", "JPEG"等）、デフォルト: "PNG"
- return_format (str, オプション) - 返却形式（"bytes"または"json"）、デフォルト: "bytes"

**戻り値**: 動的型（return_formatに応じて変化）
- **return_format="bytes"**: bytes型（生のバイナリデータ）
- **return_format="json"**: str型（JSON配列形式の文字列、例: `"[137, 80, 78, 71, ...]"`）

**機能**:
1. **IMAGE tensor対応**: ComfyUIノードから直接IMAGE型を受け取り可能
2. **ファイルパス対応**: 従来の画像ファイルパス指定も可能
3. **自動リサイズ**: アスペクト比を維持しながら指定サイズにリサイズ
4. **JPEG圧縮**: format="JPEG"指定時、quality=50で圧縮（ファイルサイズ削減）
5. **RGBA→RGB変換**: JPEG出力時、透明背景を白背景に自動変換
6. **JSON配列変換**: Cloudflare API等で直接使用可能な整数配列形式

**エンコーディング仕様**:
- Base64ではない
- MIMEエンコードではない
- return_format="bytes": 生のバイナリデータをbytes型で返す
- return_format="json": 整数配列 [0-255] のJSON文字列を返す
- Cloudflare APIでは、JSON配列形式が直接使用可能

**例**:
```vba
' ファイルパス入力（従来の方法）
json_array = IMAGETOBYTEARRAY("C:/path/to/image.png", 336, "JPEG", "json")
PRINT("JSON配列長: " & LEN(json_array))

' IMAGE tensor入力（ComfyUIノード接続から）
' VAL1にLoadImageノード等からIMAGE型が渡される
json_array = IMAGETOBYTEARRAY(VAL1, 336, "JPEG", "json")
RETURN1 = json_array

' Cloudflare Workers AI Image-to-Text API送信例
```

**セキュリティ制限**:
なし（ファイルパス指定時は、存在しないファイルでFileNotFoundError）

**エラー処理**:
- FileNotFoundError: 画像ファイルが存在しない（文字列入力時）
- RuntimeError: PIL (Pillow) 未インストール、画像処理エラー
- ValueError: return_format が無効、または画像サイズが不正
- TypeError: 無効な入力型（str/torch.Tensor以外）

**注意事項**:
- PIL (Pillow) ライブラリが必要です（`pip install Pillow`）
- torch.Tensorを扱う場合、PyTorchが必要です（ComfyUI環境では通常インストール済み）
- JPEG形式はquality=50で圧縮されるため、画質よりファイルサイズを優先します
- 大きな画像（4K等）をリサイズせずJSON変換すると、JSON文字列が巨大になる可能性があります

---

### IMAGETOBASE64(image_input, [max_size], [format], [return_format])

**説明**: IMAGE tensorまたは画像ファイルパスを受け取り、リサイズ・圧縮してBase64エンコードまたはdata URL形式に変換します。主にREST APIへの送信用データとして使用します。

**引数**:
- image_input (str | torch.Tensor, 必須) - 画像ソース
  - 文字列: 画像ファイルパス（例: `"C:/path/to/image.png"`）
  - torch.Tensor: ComfyUI IMAGE形式 `[batch, height, width, channels]`
- max_size (int, オプション) - リサイズ後の最大サイズ（長辺、ピクセル）、デフォルト: 512
- format (str, オプション) - 出力画像フォーマット（"PNG", "JPEG"等）、デフォルト: "PNG"
- return_format (str, オプション) - 返却形式（"base64"または"data_url"）、デフォルト: "base64"

**戻り値**: str型（return_formatに応じて変化）
- **return_format="base64"**: Base64エンコードされた文字列（例: `"iVBORw0KGgoAAAANSUhEUgAA..."`）
- **return_format="data_url"**: data URL形式の文字列（例: `"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."`）

**機能**:
1. **IMAGE tensor対応**: ComfyUIノードから直接IMAGE型を受け取り可能
2. **ファイルパス対応**: 従来の画像ファイルパス指定も可能
3. **自動リサイズ**: アスペクト比を維持しながら指定サイズにリサイズ
4. **JPEG圧縮**: format="JPEG"指定時、quality=85で圧縮（画質とサイズのバランス）
5. **RGBA→RGB変換**: JPEG出力時、透明背景を白背景に自動変換
6. **Base64エンコード**: 標準Base64エンコーディング、data URL形式にも対応

**エンコーディング仕様**:
- Base64標準エンコーディング
- return_format="base64": Base64文字列のみを返す
- return_format="data_url": data URL形式（`"data:image/png;base64,..."`）で返す
- Vision APIで直接使用可能

**例**:
```vba
' ファイルパス入力（Base64文字列）
base64_str = IMAGETOBASE64("C:/path/to/image.png", 512, "PNG", "base64")
PRINT("Base64長: " & LEN(base64_str))

' IMAGE tensor入力（data URL形式）
' ANY_INPUTにLoadImageノード等からIMAGE型が渡される
data_url = IMAGETOBASE64(ANY_INPUT, 512, "PNG", "data_url")
RETURN1 = data_url
```

**セキュリティ制限**:
なし（ファイルパス指定時は、存在しないファイルでFileNotFoundError）

**エラー処理**:
- FileNotFoundError: 画像ファイルが存在しない（文字列入力時）
- RuntimeError: PIL (Pillow) 未インストール、画像処理エラー
- ValueError: return_format が無効、または画像サイズが不正
- TypeError: 無効な入力型（str/torch.Tensor以外）

**注意事項**:
- PIL (Pillow) ライブラリが必要です（`pip install Pillow`）
- torch.Tensorを扱う場合、PyTorchが必要です（ComfyUI環境では通常インストール済み）
- JPEG形式はquality=85で圧縮されます（高品質とファイルサイズのバランス）
- 大きな画像（4K等）をリサイズせずBase64変換すると、文字列が巨大になる可能性があります
- data URL形式は画像データ全体を文字列に含むため、JSONボディが大きくなります

---

## 画像・Latentデータ取得関数

### GETANYWIDTH([any_data])

**説明**: IMAGE/LATENT型データの幅（ピクセル数）を取得

**引数**:
- any_data (torch.Tensor, optional) - IMAGE/LATENTデータ
  - 引数なしの場合、any_input入力ソケットのデータを自動使用

**戻り値**: float - 幅（ピクセル数、取得できない場合は0.0）

**対応形式**:
- IMAGE型: torch.Tensor形式 `[batch, height, width, channels]`
- LATENT型: torch.Tensor形式 `[batch, channels, height, width]`

**例**:
```vba
' any_input入力ソケットから自動取得
width = GETANYWIDTH()
PRINT("幅: " & width)
RETURN1 = width

' 明示的にデータを指定
imageData = INPUT("sample.png")
w = GETANYWIDTH(imageData)
PRINT("画像幅: " & w)
```

---

### GETANYHEIGHT([any_data])

**説明**: IMAGE/LATENT型データの高さ（ピクセル数）を取得

**引数**:
- any_data (torch.Tensor, optional) - IMAGE/LATENTデータ
  - 引数なしの場合、any_input入力ソケットのデータを自動使用

**戻り値**: float - 高さ（ピクセル数、取得できない場合は0.0）

**対応形式**:
- IMAGE型: torch.Tensor形式 `[batch, height, width, channels]`
- LATENT型: torch.Tensor形式 `[batch, channels, height, width]`

**例**:
```vba
' any_input入力ソケットから自動取得
height = GETANYHEIGHT()
PRINT("高さ: " & height)
RETURN2 = height

' 解像度に応じた条件分岐
w = GETANYWIDTH()
h = GETANYHEIGHT()
IF w >= 1024 AND h >= 1024 THEN
    PRINT("高解像度画像")
    scale = 1.0
ELSE
    PRINT("標準解像度画像")
    scale = 2.0
END IF
RETURN1 = scale
```

---

### GETANYTYPE([any_data])

**説明**: ANY型データの型名を判定

**引数**:
- any_data (Any, optional) - 型判定対象のデータ
  - 引数なしの場合、any_input入力ソケットのデータを自動使用

**戻り値**: str - 型名
- "int", "float", "string" - 基本型
- "image", "latent" - 画像・Latent
- "model", "vae", "clip" - ComfyUIモデル型
- "conditioning", "control_net", "clip_vision", "style_model", "gligen", "lora" - ComfyUI固有型
- "none" - None値
- "unknown" - 判定不能

**例**:
```vba
' any_input入力ソケットから自動判定
type_name = GETANYTYPE()
PRINT("型: " & type_name)

SELECT CASE type_name
    CASE "image"
        w = GETANYWIDTH()
        h = GETANYHEIGHT()
        PRINT("IMAGE型: " & w & "x" & h)
    CASE "latent"
        PRINT("LATENT型です")
    CASE "model"
        PRINT("MODEL型です")
    CASE "string"
        PRINT("STRING型です")
    CASE ELSE
        PRINT("その他の型: " & type_name)
END SELECT
```

---

### GETANYVALUEINT([any_data])

**説明**: ANY型データから整数値を取得

**引数**:
- any_data (Any, optional) - データ
  - 引数なしの場合、any_input入力ソケットのデータを自動使用

**戻り値**: int - 整数値（取得できない場合は0）

**例**:
```vba
' any_input入力ソケットから整数値取得
int_value = GETANYVALUEINT()
PRINT("整数値: " & int_value)
RETURN1 = int_value
```

---

### GETANYVALUEFLOAT([any_data])

**説明**: ANY型データから浮動小数点値を取得

**引数**:
- any_data (Any, optional) - データ
  - 引数なしの場合、any_input入力ソケットのデータを自動使用

**戻り値**: float - 浮動小数点値（取得できない場合は0.0）

**例**:
```vba
' any_input入力ソケットから浮動小数点値取得
float_value = GETANYVALUEFLOAT()
PRINT("浮動小数点値: " & float_value)
RETURN1 = float_value
```

---

### GETANYSTRING([any_data])

**説明**: ANY型データから文字列を取得

**引数**:
- any_data (Any, optional) - データ
  - 引数なしの場合、any_input入力ソケットのデータを自動使用

**戻り値**: str - 文字列（取得できない場合は空文字列）

**例**:
```vba
' any_input入力ソケットから文字列取得
str_value = GETANYSTRING()
PRINT("文字列: " & str_value)
RETURN1 = str_value
```

---

## 型判定関数

### ISNUMERIC(value)

**説明**: 値が数値かどうかを判定

**引数**:
- value - 検査する値

**戻り値**: 1（数値）または0（非数値）

**例**:
```vba
result = ISNUMERIC("123")      ' 1
PRINT("ISNUMERIC('123') = " & result)
result = ISNUMERIC("12.34")    ' 1
PRINT("ISNUMERIC('12.34') = " & result)
result = ISNUMERIC("abc")      ' 0
PRINT("ISNUMERIC('abc') = " & result)
result = ISNUMERIC("")         ' 0
PRINT("ISNUMERIC('') = " & result)

' 実用例：入力値の検証
IF ISNUMERIC(TXT1) THEN
    value = CDBL(TXT1)
    PRINT("数値として処理: " & value)
ELSE
    PRINT("エラー: 数値ではありません")
END IF
```

---

### ISDATE(value)

**説明**: 値が日付として解析可能かを判定

**引数**:
- value - 検査する値

**戻り値**: 1（日付）または0（非日付）

**例**:
```vba
result = ISDATE("2024-01-15")     ' 1
PRINT("ISDATE('2024-01-15') = " & result)
result = ISDATE("2024/01/15")     ' 1
PRINT("ISDATE('2024/01/15') = " & result)
result = ISDATE("15:30:00")       ' 1（時刻も判定可）
PRINT("ISDATE('15:30:00') = " & result)
result = ISDATE("hello")          ' 0
PRINT("ISDATE('hello') = " & result)

' 実用例：日付の検証
IF ISDATE(TXT1) THEN
    dateVal = DATEVALUE(TXT1)
    PRINT("日付として処理します: " & dateVal)
ELSE
    PRINT("エラー: 日付形式ではありません")
END IF
```

**対応フォーマット**:
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

**説明**: 変数が配列かどうかを判定

**引数**:
- variable_name - 変数名（文字列）または配列変数参照（ARR[]記法）

**戻り値**: 1（配列）または0（非配列）

**例**:
```vba
REDIM arr, 10
result = ISARRAY(arr[])      ' 1（配列参照）
PRINT("ISARRAY(arr[]) = " & result)
result = ISARRAY("arr")      ' 1（配列名文字列）
PRINT("ISARRAY('arr') = " & result)
result = ISARRAY("VAL1")     ' 0（通常変数）
PRINT("ISARRAY('VAL1') = " & result)

' 実用例：変数の型確認
REDIM myData, 5
myData[0] = "a"
myData[1] = "b"
IF ISARRAY(myData[]) THEN
    PRINT("配列です。要素数: " & (UBOUND(myData[]) + 1))
ELSE
    PRINT("配列ではありません")
END IF
```

**注意**:
- 配列名を文字列として渡すか、ARR[]記法で配列変数参照を渡してください

---

### TYPE(value)

**説明**: 変数の型を文字列で返す

**引数**:
- value - 型を調べたい値

**戻り値**: 型名（"NUMBER", "STRING", "BOOLEAN", "ARRAY", "NULL", "OBJECT"）

**例**:
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

' 実用例：汎用的な型処理
myValue = VAL1
dataType = TYPE(myValue)
PRINT("TYPE(myValue) = " & dataType)
SELECT CASE dataType
    CASE "NUMBER"
        PRINT("数値: " & myValue)
    CASE "STRING"
        PRINT("文字列: " & myValue)
    CASE "ARRAY"
        PRINT("配列（要素数: " & (UBOUND(myValue[]) + 1) & "）")
    CASE "NULL"
        PRINT("値がありません")
END SELECT
```

---

## 実用例

### デバッグ出力の活用

```vba
' 処理の各段階で値を確認
originalValue = VAL1
PRINT("元の値: " & originalValue)

processedValue = originalValue * 2
PRINT("2倍後: " & processedValue)

finalValue = processedValue + 10
PRINT("最終値: " & finalValue)

RETURN1 = finalValue
PRINT("RETURN1に代入: " & RETURN1)
```

### 入力値の検証

```vba
' 数値かどうかチェックしてから処理
IF ISNUMERIC(TXT1) THEN
    number = CDBL(TXT1)
    PRINT("TXT1を数値に変換: " & number)
    result = number * VAL1
    PRINT("計算結果: " & result)
    RETURN1 = result
    PRINT("RETURN1に代入: " & RETURN1)
ELSE
    PRINT("エラー: TXT1は数値ではありません")
    RETURN1 = 0
    PRINT("RETURN1にデフォルト値を代入: " & RETURN1)
END IF
```

### 型に応じた処理分岐

```vba
' データ型に応じて処理を変える
myData = VAL1
dataType = TYPE(myData)
PRINT("TYPE(myData) = " & dataType)

IF dataType = "NUMBER" THEN
    result = myData * 2
    PRINT("数値処理: " & result)
ELSEIF dataType = "STRING" THEN
    result = UCASE(myData)
    PRINT("文字列処理: " & result)
ELSEIF dataType = "ARRAY" THEN
    count = UBOUND(myData[]) + 1
    PRINT("配列処理: 要素数=" & count)
    FOR i = 0 TO UBOUND(myData[])
        PRINT("  [" & i & "] = " & myData[i])
    NEXT
ELSE
    PRINT("未対応の型: " & dataType)
END IF
```

---

[← ビルトイン関数索引に戻る](00_index.md)
