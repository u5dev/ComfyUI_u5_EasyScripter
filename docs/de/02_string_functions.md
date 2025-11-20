# Zeichenkettenfunktionen-Referenz

[← Zurück zum Index der integrierten Funktionen](00_index.md)

Vollständige Referenz der Zeichenkettenfunktionen, die in u5 EasyScripter verfügbar sind.

## Funktionsliste
28 Zeichenkettenfunktionen werden bereitgestellt.

---

### LEN(text)
**Beschreibung**: Gibt die Länge einer Zeichenkette zurück
**Argumente**: text - Zeichenkette
**Rückgabewert**: Anzahl der Zeichen
**Beispiel**:
```vba
result = LEN("Hello")
PRINT(result)     ' 5
text1 = "Sample Text"
result = LEN(text1)
PRINT(result)     ' 11
result = LEN("")
PRINT(result)     ' 0
```

### LEFT(text, length)
**Beschreibung**: Extrahiert die angegebene Anzahl von Zeichen von links
**Argumente**:
- text - Zeichenkette
- length - Anzahl der zu extrahierenden Zeichen
**Rückgabewert**: Teilzeichenkette
**Beispiel**:
```vba
result = LEFT("Hello World", 5)
PRINT(result)   ' "Hello"
text1 = "ComfyUI EasyScripter"
result = LEFT(text1, 10)
PRINT(result)   ' "ComfyUI Ea"
result = LEFT("ABC", 10)
PRINT(result)   ' "ABC" (gesamte Zeichenkette wenn länger)
```

### RIGHT(text, length)
**Beschreibung**: Extrahiert die angegebene Anzahl von Zeichen von rechts
**Argumente**:
- text - Zeichenkette
- length - Anzahl der zu extrahierenden Zeichen
**Rückgabewert**: Teilzeichenkette
**Beispiel**:
```vba
result = RIGHT("Hello World", 5)
PRINT(result)  ' "World"
text1 = "ComfyUI EasyScripter"
result = RIGHT(text1, 10)
PRINT(result)  ' "syScripter"
result = RIGHT("ABC", 10)
PRINT(result)  ' "ABC"
```

### MID(text, start, length)
**Beschreibung**: Extrahiert Teilzeichenkette ab angegebener Position

**Wichtig**: Startposition 0 wird als 1 behandelt.

**Argumente**:
- text - Zeichenkette
- start - Startposition (1-basiert, 0 wird als 1 behandelt)
- length - Anzahl der zu extrahierenden Zeichen
**Rückgabewert**: Teilzeichenkette
**Beispiel**:
```vba
result = MID("Hello World", 7, 5)
PRINT(result)  ' "World"
result = MID("ABCDEFG", 3, 2)
PRINT(result)  ' "CD"
result = MID("ABCDEFG", 0, 2)
PRINT(result)  ' "AB" (0 wird als 1 behandelt)
text1 = "EasyScripter Node"
result = MID(text1, 5, 10)
PRINT(result)  ' "Scripter N"
```

### UPPER(text)
**Beschreibung**: Konvertiert in Großbuchstaben
**Argumente**: text - Zeichenkette
**Rückgabewert**: In Großbuchstaben konvertierte Zeichenkette
**Beispiel**:
```vba
result = UPPER("Hello")
PRINT(result)      ' "HELLO"
result = UPPER("abc123XYZ")
PRINT(result)  ' "ABC123XYZ"
```

### LOWER(text)
**Beschreibung**: Konvertiert in Kleinbuchstaben
**Argumente**: text - Zeichenkette
**Rückgabewert**: In Kleinbuchstaben konvertierte Zeichenkette
**Beispiel**:
```vba
result = LOWER("HELLO")
PRINT(result)      ' "hello"
result = LOWER("ABC123xyz")
PRINT(result)  ' "abc123xyz"
```

### TRIM(text)
**Beschreibung**: Entfernt führende und nachfolgende Leerzeichen
**Argumente**: text - Zeichenkette
**Rückgabewert**: Getrimmte Zeichenkette
**Beispiel**:
```vba
result = TRIM("  Hello  ")
PRINT(result)    ' "Hello"
result = TRIM("   ")
PRINT(result)    ' ""
```

### REPLACE(text, old, new)
**Beschreibung**: Ersetzt Zeichenkette
**Argumente**:
- text - Zielzeichenkette
- old - Suchzeichenkette
- new - Ersetzungszeichenkette
**Rückgabewert**: Ersetzte Zeichenkette
**Beispiel**:
```vba
result = REPLACE("Hello World", "World", "ComfyUI")
PRINT(result)  ' "Hello ComfyUI"
text1 = "Hello World Test"
result = REPLACE(text1, " ", "_")
PRINT(result)  ' "Hello_World_Test"
result = REPLACE("AAABBB", "A", "X")
PRINT(result)  ' "XXXBBB"
```

### INSTR([start,] text, search)
**Beschreibung**: Sucht Zeichenkette (gibt Position zurück)
**Argumente**:
- start - Suchstartposition (Standard: 1)
- text - Zielzeichenkette
- search - Suchzeichenkette
**Rückgabewert**: Gefundene Position (0 = nicht gefunden)
**Beispiel**:
```vba
result = INSTR("Hello World", "World")
PRINT(result)     ' 7
result = INSTR("ABCABC", "BC")
PRINT(result)     ' 2
result = INSTR(3, "ABCABC", "BC")
PRINT(result)     ' 5 (Suche ab 3. Zeichen)
text1 = "This is a keyword example"
result = INSTR(text1, "keyword")
PRINT(result)     ' 11
```

### INSTRREV(text, search, [start])
**Beschreibung**: Sucht Zeichenkette von hinten
**Argumente**:
- text - Zielzeichenkette
- search - Suchzeichenkette
- start - Suchstartposition (Standard: Ende)
**Rückgabewert**: Gefundene Position
**Beispiel**:
```vba
result = INSTRREV("Hello World", "o")
PRINT(result)      ' 8 (letztes o)
result = INSTRREV("ABCABC", "BC")
PRINT(result)      ' 5
result = INSTRREV("path/to/file", "/")
PRINT(result)      ' 8 (letzter Schrägstrich)
```

### STRREVERSE(text)
**Beschreibung**: Kehrt Zeichenkette um
**Argumente**: text - Zeichenkette
**Rückgabewert**: Umgekehrte Zeichenkette
**Beispiel**:
```vba
result = STRREVERSE("Hello")
PRINT(result)    ' "olleH"
result = STRREVERSE("12345")
PRINT(result)    ' "54321"
```

### STRCOMP(text1, text2, [compare])
**Beschreibung**: Vergleicht Zeichenketten
**Argumente**:
- text1 - Zeichenkette 1
- text2 - Zeichenkette 2
- compare - Vergleichsmethode (0=Binär, 1=Text)
**Rückgabewert**: -1/0/1 (kleiner/gleich/größer)
**Beispiel**:
```vba
result = STRCOMP("abc", "ABC", 1)
PRINT(result)    ' 0 (Groß-/Kleinschreibung ignorieren)
result = STRCOMP("abc", "ABC", 0)
PRINT(result)    ' 1 (Groß-/Kleinschreibung unterscheiden)
result = STRCOMP("a", "b")
PRINT(result)    ' -1
```

### SPACE(number)
**Beschreibung**: Erzeugt angegebene Anzahl von Leerzeichen
**Argumente**: number - Anzahl der Leerzeichen
**Rückgabewert**: Leerzeichen-Zeichenkette
**Beispiel**:
```vba
result = SPACE(5)
PRINT(result)               ' "     "
result = "A" & SPACE(3) & "B"
PRINT(result)   ' "A   B"
```

### STRING(number, character)
**Beschreibung**: Wiederholt Zeichen
**Argumente**:
- number - Wiederholungszahl
- character - Zu wiederholendes Zeichen
**Rückgabewert**: Wiederholte Zeichenkette
**Beispiel**:
```vba
result = STRING(5, "A")
PRINT(result)     ' "AAAAA"
result = STRING(10, "-")
PRINT(result)    ' "----------"
```

### FORMAT(value, format_string)
**Beschreibung**: Formatiert Wert
**Argumente**:
- value - Wert
- format_string - Formatzeichenkette
**Rückgabewert**: Formatierte Zeichenkette
**Unterstützte Formate**:
- `{:.Nf}` - N Dezimalstellen
- `{:0Nd}` - N-stelliges Nullen-Padding
- `{:,}` - 3-stellige Kommatrennung
- `%Y-%m-%d` - Datumsformat
**Beispiel**:
```vba
result = FORMAT(3.14159, "{:.2f}")
PRINT(result)      ' "3.14"
result = FORMAT(42, "{:05d}")
PRINT(result)      ' "00042"
result = FORMAT(1234567, "{:,}")
PRINT(result)      ' "1,234,567.0"
result = FORMAT(NOW(), "%Y/%m/%d")
PRINT(result)      ' "2024/01/15"
```

### SPLIT(text, [delimiter])
**Beschreibung**: Teilt Zeichenkette in Array
**Argumente**:
- text - Zu teilende Zeichenkette
- delimiter - Trennzeichen (Standard: Komma)
**Rückgabewert**: Geteiltes Array
**Beispiel**:
```vba
' Kommagetrenntes teilen
result = SPLIT("apple,banana,cherry")
PRINT(result(0))  ' "apple"
PRINT(result(1))  ' "banana"
' Leerzeichengetrenntes teilen
result = SPLIT("one two three", " ")
PRINT(result(2))  ' "three"
```

### JOIN(array, [delimiter])
**Beschreibung**: Verbindet Array zu Zeichenkette
**Argumente**:
- array - Zu verbindendes Array
- delimiter - Trennzeichen (Standard: Komma)
**Rückgabewert**: Verbundene Zeichenkette
**Beispiel**:
```vba
ARRAY(arr, "A", "B", "C")
result = JOIN(arr, "-")
PRINT(result)  ' "A-B-C"
result = JOIN(arr)
PRINT(result)  ' "A,B,C"
```

### LTRIM(text)
**Beschreibung**: Entfernt Leerzeichen links
**Argumente**: text - Zeichenkette
**Rückgabewert**: Zeichenkette mit entfernten Leerzeichen links
**Beispiel**:
```vba
result = LTRIM("  Hello")
PRINT(result)  ' "Hello"
result = LTRIM("  Text  ")
PRINT(result)  ' "Text  "
```

### RTRIM(text)
**Beschreibung**: Entfernt Leerzeichen rechts
**Argumente**: text - Zeichenkette
**Rückgabewert**: Zeichenkette mit entfernten Leerzeichen rechts
**Beispiel**:
```vba
result = RTRIM("Hello  ")
PRINT(result)  ' "Hello"
result = RTRIM("  Text  ")
PRINT(result)  ' "  Text"
```

### UCASE(text)
**Beschreibung**: Konvertiert zu Großbuchstaben (Alias für UPPER)
**Argumente**: text - Zeichenkette
**Rückgabewert**: In Großbuchstaben konvertierte Zeichenkette
**Beispiel**:
```vba
result = UCASE("hello")
PRINT(result)  ' "HELLO"
```

### LCASE(text)
**Beschreibung**: Konvertiert zu Kleinbuchstaben (Alias für LOWER)
**Argumente**: text - Zeichenkette
**Rückgabewert**: In Kleinbuchstaben konvertierte Zeichenkette
**Beispiel**:
```vba
result = LCASE("HELLO")
PRINT(result)  ' "hello"
```

### PROPER(text)
**Beschreibung**: Konvertiert zu Titelfall (Großschreibung des ersten Buchstabens jedes Wortes)
**Argumente**: text - Zeichenkette
**Rückgabewert**: In Titelfall konvertierte Zeichenkette
**Beispiel**:
```vba
result = PROPER("hello world")
PRINT(result)  ' "Hello World"
result = PROPER("easyScripter node")
PRINT(result)  ' "Easyscripter Node"
```

### CHR(code)
**Beschreibung**: Konvertiert Zeichencode zu Zeichen
**Argumente**: code - Zeichencode (0-127 im ASCII-Bereich)
**Rückgabewert**: Entsprechendes Zeichen
**Beispiel**:
```vba
result = CHR(65)
PRINT(result)  ' "A"
result = CHR(97)
PRINT(result)  ' "a"
result = CHR(48)
PRINT(result)  ' "0"
```

### ASC(char)
**Beschreibung**: Konvertiert Zeichen zu Zeichencode
**Argumente**: char - Zeichen oder Zeichenkette (verwendet erstes Zeichen)
**Rückgabewert**: Zeichencode (ASCII)
**Beispiel**:
```vba
result = ASC("A")
PRINT(result)  ' 65
result = ASC("Hello")
PRINT(result)  ' 72 ("H" Code)
```

### STR(value)
**Beschreibung**: Konvertiert Zahl zu Zeichenkette
**Argumente**: value - Zahl
**Rückgabewert**: Als Zeichenkette konvertierte Zahl
**Beispiel**:
```vba
result = STR(123)
PRINT(result)  ' "123"
result = STR(3.14)
PRINT(result)  ' "3.14"
```

### URLENCODE(text, [encoding])
**Beschreibung**: Führt URL-Codierung (Prozent-Codierung) aus
**Argumente**:
- text - Zu codierende Zeichenkette
- encoding - Zeichencodierung (Standard: utf-8)
**Rückgabewert**: URL-codierte Zeichenkette
**Beispiel**:
```vba
' Japanisch URL-codieren
encoded = URLENCODE("あいうえお")
PRINT(encoded)  ' → %E3%81%82%E3%81%84%E3%81%86%E3%81%88%E3%81%8A
' Suchanfrage codieren
query = "EasyScripter HTTP 関数"
url = "https://www.google.com/search?q=" & URLENCODE(query)
PRINT(url)
```

### URLDECODE(text, [encoding])
**Beschreibung**: Führt URL-Decodierung (Prozent-Codierungs-Decodierung) aus
**Argumente**:
- text - Zu decodierende Zeichenkette
- encoding - Zeichencodierung (Standard: utf-8)
**Rückgabewert**: URL-decodierte Zeichenkette
**Beispiel**:
```vba
' URL-codierte Zeichenkette decodieren
decoded = URLDECODE("%E3%81%82%E3%81%84%E3%81%86%E3%81%88%E3%81%8A")
PRINT(decoded)  ' → あいうえお
' Abfrageparameter decodieren
param = URLDECODE("EasyScripter+HTTP+%E9%96%A2%E6%95%B0")
PRINT(param)  ' → EasyScripter+HTTP+関数
```

### ESCAPEPATHSTR(path, [replacement])
**Beschreibung**: Ersetzt oder entfernt verbotene Zeichen für Dateipfade
**Argumente**:
- path - Zu verarbeitende Zeichenkette
- replacement - Ersetzungszeichenkette (Standard: entfernen)
**Rückgabewert**: Verarbeitete Zeichenkette

**Verbotene Zeichen**: `\`, `/`, `:`, `*`, `?`, `"`, `<`, `>`, `|`

**Reservierte Wörter** (als vollständiger Dateiname verboten): CON, PRN, AUX, NUL, COM1-9, LPT1-9 (Groß-/Kleinschreibung unabhängig)

**Beispiel**:
```vba
' Verbotene Zeichen durch Unterstrich ersetzen
safe_name = ESCAPEPATHSTR("file:name*.txt", "_")
PRINT(safe_name)  ' → file_name_.txt

' Verbotene Zeichen entfernen
safe_name = ESCAPEPATHSTR("file:name*.txt")
PRINT(safe_name)  ' → filename.txt

' Verarbeitung von reservierten Wörtern
safe_name = ESCAPEPATHSTR("CON.txt", "_")
PRINT(safe_name)  ' → _.txt

' Als Teil des Dateinamens erlaubt
safe_name = ESCAPEPATHSTR("myConFile.txt", "_")
PRINT(safe_name)  ' → myConFile.txt
```

---

[← Zurück zum Index der integrierten Funktionen](00_index.md)
