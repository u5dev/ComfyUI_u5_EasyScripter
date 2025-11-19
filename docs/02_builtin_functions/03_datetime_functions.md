# 日時関数リファレンス

[← ビルトイン関数索引に戻る](00_index.md)

u5 EasyScripterで使用できる日時関数の完全リファレンスです。

## 関数一覧
12個の日時関数を提供しています。

---

### NOW()
**説明**: 現在の日時を取得
**引数**: なし
**戻り値**: 日時文字列（YYYY-MM-DD HH:MM:SS）
**例**:
```vba
currentTime = NOW()
PRINT(currentTime)    ' "2024-01-15 14:30:45"
PRINT("現在時刻: " & NOW())
```

### DATE()
**説明**: 今日の日付を取得
**引数**: なし
**戻り値**: 日付文字列（YYYY-MM-DD）
**例**:
```vba
today = DATE()
PRINT(today)    ' "2024-01-15"
```

### TIME()
**説明**: 現在時刻を取得
**引数**: なし
**戻り値**: 時刻文字列（HH:MM:SS）
**例**:
```vba
currentTime = TIME()
PRINT(currentTime)    ' "14:30:45"
```

### YEAR([date])
**説明**: 年を取得
**引数**: date - 日付文字列（省略時:今日）
**戻り値**: 年（数値）
**例**:
```vba
result = YEAR()
PRINT(result)              ' 2024（今年）
result = YEAR("2023-12-25")
PRINT(result)              ' 2023
```

### MONTH([date])
**説明**: 月を取得
**引数**: date - 日付文字列（省略時:今日）
**戻り値**: 月（1-12）
**例**:
```vba
result = MONTH()
PRINT(result)             ' 1（今月）
result = MONTH("2023-12-25")
PRINT(result)             ' 12
```

### DAY([date])
**説明**: 日を取得
**引数**: date - 日付文字列（省略時:今日）
**戻り値**: 日（1-31）
**例**:
```vba
result = DAY()
PRINT(result)               ' 15（今日）
result = DAY("2023-12-25")
PRINT(result)               ' 25
```

### HOUR([time])
**説明**: 時を取得
**引数**: time - 時刻文字列（省略時:現在）
**戻り値**: 時（0-23）
**例**:
```vba
result = HOUR()
PRINT(result)              ' 14（現在の時）
result = HOUR("15:30:45")
PRINT(result)              ' 15
```

### MINUTE([time])
**説明**: 分を取得
**引数**: time - 時刻文字列（省略時:現在）
**戻り値**: 分（0-59）
**例**:
```vba
result = MINUTE()
PRINT(result)            ' 30（現在の分）
result = MINUTE("15:30:45")
PRINT(result)            ' 30
```

### SECOND([time])
**説明**: 秒を取得
**引数**: time - 時刻文字列（省略時:現在）
**戻り値**: 秒（0-59）
**例**:
```vba
result = SECOND()
PRINT(result)            ' 45（現在の秒）
result = SECOND("15:30:45")
PRINT(result)            ' 45
```

### DATEADD(interval, number, [date])
**説明**: 日付に加算/減算
**引数**:
- interval - 単位（"d"=日, "m"=月, "y"=年, "h"=時, "n"=分, "s"=秒）
- number - 加算する数値
- date - 基準日時（省略時:現在）
**戻り値**: 計算後の日時（YYYY/MM/DD HH:MM:SS形式）
**例**:
```vba
tomorrow = DATEADD("d", 1, DATE())
PRINT(tomorrow)        ' 明日（例: "2025/10/23 00:00:00"）
nextMonth = DATEADD("m", 1, "2024-01-15")
PRINT(nextMonth)       ' "2024/02/15 00:00:00"
inOneHour = DATEADD("h", 1, NOW())
PRINT(inOneHour)       ' 1時間後（例: "2025/10/22 15:30:00"）
```

### DATEDIFF(interval, date1, [date2])
**説明**: 日付の差を計算
**引数**:
- interval - 単位（"d"=日, "m"=月, "y"=年, "h"=時, "n"=分, "s"=秒）
- date1 - 開始日時
- date2 - 終了日時（省略時:現在）
**戻り値**: 差（数値）
**例**:
```vba
days = DATEDIFF("d", "2024-01-01", "2024-01-15")
PRINT(days)  ' 14
age = DATEDIFF("y", "1990-01-01", DATE())
PRINT(age)   ' 年齢
hours = DATEDIFF("h", "2024-01-15 10:00:00", NOW())
PRINT(hours) ' 経過時間
```

### CDATE(date_string)
**説明**: 日付文字列を日付型に変換（VBA互換）
**引数**: date_string - 日付を表す文字列
**戻り値**: 日付文字列（YYYY/MM/DD HH:MM:SS形式）
**柔軟なフォーマット対応**:
- 完全な日時: `"2025/11/05 15:39:49"` → `2025/11/05 15:39:49`
- 日付のみ: `"2025/11/05"` → `2025/11/05 00:00:00` （時刻は00:00:00）
- 年月のみ: `"2025/11"` → `2025/11/01 00:00:00` （日=1、時刻=00:00:00）
- 年のみ: `"2025"` → `2025/01/01 00:00:00` （月日=1/1、時刻=00:00:00）
- 時のみ: `"2025/11/05 15"` → `2025/11/05 15:00:00` （分秒=00）
- 時分のみ: `"2025/11/05 15:39"` → `2025/11/05 15:39:00` （秒=00）

**区切り文字の柔軟性**:
- `/` と `-` と `:` と空白の混在を許容
- `"2025-11-05-15-39-49"` も `"2025-11-05 15-39-49"` も `"2025-11-05 15:39:49"` も同様に処理

**例**:
```vba
' 完全な日時
result = CDATE("2025/11/05 15:39:49")
PRINT(result)  ' "2025/11/05 15:39:49"

' 日付のみ（時刻は00:00:00になる）
result = CDATE("2025/11/05")
PRINT(result)  ' "2025/11/05 00:00:00"

' 区切り文字の混在OK
result = CDATE("2025-11-05 15:39:49")
PRINT(result)  ' "2025/11/05 15:39:49"

' 部分的な日付（不足部分は補完される）
result = CDATE("2025/11")
PRINT(result)  ' "2025/11/01 00:00:00"
```

---

[← ビルトイン関数索引に戻る](00_index.md)
