# Skriptsprachen-Referenz

[← Zurück zur Hauptdokumentation](README.md)

---

## 📑 Inhaltsverzeichnis

- [Grundlagen der Sprachspezifikation](#grundlagen-der-sprachspezifikation)
- [Variablen und Zuweisung](#variablen-und-zuweisung)
- [Reservierte Variablen (Ein-/Ausgabevariablen)](#reservierte-variablen-ein-ausgabevariablen)
- [Datentypsystem](#datentypsystem)
- [Array-Operationen](#array-operationen)
- [Operator-Referenz](#operator-referenz)
- [Kontrollstrukturen](#kontrollstrukturen)
- [Benutzerdefinierte Funktionen (FUNCTION-Anweisung)](#benutzerdefinierte-funktionen-function-anweisung)
- [Kommentarnotation](#kommentarnotation)

---

## 📖 Grundlagen der Sprachspezifikation

### Grundregeln

**Groß-/Kleinschreibung**
- **Variablennamen**: Keine Unterscheidung (`value` und `VALUE` sind gleich)
- **Funktionsnamen**: Keine Unterscheidung (`len` und `LEN` sind gleich)
- **Zeichenkettenvergleich**: Keine Unterscheidung (`"Hello" = "HELLO"` ist True)

**Wichtig**: Wie bei VBA wird bei Variablennamen, Funktionsnamen und Schlüsselwörtern nicht zwischen Groß- und Kleinschreibung unterschieden.

---

## 📝 Variablen und Zuweisung

Variablen können ohne Deklaration verwendet werden. Alle Variablen werden intern als Gleitkommazahlen oder Zeichenketten behandelt.

### Variablendeklaration und Typ

```vba
' Variablen können ohne Deklaration verwendet werden
x = 10
name = "Alice"

' Explizite Deklaration mit DIM-Anweisung (optional)
DIM result
result = x * 2
PRINT(result)  ' 20

' Typen werden automatisch konvertiert
number = "123"    ' Zeichenkette
result = number + 10
PRINT(result)  ' 133
```

### Grundlegende Zuweisung

```vba
' Numerische Zuweisung
a = 10
b = 3.14
c = VAL1 + VAL2

' Zeichenkettenzuweisung
name = "World"
message = TXT1

' Zuweisung von Berechnungsergebnissen
result = a * b + c
PRINT(result)  ' 31.400000000000002
```

---

## 🎯 Reservierte Variablen (Ein-/Ausgabevariablen)

Automatisch verfügbare reservierte Variablen aus ComfyUI:

- **`VAL1`**, **`VAL2`**: Numerische Eingaben (aus ComfyUI verbunden)
- **`TXT1`**, **`TXT2`**: Texteingaben (aus ComfyUI verbunden)
- **`RETURN1`**, **`RETURN2`**: Rückgabewerte des Skripts (numerisch oder Zeichenkette)
  - `RETURN` ist ein Abwärtskompatibilitäts-Alias für RETURN1
- **`RELAY_OUTPUT`**: Steuert den Wert des relay_output-Ausgangssockets (ANY-Typ) (Tier 3-Implementierung)
- **`PRINT`**: Für Debug-Ausgabe (wird mit PRINT-Funktion hinzugefügt)

**Verwendungsbeispiel**:
```vba
' Eingabewerte verarbeiten
result = VAL1 * 2 + VAL2
PRINT(result)  ' 0

' In Ausgabe speichern
RETURN1 = result
RETURN2 = "Berechnungsergebnis: " & result
```

#### RELAY_OUTPUT-Variable

Die `RELAY_OUTPUT`-Variable ist eine spezielle Variable, die den Wert des relay_output-Ausgangssockets (ANY-Typ) steuert.

**Funktionalität**:
- Wenn Sie im Skript einen Wert zu `RELAY_OUTPUT` zuweisen, wird dieser Wert über den relay_output-AusgangsSocket ausgegeben
- Wenn RELAY_OUTPUT nicht verwendet wird, wird wie bisher der any_input-Eingang durchgeleitet

**Verwendungszwecke**:
- Übergabe von mit INPUT-Funktion geladenen Bildern (torch.Tensor) an nachfolgende ComfyUI-Knoten
- Übergabe beliebiger ANY-Typ-Daten (latent, mask etc.) an nachfolgende Knoten

**Verwendungsbeispiel**:
```vba
' Bilddatei laden und an nachfolgenden Knoten übergeben
IMG1 = INPUT("reference.png")
RELAY_OUTPUT = IMG1
```

**Hinweise**:
- Typen, die der RELAY_OUTPUT-Variablen zugewiesen werden können: ANY-Typ (torch.Tensor, list, dict, str, int, float etc.)
- Keine Typkonvertierung (der zugewiesene Wert wird direkt ausgegeben)
- Funktioniert unabhängig von RETURN1/RETURN2

---

## 📊 Datentypsystem

### Grundlegende Datentypen

1. **Numerischer Typ**: Ganzzahlen und Gleitkommazahlen (intern als float)
2. **Zeichenkettentyp**: Umschlossen von doppelten oder einfachen Anführungszeichen
3. **Array-Typ**: Nur eindimensionale Arrays werden unterstützt

### Arten von Zeichenkettenliteralen

#### Normale Zeichenkettenliterale

```vba
' Doppelte Anführungszeichen
text1 = "Hello, World!"

' VBA-Stil-Escape: "" repräsentiert "
text2 = "He said ""hello"""  ' → He said "hello"

' Escape-Sequenzen
text3 = "Line1\nLine2"  ' → Zeilenumbruch wird eingefügt
text4 = "Tab\there"     ' → Tab wird eingefügt
```

#### Raw-Zeichenkettenliterale

Raw-Zeichenkettenliterale minimieren die Escape-Verarbeitung und werden verwendet, wenn Backslashes unverändert behandelt werden sollen.

```vba
' Syntax: r"..."
' Nur VBA-Stil-Escape ("") wird verarbeitet, andere Escape-Sequenzen nicht

' Windows-Pfad (Backslash direkt verwenden)
path = r"C:\Users\Admin\file.txt"
PRINT(path)  ' C:\Users\Admin\file.txt

' JSON-Zeichenkette (VBA-Stil "" verwenden)
json_str = r"{""key"": ""value""}"
PRINT(json_str)  ' {"key": "value"}
result = PYEXEC("json.loads", json_str)
PRINT(result)  ' {"key": "value"}

' Zeichenkette mit Backslashes
pattern = r"Line1\nLine2"
PRINT(pattern)  ' Line1\nLine2
```

**Raw-Zeichenketten-Spezifikation**:
- In `r"..."`-Form geschrieben
- Nur VBA-Stil-Escape `""` wird verarbeitet (`""` → `"`)
- `\` wird als normales Zeichen behandelt (Escapes wie `\n`, `\t` werden nicht verarbeitet)
- `\"` wird als Stringende behandelt (um `"` im String zu verwenden, `""` verwenden)

### Automatische Typkonvertierung

```vba
' Zeichenkette → Zahl
a = "42"
b = a + 8
PRINT(b)  ' 50

' Zahl → Zeichenkette
c = 100
d = "Wert ist " & c
PRINT(d)  ' Wert ist 100

' Umgang mit Wahrheitswerten
trueValue = 1
PRINT(trueValue)  ' 1
falseValue = 0
PRINT(falseValue)  ' 0
```

---

## 🔬 Array-Operationen

Auf Arrays wird mit `[]`-Notation zugegriffen.

### Array-Deklaration und Verwendung

```vba
' Array-Deklaration (DIM ist optional)
DIM numbers[10]

' Wertzuweisung
numbers[0] = 100
numbers[1] = 200
numbers[2] = 300

' Wertreferenz
total = numbers[0] + numbers[1] + numbers[2]
PRINT(total)  ' 600

' Dynamischer Index
FOR i = 0 TO 9
    numbers[i] = i * 10
    PRINT(numbers[i])
NEXT
```

### Zuweisung und Referenz zu Arrays

```vba
' Array-Deklaration und Initialisierung
DIM arr[3]

' Zuweisung zum Array
arr[0] = 100
arr[1] = 200
arr[2] = arr[0] + arr[1]
PRINT(arr[2])  ' 300

' Array-Referenz
RETURN1 = arr[2]
PRINT(RETURN1)  ' 300
```

---

## 🔧 Operator-Referenz

### Arithmetische Operatoren

| Operator | Beschreibung | Beispiel | Ergebnis |
|----------|--------------|----------|----------|
| + | Addition | `5 + 3` | 8 |
| - | Subtraktion | `10 - 3` | 7 |
| * | Multiplikation | `4 * 3` | 12 |
| / | Division | `15 / 3` | 5 |
| ^ | Potenzierung | `2 ^ 3` | 8 |
| MOD | Modulo | `10 MOD 3` | 1 |
| \\ | Ganzzahldivision | `10 \\ 3` | 3 |

**Beispiel**:
```vba
' Addition
result = 10 + 5
PRINT(result)  ' 15

' Subtraktion
result = 10 - 3
PRINT(result)  ' 7

' Multiplikation
result = 4 * 3
PRINT(result)  ' 12

' Division
result = 15 / 3
PRINT(result)  ' 5

' Potenzierung
result = 2 ^ 3
PRINT(result)  ' 8

' Modulo (MOD)
result = 10 MOD 3
PRINT(result)  ' 1

' Zusammengesetzte Operation (Priorität durch Klammern)
result = (10 + 5) * 2
PRINT(result)  ' 30
result = 10 + 5 * 2
PRINT(result)  ' 20
```

### Vergleichsoperatoren

| Operator | Beschreibung | Beispiel | Ergebnis |
|----------|--------------|----------|----------|
| = | Gleich | `5 = 5` | 1 (True) |
| <> | Ungleich | `5 <> 3` | 1 (True) |
| != | Ungleich (C-Stil) | `5 != 3` | 1 (True) |
| < | Kleiner als | `3 < 5` | 1 (True) |
| > | Größer als | `5 > 3` | 1 (True) |
| <= | Kleiner gleich | `3 <= 3` | 1 (True) |
| >= | Größer gleich | `5 >= 5` | 1 (True) |

**Hinweis**: Bei Zeichenkettenvergleichen wird wie bei VBA nicht zwischen Groß- und Kleinschreibung unterschieden. Beispiel: `"Hello" = "HELLO"` ist True.

**Beispiel**:
```vba
' Gleich
result = 5 = 5
PRINT(result)  ' 1
result = 5 = 3
PRINT(result)  ' 0

' Ungleich (<> oder != verwendbar)
result = 5 <> 3
PRINT(result)  ' 1
result = 5 != 3
PRINT(result)  ' 1 (C-Stil auch verwendbar)
result = 5 <> 5
PRINT(result)  ' 0

' Größer als
result = 10 > 5
PRINT(result)  ' 1

' Kleiner als
result = 3 < 10
PRINT(result)  ' 1

' Größer gleich
result = 5 >= 5
PRINT(result)  ' 1
result = 5 >= 6
PRINT(result)  ' 0

' Kleiner gleich
result = 3 <= 10
PRINT(result)  ' 1
```

### Logische Operatoren

| Operator | Beschreibung | Beispiel | Ergebnis |
|----------|--------------|----------|----------|
| AND | Logisches UND | `(5>3) AND (2<4)` | 1 (True) |
| OR | Logisches ODER | `(5<3) OR (2<4)` | 1 (True) |
| NOT | Logisches NICHT | `NOT (5>3)` | 0 (False) |

**Beispiel**:
```vba
' AND-Operation
result = (5 > 3) AND (10 > 5)
PRINT(result)  ' 1
result = (5 > 3) AND (2 > 5)
PRINT(result)  ' 0

' OR-Operation
result = (5 > 3) OR (2 > 5)
PRINT(result)  ' 1
result = (2 > 5) OR (1 > 3)
PRINT(result)  ' 0

' NOT-Operation
result = NOT (5 > 3)
PRINT(result)  ' 0
result = NOT (2 > 5)
PRINT(result)  ' 1
```

### Zeichenkettenoperatoren

| Operator | Beschreibung | Beispiel | Ergebnis |
|----------|--------------|----------|----------|
| & | Verkettung | `"Hello" & " " & "World"` | "Hello World" |

**Beispiel**:
```vba
' Zeichenkettenverkettung (&-Operator)
greeting = "Hello" & " " & "World"
PRINT(greeting)  ' Hello World
result = "Wert ist " & VAL1 & " "
PRINT(result)
```

---

## 🎮 Kontrollstrukturen

### IF-Anweisung (Bedingte Verzweigung)

#### Grundform: IF-Anweisung (Blockform)

```vba
IF VAL1 > 50 THEN
    RETURN1 = "Groß"
END IF
```

#### Mehrzeilige IF-Anweisung

```vba
IF VAL1 > 100 THEN
    RETURN1 = "Sehr groß"
    PRINT("Wert: " & VAL1)
ELSE
    RETURN1 = "Standard"
END IF
```

#### Mehrfachverzweigung mit ELSEIF

```vba
IF VAL1 > 100 THEN
    grade = "A"
ELSEIF VAL1 > 80 THEN
    grade = "B"
ELSEIF VAL1 > 60 THEN
    grade = "C"
ELSE
    grade = "D"
END IF
PRINT(grade)
```

#### Verschachtelte IF-Anweisungen

```vba
IF TXT1 <> "" THEN
    IF LEN(TXT1) > 10 THEN
        IF INSTR(TXT1, "keyword") > 0 THEN
            RETURN1 = "Schlüsselwort gefunden (langer Text)"
        ELSE
            RETURN1 = "Langer Text (kein Schlüsselwort)"
        END IF
    ELSE
        RETURN1 = "Kurzer Text"
    END IF
ELSE
    RETURN1 = "Keine Eingabe"
END IF
```

### FOR...NEXT-Anweisung (Zählschleife)

#### Grundform

```vba
' Von 1 bis 10 wiederholen
FOR i = 1 TO 10
    PRINT("Zähler: " & i)
NEXT
```

#### STEP-Spezifikation

```vba
' In 2er-Schritten erhöhen (nur gerade Zahlen)
sum = 0
FOR i = 0 TO 20 STEP 2
    sum = sum + i
    PRINT(sum)
NEXT

' Rückwärts (Countdown)
FOR i = 10 TO 1 STEP -1
    PRINT(i & "...")
NEXT
PRINT("Start!")
```

#### Verschachtelte Schleifen

```vba
' Einmaleins-Tabelle erstellen
FOR i = 1 TO 9
    row = ""
    FOR j = 1 TO 9
        row = row & (i * j) & " "
    NEXT
    PRINT(row)
NEXT
```

### WHILE...WEND-Anweisung (Bedingungsschleife)

#### Grundform

```vba
count = 0
WHILE count < 10
    count = count + 1
    PRINT("Zähler: " & count)
WEND
```

#### Bedingte Schleife

```vba
' Bestimmtes Zeichen in Eingabezeichenkette suchen
position = 1
found = 0
WHILE position <= LEN(TXT1) AND found = 0
    IF MID(TXT1, position, 1) = "X" THEN
        found = position
    END IF
    position = position + 1
WEND

IF found > 0 THEN
    RETURN1 = "X ist an Position " & found
    PRINT(RETURN1)
ELSE
    RETURN1 = "X nicht gefunden"
    PRINT(RETURN1)
END IF
```

### SELECT CASE-Anweisung (Mehrfachverzweigung)

VBA-Stil SELECT CASE-Anweisungen ermöglichen die prägnante Beschreibung mehrerer bedingter Verzweigungen. Die erste übereinstimmende Case-Klausel wird ausgeführt, danach erfolgt keine weitere Auswertung.

#### Grundform

```vba
SELECT CASE VAL1
    CASE 1
        RETURN1 = "Eins"
    CASE 2
        RETURN1 = "Zwei"
    CASE 3
        RETURN1 = "Drei"
    CASE ELSE
        RETURN1 = "Sonstiges"
END SELECT
```

#### Mehrwertige Case-Anweisung

```vba
' Mehrere Werte kommagetrennt angeben
value = 5
SELECT CASE value
    CASE 1, 3, 5, 7, 9
        result = "Ungerade"
    CASE 2, 4, 6, 8, 10
        result = "Gerade"
    CASE ELSE
        result = "Außerhalb des Bereichs"
END SELECT
PRINT(result)  ' Ungerade
```

#### Case-Anweisung mit Bereichsangabe

```vba
' Bereich mit TO-Operator angeben
score = 75
SELECT CASE score
    CASE 0 TO 59
        grade = "F"
    CASE 60 TO 69
        grade = "D"
    CASE 70 TO 79
        grade = "C"
    CASE 80 TO 89
        grade = "B"
    CASE 90 TO 100
        grade = "A"
    CASE ELSE
        grade = "Ungültig"
END SELECT
PRINT(grade)  ' C
```

#### Kommagetrennte Mehrfachangabe (Wochentagsbeispiel)

```vba
dayNum = WEEKDAY(NOW())
SELECT CASE dayNum
    CASE 1, 7
        dayType = "Wochenende"
    CASE 2, 3, 4, 5, 6
        dayType = "Werktag"
END SELECT
PRINT(dayType)
```

---

## 🔨 Benutzerdefinierte Funktionen (FUNCTION-Anweisung)

In u5 EasyScripter können Sie benutzerdefinierte Funktionen mit VBA-Stil-Function-Anweisungen erstellen. Funktionen bieten einen unabhängigen lokalen Gültigkeitsbereich und verhindern Interferenzen mit globalen Variablen.

### Grundlegende Funktionsdefinition

```vba
' Funktion zum Addieren zweier Zahlen
FUNCTION add(a, b)
    add = a + b  ' Rückgabewert durch Zuweisung an Funktionsname setzen
END FUNCTION

' Funktionsaufruf
result = add(5, 3)
PRINT(result)  ' 8
```

### Funktion, die die größere von zwei Zahlen zurückgibt

```vba
' Funktion, die die größere von zwei Zahlen zurückgibt
FUNCTION maxValue(a, b)
    IF a > b THEN
        maxValue = a
    ELSE
        maxValue = b
    END IF
END FUNCTION

' Verwendungsbeispiel
result = maxValue(10, 20)
PRINT(result)  ' 20
```

### Funktion mit mehreren Argumenten

```vba
' Funktion zum Dekorieren von Prompts
FUNCTION decoratePrompt(prompt, quality, style)
    decorated = prompt

    IF quality = "high" THEN
        decorated = decorated & ", masterpiece, best quality"
    END IF

    IF style <> "" THEN
        decorated = decorated & ", " & style & " style"
    END IF

    decoratePrompt = decorated
END FUNCTION

' Verwendungsbeispiel
finalPrompt = decoratePrompt("portrait", "high", "anime")
PRINT(finalPrompt)  ' portrait, masterpiece, best quality, anime style
```

### Rekursive Funktion

```vba
' Rekursive Funktion zur Berechnung der Fakultät
FUNCTION factorial(n)
    IF n <= 1 THEN
        factorial = 1
    ELSE
        factorial = n * factorial(n - 1)
    END IF
END FUNCTION

result = factorial(5)
PRINT(result)  ' 120
```

---

## 💬 Kommentarnotation

Kommentare beginnen mit einem einfachen Anführungszeichen (`'`).

```vba
' Dies ist ein Kommentar
x = 10  ' Zeilenende-Kommentare sind ebenfalls möglich
PRINT(x)  ' 10

' Mehrzeilige Kommentare
' Jede Zeile beginnt mit einem einfachen Anführungszeichen
```

---

## 📚 Nächste Schritte

- [Integrierte Funktionsreferenz](00_index.md) - Details zu 120 Funktionen
- [Hauptdokumentation](README.md) - Gesamtüberblick und Installationsanleitung

---

**Letzte Aktualisierung**: 3. Oktober 2024

---

[← Zurück zur Hauptdokumentation](README.md)
