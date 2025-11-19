# Mathematikfunktionen-Referenz

**Sprachen**: [English](../02_builtin_functions/01_math_functions.md) | [日本語](../02_builtin_functions/01_math_functions.md) | [한국어](../ko/01_math_functions.md) | [Français](../fr/01_math_functions.md) | **Deutsch** | [Español](../es/01_math_functions.md)

![](../img/comfyui_u5_easyscripter_banner_800x200.png)

[← Zurück zum Index der integrierten Funktionen](00_index.md)

Vollständige Referenz der mathematischen Funktionen, die in u5 EasyScripter verfügbar sind.

## Funktionsliste
24 mathematische Funktionen werden bereitgestellt.

---

## Mathematische Funktionen
Bieten grundlegende mathematische Funktionalität.
In den Beispielen werden unendliche periodische Dezimalzahlen (0.9999...) der Einfachheit halber gerundet.


### ABS(value)
**Beschreibung**: Gibt den Absolutwert zurück
**Argumente**: value - Numerischer Wert oder konvertierbarer Wert
**Rückgabewert**: Absolutwert (float)
**Beispiel**:
```vba
result = ABS(-5.5)
PRINT(result)  ' 5.5
result = ABS(10)
PRINT(result)  ' 10
result = ABS("-3.14")
PRINT(result)  ' 3.14
```

### INT(value)
**Beschreibung**: Gibt den ganzzahligen Teil zurück (Nachkommastellen abschneiden)
**Argumente**: value - Numerischer Wert
**Rückgabewert**: Ganzzahliger Teil (float-Format)
**Beispiel**:
```vba
result = INT(5.9)
PRINT(result)  ' 5
result = INT(-2.3)
PRINT(result)  ' -2
result = INT("10.5")
PRINT(result)  ' 10
```

### ROUND(value, [digits])
**Beschreibung**: Gibt einen gerundeten Wert zurück
**Argumente**:
- value - Numerischer Wert
- digits - Anzahl der Nachkommastellen (Standard: 0)
**Rückgabewert**: Gerundeter Wert
**Beispiel**:
```vba
result = ROUND(3.14159, 2)
PRINT(result)  ' 3.14
result = ROUND(5.5)
PRINT(result)  ' 6
result = ROUND(123.456, 1)
PRINT(result)  ' 123.5
```

### SQRT(value)
**Beschreibung**: Gibt die Quadratwurzel zurück
**Argumente**: value - Wert größer oder gleich 0
**Rückgabewert**: Quadratwurzel
**Fehler**: Negative Werte verursachen einen Fehler
**Beispiel**:
```vba
result = SQRT(16)
PRINT(result)  ' 4
result = SQRT(2)
PRINT(result)  ' 1.4142135623730951
' result = SQRT(-1) ' Fehler!
```

### MIN(value1, value2, ...)
**Beschreibung**: Gibt den Minimalwert zurück
**Argumente**: Mehrere numerische Werte
**Rückgabewert**: Minimalwert
**Beispiel**:
```vba
result = MIN(5, 2, 8, 1)
PRINT(result)  ' 1
result = MIN(VAL1, VAL2)
PRINT(result)  ' Kleinerer der beiden Eingabewerte
```

### MAX(value1, value2, ...)
**Beschreibung**: Gibt den Maximalwert zurück
**Argumente**: Mehrere numerische Werte
**Rückgabewert**: Maximalwert
**Beispiel**:
```vba
result = MAX(5, 2, 8, 1)
PRINT(result)  ' 8
result = MAX(0, VAL1)
PRINT(result)  ' Auf 0 oder größer begrenzen
```

### SIN(radians)
**Beschreibung**: Gibt den Sinus zurück
**Argumente**: radians - Winkel in Radiant
**Rückgabewert**: Wert zwischen -1 und 1
**Beispiel**:
```vba
result = SIN(0)
PRINT(result)  ' 0
result = SIN(3.14159/2)
PRINT(result)  ' 0.9999999999991198 (ca. 1)
result = SIN(RADIANS(30))
PRINT(result)  ' 0.49999999999999994 (ca. 0.5)
```

### COS(radians)
**Beschreibung**: Gibt den Kosinus zurück
**Argumente**: radians - Winkel in Radiant
**Rückgabewert**: Wert zwischen -1 und 1
**Beispiel**:
```vba
result = COS(0)
PRINT(result)  ' 1
result = COS(3.14159)
PRINT(result)  ' -0.9999999999964793 (ca. -1)
result = COS(RADIANS(60))
PRINT(result)  ' 0.5000000000000001 (ca. 0.5)
```

### TAN(radians)
**Beschreibung**: Gibt den Tangens zurück
**Argumente**: radians - Winkel in Radiant
**Rückgabewert**: Tangenswert
**Beispiel**:
```vba
result = TAN(0)
PRINT(result)  ' 0
result = TAN(3.14159/4)
PRINT(result)  ' 0.9999986732059836 (ca. 1)
result = TAN(RADIANS(45))
PRINT(result)  ' 0.9999999999999999 (ca. 1)
```

### RADIANS(degrees)
**Beschreibung**: Konvertiert Grad in Radiant
**Argumente**: degrees - Winkel in Grad
**Rückgabewert**: Radiant
**Beispiel**:
```vba
result = RADIANS(180)
PRINT(result)  ' 3.141592653589793
result = RADIANS(90)
PRINT(result)  ' 1.5707963267948966
result = RADIANS(45)
PRINT(result)  ' 0.7853981633974483
```

### DEGREES(radians)
**Beschreibung**: Konvertiert Radiant in Grad
**Argumente**: radians - Winkel in Radiant
**Rückgabewert**: Grad
**Beispiel**:
```vba
result = DEGREES(3.14159)
PRINT(result)  ' 179.9998479605043 (ca. 180)
result = DEGREES(1.5708)
PRINT(result)  ' 90.00021045914971 (ca. 90)
result = DEGREES(0.7854)
PRINT(result)  ' 45.00010522957486 (ca. 45)
```

### POW(base, exponent)
**Beschreibung**: Berechnet Potenz (base^exponent)
**Argumente**:
- base - Basis
- exponent - Exponent
**Rückgabewert**: Ergebnis der Potenzierung
**Beispiel**:
```vba
result = POW(2, 10)
PRINT(result)  ' 1024
result = POW(5, 3)
PRINT(result)  ' 125
result = POW(10, -2)
PRINT(result)  ' 0.01
```

### LOG(value, [base])
**Beschreibung**: Gibt den Logarithmus zurück

**Wichtig**: LOG-Funktion gibt standardmäßig den natürlichen Logarithmus (Basis e) zurück.

**Argumente**:
- value - Positive Zahl
- base - Basis (Standard: natürlicher Logarithmus e)
**Rückgabewert**: Logarithmus
**Beispiel**:
```vba
result = LOG(2.718282)
PRINT(result)  ' 1.0000000631063886 (ca. 1)
result = LOG(8, 2)
PRINT(result)  ' 3 (Basis 2)
result = LOG(1000, 10)
PRINT(result)  ' 2.9999999999999996 (ca. 3)
```

### EXP(value)
**Beschreibung**: Potenz von e (Basis des natürlichen Logarithmus)
**Argumente**: value - Exponent
**Rückgabewert**: e^value
**Beispiel**:
```vba
result = EXP(0)
PRINT(result)  ' 1
result = EXP(1)
PRINT(result)  ' 2.718281828459045
result = EXP(2)
PRINT(result)  ' 7.38905609893065
```

### AVG(value1, value2, ...)
**Beschreibung**: Berechnet den Durchschnitt
**Argumente**: Mehrere numerische Werte
**Rückgabewert**: Durchschnittswert
**Beispiel**:
```vba
result = AVG(10, 20, 30)
PRINT(result)  ' 20
result = AVG(1, 2, 3, 4, 5)
PRINT(result)  ' 3
```

### SUM(value1, value2, ...)
**Beschreibung**: Berechnet die Summe
**Argumente**: Mehrere numerische Werte
**Rückgabewert**: Summenwert
**Beispiel**:
```vba
result = SUM(10, 20, 30)
PRINT(result)  ' 60
result = SUM(1, 2, 3, 4, 5)
PRINT(result)  ' 15
```

---

[← Zurück zum Index der integrierten Funktionen](00_index.md)
