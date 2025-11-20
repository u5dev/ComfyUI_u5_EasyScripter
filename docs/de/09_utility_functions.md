# Hilfsfunktionen-Referenz

[← Zurück zum Index der integrierten Funktionen](00_index.md)

Hilfsfunktionen sind praktische Funktionsgruppen zur Unterstützung der Skriptentwicklung wie Debug-Ausgabe, Typprüfung und Eingabeverarbeitung.

---

## Ausgabefunktionen

### PRINT(message, ...)

**Beschreibung**: Gibt Wert in Textbereich aus (für Debugging)

**Argumente**:
- message - Auszugebender Wert (mehrere Angaben möglich)

**Rückgabewert**: Keine (wird zu PRINT-Variable hinzugefügt)

**Beispiel**:
```vba
' Variablenwert verfolgen
value = VAL1 * 2
PRINT("value after multiplication: " & value)

' Schleifenfortschritt
FOR i = 1 TO 10
    PRINT("Loop iteration: " & i)
    ' Verarbeitung...
NEXT

' Verzweigungsbestätigung
condition = VAL1 > 100
IF condition THEN
    PRINT("Condition was TRUE")
ELSE
    PRINT("Condition was FALSE")
END IF

' Mehrere Werte gleichzeitig ausgeben
PRINT("VAL1:", VAL1, "VAL2:", VAL2)
result = VAL1 + VAL2
PRINT("Berechnungsergebnis:", result)
```

**Hinweis**:
- Mit PRINT-Funktion ausgegebene Inhalte werden im Textbereich unterhalb des Knotens angezeigt
- Praktisch zur Überprüfung von Variablenwerten beim Debugging

---

### OUTPUT(arg, [path], [flg])

**Beschreibung**: Gibt Text, Zahlen, Array, Bild, Binärdaten in Datei aus

**Argumente**:
- arg (Any) - Auszugebender Wert (Zeichenkette, Zahl, Array, torch.Tensor, bytes)
- path (str, optional) - Ausgabepfad (relativer Pfad, Standard="")
- flg (str, optional) - Betriebsmodus ("NEW"=Neu/Duplikatvermeidung, "ADD"=Anhängen, Standard="NEW")

**Rückgabewert**: str - Absoluter Pfad der ausgegebenen Datei (leere Zeichenkette bei Fehler)

**Funktionen**:
1. **Textausgabe**: Gibt Zeichenketten, Zahlen, Arrays als Textdatei aus
2. **Bildausgabe**: Gibt torch.Tensor (ComfyUI-Bilddaten) als PNG/JPEG etc. aus
3. **Binärausgabe**: Gibt bytes-Typ-Daten als Binärdatei aus
4. **NEW-Modus**: Fügt automatisch `_0001`, `_0002`... bei Duplikaten hinzu
5. **ADD-Modus**: Hängt an bestehende Datei an
6. **Sicherheit**: Absoluter Pfad/UNC-Pfad abgelehnt (nur relativer Pfad erlaubt)
7. **Unterverzeichnis**: Automatische rekursive Erstellung
8. **Automatische Erweiterungsergänzung**: `.txt` (Text), `.png` (Bild)

**Beispiel**:
```vba
' Textausgabe
path = OUTPUT("Hello World", "output.txt", "NEW")
PRINT("Ausgabeziel: " & path)

' Zahlenausgabe
path = OUTPUT(12345, "number.txt")
PRINT("Ausgabeziel: " & path)

' Array-Ausgabe
ARR = ARRAY("apple", "banana", "cherry")
path = OUTPUT(ARR, "fruits.txt")
PRINT("Ausgabeziel: " & path)

' Ausgabe aus reservierter Variable
path = OUTPUT("TXT1", "user_input.txt")
PRINT("TXT1-Wert ausgegeben: " & path)

' Anhänge-Modus
path1 = OUTPUT("First Line", "log.txt", "NEW")
PRINT("Neu erstellt: " & path1)
path2 = OUTPUT("Second Line", "log.txt", "ADD")
PRINT("Angehängt: " & path2)
```

---

### INPUT(path)

**Beschreibung**: Liest Datei aus ComfyUI-Ausgabeordner (symmetrische Funktion zu OUTPUT)

**Argumente**:
- path (str, erforderlich) - Relativer Pfad vom ComfyUI-Ausgabeordner

**Rückgabewert**: Dynamischer Typ (automatische Bestimmung nach Dateiformat)
- Textdatei (`.txt`, `.md`) → str-Typ
- JSON-Zahl → float-Typ
- JSON-Array → list-Typ
- Bilddatei (`.png`, `.jpg`, `.jpeg`, `.bmp`, `.webp`) → torch.Tensor-Typ (ComfyUI-kompatibel)
- Sonstige → bytes-Typ (binär)

**Beispiel**:
```vba
' Textdatei lesen
prompt = INPUT("prompts/positive.txt")
PRINT("Gelesener Prompt: " & prompt)
RETURN1 = prompt

' JSON-Array lesen
dataArray = INPUT("data_array.json")
PRINT("Array-Elementanzahl: " & (UBOUND(dataArray[]) + 1))

' Bild lesen (torch.Tensor-Format)
refImage = INPUT("reference_images/style_sample.png")
' refImage kann direkt mit ComfyUI-Bildeingabeknoten verbunden werden

' Aus Unterverzeichnis lesen
configText = INPUT("configs/model_settings.txt")
PRINT("Konfigurationsinhalt: " & configText)
```

#### Koordination zwischen INPUT-Funktion und RELAY_OUTPUT

Um Bilder oder Daten, die mit der INPUT-Funktion geladen wurden, an nachfolgende Knoten zu übergeben, verwenden Sie die RELAY_OUTPUT-Variable.

```vba
' Prompt aus Textdatei lesen und an nachfolgendes CLIPTextEncode übergeben
PROMPT_TEXT = INPUT("prompts/positive.txt")
RELAY_OUTPUT = PROMPT_TEXT

' Oder Bilddatei lesen und an nachfolgendes LoadImage übergeben
IMG1 = INPUT("reference_images/base.png")
RELAY_OUTPUT = IMG1
```

**RETURN1/RETURN2 vs RELAY_OUTPUT**:
- RETURN1/RETURN2: Nur primitive Typen (INT, FLOAT, STRING)
- RELAY_OUTPUT: Unterstützt ANY-Typ (Objekte wie torch.Tensor, list, dict sind ebenfalls möglich)

**Hinweis**:
- Wenn die Datei nicht existiert, wird eine Warnmeldung mit PRINT ausgegeben und None zurückgegeben
- Das Lesen großer Dateien (Bilder usw.) kann einige Zeit in Anspruch nehmen

---

### ISFILEEXIST(path, [flg])

**Beschreibung**: Dateiexistenzprüfung und erweiterte Informationserfassung im ComfyUI-Ausgabeordner

**Argumente**:
- path (str, erforderlich) - Relativer Pfad vom ComfyUI-Ausgabeordner
- flg (str, optional) - Options-Flag (Standard: "")
  - `""` (Standard): Nur Existenzprüfung
  - `"NNNN"`: Suche nach Dateipfad mit höchster _NNNN-Nummer
  - `"PIXEL"`: Bildgröße (Breite/Höhe) abrufen
  - `"SIZE"`: Dateigröße (Bytes) abrufen

**Rückgabewert**: Dynamischer Typ (ändert sich je nach flg)
- **flg=""**: `"TRUE"` oder `"FALSE"` (str-Typ)
- **flg="NNNN"**: Dateipfad mit höchster Nummer (relativer Pfad, str-Typ), `"FALSE"` wenn nicht vorhanden
- **flg="PIXEL"**: Array-Zeichenkette im Format `"[width, height]"` (str-Typ), `"FALSE"` wenn kein Bild/nicht vorhanden
- **flg="SIZE"**: Dateigröße in Bytes (str-Typ), `"FALSE"` wenn nicht vorhanden

**Beispiel**:
```vba
' Grundlegende Existenzprüfung
exists = ISFILEEXIST("output.txt")
PRINT("exists = " & exists)
IF exists = "TRUE" THEN
    PRINT("Datei existiert")
ELSE
    PRINT("Datei existiert nicht")
END IF

' Suche nach höchster _NNNN-Nummer
latestFile = ISFILEEXIST("ComfyUI_00001_.png", "NNNN")
PRINT("latestFile = " & latestFile)
IF latestFile <> "FALSE" THEN
    PRINT("Neueste Datei: " & latestFile)
ELSE
    PRINT("Keine entsprechende Datei")
END IF

' Bildgröße abrufen
imageSize = ISFILEEXIST("sample_image.png", "PIXEL")
PRINT("imageSize = " & imageSize)
IF imageSize <> "FALSE" THEN
    PRINT("Bildgröße: " & imageSize)
ELSE
    PRINT("Keine Bilddatei")
END IF

' Dateigröße abrufen
fileSize = ISFILEEXIST("data.txt", "SIZE")
PRINT("fileSize = " & fileSize)
IF fileSize <> "FALSE" THEN
    PRINT("Dateigröße: " & fileSize & " bytes")
ELSE
    PRINT("Datei nicht gefunden")
END IF
```

---

### VRAMFREE([min_free_vram_gb])

**Beschreibung**: Funktion zur Freigabe von VRAM und RAM. Führt Modell-Entladen, Cache-Löschen, Garbage Collection aus.

**⚠️ WARNUNG**: Modell-Entladen ist eine heikle Operation. Je nach Ausführungszeitpunkt kann es zu unerwartetem Verhalten während der Workflow-Ausführung führen. Verwenden Sie mit Vorsicht.

**Syntax**:
```vba
result = VRAMFREE(min_free_vram_gb)
```

**Parameter**:
- `min_free_vram_gb` (float, optional): Ausführungsschwellenwert (in GB)
  - Überspringt Verarbeitung wenn aktueller freier VRAM größer oder gleich diesem Wert
  - Standard: 0.0 (immer ausführen)

**Rückgabewert**:
dict (detaillierte Informationen zum Ausführungsergebnis)
- `success`: Ausführungserfolgsflag (bool)
- `message`: Ausführungsergebnis-Nachricht (str)
- `freed_vram_gb`: Freigegebene VRAM-Menge (float)
- `freed_ram_gb`: Freigegebene RAM-Menge (float)
- `initial_status`: Speicherstatus vor Ausführung (dict)
- `final_status`: Speicherstatus nach Ausführung (dict)
- `actions_performed`: Liste ausgeführter Aktionen (list)

**Beispiel**:
```vba
' Immer ausführen (ohne Schwellenwert)
result = VRAMFREE(0.0)
PRINT("VRAM freed: " & result["freed_vram_gb"] & " GB")

' Nur ausführen wenn freier VRAM unter 2GB
result = VRAMFREE(2.0)
IF result["success"] = TRUE THEN
    PRINT("Cleanup completed")
ELSE
    PRINT("Cleanup failed")
END IF
```

---

### SLEEP([milliseconds])

**Beschreibung**: Pausiert Verarbeitung für angegebene Millisekunden (Sleep). Wird zur Geschwindigkeitssteuerung von WHILE()-Schleifen und Verarbeitungssynchronisierung verwendet.

**Argumente**:
- milliseconds (FLOAT, optional): Sleep-Zeit (Millisekunden), Standard: 10ms

**Rückgabewert**: Keine (gibt intern 0.0 zurück)

**Syntax**:
```vba
SLEEP(milliseconds)
```

**Verwendungsbeispiele**:
```vba
' Standard-10ms-Sleep
SLEEP()

' 0,5 Sekunden Sleep
SLEEP(500)

' Geschwindigkeitssteuerung von WHILE()-Schleife (CPU-Auslastungsreduzierung)
VAL1 = 0
WHILE VAL1 < 100
    VAL1 = VAL1 + 1
    SLEEP(100)  ' 100ms warten
WEND
PRINT("Schleife abgeschlossen: " & VAL1)
RETURN1 = VAL1

' Verarbeitungssynchronisierung
PRINT("Verarbeitung startet")
result = VAL1 * 2
SLEEP(1000)  ' 1 Sekunde warten
PRINT("Verarbeitung abgeschlossen: " & result)
RETURN1 = result
```

**Hauptzwecke**:
1. **Geschwindigkeitssteuerung von WHILE()-Schleifen**: CPU-Auslastung reduzieren und Systemlast verringern
2. **Verarbeitungssynchronisierung**: Warten auf externe Systemantwort oder beabsichtigte Verzögerungsverarbeitung
3. **Debugging**: Temporäre Pause zur Beobachtung des Verarbeitungsflusses

**ComfyUI-Integration**:
- Koordinierte Arbeit mit ComfyUI's thread-basierter Warteschlangenverwaltung (ScriptExecutionQueue)
- Synchrone blockierende Ausführung durch time.sleep()
- ScriptExecutionQueue garantiert Sicherheit bei gleichzeitiger Ausführung mehrerer EasyScripter-Knoten

**Hinweise**:
- SLEEP() blockiert den aktuellen Thread (andere Verarbeitungen werden nicht ausgeführt)
- Asynchrone Verarbeitung (asyncio) wird nicht verwendet (ComfyUI ist nicht ereignisschleifengesteuert)
- Lange Sleeps erhöhen die Ausführungszeit des gesamten Workflows

---

## Bildverarbeitungsfunktionen

### IMAGETOBYTEARRAY(image_input, [max_size], [format], [return_format])

**Beschreibung**: Empfängt IMAGE-Tensor oder Bilddateipfad, verkleinert/komprimiert und konvertiert zu Byte-Array oder JSON-Array. Wird hauptsächlich als Daten für Versand an REST-API verwendet.

**Argumente**:
- image_input (str | torch.Tensor, erforderlich) - Bildquelle
  - Zeichenkette: Bilddateipfad (z.B.: `"C:/path/to/image.png"`)
  - torch.Tensor: ComfyUI IMAGE-Format `[batch, height, width, channels]`
- max_size (int, optional) - Maximale Größe nach Verkleinerung (lange Seite, Pixel), Standard: 336
- format (str, optional) - Ausgabebildformat ("PNG", "JPEG" etc.), Standard: "PNG"
- return_format (str, optional) - Rückgabeform ("bytes" oder "json"), Standard: "bytes"

**Rückgabewert**: Dynamischer Typ (ändert sich je nach return_format)
- **return_format="bytes"**: bytes-Typ (rohe Binärdaten)
- **return_format="json"**: str-Typ (JSON-Array-Format-Zeichenkette, z.B.: `"[137, 80, 78, 71, ...]"`)

**Beispiel**:
```vba
' Dateipfad-Eingabe (herkömmliche Methode)
json_array = IMAGETOBYTEARRAY("C:/path/to/image.png", 336, "JPEG", "json")
PRINT("JSON-Array-Länge: " & LEN(json_array))

' IMAGE-Tensor-Eingabe (aus ComfyUI-Knotenverbindung)
' IMAGE-Typ wird von LoadImage-Knoten etc. an VAL1 übergeben
json_array = IMAGETOBYTEARRAY(VAL1, 336, "JPEG", "json")
RETURN1 = json_array
```

---

### IMAGETOBASE64(image_input, [max_size], [format], [return_format])

**Beschreibung**: Empfängt IMAGE-Tensor oder Bilddateipfad, verkleinert/komprimiert und konvertiert zu Base64-Codierung oder data URL-Format. Wird hauptsächlich als Daten für Versand an REST-API verwendet.

**Argumente**:
- image_input (str | torch.Tensor, erforderlich) - Bildquelle
- max_size (int, optional) - Maximale Größe nach Verkleinerung (lange Seite, Pixel), Standard: 512
- format (str, optional) - Ausgabebildformat ("PNG", "JPEG" etc.), Standard: "PNG"
- return_format (str, optional) - Rückgabeform ("base64" oder "data_url"), Standard: "base64"

**Rückgabewert**: str-Typ (ändert sich je nach return_format)
- **return_format="base64"**: Base64-codierte Zeichenkette (z.B.: `"iVBORw0KGgoAAAANSUhEUgAA..."`)
- **return_format="data_url"**: data URL-Format-Zeichenkette (z.B.: `"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."`)

**Beispiel**:
```vba
' Dateipfad-Eingabe (Base64-Zeichenkette)
base64_str = IMAGETOBASE64("C:/path/to/image.png", 512, "PNG", "base64")
PRINT("Base64-Länge: " & LEN(base64_str))

' IMAGE-Tensor-Eingabe (data URL-Format)
' IMAGE-Typ wird von LoadImage-Knoten etc. an ANY_INPUT übergeben
data_url = IMAGETOBASE64(ANY_INPUT, 512, "PNG", "data_url")
RETURN1 = data_url
```

---

## Funktionen zum Abrufen von Bild-/Latent-Daten

### GETANYWIDTH([any_data])

**Beschreibung**: Ruft Breite (Pixelanzahl) von IMAGE/LATENT-Typ-Daten ab

**Argumente**:
- any_data (torch.Tensor, optional) - IMAGE/LATENT-Daten
  - Bei fehlender Angabe automatische Verwendung der Daten vom any_input-Eingabe-Socket

**Rückgabewert**: float - Breite (Pixelanzahl, 0.0 wenn nicht abrufbar)

**Beispiel**:
```vba
' Automatisches Abrufen vom any_input-Eingabe-Socket
width = GETANYWIDTH()
PRINT("Breite: " & width)
RETURN1 = width

' Explizite Datenangabe
imageData = INPUT("sample.png")
w = GETANYWIDTH(imageData)
PRINT("Bildbreite: " & w)
```

---

### GETANYHEIGHT([any_data])

**Beschreibung**: Ruft Höhe (Pixelanzahl) von IMAGE/LATENT-Typ-Daten ab

**Argumente**:
- any_data (torch.Tensor, optional) - IMAGE/LATENT-Daten

**Rückgabewert**: float - Höhe (Pixelanzahl, 0.0 wenn nicht abrufbar)

**Beispiel**:
```vba
' Automatisches Abrufen vom any_input-Eingabe-Socket
height = GETANYHEIGHT()
PRINT("Höhe: " & height)
RETURN2 = height

' Verzweigung nach Auflösung
w = GETANYWIDTH()
h = GETANYHEIGHT()
IF w >= 1024 AND h >= 1024 THEN
    PRINT("Hochauflösungsbild")
    scale = 1.0
ELSE
    PRINT("Standardauflösungsbild")
    scale = 2.0
END IF
RETURN1 = scale
```

---

### GETANYTYPE([any_data])

**Beschreibung**: Bestimmt Typname von ANY-Typ-Daten

**Argumente**:
- any_data (Any, optional) - Zu prüfende Daten

**Rückgabewert**: str - Typname
- "int", "float", "string" - Grundtypen
- "image", "latent" - Bild/Latent
- "model", "vae", "clip" - ComfyUI-Modelltypen
- "conditioning", "control_net", "clip_vision", "style_model", "gligen", "lora" - ComfyUI-spezifische Typen
- "none" - None-Wert
- "unknown" - Nicht bestimmbar

**Beispiel**:
```vba
' Automatische Bestimmung vom any_input-Eingabe-Socket
type_name = GETANYTYPE()
PRINT("Typ: " & type_name)

SELECT CASE type_name
    CASE "image"
        w = GETANYWIDTH()
        h = GETANYHEIGHT()
        PRINT("IMAGE-Typ: " & w & "x" & h)
    CASE "latent"
        PRINT("LATENT-Typ")
    CASE "model"
        PRINT("MODEL-Typ")
    CASE "string"
        PRINT("STRING-Typ")
    CASE ELSE
        PRINT("Sonstiger Typ: " & type_name)
END SELECT
```

---

### GETANYVALUEINT([any_data])

**Beschreibung**: Ruft ganzzahligen Wert aus ANY-Typ-Daten ab

**Argumente**:
- any_data (Any, optional) - Daten
  - Ohne Argumente werden automatisch Daten vom any_input-Eingabe-Socket verwendet

**Rückgabewert**: int - Ganzzahlwert (0, wenn nicht abrufbar)

**Beispiel**:
```vba
' Ganzzahlwert vom any_input-Eingabe-Socket abrufen
int_value = GETANYVALUEINT()
PRINT("Ganzzahlwert: " & int_value)
RETURN1 = int_value
```

---

### GETANYVALUEFLOAT([any_data])

**Beschreibung**: Ruft Gleitkommawert aus ANY-Typ-Daten ab

**Argumente**:
- any_data (Any, optional) - Daten
  - Ohne Argumente werden automatisch Daten vom any_input-Eingabe-Socket verwendet

**Rückgabewert**: float - Gleitkommawert (0.0, wenn nicht abrufbar)

**Beispiel**:
```vba
' Gleitkommawert vom any_input-Eingabe-Socket abrufen
float_value = GETANYVALUEFLOAT()
PRINT("Gleitkommawert: " & float_value)
RETURN1 = float_value
```

---

### GETANYSTRING([any_data])

**Beschreibung**: Ruft Zeichenkette aus ANY-Typ-Daten ab

**Argumente**:
- any_data (Any, optional) - Daten
  - Ohne Argumente werden automatisch Daten vom any_input-Eingabe-Socket verwendet

**Rückgabewert**: str - Zeichenkette (leere Zeichenkette, wenn nicht abrufbar)

**Beispiel**:
```vba
' Zeichenkette vom any_input-Eingabe-Socket abrufen
str_value = GETANYSTRING()
PRINT("Zeichenkette: " & str_value)
RETURN1 = str_value
```

---

## Typprüfungsfunktionen

### ISNUMERIC(value)

**Beschreibung**: Prüft, ob ein Wert numerisch ist

**Argumente**:
- value - Zu prüfender Wert

**Rückgabewert**: 1 (numerisch) oder 0 (nicht numerisch)

**Beispiel**:
```vba
result = ISNUMERIC("123")      ' 1
PRINT("ISNUMERIC('123') = " & result)
result = ISNUMERIC("12.34")    ' 1
PRINT("ISNUMERIC('12.34') = " & result)
result = ISNUMERIC("abc")      ' 0
PRINT("ISNUMERIC('abc') = " & result)
result = ISNUMERIC("")         ' 0
PRINT("ISNUMERIC('') = " & result)

' Praktisches Beispiel: Eingabewertvalidierung
IF ISNUMERIC(TXT1) THEN
    value = CDBL(TXT1)
    PRINT("Als Zahlenwert verarbeitet: " & value)
ELSE
    PRINT("Fehler: Kein Zahlenwert")
END IF
```

---

### ISDATE(value)

**Beschreibung**: Prüft, ob ein Wert als Datum interpretierbar ist

**Argumente**:
- value - Zu prüfender Wert

**Rückgabewert**: 1 (Datum) oder 0 (kein Datum)

**Beispiel**:
```vba
result = ISDATE("2024-01-15")     ' 1
PRINT("ISDATE('2024-01-15') = " & result)
result = ISDATE("2024/01/15")     ' 1
PRINT("ISDATE('2024/01/15') = " & result)
result = ISDATE("15:30:00")       ' 1 (auch Zeitangaben werden erkannt)
PRINT("ISDATE('15:30:00') = " & result)
result = ISDATE("hello")          ' 0
PRINT("ISDATE('hello') = " & result)

' Praktisches Beispiel: Datumsvalidierung
IF ISDATE(TXT1) THEN
    dateVal = DATEVALUE(TXT1)
    PRINT("Als Datum verarbeitet: " & dateVal)
ELSE
    PRINT("Fehler: Kein Datumsformat")
END IF
```

**Unterstützte Formate**:
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

**Beschreibung**: Prüft, ob eine Variable ein Array ist

**Argumente**:
- variable_name - Variablenname (Zeichenkette) oder Array-Variablenreferenz (ARR[]-Notation)

**Rückgabewert**: 1 (Array) oder 0 (kein Array)

**Beispiel**:
```vba
REDIM arr, 10
result = ISARRAY(arr[])      ' 1 (Array-Referenz)
PRINT("ISARRAY(arr[]) = " & result)
result = ISARRAY("arr")      ' 1 (Array-Name als Zeichenkette)
PRINT("ISARRAY('arr') = " & result)
result = ISARRAY("VAL1")     ' 0 (normale Variable)
PRINT("ISARRAY('VAL1') = " & result)

' Praktisches Beispiel: Variablentypprüfung
REDIM myData, 5
myData[0] = "a"
myData[1] = "b"
IF ISARRAY(myData[]) THEN
    PRINT("Es ist ein Array. Anzahl Elemente: " & (UBOUND(myData[]) + 1))
ELSE
    PRINT("Es ist kein Array")
END IF
```

**Hinweis**:
- Übergeben Sie den Array-Namen als Zeichenkette oder eine Array-Variablenreferenz in ARR[]-Notation

---

### TYPE(value)

**Beschreibung**: Gibt den Typ einer Variable als Zeichenkette zurück

**Argumente**:
- value - Wert, dessen Typ ermittelt werden soll

**Rückgabewert**: Typname ("NUMBER", "STRING", "BOOLEAN", "ARRAY", "NULL", "OBJECT")

**Beispiel**:
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

' Praktisches Beispiel: Universelle Typverarbeitung
myValue = VAL1
dataType = TYPE(myValue)
PRINT("TYPE(myValue) = " & dataType)
SELECT CASE dataType
    CASE "NUMBER"
        PRINT("Zahlenwert: " & myValue)
    CASE "STRING"
        PRINT("Zeichenkette: " & myValue)
    CASE "ARRAY"
        PRINT("Array (Anzahl Elemente: " & (UBOUND(myValue[]) + 1) & ")")
    CASE "NULL"
        PRINT("Kein Wert vorhanden")
END SELECT
```

---

## Praktische Beispiele

### Nutzung von Debug-Ausgaben

```vba
' Werte in jedem Verarbeitungsschritt überprüfen
originalValue = VAL1
PRINT("Ursprünglicher Wert: " & originalValue)

processedValue = originalValue * 2
PRINT("Nach Verdopplung: " & processedValue)

finalValue = processedValue + 10
PRINT("Endwert: " & finalValue)

RETURN1 = finalValue
PRINT("In RETURN1 zugewiesen: " & RETURN1)
```

### Eingabewertvalidierung

```vba
' Prüfen, ob numerisch, dann verarbeiten
IF ISNUMERIC(TXT1) THEN
    number = CDBL(TXT1)
    PRINT("TXT1 in Zahl konvertiert: " & number)
    result = number * VAL1
    PRINT("Berechnungsergebnis: " & result)
    RETURN1 = result
    PRINT("In RETURN1 zugewiesen: " & RETURN1)
ELSE
    PRINT("Fehler: TXT1 ist keine Zahl")
    RETURN1 = 0
    PRINT("Standardwert in RETURN1 zugewiesen: " & RETURN1)
END IF
```

### Verzweigung je nach Typ

```vba
' Verarbeitung je nach Datentyp ändern
myData = VAL1
dataType = TYPE(myData)
PRINT("TYPE(myData) = " & dataType)

IF dataType = "NUMBER" THEN
    result = myData * 2
    PRINT("Zahlenverarbeitung: " & result)
ELSEIF dataType = "STRING" THEN
    result = UCASE(myData)
    PRINT("Zeichenkettenverarbeitung: " & result)
ELSEIF dataType = "ARRAY" THEN
    count = UBOUND(myData[]) + 1
    PRINT("Array-Verarbeitung: Anzahl Elemente=" & count)
    FOR i = 0 TO UBOUND(myData[])
        PRINT("  [" & i & "] = " & myData[i])
    NEXT
ELSE
    PRINT("Nicht unterstützter Typ: " & dataType)
END IF
```

---

[← Zurück zum Index der integrierten Funktionen](00_index.md)
