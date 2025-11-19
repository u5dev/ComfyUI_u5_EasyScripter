# u5 EasyScripter Node

[日本語](../../README.md) | [English](../en/README.md) | [中文](../zh/README.md) | [Español](../es/README.md) | [Français](../fr/README.md) | **Deutsch**

---

## Was ist das?
- Ein benutzerdefinierter Knoten für ComfyUI, mit dem Sie **einfache VBA-ähnliche Skripte** ausführen können
- Ermöglicht verschiedene Integrationen wie bedingte Verzweigungen, Prompt-Generierung, Schleifenverarbeitung und externe API-Aufrufe
- **Fast alle Funktionen werden mit Kopier-Einfügen-Beispielen** bereitgestellt, sodass keine Programmiererfahrung erforderlich ist
- Enthält auch verbesserte Versionen von sequentiellen Knoten und Speicherfreigabe-Tools, die anderswo veröffentlicht wurden

```
Entwickelt, weil die Konfiguration mit Standardknoten oder einzelnen Knoten redundant wurde und eine feinkörnige Steuerung schwierig war
```

---

## Empfohlene Funktionen und Anwendungsfälle
- Sie können Workflow-Screenshot-Bilder in ComfyUI ziehen und sofort verwenden

### Automatisch viele Variationen erstellen
- Es ist mühsam, jedes Mal über Prompts nachzudenken. Erstellen Sie schnell viele Ausgaben im Diashow-Stil!
```vba
' Basis-Prompt + jedes Mal zufällig Ausdruck und Pose ändern, um Prompt zu erstellen
' → "base prompt" & "," & RNDCSV("Posen-Kandidaten-CSV") & "," & RNDCSV("Ausdrucks-Kandidaten-CSV")

RETURN1 = "woman, a girl, nurse, with a bandage, pale skin, green eyes, pink hair, blunt bangs,upper body, full body shot, masterpiece, best quality, high quality," & RNDCSV("looking at viewer, looking away, looking back, wink, making a peace sign, making a heart with hands, making a thumbs up, waving at the camera") & "," & RNDCSV("blush, smiling, embarrassed, sleepy, serious expression, fear")
```
<img src="../img/AUTO_SLIDESHOW.png" alt="Beispiel für Prompt-Generierungsskript im EasyScripter-Knoten" width="80%"><br>
  ↓<br>
  Durch Einfügen nur einer Zeile<br>
  ↓<br>
<img src="../img/SLIDES.png" alt="Diashow automatisch generierter Variationsbilder" width="100%">

### Automatische Anpassung der modellspezifischen Latent-Größe
- Das ist SDXL, also die Auflösung ist so und so – wer hat Zeit dafür!
```vba
result = OPTIMAL_LATENT("SDXL", 4, 3) ' Wird automatisch auf 1152x896 angepasst
RETURN1 = RESULT[0] '1152
RETURN2 = RESULT[1] '896
```
<img src="../img/OPTIMAL_LATENT.png" alt="Beispiel für automatische Anpassung der modelloptimalen Auflösung mit der OPTIMAL_LATENT-Funktion" width="80%"><br>

**Fügen Sie es einfach in das Skriptfenster am unteren Rand des Knotens ein, und es verwandelt sich sofort in einen professionellen Knoten mit Spezialfunktionen**

---

## 📖 Dokumentation

Detaillierte Dokumentation finden Sie hier:

- **[📖 Skriptsprachen-Referenz](01_syntax_reference.md)** - Vollständiger Leitfaden zu Grammatik und Kontrollstrukturen
- **[🔧 Integrierte Funktionsreferenz](00_index.md)** - Vollständige Referenz von über 100 integrierten Funktionen
- **[🌟 Bitte unterstützen Sie uns](CONTENTS.md)** - Praktischere und nützlichere Beispiele, umfangreiche Workflow-Bilder, detaillierte Erklärungen

---

## Lösungen mit u5 EasyScripter

**Ein Knoten, unendliche Möglichkeiten** - u5 EasyScripter ist eine universelle Skript-Engine, die auf ComfyUI läuft:

- ✅ **Ersetzt über 10 dedizierte Knoten**: Textverarbeitung, mathematische Berechnungen, bedingte Logik, Zufallsgenerierung
- ✅ **Beschleunigt Batch-Verarbeitung**: Automatische Parameter-Sweeps, intelligente Variationsgenerierung
- ✅ **Verbessert Prompt Engineering**: Dynamische Gewichtsanpassung, Modifikationen durch bedingte Verzweigungen, intelligente Variationen
- ✅ **Optimiert Workflows**: Saubere Graphen, schnelles Laden, einfaches Teilen
- ✅ **Skalierbar**: Von einfachen Berechnungen bis zu komplexen Automatisierungsalgorithmen
- ✅ **Parallele Ausführungsschutz**: Sichere Warteschlangenverarbeitung ohne Einfrieren bei gleichzeitiger Ausführung mehrerer Knoten
- ✅ **Mehrsprachig**: Fehlermeldungen und Debug-Ausgaben in Japanisch und Englisch

---

## ⚡ Schnellstart

### Installation

```bash
# In das custom_nodes-Verzeichnis von ComfyUI klonen
git clone https://github.com/u5dev/ComfyUI_u5_EasyScripter.git
```

### Ihr erster intelligenter Workflow
- Intelligente Anpassung basierend auf Prompt-Regeln, die vom Modelltyp gefordert werden

```vba
model_type = TXT1  ' Modellname verbinden ("sdxl" oder "Flux")
PRINT(model_type)  ' Modelltyp bestätigen
base_prompt = "beautiful landscape"

SELECT CASE model_type
    CASE "sdxl"
        RETURN1 = "(" & base_prompt & ", ultra-detailed wide landscape, crisp daylight photography, shot on full-frame DSLR, high dynamic range, 8k uhd, professional photography:1.2)"
        PRINT(RETURN1)  ' SDXL-Prompt bestätigen
    CASE "flux"
        RETURN1 = "(" & base_prompt & "moody cinematic wide shot of a beautiful landscape at golden hour, dramatic backlight haze, soft volumetric light, cinematic lighting:1.1, subtle film grain)"
        PRINT(RETURN1)  ' Flux-Prompt bestätigen
    CASE ELSE
        RETURN1 = base_prompt & ", high quality"
        PRINT(RETURN1)  ' Standard-Prompt bestätigen
END SELECT
```
<img src="../img/FIRST_WORFLOW.png" alt="Beispiel für Workflow mit Prompt-Anpassung nach Modelltyp" width="50%">

---

## 💡 Grundlegende Verwendung

### Knotenkonfiguration

Der **EasyScripter-Knoten** hat folgende Konfiguration:

#### Eingaben
- `script`: VBA-Stil-Skript schreiben (erforderlich)
- `VAL1_int`, `VAL1_float`: Numerische Eingabe 1 (summiert als `VAL1` verfügbar)
- `VAL2_int`, `VAL2_float`: Numerische Eingabe 2 (summiert als `VAL2` verfügbar)
- `TXT1`, `TXT2`: Texteingaben
- `any_input`: ANY-Typ-Eingabe (akzeptiert alles: MODEL, CLIP, VAE, etc.)

#### Ausgaben
- `RETURN1_int`, `RETURN1_float`, `RETURN1_text`: Hauptrückgabewert (gleichzeitige Ausgabe in 3 Formaten)
- `RETURN2_int`, `RETURN2_float`, `RETURN2_text`: Sekundärrückgabewert (gleichzeitige Ausgabe in 3 Formaten)
- `relay_output`: Vollständige Bypass-Ausgabe von `any_input` (steuerbar mit RELAY_OUTPUT-Variable)

![Beispiel für grundlegende Verbindung des EasyScripter-Knotens](../img/SimpleConnection.png)

### Einfache Beispiele
Kopieren und fügen Sie diese in den obigen Workflow ein

#### Grundlegende Berechnung
```vba
' Addiert zwei Werte und gibt das Ergebnis zurück
result = VAL1 + VAL2
PRINT(result)  ' Ergebnis bestätigen
RETURN1 = result
```

#### Zeichenkettenverkettung
```vba
' Kombiniert zwei Texte
combined = TXT1 & " " & TXT2
PRINT(combined)  ' Kombiniertes Ergebnis bestätigen
RETURN1 = combined
```

#### Bedingte Verzweigung
```vba
' Nachricht je nach Wert ändern
IF VAL1 > 10 THEN
    RETURN1 = "Groß"
    PRINT(RETURN1)  ' Verzweigungsergebnis bestätigen
ELSE
    RETURN1 = "Klein"
    PRINT(RETURN1)  ' Verzweigungsergebnis bestätigen
END IF
```

**Einzeilige IF-Anweisungen und EXIT-Anweisungen** (ab v2.1.1):
```vba
' Frühzeitige Rückkehr in Funktionen
FUNCTION Validate(value)
    IF value < 0 THEN EXIT FUNCTION  ' Bei negativem Wert sofort beenden
    Validate = value * 2
END FUNCTION

' Frühzeitiger Abbruch von Schleifen
FOR i = 1 TO 100
    IF i > 50 THEN EXIT FOR  ' Schleife beenden, wenn i über 50
    sum = sum + i
NEXT

RETURN1 = sum
RETURN2 = i
```

#### Zufallsauswahl
```vba
' Zufällige Auswahl aus CSV (bei Auslassung des Index)
styles = "realistic, anime, oil painting, watercolor"
selected = PICKCSV(styles)  ' Zufallsauswahl
PRINT(selected)  ' Auswahlresultat bestätigen
RETURN1 = selected

' Oder spezifischen Index angeben (1-basiert)
' selected = PICKCSV(styles, 2)  ' Wählt zweites Element "anime"
' PRINT(selected)  ' "anime"
```

---

## 🛠️ u5 Loader-Serie

Loader-Knoten mit Dateinamenausgabefunktion zur Verwendung mit EasyScripter:

- **u5 Checkpoint Loader** - MODEL, CLIP, VAE + Dateinamenausgabe
- **u5 LoRA Loader** - Modell + LoRA-Anwendung + Dateinamenausgabe
- **u5 VAE Loader** - VAE + Dateinamenausgabe
- **u5 ControlNet Loader** - ControlNet + Dateinamenausgabe
- **u5 CLIP Vision Loader** - CLIP Vision + Dateinamenausgabe
- **u5 Style Model Loader** - StyleModel + Dateinamenausgabe
- **u5 GLIGEN Loader** - GLIGEN + Dateinamenausgabe
- **u5 UNET Loader** - UNET + Dateinamenausgabe
- **u5 CLIP Loader** - CLIP + Dateinamenausgabe

Alle u5-Loader haben folgende gemeinsame Funktionen:
- Dateinamensuche über `text_input`-Feld (Teilübereinstimmung)
- `filename`-Ausgabe gibt geladenen Dateinamen als Text aus

---

## 🔍 Fehlerbehebung

### Skript verursacht Fehler
- Bei Verwendung der PRINT-Funktion für Debug-Ausgabe verwenden Sie die Funktionsform mit Klammern: `PRINT("LOG", wert)`
  - **Hinweis**: Die VBA-Anweisungsform (`PRINT "LOG", wert`) wird nicht unterstützt
- Überprüfen Sie Rechtschreibfehler und Groß-/Kleinschreibung von Variablennamen

### Funktion nicht gefunden
- Überprüfen Sie die Schreibweise des Funktionsnamens
- Bestätigen Sie den korrekten Funktionsnamen im [Index der integrierten Funktionen](00_index.md)

### Rückgabewert entspricht nicht den Erwartungen
- Bei Verwendung der PRINT-Funktion zur Überprüfung von Zwischenwerten verwenden Sie auch die Form mit Klammern (`PRINT("Zwischenwert:", variable)`)
- Prüfen Sie, ob Typkonvertierung (CINT, CDBL, CSTR) erforderlich ist

### Sieht merkwürdig aus
- Speichern Sie den Workflow und aktualisieren Sie mit F5

---

## 📜 Lizenz

MIT License

Copyright (c) 2025 u5dev

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

## 📝 Änderungshistorie

Detaillierte Versionshistorie finden Sie in [CHANGELOG.md](CHANGELOG.md).

---

## 🙏 Danksagungen

Vielen Dank an die ComfyUI-Community.
