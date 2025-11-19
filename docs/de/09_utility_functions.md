# Hilfsfunktionen-Referenz

**Sprachen**: [English](../02_builtin_functions/09_utility_functions.md) | [日本語](../02_builtin_functions/09_utility_functions.md) | [한국어](../ko/09_utility_functions.md) | [Français](../fr/09_utility_functions.md) | **Deutsch** | [Español](../es/09_utility_functions.md)

![](../img/comfyui_u5_easyscripter_banner_800x200.png)

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

**Beispiel**:
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
```

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

[← Zurück zum Index der integrierten Funktionen](00_index.md)
