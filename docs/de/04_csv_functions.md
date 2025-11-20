# CSV-Funktionen-Referenz

[← Zurück zum Index der integrierten Funktionen](00_index.md)

## Übersicht

Funktionsgruppe zur Manipulation von CSV-Zeichenketten (durch Komma getrennte Werte). Nützlich für Prompt-Generierung und Verwaltung von Konfigurationswerten.

- Zählen und Abrufen von CSV-Elementen
- Prompt-Generierung durch zufällige Auswahl
- Duplikatentfernung und Differenzermittlung
- Gegenseitige Konvertierung zwischen Array und CSV

---

## Funktionsliste

### CSVCOUNT(csv_text)

**Beschreibung**: Zählt CSV-Elemente

**Argumente**:
- csv_text - Durch Komma getrennte Zeichenkette

**Rückgabewert**: Anzahl der Elemente (Ganzzahl)

**Beispiel**:
```vba
count = CSVCOUNT("apple,banana,orange")
PRINT(count)    ' 3
count = CSVCOUNT("")
PRINT(count)    ' 0
count = CSVCOUNT("single")
PRINT(count)    ' 1
```

---

### CSVREAD(csv_text, index)

**Beschreibung**: Ruft Element am angegebenen Index aus CSV-Zeichenkette ab

**Argumente**:
- csv_text - Durch Komma getrennte Zeichenkette
- index - Abzurufender Element-Index (1-basiert)

**Rückgabewert**: Element an angegebener Position (Zeichenkette). Leere Zeichenkette bei außerhalb des Bereichs

**Beispiel**:
```vba
element = CSVREAD("apple,banana,orange", 2)
PRINT(element)    ' banana
element = CSVREAD("a,b,c,d", 1)
PRINT(element)    ' a
element = CSVREAD("x,y,z", 10)
PRINT(element)    ' (leere Zeichenkette bei außerhalb des Bereichs)
```

---

### CSVUNIQUE(csv_text)

**Beschreibung**: Entfernt Duplikate

**Argumente**:
- csv_text - Durch Komma getrennte Zeichenkette

**Rückgabewert**: CSV-Zeichenkette nach Duplikatentfernung

**Beispiel**:
```vba
result = CSVUNIQUE("a,b,a,c,b")
PRINT(result)    ' a,b,c
result = CSVUNIQUE("1,2,3,2,1")
PRINT(result)    ' 1,2,3
```

---

### CSVMERGE(csv1, csv2, ...)

**Beschreibung**: Verbindet mehrere CSVs

**Argumente**:
- csv1, csv2, ... - Mehrere CSV-Zeichenketten (variable Argumentlänge)

**Rückgabewert**: Verbundene CSV-Zeichenkette

**Beispiel**:
```vba
result = CSVMERGE("a,b", "c,d")
PRINT(result)        ' a,b,c,d
result = CSVMERGE("1,2", "3", "4,5")
PRINT(result)        ' 1,2,3,4,5
```

---

### CSVDIFF(array_name, csv1, csv2)

**Beschreibung**: Speichert Differenz zweier CSV-Zeichenketten (Elemente, die nur in einer von beiden existieren) in Array

**Argumente**:
- array_name - Variablenname des Arrays zur Speicherung des Ergebnisses
- csv1 - CSV-Zeichenkette 1
- csv2 - CSV-Zeichenkette 2

**Rückgabewert**: Anzahl der Differenzelemente (Ganzzahl)

**Beispiel**:
```vba
' Ruft Elemente ab, die in csv1 aber nicht in csv2 existieren, sowie Elemente, die in csv2 aber nicht in csv1 existieren
DIM diff_array
count = CSVDIFF(diff_array, "a,b,c,d", "b,d,e")
PRINT(count)           ' 3
PRINT(diff_array(0))   ' a
PRINT(diff_array(1))   ' c
PRINT(diff_array(2))   ' e
```

---

### PICKCSV(csv_text, [index])

**Beschreibung**: Wählt CSV-Element aus

**Argumente**:
- csv_text - CSV-Zeichenkette
- index - Index (Standard: zufällige Auswahl)

**Rückgabewert**: Ausgewähltes Element (Zeichenkette)

**Beispiel**:
```vba
result = PICKCSV("red,green,blue", 2)
PRINT(result)     ' green
result = PICKCSV("A,B,C,D")
PRINT(result)     ' Eines von A, B, C oder D
```

---

### RNDCSV(csv_text, [count])

**Beschreibung**: Zufällige Auswahl aus CSV (auch mehrfache Element-Array-Abruf möglich)

**Argumente**:
- csv_text - CSV-Zeichenkette
- count - Anzahl der auszuwählenden Elemente (Standard: gibt 1 Zeichenkette zurück)

**Rückgabewert**:
- count nicht angegeben: Zufällig ausgewähltes 1 Element (Zeichenkette)
- count=1: Zufällig ausgewähltes 1 Element (Zeichenkette)
- count≥2: Liste zufällig ausgewählter Elemente
- count >= Elementanzahl: Vollständiges Array mit Beibehaltung der ursprünglichen Sortierreihenfolge

**Beispiel**:
```vba
' Auswahl eines Elements (wie bisher)
style = RNDCSV("realistic,anime,cartoon,abstract")
PRINT(style)
color = RNDCSV("red,blue,green,yellow,purple")
PRINT(color)

' Abrufen mehrerer Elemente als Array (mit Duplikaten)
DIM selected[3]
selected = RNDCSV("A,B,B,B,C,C,D", 3)
PRINT(selected)  ' z.B.: ["B", "B", "D"]

' Bei Überschreitung der Elementanzahl alle Elemente in ursprünglicher Reihenfolge
DIM all[3]
all = RNDCSV("X,Y,Z", 5)
PRINT(all)  ' ["X", "Y", "Z"] (Beibehaltung der ursprünglichen Reihenfolge)

' Zusammenarbeit mit RANDOMIZE (fester Seed-Wert)
RANDOMIZE(12345)
result = RNDCSV("1,2,3,4,5", 3)
PRINT(result)  ' Reproduzierbare zufällige Auswahl
```

---

### CSVJOIN(array, [delimiter])

**Beschreibung**: Verbindet Array zu CSV-Zeichenkette

**Argumente**:
- array - Array
- delimiter - Trennzeichen (Standard: Komma)

**Rückgabewert**: Verbundene CSV-Zeichenkette

**Beispiel**:
```vba
DIM items(2)
items(0) = "apple"
items(1) = "banana"
items(2) = "orange"
result = CSVJOIN(items)
PRINT(result)           ' apple,banana,orange
result = CSVJOIN(items, "|")
PRINT(result)           ' apple|banana|orange
```

---

### CSVSORT(csv_text, [delimiter], [descending])

**Beschreibung**: Sortiert CSV-Elemente

**Argumente**:
- csv_text - Text, getrennt durch Trennzeichen
- delimiter - Trennzeichen (Standard: ",")
- descending - Absteigende Reihenfolge-Flag (Standard: False, 0=aufsteigend, 1 oder True=absteigend)

**Rückgabewert**: Sortierte CSV-Zeichenkette

**Beispiel**:
```vba
result = CSVSORT("dog,cat,bird,ant")
PRINT(result)      ' ant,bird,cat,dog
result = CSVSORT("3,1,4,1,5,9,2,6")
PRINT(result)      ' 1,1,2,3,4,5,6,9
result = CSVSORT("Z,A,M,B", ",", 1)
PRINT(result)      ' Z,M,B,A
result = CSVSORT("z;a;m;b", ";")
PRINT(result)      ' a;b;m;z
```

---

## Praktische Beispiele

### Zufällige Auswahl für Prompt-Generierung

```vba
' Zufällige Auswahl eines Stils (1 Element)
style = RNDCSV("photorealistic,anime,oil painting,watercolor")
PRINT(style)
' Zufällige Auswahl des Farbtons
tone = RNDCSV("warm,cool,vivid,muted,monochrome")
PRINT(tone)
' Zufällige Auswahl der Tageszeit
time = RNDCSV("morning,noon,sunset,night")
PRINT(time)

PRINT("1girl, " & style & ", " & tone & " tone, " & time)

' Mischung mehrerer Stile (Array-Auswahl)
DIM styles[3]
styles = RNDCSV("realistic,anime,3d,sketch,oil,watercolor,digital", 3)
PRINT(styles)
stylePrompt = CSVJOIN(styles, ", ")
PRINT(stylePrompt)
PRINT("1girl, " & stylePrompt)
```


### Duplikatentfernung und Verbindung von Listen

```vba
' Verbinden mehrerer Tag-Listen
tags1 = "girl,outdoor,sunny,smile"
PRINT(tags1)
tags2 = "outdoor,happy,smile,park"
PRINT(tags2)
tags3 = "girl,smile,nature"
PRINT(tags3)

' Verbinden
allTags = CSVMERGE(tags1, tags2, tags3)
PRINT(allTags)
' "girl,outdoor,sunny,smile,happy,smile,park,girl,smile,nature"

' Duplikate entfernen
uniqueTags = CSVUNIQUE(allTags)
PRINT(uniqueTags)
' "girl,outdoor,sunny,smile,happy,park,nature"
```

---

[← Zurück zum Index der integrierten Funktionen](00_index.md)
