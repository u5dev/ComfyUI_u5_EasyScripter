# Référence des fonctions de conversion et jugement de type

[← Retour à l'index des fonctions intégrées](00_index.md)

## Vue d'ensemble

Les fonctions de conversion et de jugement de type sont un groupe de fonctions pour convertir le type de valeurs ou juger le type de variables.

**Fonctions de conversion de type** :
- CSTR - Conversion en chaîne
- CINT - Conversion en entier
- CDBL - Conversion en nombre à virgule flottante
- FORMAT - Formatage de nombres/dates dans un format spécifié (compatible VBA)

**Fonctions de jugement de type** :
- ISNUMERIC - Juge si numérique
- ISDATE - Juge si date
- ISARRAY - Juge si tableau

---

## Fonctions de conversion de type

### CSTR(value)

**Description** : Convertit en chaîne

**Arguments** :
- `value` - Toute valeur

**Retour** : Chaîne

**Exemples** :
```vba
text = CSTR(123)
PRINT(text)             ' 123
text = CSTR(3.14)
PRINT(text)             ' 3.14
text = CSTR(True)
PRINT(text)             ' 1
```

---

### CINT(value)

**Description** : Convertit en entier

**Arguments** :
- `value` - Nombre ou chaîne

**Retour** : Entier (format float)

**Exemples** :
```vba
number = CINT("123")
PRINT(number)            ' 123
number = CINT(45.67)
PRINT(number)            ' 46 (arrondi)
number = CINT("3.14")
PRINT(number)            ' 3
```

---

### CDBL(value)

**Description** : Convertit en nombre à virgule flottante

**Arguments** :
- `value` - Nombre ou chaîne

**Retour** : float

**Exemples** :
```vba
number = CDBL("123.45")
PRINT(number)            ' 123.45
number = CDBL(10)
PRINT(number)            ' 10
```

---

### FORMAT(value, [format_string])

**Description** : Formate les nombres/dates dans un format spécifié (compatible VBA)

**Arguments** :
- `value` (Any, requis) - Valeur à formater (nombre, chaîne, date)
- `format_string` (str, optionnel) - Spécificateur de format (par défaut : "")

**Retour** : str - Chaîne formatée

**Formats supportés** :

1. **Format VBA** :
   - `"0"` - Entier (arrondi)
   - `"0.0"` - 1 décimale
   - `"0.00"` - 2 décimales
   - `"#"`, `"#.#"`, `"#.##"` - Précision automatique

2. **Format Python** :
   - `"{:.2f}"` - Syntaxe de format Python
   - `".2f"`, `","` - Format spec

3. **Format de date (strftime)** :
   - `"%Y-%m-%d %H:%M:%S"` - Format date-heure
   - `"%Y/%m/%d"` - Date seulement

**Exemples** :
```vba
' Format VBA
result = FORMAT(123.456, "0")       ' "123" (entier)
PRINT("Entier: " & result)
result = FORMAT(123.456, "0.0")     ' "123.5" (1 décimale)
PRINT("1 décimale: " & result)
result = FORMAT(123.456, "0.00")    ' "123.46" (2 décimales)
PRINT("2 décimales: " & result)

' Format Python
result = FORMAT(3.14159, "{:.2f}")  ' "3.14"
PRINT("Pi: " & result)
result = FORMAT(1234567, ",")       ' "1,234,567"
PRINT("Séparateur de milliers: " & result)

' Format de date
now_str = NOW()
result = FORMAT(now_str, "%Y-%m-%d %H:%M:%S")
PRINT("Date-heure: " & result)             ' "2024-01-15 14:30:00"
result = FORMAT(now_str, "%Y年%m月%d日")
PRINT("Date: " & result)             ' "2024年01月15日"
```

**Attention** :
- Si `format_string` est omis, convertit la valeur en chaîne telle quelle
- Pour les formats non supportés, retourne la valeur avec str()

---

## Fonctions de jugement de type

### ISNUMERIC(value)

**Description** : Juge si numérique

**Arguments** :
- `value` - Valeur à examiner

**Retour** : 1 (numérique) ou 0

**Exemples** :
```vba
result = ISNUMERIC("123")
PRINT(result)                  ' 1
result = ISNUMERIC("12.34")
PRINT(result)                  ' 1
result = ISNUMERIC("abc")
PRINT(result)                  ' 0
result = ISNUMERIC("")
PRINT(result)                  ' 0
```

---

### ISDATE(value)

**Description** : Juge si analysable comme date

**Arguments** :
- `value` - Valeur à examiner

**Retour** : 1 (date) ou 0

**Exemples** :
```vba
result = ISDATE("2024-01-15")
PRINT(result)                     ' 1
result = ISDATE("2024/01/15")
PRINT(result)                     ' 1
result = ISDATE("15:30:00")
PRINT(result)                     ' 1 (heure aussi)
result = ISDATE("hello")
PRINT(result)                     ' 0
```

---

### ISARRAY(variable_name)

**Description** : Juge si tableau

**Important** : Passez le nom du tableau comme chaîne ou passez une référence de variable de tableau avec la notation ARR[].

**Arguments** :
- `variable_name` - Nom de variable (chaîne) ou référence de variable de tableau

**Retour** : 1 (tableau) ou 0

**Exemples** :
```vba
REDIM ARR, 10
result = ISARRAY(ARR[])
PRINT(result)                ' 1 (référence de tableau)
result = ISARRAY("ARR")
PRINT(result)                ' 1 (chaîne de nom de tableau)
result = ISARRAY("VAL1")
PRINT(result)                ' 0 (variable ordinaire)
```

---

[← Retour à l'index des fonctions intégrées](00_index.md)
