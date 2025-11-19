# Array-Funktionen-Referenz

**Sprachen**: [English](../02_builtin_functions/06_array_functions.md) | [日本語](../02_builtin_functions/06_array_functions.md) | [한국어](../ko/06_array_functions.md) | [Français](../fr/06_array_functions.md) | **Deutsch** | [Español](../es/06_array_functions.md)

![](../img/comfyui_u5_easyscripter_banner_800x200.png)

[← Zurück zum Index der integrierten Funktionen](00_index.md)

## Übersicht

Array-Funktionen bieten Operationen wie Array-Initialisierung, Größenänderung und Grenzenermittlung. In u5 EasyScripter verwenden Arrays 0-basierte Indizes und werden mit `[]`-Notation zugegriffen.

**Anzahl der Funktionen in dieser Kategorie**: 3

## Funktionsliste

### UBOUND(array)

**Beschreibung**: Ruft oberen Grenzindex des Arrays ab

**Argumente**:
- array - Array-Variable

**Rückgabewert**: Oberer Grenzindex (0-basiert)

**Spezielle Verarbeitung**: Spezielle Funktion, die von script_engine.py verarbeitet wird

**Beispiel**:
```vba
' Obere Grenze des Arrays abrufen
REDIM ARR, 5
upper = UBOUND(ARR[])
PRINT(upper)   ' 4 (5 Elemente von 0 bis 4)

' Gesamtes Array mit Schleife verarbeiten
ARRAY data[], 10, 20, 30, 40, 50
FOR I = 0 TO UBOUND(data[])
    PRINT(data[I])
NEXT

' Array-Größe bestätigen
ARRAY items[], "apple", "banana", "orange"
size = UBOUND(items[]) + 1
PRINT(size)  ' 3 Elemente
```

---

### ARRAY(variable_name, value1, value2, ...)

**Beschreibung**: Initialisiert Array und setzt Werte

**Argumente**:
- variable_name - Array-Variablenname
- value1, value2, ... - Anfangswerte

**Spezielle Verarbeitung**: Spezielle Funktion, die von script_engine.py verarbeitet wird

**Beispiel**:
```vba
' Initialisierung eines Zeichenketten-Arrays
ARRAY items[], "apple", "banana", "orange"
' items[0] = "apple", items[1] = "banana", items[2] = "orange"

' Initialisierung eines numerischen Arrays
ARRAY numbers[], 10, 20, 30, 40, 50
' numbers[0] = 10, numbers[1] = 20, ...

' Zugriff auf Array-Elemente
ARRAY colors[], "red", "green", "blue"
favoriteColor = colors[1]
PRINT(favoriteColor)  ' "green"

' Array mit Schleife verarbeiten
ARRAY scores[], 85, 92, 78, 95
total = 0
FOR I = 0 TO UBOUND(scores[])
    total = total + scores[I]
NEXT
average = total / (UBOUND(scores[]) + 1)
PRINT(average)
```

---

### REDIM(array_name, size)

**Beschreibung**: Ändert Array-Größe (Neudefinition)

**Argumente**:
- array_name - Array-Name (Zeichenkette)
- size - Neue Größe

**Spezielle Verarbeitung**: Spezielle Funktion, die von script_engine.py verarbeitet wird

**Hinweis**: REDIM löscht bestehende Array-Elemente

**Beispiel**:
```vba
' Array-Initialisierung
REDIM ARR, 10        ' ARR-Array mit 10 Elementen neu definieren
REDIM DATA, 100      ' DATA-Array mit 100 Elementen neu definieren

' Dynamische Größenänderung
size = VAL1
PRINT(size)
REDIM MyArray, size  ' Größe entsprechend VAL1-Wert ändern

' Dynamische Datenverarbeitung mit Array
itemCount = CSVCOUNT(TXT1)
PRINT(itemCount)
REDIM items, itemCount
FOR I = 0 TO itemCount - 1
    items[I] = CSVREAD(TXT1, I + 1)
NEXT
```

## Verwendungsbeispiele für Arrays

### Grundlegende Array-Operationen
```vba
' Array erstellen und Werte setzen
ARRAY names[], "Alice", "Bob", "Charlie", "David"

' Array-Größe bestätigen
count = UBOUND(names[]) + 1
PRINT(count)
PRINT("Anzahl der Array-Elemente: " & count)  ' "Anzahl der Array-Elemente: 4"

' Array nacheinander verarbeiten
FOR I = 0 TO UBOUND(names[])
    PRINT("Name[" & I & "]: " & names[I])
NEXT
```

### Dynamische Array-Größenänderung
```vba
' Array mit Anfangsgröße erstellen
REDIM buffer, 5
FOR I = 0 TO 4
    buffer[I] = I * 10
NEXT

' Größe bei Bedarf ändern
newSize = 10
PRINT(newSize)
REDIM buffer, newSize
' Hinweis: REDIM löscht bestehende Daten
```

### Kombination von Array und CSV
```vba
' CSV-Daten in Array konvertieren
csvData = "apple,banana,orange,grape,melon"
PRINT(csvData)
itemCount = CSVCOUNT(csvData)
PRINT(itemCount)
REDIM fruits, itemCount

FOR I = 0 TO itemCount - 1
    fruits[I] = CSVREAD(csvData, I + 1)
NEXT

' Array-Inhalt bestätigen
FOR I = 0 TO UBOUND(fruits[])
    PRINT("Fruit[" & I & "]: " & fruits[I])
NEXT
```

### Array-Aggregationsverarbeitung
```vba
' Initialisierung eines numerischen Arrays
ARRAY scores[], 85, 92, 78, 95, 88, 91

' Summe berechnen
total = 0
FOR I = 0 TO UBOUND(scores[])
    total = total + scores[I]
NEXT
PRINT(total)

' Durchschnitt berechnen
count = UBOUND(scores[]) + 1
PRINT(count)
average = total / count
PRINT(average)

' Maximalwert suchen
maxScore = scores[0]
PRINT(maxScore)
FOR I = 1 TO UBOUND(scores[])
    IF scores[I] > maxScore THEN
        maxScore = scores[I]
        PRINT(maxScore)
    END IF
NEXT

PRINT("Summe: " & total)
PRINT("Durchschnitt: " & ROUND(average, 2))
PRINT("Höchstpunktzahl: " & maxScore)
```

---

[← Zurück zum Index der integrierten Funktionen](00_index.md)
