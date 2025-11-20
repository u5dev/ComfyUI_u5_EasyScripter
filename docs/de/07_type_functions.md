# Typkonvertierungs- und Typprüfungsfunktionen-Referenz

[← Zurück zum Index der integrierten Funktionen](00_index.md)

## Übersicht

Typkonvertierungs- und Typprüfungsfunktionen sind Funktionsgruppen zur Konvertierung von Werttypen oder Prüfung von Variablentypen.

**Typkonvertierungsfunktionen**:
- CSTR - Konvertierung zu Zeichenkette
- CINT - Konvertierung zu Ganzzahl
- CDBL - Konvertierung zu Gleitkommazahl
- FORMAT - Formatierung von Zahlen/Datum in angegebenem Format (VBA-kompatibel)

**Typprüfungsfunktionen**:
- ISNUMERIC - Prüfung ob numerisch
- ISDATE - Prüfung ob Datum
- ISARRAY - Prüfung ob Array

---

## Typkonvertierungsfunktionen

### CSTR(value)

**Beschreibung**: Konvertiert zu Zeichenkette

**Argumente**:
- `value` - Beliebiger Wert

**Rückgabewert**: Zeichenkette

**Beispiel**:
```vba
text = CSTR(123)
PRINT(text)             ' 123
text = CSTR(3.14)
PRINT(text)             ' 3.14
text = CSTR(True)
PRINT(text)             ' 1
```

---

### CINT(value)

**Beschreibung**: Konvertiert zu Ganzzahl

**Argumente**:
- `value` - Numerischer Wert oder Zeichenkette

**Rückgabewert**: Ganzzahl (float-Format)

**Beispiel**:
```vba
number = CINT("123")
PRINT(number)            ' 123
number = CINT(45.67)
PRINT(number)            ' 46 (Rundung)
number = CINT("3.14")
PRINT(number)            ' 3
```

---

### CDBL(value)

**Beschreibung**: Konvertiert zu Gleitkommazahl

**Argumente**:
- `value` - Numerischer Wert oder Zeichenkette

**Rückgabewert**: float

**Beispiel**:
```vba
number = CDBL("123.45")
PRINT(number)            ' 123.45
number = CDBL(10)
PRINT(number)            ' 10
```

---

### FORMAT(value, [format_string])

**Beschreibung**: Formatiert Zahlen/Datum in angegebenem Format (VBA-kompatibel)

**Argumente**:
- `value` (Any, erforderlich) - Zu formatierender Wert (Zahl, Zeichenkette, Datum)
- `format_string` (str, optional) - Formatbezeichner (Standard: "")

**Rückgabewert**: str - Formatierte Zeichenkette

**Unterstützte Formatformen**:

1. **VBA-Form**:
   - `"0"` - Ganzzahl (Rundung)
   - `"0.0"` - 1 Dezimalstelle
   - `"0.00"` - 2 Dezimalstellen
   - `"#"`, `"#.#"`, `"#.##"` - Automatische Genauigkeit

2. **Python format-Form**:
   - `"{:.2f}"` - Python format-Syntax
   - `".2f"`, `","` - format spec

3. **Datumsform (strftime)**:
   - `"%Y-%m-%d %H:%M:%S"` - Datum/Zeit-Format
   - `"%Y/%m/%d"` - Nur Datum

**Beispiel**:
```vba
' VBA-Form
result = FORMAT(123.456, "0")       ' "123" (Ganzzahl)
PRINT("Ganzzahl: " & result)
result = FORMAT(123.456, "0.0")     ' "123.5" (1 Dezimalstelle)
PRINT("1 Dezimalstelle: " & result)
result = FORMAT(123.456, "0.00")    ' "123.46" (2 Dezimalstellen)
PRINT("2 Dezimalstellen: " & result)

' Python format-Form
result = FORMAT(3.14159, "{:.2f}")  ' "3.14"
PRINT("Pi: " & result)
result = FORMAT(1234567, ",")       ' "1,234,567"
PRINT("Kommagetrennt: " & result)

' Datumsformat
now_str = NOW()
result = FORMAT(now_str, "%Y-%m-%d %H:%M:%S")
PRINT("Datum/Zeit: " & result)             ' "2024-01-15 14:30:00"
result = FORMAT(now_str, "%Y年%m月%d日")
PRINT("Datum: " & result)             ' "2024年01月15日"
```

**Hinweis**:
- Bei Weglassen von `format_string` wird Wert direkt in Zeichenkette konvertiert
- Bei nicht unterstütztem Format wird Wert mit str() zurückgegeben

---

## Typprüfungsfunktionen

### ISNUMERIC(value)

**Beschreibung**: Prüft ob numerisch

**Argumente**:
- `value` - Zu prüfender Wert

**Rückgabewert**: 1 (numerisch) oder 0

**Beispiel**:
```vba
result = ISNUMERIC("123")
PRINT(result)                  ' 1
result = ISNUMERIC("12.34")
PRINT(result)                  ' 1
result = ISNUMERIC("abc")
PRINT(result)                  ' 0
result = ISNUMERIC("")
PRINT(result)                  ' 0
```

---

### ISDATE(value)

**Beschreibung**: Prüft ob als Datum analysierbar

**Argumente**:
- `value` - Zu prüfender Wert

**Rückgabewert**: 1 (Datum) oder 0

**Beispiel**:
```vba
result = ISDATE("2024-01-15")
PRINT(result)                     ' 1
result = ISDATE("2024/01/15")
PRINT(result)                     ' 1
result = ISDATE("15:30:00")
PRINT(result)                     ' 1 (auch Zeit)
result = ISDATE("hello")
PRINT(result)                     ' 0
```

---

### ISARRAY(variable_name)

**Beschreibung**: Prüft ob Array

**Wichtig**: Übergeben Sie Array-Name als Zeichenkette oder Array-Variablenreferenz mit ARR[]-Notation.

**Argumente**:
- `variable_name` - Variablenname (Zeichenkette) oder Array-Variablenreferenz

**Rückgabewert**: 1 (Array) oder 0

**Beispiel**:
```vba
REDIM ARR, 10
result = ISARRAY(ARR[])
PRINT(result)                ' 1 (Array-Referenz)
result = ISARRAY("ARR")
PRINT(result)                ' 1 (Array-Name-Zeichenkette)
result = ISARRAY("VAL1")
PRINT(result)                ' 0 (normale Variable)
```

---

[← Zurück zum Index der integrierten Funktionen](00_index.md)
