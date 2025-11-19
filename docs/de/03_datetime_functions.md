# Datums- und Zeitfunktionen-Referenz

**Sprachen**: [English](../02_builtin_functions/03_datetime_functions.md) | [日本語](../02_builtin_functions/03_datetime_functions.md) | [한국어](../ko/03_datetime_functions.md) | [Français](../fr/03_datetime_functions.md) | **Deutsch** | [Español](../es/03_datetime_functions.md)

![](../img/comfyui_u5_easyscripter_banner_800x200.png)

[← Zurück zum Index der integrierten Funktionen](00_index.md)

Vollständige Referenz der Datums- und Zeitfunktionen, die in u5 EasyScripter verfügbar sind.

## Funktionsliste
12 Datums- und Zeitfunktionen werden bereitgestellt.

---

### NOW()
**Beschreibung**: Aktuelles Datum und Uhrzeit abrufen
**Argumente**: Keine
**Rückgabewert**: Datums-/Zeitzeichenkette (YYYY-MM-DD HH:MM:SS)
**Beispiel**:
```vba
currentTime = NOW()
PRINT(currentTime)    ' "2024-01-15 14:30:45"
PRINT("Aktuelle Zeit: " & NOW())
```

### DATE()
**Beschreibung**: Heutiges Datum abrufen
**Argumente**: Keine
**Rückgabewert**: Datumszeichenkette (YYYY-MM-DD)
**Beispiel**:
```vba
today = DATE()
PRINT(today)    ' "2024-01-15"
```

### TIME()
**Beschreibung**: Aktuelle Uhrzeit abrufen
**Argumente**: Keine
**Rückgabewert**: Zeitzeichenkette (HH:MM:SS)
**Beispiel**:
```vba
currentTime = TIME()
PRINT(currentTime)    ' "14:30:45"
```

### YEAR([date])
**Beschreibung**: Jahr abrufen
**Argumente**: date - Datumszeichenkette (Standard: heute)
**Rückgabewert**: Jahr (numerisch)
**Beispiel**:
```vba
result = YEAR()
PRINT(result)              ' 2024 (dieses Jahr)
result = YEAR("2023-12-25")
PRINT(result)              ' 2023
```

### MONTH([date])
**Beschreibung**: Monat abrufen
**Argumente**: date - Datumszeichenkette (Standard: heute)
**Rückgabewert**: Monat (1-12)
**Beispiel**:
```vba
result = MONTH()
PRINT(result)             ' 1 (dieser Monat)
result = MONTH("2023-12-25")
PRINT(result)             ' 12
```

### DAY([date])
**Beschreibung**: Tag abrufen
**Argumente**: date - Datumszeichenkette (Standard: heute)
**Rückgabewert**: Tag (1-31)
**Beispiel**:
```vba
result = DAY()
PRINT(result)               ' 15 (heute)
result = DAY("2023-12-25")
PRINT(result)               ' 25
```

### HOUR([time])
**Beschreibung**: Stunde abrufen
**Argumente**: time - Zeitzeichenkette (Standard: jetzt)
**Rückgabewert**: Stunde (0-23)
**Beispiel**:
```vba
result = HOUR()
PRINT(result)              ' 14 (aktuelle Stunde)
result = HOUR("15:30:45")
PRINT(result)              ' 15
```

### MINUTE([time])
**Beschreibung**: Minute abrufen
**Argumente**: time - Zeitzeichenkette (Standard: jetzt)
**Rückgabewert**: Minute (0-59)
**Beispiel**:
```vba
result = MINUTE()
PRINT(result)            ' 30 (aktuelle Minute)
result = MINUTE("15:30:45")
PRINT(result)            ' 30
```

### SECOND([time])
**Beschreibung**: Sekunde abrufen
**Argumente**: time - Zeitzeichenkette (Standard: jetzt)
**Rückgabewert**: Sekunde (0-59)
**Beispiel**:
```vba
result = SECOND()
PRINT(result)            ' 45 (aktuelle Sekunde)
result = SECOND("15:30:45")
PRINT(result)            ' 45
```

### DATEADD(interval, number, [date])
**Beschreibung**: Datum addieren/subtrahieren
**Argumente**:
- interval - Einheit ("d"=Tag, "m"=Monat, "y"=Jahr, "h"=Stunde, "n"=Minute, "s"=Sekunde)
- number - Zu addierende Zahl
- date - Referenzdatum/-zeit (Standard: jetzt)
**Rückgabewert**: Berechnetes Datum/Zeit (Format YYYY/MM/DD HH:MM:SS)
**Beispiel**:
```vba
tomorrow = DATEADD("d", 1, DATE())
PRINT(tomorrow)        ' Morgen (z.B.: "2025/10/23 00:00:00")
nextMonth = DATEADD("m", 1, "2024-01-15")
PRINT(nextMonth)       ' "2024/02/15 00:00:00"
inOneHour = DATEADD("h", 1, NOW())
PRINT(inOneHour)       ' In einer Stunde (z.B.: "2025/10/22 15:30:00")
```

### DATEDIFF(interval, date1, [date2])
**Beschreibung**: Datumsdifferenz berechnen
**Argumente**:
- interval - Einheit ("d"=Tag, "m"=Monat, "y"=Jahr, "h"=Stunde, "n"=Minute, "s"=Sekunde)
- date1 - Startdatum/-zeit
- date2 - Enddatum/-zeit (Standard: jetzt)
**Rückgabewert**: Differenz (numerisch)
**Beispiel**:
```vba
days = DATEDIFF("d", "2024-01-01", "2024-01-15")
PRINT(days)  ' 14
age = DATEDIFF("y", "1990-01-01", DATE())
PRINT(age)   ' Alter
hours = DATEDIFF("h", "2024-01-15 10:00:00", NOW())
PRINT(hours) ' Verstrichene Zeit
```

### CDATE(date_string)
**Beschreibung**: Konvertiert Datumszeichenkette in Datumstyp (VBA-kompatibel)
**Argumente**: date_string - Zeichenkette, die ein Datum darstellt
**Rückgabewert**: Datumszeichenkette (Format YYYY/MM/DD HH:MM:SS)
**Flexible Formatunterstützung**:
- Vollständiges Datum/Zeit: `"2025/11/05 15:39:49"` → `2025/11/05 15:39:49`
- Nur Datum: `"2025/11/05"` → `2025/11/05 00:00:00` (Zeit ist 00:00:00)
- Nur Jahr/Monat: `"2025/11"` → `2025/11/01 00:00:00` (Tag=1, Zeit=00:00:00)
- Nur Jahr: `"2025"` → `2025/01/01 00:00:00` (Monat/Tag=1/1, Zeit=00:00:00)
- Nur Stunde: `"2025/11/05 15"` → `2025/11/05 15:00:00` (Minute/Sekunde=00)
- Nur Stunde/Minute: `"2025/11/05 15:39"` → `2025/11/05 15:39:00` (Sekunde=00)

**Flexibilität der Trennzeichen**:
- Gemischte Verwendung von `/`, `-`, `:` und Leerzeichen erlaubt
- `"2025-11-05-15-39-49"` und `"2025-11-05 15-39-49"` und `"2025-11-05 15:39:49"` werden gleich verarbeitet

**Beispiel**:
```vba
' Vollständiges Datum/Zeit
result = CDATE("2025/11/05 15:39:49")
PRINT(result)  ' "2025/11/05 15:39:49"

' Nur Datum (Zeit wird 00:00:00)
result = CDATE("2025/11/05")
PRINT(result)  ' "2025/11/05 00:00:00"

' Gemischte Trennzeichen OK
result = CDATE("2025-11-05 15:39:49")
PRINT(result)  ' "2025/11/05 15:39:49"

' Teilweises Datum (fehlende Teile werden ergänzt)
result = CDATE("2025/11")
PRINT(result)  ' "2025/11/01 00:00:00"
```

---

[← Zurück zum Index der integrierten Funktionen](00_index.md)
