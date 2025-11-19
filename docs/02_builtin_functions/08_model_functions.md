# モデル関数リファレンス

[← ビルトイン関数索引に戻る](00_index.md)

## 概要

モデル関数は、ComfyUIで使用する各種生成モデルの最適解像度を自動判定する機能を提供します。モデル名とアスペクト比から、そのモデルに最適なLatent空間のサイズを自動的に計算します。

対応モデル: Stable Diffusion 1.5/2.1/XL、SD3/3.5、FLUX.1、Hunyuan-DiT、Kandinsky、PixArt、Playground等（30種類以上）

---

## モデル関数一覧

### OPTIMAL_LATENT(model_hint, width, height)

**説明**: モデル名とアスペクト比から最適なLatentサイズを自動判定

**引数**:
- model_hint - モデル名のヒント（文字列）
  - 例: "SDXL", "SD 1.5", "Flux", "Hunyuan"
- width - 希望する幅（整数）
- height - 希望する高さ（整数）

**戻り値**: 最適なLatentサイズの配列 [width, height]

**サポートモデル**: SD1.5, SD2.1, SDXL, SD3/3.5, Hunyuan-DiT, FLUX.1, Kandinsky, PixArt, Playground等（30+モデル）

**例**:
```vba
' SDXL最適な4:3解像度を取得
DIM result
result = OPTIMAL_LATENT("SDXL", 4, 3)
PRINT(result)  ' 中間結果確認
PRINT("Optimal Size: " & result(0) & "x" & result(1))
' 出力: "Model: SDXL 1.0 (base) | Optimal: 1152x896 (4:3)"
' 出力: "{0: 1152, 1: 896}"
' 出力: "Optimal Size: 1152x896"

' Stable Diffusion 1.5で16:9を取得
result = OPTIMAL_LATENT("SD 1.5", 16, 9)
PRINT(result)  ' 中間結果確認
PRINT(result(0) & "x" & result(1))
' 出力: "Model: blue_pencil（SD1.5） | Optimal: 704x384 (11:6)"
' 出力: "{0: 704, 1: 384}"
' 出力: "704x384"

' FLUX.1で正方形
result = OPTIMAL_LATENT("Flux", 256, 256)
PRINT(result)  ' 中間結果確認
' 出力: "Model: FLUX.1 (dev/pro) | Optimal: 1024x1024 (1:1)"
' 出力: "{0: 1024, 1: 1024}"
```

---

## モデルデータの更新

新しいモデルを追加する場合は、`data/model_resolutions.csv`を編集してください。

**CSVフォーマット**:
```csv
model_key,model_display_name,aliases,version,width,height,aspect_ratio,description
new_model,New Model v1.0,newmodel|new,1.0,1024,1024,1:1,説明
```

**注意**: ComfyUIを再起動すると新しいデータが反映されます。

---

## 使用例

### SDXLワークフローでの最適解像度判定

```vba
' ユーザー入力の解像度からSDXLに最適な解像度を自動計算
DIM user_width
DIM user_height
user_width = 1920  ' フルHD幅
PRINT(user_width)  ' 中間結果確認
' 出力: "1920"
user_height = 1080 ' フルHD高さ
PRINT(user_height)  ' 中間結果確認
' 出力: "1080"

DIM optimal
optimal = OPTIMAL_LATENT("SDXL", user_width, user_height)
PRINT(optimal)  ' 中間結果確認
' 出力: "Model: SDXL 1.0 (base) | Optimal: 1344x768 (16:9)"
' 出力: "{0: 1344, 1: 768}"

' optimal配列から最適な幅と高さを取得
DIM final_width
DIM final_height
final_width = optimal(0)
PRINT(final_width)  ' 中間結果確認
' 出力: "1344"
final_height = optimal(1)
PRINT(final_height)  ' 中間結果確認
' 出力: "768"

PRINT("Input: " & user_width & "x" & user_height)
PRINT("SDXL Optimal: " & final_width & "x" & final_height)
' 出力: "Input: 1920x1080"
' 出力: "SDXL Optimal: 1344x768"
```

### 複数モデル対応の汎用スクリプト

```vba
' モデル名を変更するだけで各モデルの最適解像度を取得
DIM model_name
DIM aspect_width
DIM aspect_height

model_name = "Flux"
PRINT(model_name)  ' 中間結果確認
' 出力: "Flux"
aspect_width = 1024
PRINT(aspect_width)  ' 中間結果確認
' 出力: "1024"
aspect_height = 1024
PRINT(aspect_height)  ' 中間結果確認
' 出力: "1024"

DIM result
result = OPTIMAL_LATENT(model_name, aspect_width, aspect_height)
PRINT(result)  ' 中間結果確認
' 出力: "Model: FLUX.1 (dev/pro) | Optimal: 1024x1024 (1:1)"
' 出力: "{0: 1024, 1: 1024}"
PRINT(model_name & " -> " & result(0) & "x" & result(1))
' 出力: "Flux -> 1024x1024"

' SD1.5に変更
model_name = "SD 1.5"
PRINT(model_name)  ' 中間結果確認
' 出力: "SD 1.5"
result = OPTIMAL_LATENT(model_name, aspect_width, aspect_height)
PRINT(result)  ' 中間結果確認
' 出力: "Model: blue_pencil（SD1.5） | Optimal: 512x512 (1:1)"
' 出力: "{0: 512, 1: 512}"
PRINT(model_name & " -> " & result(0) & "x" & result(1))
' 出力: "SD 1.5 -> 512x512"
```

---

[← ビルトイン関数索引に戻る](00_index.md)
