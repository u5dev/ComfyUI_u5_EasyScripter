# Änderungshistorie (CHANGELOG)

Dies ist die wichtigste Versionsaktualisierungshistorie von u5 EasyScripter.

---

## 📝 Änderungshistorie

### v3.1.2 (2025-11-18) - Dokumentationsformat-Korrekturen

#### Fixed
- **Funktionsanzahl-Querverweis-Korrektur**: Funktionsanzahl in docs/02_builtin_functions/00_index.md an tatsächliche Implementierungsanzahl angepasst
  - Mathematische Funktionen: 24 → 16
  - CSV-Funktionen: 11 → 9
  - Array-Funktionen: 7 → 3
  - Modellfunktionen: 3 → 1
  - Dienstprogrammfunktionen: 21 → 18
  - Schleifenkontrollfunktionen: 9 → 1
  - HTTP-Kommunikationsfunktionen: 17 → 9
  - Python-Funktionsausführung: 3 → 4
- **Schnellreferenztabellen-Korrektur**: Schnellreferenztabelle in 00_index.md korrigiert
  - 8 nicht existierende Funktionen aus mathematischer Funktionstabelle entfernt (RND, RANDOMIZE, FIX, SGN, ASIN, ACOS, ATAN, ATAN2)
  - CSVDIFF-Funktionsargumente korrigiert: CSVDIFF(csv1, csv2) → CSVDIFF(array_name, csv1, csv2)
  - PYDECODE-Funktion zur Python-Funktionstabelle hinzugefügt
- **Zeichenkettenfunktionsanzahl-Korrektur**: Funktionsanzahl in docs/02_builtin_functions/02_string_functions.md von 29 → 28 korrigiert
- **Inhaltsverzeichnis-Ankerlink-Korrektur**: Führenden Bindestrich aus Inhaltsverzeichnis-Ankerlinks in docs/01_syntax_reference.md entfernt (GitHub-Markdown-Spezifikation entsprechend)

### v3.1.1 (2025-11-17) - Zeichenkettenfunktions-Dokumentation hinzugefügt

#### Added
- **Zeichenkettenfunktions-Dokumentation hinzugefügt**: Dokumentation für 7 implementierte Zeichenkettenfunktionen hinzugefügt
  - **ESCAPEPATHSTR(path, [replacement])**: Ersetzt oder entfernt verbotene Zeichen in Dateipfaden
  - **URLENCODE(text, [encoding])**: URL-Kodierung (Prozent-Kodierung)
  - **URLDECODE(text, [encoding])**: URL-Dekodierung
  - **PROPER(text)**: In Titelfall konvertieren (ersten Buchstaben jedes Wortes großschreiben)
  - **CHR(code)**: Zeichencode→Zeichen-Konvertierung (ASCII-Bereich)
  - **ASC(char)**: Zeichen→Zeichencode-Konvertierung
  - **STR(value)**: Zahl→Zeichenkette-Konvertierung
  - Dokumentation: docs/02_builtin_functions/02_string_functions.md
  - Funktionsanzahl: Von 21 → 23 korrigiert

#### Changed
- **Gesamtzahl integrierter Funktionen**: Von 135 Einträgen → 137 Einträge aktualisiert
  - 135 einzigartige Funktionen (133 Funktionen + 2 Aliase)
  - README.md, docs/02_builtin_functions/00_index.md aktualisiert

### v3.1.0 (2025-11-17) - Unterstützung für != Operator

#### Added
- **!= Operator**: C-Stil-Ungleichheitsoperator hinzugefügt
  - Exakt gleiche Funktion wie `<>` Operator (beide verwendbar)
  - Implementierung: script_parser.py (zu TOKEN_PATTERNS-Array hinzugefügt)
  - Test: tests/test_neq_operator.py
  - Dokumentation: docs/01_syntax_reference.md

### v3.0.0 (2025-11-13) - Any_input-Eingangssocket-bezogene Verbesserungen und mehr

### Added
- **IMAGETOBASE64-Funktion**: Funktion zum Konvertieren von IMAGE-Tensoren oder Bilddateipfaden in Base64-Kodierung (oder data-URL-Format) hinzugefügt
  - Unterstützt Datengenerierung für Vision-API-Übertragung (OpenAI etc.)
  - Unterstützt sowohl IMAGE-Tensor (ComfyUI-Knotenverbindung) als auch Dateipfad-Eingabe
  - Bietet Größenänderung, JPEG-Komprimierung (quality=85), RGBA→RGB-Konvertierung, Base64/data-URL-Rückgabe
  - Implementierung: functions/misc_functions.py (MiscFunctions.IMAGETOBASE64)
  - Dokumentation: docs/02_builtin_functions/09_utility_functions.md

- **IMAGETOBYTEARRAY-Funktion**: Funktion zum Konvertieren von IMAGE-Tensoren oder Bilddateipfaden in JSON-Array (oder Byte-Array) hinzugefügt
  - Unterstützt Datengenerierung für REST-API-Übertragung (Cloudflare Workers AI etc.)
  - Unterstützt sowohl IMAGE-Tensor (ComfyUI-Knotenverbindung) als auch Dateipfad-Eingabe
  - Bietet Größenänderung, JPEG-Komprimierung, RGBA→RGB-Konvertierung, JSON-Array/bytes-Typ-Rückgabe
  - Implementierung: functions/misc_functions.py (MiscFunctions.IMAGETOBYTEARRAY)
  - Dokumentation: docs/02_builtin_functions/09_utility_functions.md

- **FORMAT-Funktion**: Funktion zum Formatieren von Zahlen/Datum in angegebenem Format hinzugefügt (VBA-kompatibel)
  - Unterstützt VBA-Format ("0", "0.0", "0.00", "#.##"), Python-Format-Format, Datum-strftime-Format
  - Implementierung: functions/misc_functions.py (MiscFunctions.FORMAT)
  - Dokumentation: docs/02_builtin_functions/07_type_functions.md

- **GETANYTYPE-Funktion**: Funktion zur Bestimmung des Typnamens von ANY-Typ-Daten hinzugefügt
  - Bestimmt Grundtypen (int, float, string), ComfyUI-Typen (image, latent, model, vae, clip etc.)
  - Automatischer Abruf aus any_input-Eingangssocket oder explizite Datenangabe möglich
  - Implementierung: functions/misc_functions.py (MiscFunctions.GETANYTYPE)
  - Dokumentation: docs/02_builtin_functions/09_utility_functions.md

[... weitere Versionsdetails ...]

---

**Vollständige Änderungshistorie**: Siehe [GitHub Releases](https://github.com/u5dev/ComfyUI_u5_EasyScripter/releases)

[← Zurück zur Hauptdokumentation](README.md)
