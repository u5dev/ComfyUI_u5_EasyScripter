# Vollständiger Index der integrierten Funktionen

[← Zurück zur Hauptdokumentation](README.md)

**Diese Seite ist der Referenz-Index für die integrierten Funktionen von u5 EasyScripter.**

u5 EasyScripter bietet eine Fülle von integrierten Funktionen zur Verwendung in VBA-Stil-Skripten.

## Funktionskategorie-Liste

### [Mathematische Funktionen-Referenz](01_math_functions.md)
16 mathematische Funktionen - Grundrechenarten, trigonometrische Funktionen, Logarithmen, statistische Funktionen etc.

### [Zeichenkettenfunktionen-Referenz](02_string_functions.md)
28 Zeichenkettenfunktionen - Zeichenkettenmanipulation, Suche, Ersetzung, Formatierung etc.

### [Datums-/Zeitfunktionen-Referenz](03_datetime_functions.md)
12 Datums-/Zeitfunktionen - Aktuelle Datum/Uhrzeit, Datumsberechnungen, Datums-/Zeitkomponentenabruf, Datumskonvertierung etc.

### [CSV-Funktionen-Referenz](04_csv_functions.md)
9 CSV-Funktionen - CSV-Operationen, Zufallsauswahl, Duplikatentfernung etc.

### [Reguläre Ausdrucks-Funktionen-Referenz](05_regex_functions.md)
7 Funktionen für reguläre Ausdrücke - Musterabgleich, Ersetzung, Extraktion etc.

### [Array-Funktionen-Referenz](06_array_functions.md)
3 Array-Funktionen - Array-Initialisierung, Größenänderung, Abruf des oberen Index etc.

### [Typkonvertierungs-/Typprüfungs-Funktionen-Referenz](07_type_functions.md)
7 Typkonvertierungs-/Typprüfungs-Funktionen - Typkonvertierung, Typprüfung, Formatformatierung etc.

### [Modellfunktionen-Referenz](08_model_functions.md)
1 Modellfunktion - Optimale Auflösungsbestimmung für AI-Generierungsmodelle

### [Dienstprogrammfunktionen-Referenz](09_utility_functions.md)
18 Dienstprogrammfunktionen - Debug-Ausgabe, Typbestimmung, Datei-Ein-/Ausgabe, Dateiexistenzprüfung, Speicherfreigabe, Sleep, Bildverarbeitung (IMAGE→JSON-Array/Base64-Konvertierung), Bild-/Latent-Datenabruf, ANY-Typ-Datenabruf etc.

---

## Schnellreferenztabelle

### Mathematische Funktionen (16)

| Funktionsname | Übersicht |
|---------------|-----------|
| **ABS(value)** | Gibt den Absolutwert zurück |
| **INT(value)** | Gibt den ganzzahligen Teil zurück (Nachkommastellen abschneiden) |
| **ROUND(value, [digits])** | Gibt einen gerundeten Wert zurück |
| **SQRT(value)** | Gibt die Quadratwurzel zurück |
| **MIN(value1, value2, ...)** | Gibt den Mindestwert zurück |
| **MAX(value1, value2, ...)** | Gibt den Maximalwert zurück |
| **SIN(radians)** | Gibt den Sinus zurück |
| **COS(radians)** | Gibt den Kosinus zurück |
| **TAN(radians)** | Gibt den Tangens zurück |
| **RADIANS(degrees)** | Konvertiert Grad in Bogenmaß |
| **DEGREES(radians)** | Konvertiert Bogenmaß in Grad |
| **POW(base, exponent)** | Berechnet die Potenz (base^exponent) |
| **LOG(value, [base])** | Gibt den Logarithmus zurück (Standard: natürlicher Logarithmus) |
| **EXP(value)** | e (Basis des natürlichen Logarithmus) hoch Wert |
| **AVG(value1, value2, ...)** | Berechnet den Durchschnitt |
| **SUM(value1, value2, ...)** | Berechnet die Summe |

### Zeichenkettenfunktionen (28)

| Funktionsname | Übersicht |
|---------------|-----------|
| **LEN(text)** | Gibt die Länge der Zeichenkette zurück |
| **LEFT(text, length)** | Ruft die angegebene Anzahl von Zeichen von links ab |
| **RIGHT(text, length)** | Ruft die angegebene Anzahl von Zeichen von rechts ab |
| **MID(text, start, length)** | Ruft Teilzeichenkette von angegebener Position ab |
| **UPPER(text)** | In Großbuchstaben konvertieren |
| **LOWER(text)** | In Kleinbuchstaben konvertieren |
| **TRIM(text)** | Entfernt führende und nachfolgende Leerzeichen |
| **REPLACE(text, old, new)** | Ersetzt Zeichenkette |
| **INSTR([start,] text, search)** | Sucht Zeichenkette (gibt Position zurück) |
| **INSTRREV(text, search, [start])** | Sucht Zeichenkette von hinten |
| **STRREVERSE(text)** | Kehrt Zeichenkette um |
| **STRCOMP(text1, text2, [compare])** | Vergleicht Zeichenketten |
| **SPACE(number)** | Erzeugt angegebene Anzahl von Leerzeichen |
| **STRING(number, character)** | Wiederholt Zeichen |
| **FORMAT(value, format_string)** | Formatiert Wert |
| **SPLIT(text, [delimiter])** | Teilt Zeichenkette und konvertiert in Array |
| **JOIN(array, [delimiter])** | Verbindet Array zu Zeichenkette |
| **LTRIM(text)** | Entfernt linke Leerzeichen |
| **RTRIM(text)** | Entfernt rechte Leerzeichen |
| **UCASE(text)** | In Großbuchstaben konvertieren (Alias für UPPER) |
| **LCASE(text)** | In Kleinbuchstaben konvertieren (Alias für LOWER) |
| **PROPER(text)** | In Titelfall konvertieren |
| **CHR(code)** | Zeichencode→Zeichen-Konvertierung |
| **ASC(char)** | Zeichen→Zeichencode-Konvertierung |
| **STR(value)** | Zahl→Zeichenkette-Konvertierung |
| **URLENCODE(text, [encoding])** | URL-Kodierung |
| **URLDECODE(text, [encoding])** | URL-Dekodierung |
| **ESCAPEPATHSTR(path, [replacement])** | Verarbeitet Dateipfad-Verbotene-Zeichen |

### Datums-/Zeitfunktionen (12)

| Funktionsname | Übersicht |
|---------------|-----------|
| **NOW()** | Ruft aktuelles Datum und Uhrzeit ab |
| **DATE()** | Ruft heutiges Datum ab |
| **TIME()** | Ruft aktuelle Uhrzeit ab |
| **YEAR([date])** | Ruft Jahr ab |
| **MONTH([date])** | Ruft Monat ab |
| **DAY([date])** | Ruft Tag ab |
| **HOUR([time])** | Ruft Stunde ab |
| **MINUTE([time])** | Ruft Minute ab |
| **SECOND([time])** | Ruft Sekunde ab |
| **DATEADD(interval, number, [date])** | Addiert/subtrahiert vom Datum |
| **DATEDIFF(interval, date1, [date2])** | Berechnet Datumsdifferenz |
| **WEEKDAY([date], [firstday])** | Gibt Wochentag zurück (1=Sonntag) |

### CSV-Funktionen (9)

| Funktionsname | Übersicht |
|---------------|-----------|
| **CSVCOUNT(csv_text)** | Zählt CSV-Elemente |
| **CSVREAD(csv_text, index)** | Ruft Element mit angegebenem Index aus CSV-Zeichenkette ab |
| **CSVUNIQUE(csv_text)** | Entfernt Duplikate |
| **CSVMERGE(csv1, csv2, ...)** | Verbindet mehrere CSVs |
| **CSVDIFF(array_name, csv1, csv2)** | Ruft CSV-Differenz ab |
| **PICKCSV(csv_text, [index])** | Wählt CSV-Element (bei Auslassung: zufällig) |
| **RNDCSV(csv_text)** | Zufällige Auswahl aus CSV (identisch mit PICKCSV) |
| **CSVJOIN(array, [delimiter])** | Verbindet Array zu CSV-Zeichenkette |
| **CSVSORT(csv_text, [delimiter], [reverse])** | Sortiert CSV-Elemente |

### Funktionen für reguläre Ausdrücke (7)

| Funktionsname | Übersicht |
|---------------|-----------|
| **REGEX(pattern, text)** | Testet Musterabgleich |
| **REGEXMATCH(pattern, text)** | Ruft erste Übereinstimmung ab |
| **REGEXREPLACE(pattern, text, replacement)** | Ersetzt Muster |
| **REGEXEXTRACT(pattern, text, [group])** | Extrahiert Gruppe |
| **REGEXCOUNT(pattern, text)** | Zählt Übereinstimmungen |
| **REGEXMATCHES(pattern, text)** | Ruft alle Übereinstimmungen als Array ab |
| **REGEXSPLIT(pattern, text)** | Teilt nach Muster |

### Array-Funktionen (3)

| Funktionsname | Übersicht |
|---------------|-----------|
| **UBOUND(array)** | Ruft oberen Index des Arrays ab |
| **ARRAY(variable_name, value1, value2, ...)** | Initialisiert Array und setzt Werte |
| **REDIM(array_name, size)** | Ändert Array-Größe (Neudefinition) |

### Typkonvertierungs-/Typprüfungs-Funktionen (7)

| Funktionsname | Übersicht |
|---------------|-----------|
| **CSTR(value)** | In Zeichenkette konvertieren |
| **CINT(value)** | In Ganzzahl konvertieren |
| **CDBL(value)** | In Gleitkommazahl konvertieren |
| **FORMAT(value, [format_string])** | Formatiert Zahl/Datum in angegebenem Format (VBA-kompatibel) |
| **ISNUMERIC(value)** | Bestimmt, ob Zahl |
| **ISDATE(value)** | Bestimmt, ob Datum |
| **ISARRAY(variable_name)** | Bestimmt, ob Array |

### Modellfunktionen (1)

| Funktionsname | Übersicht |
|---------------|-----------|
| **OPTIMAL_LATENT(model_hint, width, height)** | Bestimmt automatisch die optimale Latent-Raumgröße aus Modellname und Seitenverhältnis |

### Dienstprogrammfunktionen (18)

| Funktionsname | Übersicht |
|---------------|-----------|
| **PRINT(message, ...)** | Gibt Wert in Textbereich aus (für Debugging) |
| **OUTPUT(arg, [path], [flg])** | Gibt Text, Zahlen, Arrays, Bilder, Binärdaten in Datei aus |
| **INPUT(path)** | Lädt Datei aus ComfyUI-Ausgabeordner (dynamische Typbestimmung) |
| **ISFILEEXIST(path, [flg])** | Dateiexistenzprüfung und erweiterte Info-Abruf (_NNNN-Suche, Bildgröße, Dateigröße) |
| **VRAMFREE([min_free_vram_gb])** | Gibt VRAM und RAM frei (Modell entladen, Cache löschen, GC) |
| **SLEEP([milliseconds])** | Pausiert Verarbeitung für angegebene Millisekunden (Standard: 10ms) |
| **IMAGETOBYTEARRAY(image_input, [max_size], [format], [return_format])** | Konvertiert IMAGE/Dateipfad in Bild-JSON-Array |
| **IMAGETOBASE64(image_input, [max_size], [format], [return_format])** | Konvertiert IMAGE/Dateipfad in Base64-Kodierung (für Vision API) |
| **GETANYWIDTH([any_data])** | Ruft Breite (Pixelanzahl) von IMAGE/LATENT-Typ-Daten ab |
| **GETANYHEIGHT([any_data])** | Ruft Höhe (Pixelanzahl) von IMAGE/LATENT-Typ-Daten ab |
| **GETANYTYPE([any_data])** | Bestimmt Typname von ANY-Typ-Daten |
| **GETANYVALUEINT([any_data])** | Ruft Ganzzahlwert von ANY-Typ-Daten ab |
| **GETANYVALUEFLOAT([any_data])** | Ruft Gleitkommawert von ANY-Typ-Daten ab |
| **GETANYSTRING([any_data])** | Ruft Zeichenkette von ANY-Typ-Daten ab |
| **ISNUMERIC(value)** | Bestimmt, ob Wert eine Zahl ist |
| **ISDATE(value)** | Bestimmt, ob Wert als Datum analysierbar ist |
| **ISARRAY(variable_name)** | Bestimmt, ob Variable ein Array ist |
| **TYPE(value)** | Gibt Typ der Variable als Zeichenkette zurück |

---

[← Zurück zur Hauptdokumentation](README.md)
