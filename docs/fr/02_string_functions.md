# Référence des fonctions de chaînes de caractères

[日本語](../../docs/02_builtin_functions/02_string_functions.md) | [English](../en/02_string_functions.md) | [中文](../zh/02_string_functions.md) | [Español](../es/02_string_functions.md) | **Français** | [Deutsch](../de/02_string_functions.md)

---

[← Retour à l'index des fonctions intégrées](00_index.md)

---

Référence complète des fonctions de chaînes de caractères disponibles dans u5 EasyScripter.

## Liste des fonctions
28 fonctions de chaînes de caractères sont fournies.

---

### LEN(text)
**Description** : Retourne la longueur de la chaîne
**Arguments** : text - Chaîne de caractères
**Retour** : Nombre de caractères
**Exemples** :
```vba
result = LEN("Hello")
PRINT(result)     ' 5
text1 = "Sample Text"
result = LEN(text1)
PRINT(result)     ' 11
result = LEN("")
PRINT(result)     ' 0
```

### LEFT(text, length)
**Description** : Obtient un nombre spécifié de caractères à partir de la gauche
**Arguments** :
- text - Chaîne de caractères
- length - Nombre de caractères à obtenir
**Retour** : Sous-chaîne
**Exemples** :
```vba
result = LEFT("Hello World", 5)
PRINT(result)   ' "Hello"
text1 = "ComfyUI EasyScripter"
result = LEFT(text1, 10)
PRINT(result)   ' "ComfyUI Ea"
result = LEFT("ABC", 10)
PRINT(result)   ' "ABC" (chaîne entière si length > longueur)
```

### RIGHT(text, length)
**Description** : Obtient un nombre spécifié de caractères à partir de la droite
**Arguments** :
- text - Chaîne de caractères
- length - Nombre de caractères à obtenir
**Retour** : Sous-chaîne
**Exemples** :
```vba
result = RIGHT("Hello World", 5)
PRINT(result)  ' "World"
text1 = "ComfyUI EasyScripter"
result = RIGHT(text1, 10)
PRINT(result)  ' "syScripter"
result = RIGHT("ABC", 10)
PRINT(result)  ' "ABC"
```

### MID(text, start, length)
**Description** : Obtient une sous-chaîne à partir d'une position spécifiée

**Important** : La position de départ 0 est traitée comme 1.

**Arguments** :
- text - Chaîne de caractères
- start - Position de départ (base 1, 0 est traité comme 1)
- length - Nombre de caractères à obtenir
**Retour** : Sous-chaîne
**Exemples** :
```vba
result = MID("Hello World", 7, 5)
PRINT(result)  ' "World"
result = MID("ABCDEFG", 3, 2)
PRINT(result)  ' "CD"
result = MID("ABCDEFG", 0, 2)
PRINT(result)  ' "AB" (0 est traité comme 1)
text1 = "EasyScripter Node"
result = MID(text1, 5, 10)
PRINT(result)  ' "Scripter N"
```

### UPPER(text)
**Description** : Convertit en majuscules
**Arguments** : text - Chaîne de caractères
**Retour** : Chaîne convertie en majuscules
**Exemples** :
```vba
result = UPPER("Hello")
PRINT(result)      ' "HELLO"
result = UPPER("abc123XYZ")
PRINT(result)  ' "ABC123XYZ"
```

### LOWER(text)
**Description** : Convertit en minuscules
**Arguments** : text - Chaîne de caractères
**Retour** : Chaîne convertie en minuscules
**Exemples** :
```vba
result = LOWER("HELLO")
PRINT(result)      ' "hello"
result = LOWER("ABC123xyz")
PRINT(result)  ' "abc123xyz"
```

### TRIM(text)
**Description** : Supprime les espaces au début et à la fin
**Arguments** : text - Chaîne de caractères
**Retour** : Chaîne tronquée
**Exemples** :
```vba
result = TRIM("  Hello  ")
PRINT(result)    ' "Hello"
result = TRIM("   ")
PRINT(result)    ' ""
```

### REPLACE(text, old, new)
**Description** : Remplace une chaîne
**Arguments** :
- text - Chaîne cible
- old - Chaîne à rechercher
- new - Chaîne de remplacement
**Retour** : Chaîne après remplacement
**Exemples** :
```vba
result = REPLACE("Hello World", "World", "ComfyUI")
PRINT(result)  ' "Hello ComfyUI"
text1 = "Hello World Test"
result = REPLACE(text1, " ", "_")
PRINT(result)  ' "Hello_World_Test"
result = REPLACE("AAABBB", "A", "X")
PRINT(result)  ' "XXXBBB"
```

### INSTR([start,] text, search)
**Description** : Recherche une chaîne (retourne la position)
**Arguments** :
- start - Position de départ de recherche (par défaut : 1)
- text - Chaîne cible
- search - Chaîne à rechercher
**Retour** : Position trouvée (0 = non trouvé)
**Exemples** :
```vba
result = INSTR("Hello World", "World")
PRINT(result)     ' 7
result = INSTR("ABCABC", "BC")
PRINT(result)     ' 2
result = INSTR(3, "ABCABC", "BC")
PRINT(result)     ' 5 (recherche à partir du 3ème caractère)
text1 = "This is a keyword example"
result = INSTR(text1, "keyword")
PRINT(result)     ' 11
```

### INSTRREV(text, search, [start])
**Description** : Recherche une chaîne depuis la fin
**Arguments** :
- text - Chaîne cible
- search - Chaîne à rechercher
- start - Position de départ de recherche (par défaut : fin)
**Retour** : Position trouvée
**Exemples** :
```vba
result = INSTRREV("Hello World", "o")
PRINT(result)      ' 8 (dernier o)
result = INSTRREV("ABCABC", "BC")
PRINT(result)      ' 5
result = INSTRREV("path/to/file", "/")
PRINT(result)      ' 8 (dernier slash)
```

### STRREVERSE(text)
**Description** : Inverse une chaîne
**Arguments** : text - Chaîne de caractères
**Retour** : Chaîne inversée
**Exemples** :
```vba
result = STRREVERSE("Hello")
PRINT(result)    ' "olleH"
result = STRREVERSE("12345")
PRINT(result)    ' "54321"
```

### STRCOMP(text1, text2, [compare])
**Description** : Compare des chaînes
**Arguments** :
- text1 - Chaîne 1
- text2 - Chaîne 2
- compare - Méthode de comparaison (0=binaire, 1=texte)
**Retour** : -1/0/1 (inférieur/égal/supérieur)
**Exemples** :
```vba
result = STRCOMP("abc", "ABC", 1)
PRINT(result)    ' 0 (ignore majuscules/minuscules)
result = STRCOMP("abc", "ABC", 0)
PRINT(result)    ' 1 (distingue majuscules/minuscules)
result = STRCOMP("a", "b")
PRINT(result)    ' -1
```

### SPACE(number)
**Description** : Génère un nombre spécifié d'espaces
**Arguments** : number - Nombre d'espaces
**Retour** : Chaîne d'espaces
**Exemples** :
```vba
result = SPACE(5)
PRINT(result)               ' "     "
result = "A" & SPACE(3) & "B"
PRINT(result)   ' "A   B"
```

### STRING(number, character)
**Description** : Répète un caractère
**Arguments** :
- number - Nombre de répétitions
- character - Caractère à répéter
**Retour** : Chaîne répétée
**Exemples** :
```vba
result = STRING(5, "A")
PRINT(result)     ' "AAAAA"
result = STRING(10, "-")
PRINT(result)    ' "----------"
```

### FORMAT(value, format_string)
**Description** : Formate une valeur
**Arguments** :
- value - Valeur
- format_string - Chaîne de format
**Retour** : Chaîne formatée
**Formats supportés** :
- `{:.Nf}` - N décimales
- `{:0Nd}` - N chiffres avec zéros
- `{:,}` - Séparateur de milliers
- `%Y-%m-%d` - Format de date
**Exemples** :
```vba
result = FORMAT(3.14159, "{:.2f}")
PRINT(result)      ' "3.14"
result = FORMAT(42, "{:05d}")
PRINT(result)      ' "00042"
result = FORMAT(1234567, "{:,}")
PRINT(result)      ' "1,234,567.0"
result = FORMAT(NOW(), "%Y/%m/%d")
PRINT(result)      ' "2024/01/15"
```

### SPLIT(text, [delimiter])
**Description** : Divise une chaîne en tableau
**Arguments** :
- text - Chaîne à diviser
- delimiter - Séparateur (par défaut : virgule)
**Retour** : Tableau divisé
**Exemples** :
```vba
' Diviser par virgules
result = SPLIT("apple,banana,cherry")
PRINT(result(0))  ' "apple"
PRINT(result(1))  ' "banana"
' Diviser par espaces
result = SPLIT("one two three", " ")
PRINT(result(2))  ' "three"
```

### JOIN(array, [delimiter])
**Description** : Joint un tableau en chaîne
**Arguments** :
- array - Tableau à joindre
- delimiter - Séparateur (par défaut : virgule)
**Retour** : Chaîne jointe
**Exemples** :
```vba
ARRAY(arr, "A", "B", "C")
result = JOIN(arr, "-")
PRINT(result)  ' "A-B-C"
result = JOIN(arr)
PRINT(result)  ' "A,B,C"
```

### LTRIM(text)
**Description** : Supprime les espaces à gauche
**Arguments** : text - Chaîne de caractères
**Retour** : Chaîne tronquée à gauche
**Exemples** :
```vba
result = LTRIM("  Hello")
PRINT(result)  ' "Hello"
result = LTRIM("  Text  ")
PRINT(result)  ' "Text  "
```

### RTRIM(text)
**Description** : Supprime les espaces à droite
**Arguments** : text - Chaîne de caractères
**Retour** : Chaîne tronquée à droite
**Exemples** :
```vba
result = RTRIM("Hello  ")
PRINT(result)  ' "Hello"
result = RTRIM("  Text  ")
PRINT(result)  ' "  Text"
```

### UCASE(text)
**Description** : Convertit en majuscules (alias de UPPER)
**Arguments** : text - Chaîne de caractères
**Retour** : Chaîne convertie en majuscules
**Exemples** :
```vba
result = UCASE("hello")
PRINT(result)  ' "HELLO"
```

### LCASE(text)
**Description** : Convertit en minuscules (alias de LOWER)
**Arguments** : text - Chaîne de caractères
**Retour** : Chaîne convertie en minuscules
**Exemples** :
```vba
result = LCASE("HELLO")
PRINT(result)  ' "hello"
```

### PROPER(text)
**Description** : Convertit en casse de titre (majuscule au début de chaque mot)
**Arguments** : text - Chaîne de caractères
**Retour** : Chaîne convertie en casse de titre
**Exemples** :
```vba
result = PROPER("hello world")
PRINT(result)  ' "Hello World"
result = PROPER("easyScripter node")
PRINT(result)  ' "Easyscripter Node"
```

### CHR(code)
**Description** : Convertit un code de caractère en caractère
**Arguments** : code - Code de caractère (plage ASCII 0-127)
**Retour** : Caractère correspondant
**Exemples** :
```vba
result = CHR(65)
PRINT(result)  ' "A"
result = CHR(97)
PRINT(result)  ' "a"
result = CHR(48)
PRINT(result)  ' "0"
```

### ASC(char)
**Description** : Convertit un caractère en code de caractère
**Arguments** : char - Caractère ou chaîne (utilise le premier caractère)
**Retour** : Code de caractère (ASCII)
**Exemples** :
```vba
result = ASC("A")
PRINT(result)  ' 65
result = ASC("Hello")
PRINT(result)  ' 72 (code de "H")
```

### STR(value)
**Description** : Convertit un nombre en chaîne
**Arguments** : value - Valeur numérique
**Retour** : Nombre converti en chaîne
**Exemples** :
```vba
result = STR(123)
PRINT(result)  ' "123"
result = STR(3.14)
PRINT(result)  ' "3.14"
```

### URLENCODE(text, [encoding])
**Description** : Effectue l'encodage URL (pourcentage)
**Arguments** :
- text - Chaîne à encoder
- encoding - Encodage de caractères (par défaut : utf-8)
**Retour** : Chaîne encodée URL
**Exemples** :
```vba
' Encoder du japonais en URL
encoded = URLENCODE("あいうえお")
PRINT(encoded)  ' → %E3%81%82%E3%81%84%E3%81%86%E3%81%88%E3%81%8A
' Encoder une requête de recherche
query = "EasyScripter HTTP 関数"
url = "https://www.google.com/search?q=" & URLENCODE(query)
PRINT(url)
```

### URLDECODE(text, [encoding])
**Description** : Effectue le décodage URL (décodage du pourcentage)
**Arguments** :
- text - Chaîne à décoder
- encoding - Encodage de caractères (par défaut : utf-8)
**Retour** : Chaîne décodée URL
**Exemples** :
```vba
' Décoder une chaîne encodée URL
decoded = URLDECODE("%E3%81%82%E3%81%84%E3%81%86%E3%81%88%E3%81%8A")
PRINT(decoded)  ' → あいうえお
' Décoder un paramètre de requête
param = URLDECODE("EasyScripter+HTTP+%E9%96%A2%E6%95%B0")
PRINT(param)  ' → EasyScripter+HTTP+関数
```

### ESCAPEPATHSTR(path, [replacement])
**Description** : Remplace ou supprime les caractères interdits dans les chemins de fichiers
**Arguments** :
- path - Chaîne à traiter
- replacement - Chaîne de remplacement (suppression si omis)
**Retour** : Chaîne avec caractères interdits traités

**Caractères interdits** : `\`, `/`, `:`, `*`, `?`, `"`, `<`, `>`, `|`

**Mots réservés** (interdits en tant que nom de fichier complet) : CON, PRN, AUX, NUL, COM1-9, LPT1-9 (insensible à la casse)

**Exemples** :
```vba
' Remplacer les caractères interdits par un underscore
safe_name = ESCAPEPATHSTR("file:name*.txt", "_")
PRINT(safe_name)  ' → file_name_.txt

' Supprimer les caractères interdits
safe_name = ESCAPEPATHSTR("file:name*.txt")
PRINT(safe_name)  ' → filename.txt

' Traitement des mots réservés
safe_name = ESCAPEPATHSTR("CON.txt", "_")
PRINT(safe_name)  ' → _.txt

' Autorisé comme partie du nom de fichier
safe_name = ESCAPEPATHSTR("myConFile.txt", "_")
PRINT(safe_name)  ' → myConFile.txt
```

---

[← Retour à l'index des fonctions intégrées](00_index.md)
