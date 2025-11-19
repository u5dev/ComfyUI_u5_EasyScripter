# Reguläre Ausdrücke-Funktionen-Referenz

**Sprachen**: [English](../02_builtin_functions/05_regex_functions.md) | [日本語](../02_builtin_functions/05_regex_functions.md) | [한국어](../ko/05_regex_functions.md) | [Français](../fr/05_regex_functions.md) | **Deutsch** | [Español](../es/05_regex_functions.md)

![](../img/comfyui_u5_easyscripter_banner_800x200.png)

[← Zurück zum Index der integrierten Funktionen](00_index.md)

## Übersicht

Reguläre Ausdrücke-Funktionen ermöglichen erweiterte Textverarbeitung wie Musterabgleich, Suche, Ersetzung und Extraktion. Verwendet die reguläre Ausdrücke-Engine von Python und bietet leistungsstarke Musterabgleichsfunktionen.

---

## REGEX(pattern, text)

**Beschreibung**: Testet Musterabgleich

**Argumente**:
- pattern - Reguläres Ausdrucksmuster
- text - Zu durchsuchende Zeichenkette

**Rückgabewert**: 1 (Übereinstimmung) oder 0

**Beispiel**:
```vba
result = REGEX("\\d+", "abc123def")
PRINT(result)  ' 1 (enthält Zahlen)

result = REGEX("^[A-Z]", "Hello")
PRINT(result)  ' 1 (beginnt mit Großbuchstaben)

result = REGEX("\\.(jpg|png)$", "a.gif")
PRINT(result)  ' 0 (weder jpg noch png)
```

---

## REGEXMATCH(pattern, text)

**Beschreibung**: Ruft erste Übereinstimmung ab

**Argumente**:
- pattern - Reguläres Ausdrucksmuster
- text - Zu durchsuchende Zeichenkette

**Rückgabewert**: Übereinstimmende Zeichenkette (leer wenn keine)

**Beispiel**:
```vba
result = REGEXMATCH("\\d+", "abc123def456")
PRINT(result)  ' "123"

result = REGEXMATCH("[A-Z]+", "helloWORLD")
PRINT(result)  ' "WORLD"
```

---

## REGEXREPLACE(pattern, text, replacement)

**Beschreibung**: Ersetzt Muster

**Argumente**:
- pattern - Reguläres Ausdrucksmuster
- text - Zielzeichenkette
- replacement - Ersetzungszeichenkette

**Rückgabewert**: Ersetzte Zeichenkette

**Beispiel**:
```vba
result = REGEXREPLACE("\\d+", "abc123def", "XXX")
PRINT(result)  ' "abcXXXdef"

result = REGEXREPLACE("\\s+", "a  b    c", " ")
PRINT(result)  ' "a b c"

result = REGEXREPLACE("[aeiou]", "hello", "*")
PRINT(result)  ' "h*ll*"
```

---

## REGEXEXTRACT(pattern, text, [group])

**Beschreibung**: Extrahiert Gruppe

**Argumente**:
- pattern - Reguläres Ausdrucksmuster (mit Gruppe)
- text - Zielzeichenkette
- group - Gruppennummer (Standard: 0=gesamt)

**Rückgabewert**: Extrahierte Zeichenkette

**Beispiel**:
```vba
result = REGEXEXTRACT("(\\d{4})-(\\d{2})", "2024-01-15", 1)
PRINT(result)  ' "2024"

result = REGEXEXTRACT("(\\w+)@(\\w+)", "user@domain", 2)
PRINT(result)  ' "domain"
```

---

## REGEXCOUNT(pattern, text)

**Beschreibung**: Zählt Übereinstimmungen

**Argumente**:
- pattern - Reguläres Ausdrucksmuster
- text - Zielzeichenkette

**Rückgabewert**: Anzahl der Übereinstimmungen

**Beispiel**:
```vba
count = REGEXCOUNT("\\d", "a1b2c3d4")
PRINT(count)  ' 4

count = REGEXCOUNT("\\w+", "hello world")
PRINT(count)  ' 2
```

---

## REGEXMATCHES(pattern, text)

**Beschreibung**: Ruft alle Übereinstimmungen als Array ab

**Argumente**:
- pattern - Reguläres Ausdrucksmuster
- text - Zielzeichenkette

**Rückgabewert**: Liste der Übereinstimmungen

**Beispiel**:
```vba
matches = REGEXMATCHES("\\d+", "a10b20c30")
PRINT(matches)  ' ["10", "20", "30"]
```

---

## REGEXSPLIT(pattern, text)

**Beschreibung**: Teilt durch Muster

**Argumente**:
- pattern - Trennmuster
- text - Zielzeichenkette

**Rückgabewert**: Geteilte Liste

**Beispiel**:
```vba
parts = REGEXSPLIT("[,;]", "a,b;c,d")
PRINT(parts)  ' ["a", "b", "c", "d"]
PRINT(parts[0]) ' a

parts = REGEXSPLIT("\\s+", "one  two  three")
PRINT(parts)  ' ["one", "two", "three"]
PRINT(parts[1]) ' two
```

---

[← Zurück zum Index der integrierten Funktionen](00_index.md)
