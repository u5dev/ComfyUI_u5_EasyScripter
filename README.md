# u5 EasyScripter Node

**Languages**: [English](docs/en/README.md) | [中文](docs/zh/README.md) | [Spanish](docs/es/README.md) | [French](docs/fr/README.md) | [German](docs/de/README.md)

## これは何？
- ComfyUI上で、VBAライクの**簡単スクリプトを動かせる**カスタムノードです
- 条件分岐やプロンプト形成をはじめ、繰り返し処理、外部API呼び出しなど様々な組み込みが可能です。
- **ほぼ全部の関数にコピペ用サンプル**を提供していますので、プログラム経験が無くても大丈夫
- 他で公開中のシーケンシャルノードやメモリ開放ツールも強化してビルトインしています

```
標準ノードや個別のノードでは構成が冗長になり、きめ細かな制御が大変だったので作りました
```

---

## おすすめ機能・用途
 - ワークフローのスクリーンショット画像をComfyUIに放り込んですぐ使えます

### とにかく色んなバリエーションを勝手に作って
- 毎回プロンプト考えるの面倒です。手っ取り早くスライドショー的に数出して！
```vba
'ベースプロンプト + 毎回ランダムな表情とポーズに入れ替えてプロンプトを作る
'→"base prompt" & "," & RNDCSV("ポーズ候補のCSV") & "," & RNDCSV("表情候補のCSV")

RETURN1 = "woman, a girl, nurse, with a bandage, pale skin, green eyes, pink hair, blunt bangs,upper body, full body shot, masterpiece, best quality, high quality," & RNDCSV("looking at viewer, looking away, looking back, wink, making a peace sign, making a heart with hands, making a thumbs up, waving at the camera") & "," & RNDCSV("blush, smiling, embarrassed, sleepy, serious expression, fear")
```
<img src="docs/img/AUTO_SLIDESHOW.png" alt="EasyScripterノードでのプロンプト生成スクリプト例" width="80%"><br>
  ↓<br>
  1行張り付けるだけで<br>
  ↓<br>
<img src="docs/img/SLIDES.png" alt="自動生成されたバリエーション画像のスライドショー" width="100%">

### モデルに特化したLatent(潜在)サイズを一発で自動調整
- これはSDXLだから解像度がどうとか、いちいちやってられませんよね！
```vba
result = OPTIMAL_LATENT("SDXL", 4, 3) ' 勝手に1152x896に調整される
RETURN1 = RESULT[0] '1152
RETURN2 = RESULT[1] '896
```
<img src="docs/img/OPTIMAL_LATENT.png" alt="OPTIMAL_LATENT関数によるモデル最適化解像度自動調整の例" width="80%"><br>



**Node下段のスクリプトウインドウに張り付けるだけで、特殊機能を持つプロフェッショナルなノードに早変わりです**

---




## 📖 ドキュメント

詳細なドキュメントは以下をご覧ください：


- **[📖 スクリプト言語リファレンス](docs/01_syntax_reference.md)** - 文法と制御構造の完全ガイド
- **[🔧 ビルトイン関数リファレンス](docs/02_builtin_functions/00_index.md)** - 100+個のビルトイン関数の完全リファレンス
- **[🌟 ご支援おねがいします](docs/CONTENTS.md)** - より実践的で便利な作例、豊富なワークフロー画像、詳細な解説


---

## u5 EasyScripterによる解決策

**一つのノード、無限の可能性** - u5 EasyScripterはComfy UI上で動く汎用スクリプトエンジンです：

- ✅ **10+の専用ノードを置換**: テキスト処理、数学計算、条件ロジック、ランダム生成
- ✅ **バッチ処理を加速**: 自動パラメータスイープ、インテリジェントなバリエーション生成
- ✅ **プロンプトエンジニアリングを強化**: 動的ウェイト調整、条件分岐による修正、スマートバリエーション
- ✅ **ワークフローを効率化**: クリーンなグラフ、高速読み込み、簡単共有
- ✅ **スケーラブル**: 簡単な計算から複雑な自動化アルゴリズムまで対応
- ✅ **並行実行ガード**: 複数ノードの同時実行時もハングアップせず、安全にキューイング処理
- ✅ **多言語対応**: 日本語と英語のエラーメッセージとデバッグ出力に対応



---

## ⚡ クイックスタート

### インストール

```bash
# ComfyUIのcustom_nodesディレクトリにクローン
git clone https://github.com/u5dev/ComfyUI_u5_EasyScripter.git
```

### 最初のスマートワークフロー
- モデルタイプが要求するプロンプトルールに基づくインテリジェントな調整

```vba

model_type = TXT1  ' モデル名を接続("sdxl"or"Flux")
PRINT(model_type)  ' モデルタイプ確認
base_prompt = "beautiful landscape"

SELECT CASE model_type
    CASE "sdxl"
        RETURN1 = "(" & base_prompt & ", ultra-detailed wide landscape, crisp daylight photography, shot on full-frame DSLR, high dynamic range, 8k uhd, professional photography:1.2)"
        PRINT(RETURN1)  ' SDXLプロンプト確認
    CASE "flux"
        RETURN1 = "(" & base_prompt & "moody cinematic wide shot of a beautiful landscape at golden hour, dramatic backlight haze, soft volumetric light, cinematic lighting:1.1, subtle film grain)"
        PRINT(RETURN1)  ' Fluxプロンプト確認
    CASE ELSE
        RETURN1 = base_prompt & ", high quality"
        PRINT(RETURN1)  ' デフォルトプロンプト確認
END SELECT
```
<img src="docs/img/FIRST_WORFLOW.png" alt="モデルタイプ別プロンプト調整のワークフロー例" width="50%">


---

## 💡 基本的な使い方

### ノード構成

**EasyScripterノード**は以下の構成です：

#### 入力
- `script`: VBAスタイルスクリプトを記述（必須）
- `VAL1_int`, `VAL1_float`: 数値入力1（合算して`VAL1`として利用可能）
- `VAL2_int`, `VAL2_float`: 数値入力2（合算して`VAL2`として利用可能）
- `TXT1`, `TXT2`: テキスト入力
- `any_input`: ANY型入力（MODEL, CLIP, VAE等すべて受け入れ）

#### 出力
- `RETURN1_int`, `RETURN1_float`, `RETURN1_text`: 主要戻り値（3形式で同時出力）
- `RETURN2_int`, `RETURN2_float`, `RETURN2_text`: サブ戻り値（3形式で同時出力）
- `relay_output`: `any_input`の完全バイパス出力（RELAY_OUTPUT変数で制御可能）


![EasyScripterノードの基本的な接続例](docs/img/SimpleConnection.png)



### 簡単な例
上のワークフローに、コピペしてみてください

#### 基本的な計算
```vba
' 2つの値を足して返す
result = VAL1 + VAL2
PRINT(result)  ' 計算結果を確認
RETURN1 = result
```

#### 文字列連結
```vba
' 2つのテキストを結合
combined = TXT1 & " " & TXT2
PRINT(combined)  ' 結合結果を確認
RETURN1 = combined
```

#### 条件分岐
```vba
' 値に応じてメッセージを変更
IF VAL1 > 10 THEN
    RETURN1 = "大きい"
    PRINT(RETURN1)  ' 分岐結果を確認
ELSE
    RETURN1 = "小さい"
    PRINT(RETURN1)  ' 分岐結果を確認
END IF
```

**1行IF文とEXIT文**（v2.1.1以降）:
```vba
' 関数内での早期リターン
FUNCTION Validate(value)
    IF value < 0 THEN EXIT FUNCTION  ' 負の値なら即終了
    Validate = value * 2
END FUNCTION

' ループの早期終了
FOR i = 1 TO 100
    IF i > 50 THEN EXIT FOR  ' 50を超えたらループ終了
    sum = sum + i
NEXT


RETURN1 = sum
RETURN2 = i
```

#### ランダム選択
```vba
' CSVからランダムに選択（インデックス省略時）
styles = "realistic, anime, oil painting, watercolor"
selected = PICKCSV(styles)  ' ランダム選択
PRINT(selected)  ' 選択結果を確認
RETURN1 = selected

' または特定のインデックスを指定（1ベース）
' selected = PICKCSV(styles, 2)  ' 2番目の"anime"を選択
' PRINT(selected)  ' "anime"
```

---

## 🛠️ u5ローダーシリーズ

EasyScripterと組み合わせて使える、ファイル名出力機能付きローダーノード群：

- **u5 Checkpoint Loader** - MODEL, CLIP, VAE + ファイル名出力
- **u5 LoRA Loader** - モデル + LoRA適用 + ファイル名出力
- **u5 VAE Loader** - VAE + ファイル名出力
- **u5 ControlNet Loader** - ControlNet + ファイル名出力
- **u5 CLIP Vision Loader** - CLIP Vision + ファイル名出力
- **u5 Style Model Loader** - StyleModel + ファイル名出力
- **u5 GLIGEN Loader** - GLIGEN + ファイル名出力
- **u5 UNET Loader** - UNET + ファイル名出力
- **u5 CLIP Loader** - CLIP + ファイル名出力

すべてのu5ローダーは以下の共通機能を持ちます：
- `text_input`フィールドによるファイル名検索指定（部分一致）して読み込み
- `filename`出力でロードしたファイル名をテキストとして出力


---


## 🔍 トラブルシューティング

### スクリプトがエラーになる
- PRINT関数でデバッグ出力を確認する場合は、括弧付き関数形式`PRINT("LOG", 値)`を使用してください
  - **注意**: VBAのステートメント形式（`PRINT "LOG", 値`）は未サポートです
- 変数名のスペルミスや大文字小文字をチェック

### 関数が見つからない
- 関数名のスペルを確認してください
- [ビルトイン関数索引](docs/02_builtin_functions/00_index.md) で正しい関数名を確認

### 戻り値が期待と違う
- PRINT関数で中間値を確認する場合も、括弧付き形式（`PRINT("中間値:", 変数)`）で呼び出してください
- 型変換（CINT, CDBL, CSTR）が必要かチェック

### 見た目が変
 - ワークフローを保存してF5更新してみてください

---

## 📜 ライセンス

MIT License

Copyright (c) 2025 u5 EasyScripter

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 📝 更新履歴

詳細なバージョン履歴は [CHANGELOG.md](docs/CHANGELOG.md) を参照してください。

---

## 🙏 謝辞

ComfyUIコミュニティの皆様に感謝します。

