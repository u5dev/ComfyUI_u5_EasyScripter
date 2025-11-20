# Référence du langage de script

[日本語](../01_syntax_reference.md) | [English](../en/01_syntax_reference.md) | [中文](../zh/01_syntax_reference.md) | [Español](../es/01_syntax_reference.md) | **Français** | [Deutsch](../de/01_syntax_reference.md)

---

[← Retour au document principal](README.md)

---

## 📑 Table des matières

- [Bases de la spécification du langage](#bases-de-la-spécification-du-langage)
- [Variables et affectation](#variables-et-affectation)
- [Variables réservées (variables d'entrée/sortie)](#variables-réservées-variables-dentréesortie)
- [Système de types de données](#système-de-types-de-données)
- [Opérations sur les tableaux](#opérations-sur-les-tableaux)
- [Référence des opérateurs](#référence-des-opérateurs)
- [Structures de contrôle](#structures-de-contrôle)
- [Fonctions définies par l'utilisateur (instruction FUNCTION)](#fonctions-définies-par-lutilisateur-instruction-function)
- [Notation des commentaires](#notation-des-commentaires)

---

## 📖 Bases de la spécification du langage

### Règles de base

**Distinction majuscules/minuscules**
- **Noms de variables** : Aucune distinction (`value` et `VALUE` sont identiques)
- **Noms de fonctions** : Aucune distinction (`len` et `LEN` sont identiques)
- **Comparaison de chaînes** : Aucune distinction (`"Hello" = "HELLO"` est True)

**Important** : Comme dans VBA, les noms de variables, de fonctions et les mots-clés ne font pas de distinction entre majuscules et minuscules.

---

## 📝 Variables et affectation

Les variables peuvent être utilisées sans déclaration. Toutes les variables sont traitées en interne comme des nombres à virgule flottante ou des chaînes de caractères.

### Déclaration et types de variables

```vba
' Les variables peuvent être utilisées sans déclaration
x = 10
name = "Alice"

' Déclaration explicite avec l'instruction DIM (optionnelle)
DIM result
result = x * 2
PRINT(result)  ' 20

' Les types sont automatiquement convertis
number = "123"    ' chaîne
result = number + 10
PRINT(result)  ' 133
```

### Affectation de base

```vba
' Affectation de nombres
a = 10
b = 3.14
c = VAL1 + VAL2

' Affectation de chaînes
name = "World"
message = TXT1

' Affectation du résultat d'un calcul
result = a * b + c
PRINT(result)  ' 31.400000000000002
```

---

## 🎯 Variables réservées (variables d'entrée/sortie)

Variables réservées automatiquement disponibles depuis ComfyUI :

- **`VAL1`**, **`VAL2`** : Entrées numériques (connectées depuis ComfyUI)
- **`TXT1`**, **`TXT2`** : Entrées de chaînes (connectées depuis ComfyUI)
- **`RETURN1`**, **`RETURN2`** : Valeurs de retour du script (nombre ou chaîne)
  - `RETURN` est un alias de RETURN1 pour la rétrocompatibilité
- **`RELAY_OUTPUT`** : Contrôle la valeur du socket de sortie relay_output (type ANY) (implémentation Tier 3)
- **`PRINT`** : Pour la sortie de débogage (ajout avec la fonction PRINT)

**Exemple d'utilisation** :
```vba
' Traiter les valeurs d'entrée
result = VAL1 * 2 + VAL2
PRINT(result)  ' 0

' Stocker dans la sortie
RETURN1 = result
RETURN2 = "Résultat du calcul: " & result
```

#### Variable RELAY_OUTPUT

La variable `RELAY_OUTPUT` est une variable spéciale qui contrôle la valeur du socket de sortie relay_output (type ANY).

**Fonctionnalité** :
- Affecter une valeur à `RELAY_OUTPUT` dans le script entraîne la sortie de cette valeur depuis le socket de sortie relay_output
- Lorsque RELAY_OUTPUT n'est pas utilisé, l'entrée any_input est transmise comme avant

**Usages** :
- Transmettre une image (torch.Tensor) lue avec la fonction INPUT aux nœuds ComfyUI suivants
- Transmettre des données de type ANY arbitraires (latent, mask, etc.) aux nœuds suivants

**Exemple d'utilisation** :
```vba
' Charger un fichier image et le transmettre aux nœuds suivants
IMG1 = INPUT("reference.png")
RELAY_OUTPUT = IMG1
```

**Remarques** :
- Types pouvant être affectés à la variable RELAY_OUTPUT : type ANY (torch.Tensor, list, dict, str, int, float, etc.)
- Aucune conversion de type n'est effectuée (la valeur affectée est sortie telle quelle)
- Fonctionne indépendamment de RETURN1/RETURN2

---

## 📊 Système de types de données

### Types de données de base

1. **Type numérique** : Entiers et nombres à virgule flottante (en interne float)
2. **Type chaîne** : Entouré de guillemets doubles ou simples
3. **Type tableau** : Seuls les tableaux à une dimension sont pris en charge

### Types de littéraux de chaînes

#### Littéraux de chaînes normaux

```vba
' Guillemets doubles
text1 = "Hello, World!"

' Échappement de style VBA : "" représente "
text2 = "He said ""hello"""  ' → He said "hello"

' Séquences d'échappement
text3 = "Line1\nLine2"  ' → Saut de ligne inséré
text4 = "Tab\there"     ' → Tabulation insérée
```

#### Littéraux de chaînes brutes (Raw strings)

Les littéraux de chaînes brutes minimisent le traitement d'échappement et sont utilisés lorsque vous souhaitez traiter les barres obliques inverses telles quelles.

```vba
' Syntaxe : r"..."
' Seul l'échappement de style VBA ("") est traité, les autres séquences d'échappement ne sont pas traitées

' Chemin Windows (utilisation de barres obliques inverses telles quelles)
path = r"C:\Users\Admin\file.txt"
PRINT(path)  ' C:\Users\Admin\file.txt

' Chaîne JSON (utilisation de "" de style VBA)
json_str = r"{""key"": ""value""}"
PRINT(json_str)  ' {"key": "value"}
result = PYEXEC("json.loads", json_str)
PRINT(result)  ' {"key": "value"}

' Chaîne contenant des barres obliques inverses
pattern = r"Line1\nLine2"
PRINT(pattern)  ' Line1\nLine2
```

**Spécification des chaînes brutes** :
- Écrites au format `r"..."`
- Seul l'échappement de style VBA `""` est traité (`""` → `"`)
- `\` est traité comme un caractère normal (les échappements `\n`, `\t`, etc. ne sont pas traités)
- `\"` est traité comme la fin de la chaîne (pour inclure `"` dans la chaîne, utilisez `""`)

### Conversion automatique de type

```vba
' Chaîne → nombre
a = "42"
b = a + 8
PRINT(b)  ' 50

' Nombre → chaîne
c = 100
d = "La valeur est " & c
PRINT(d)  ' La valeur est 100

' Gestion des valeurs booléennes
trueValue = 1
PRINT(trueValue)  ' 1
falseValue = 0
PRINT(falseValue)  ' 0
```

---

## 🔬 Opérations sur les tableaux

Les tableaux sont accessibles avec la notation `[]`.

### Déclaration et utilisation de tableaux

```vba
' Déclaration de tableau (DIM est optionnel)
DIM numbers[10]

' Affectation de valeurs
numbers[0] = 100
numbers[1] = 200
numbers[2] = 300

' Référence de valeurs
total = numbers[0] + numbers[1] + numbers[2]
PRINT(total)  ' 600

' Index dynamique
FOR i = 0 TO 9
    numbers[i] = i * 10
    PRINT(numbers[i])
NEXT
```

### Affectation et référence de tableaux

```vba
' Déclaration et initialisation de tableau
DIM arr[3]

' Affectation au tableau
arr[0] = 100
arr[1] = 200
arr[2] = arr[0] + arr[1]
PRINT(arr[2])  ' 300

' Référence du tableau
RETURN1 = arr[2]
PRINT(RETURN1)  ' 300
```

---

## 🔧 Référence des opérateurs

### Opérateurs arithmétiques

| Opérateur | Description | Exemple | Résultat |
|-----------|-------------|---------|----------|
| + | Addition | `5 + 3` | 8 |
| - | Soustraction | `10 - 3` | 7 |
| * | Multiplication | `4 * 3` | 12 |
| / | Division | `15 / 3` | 5 |
| ^ | Puissance | `2 ^ 3` | 8 |
| MOD | Modulo | `10 MOD 3` | 1 |
| \\ | Division entière | `10 \\ 3` | 3 |

**Exemples** :
```vba
' Addition
result = 10 + 5
PRINT(result)  ' 15

' Soustraction
result = 10 - 3
PRINT(result)  ' 7

' Multiplication
result = 4 * 3
PRINT(result)  ' 12

' Division
result = 15 / 3
PRINT(result)  ' 5

' Puissance
result = 2 ^ 3
PRINT(result)  ' 8

' Modulo (MOD)
result = 10 MOD 3
PRINT(result)  ' 1

' Opération composée (priorité avec parenthèses)
result = (10 + 5) * 2
PRINT(result)  ' 30
result = 10 + 5 * 2
PRINT(result)  ' 20
```

### Opérateurs de comparaison

| Opérateur | Description | Exemple | Résultat |
|-----------|-------------|---------|----------|
| = | Égal | `5 = 5` | 1 (True) |
| <> | Différent | `5 <> 3` | 1 (True) |
| != | Différent (style C) | `5 != 3` | 1 (True) |
| < | Inférieur | `3 < 5` | 1 (True) |
| > | Supérieur | `5 > 3` | 1 (True) |
| <= | Inférieur ou égal | `3 <= 3` | 1 (True) |
| >= | Supérieur ou égal | `5 >= 5` | 1 (True) |

**Remarque** : Dans les comparaisons de chaînes, comme dans VBA, les majuscules et minuscules ne sont pas distinguées. Exemple : `"Hello" = "HELLO"` est True.

**Exemples** :
```vba
' Égal
result = 5 = 5
PRINT(result)  ' 1
result = 5 = 3
PRINT(result)  ' 0

' Différent (<> ou != peut être utilisé)
result = 5 <> 3
PRINT(result)  ' 1
result = 5 != 3
PRINT(result)  ' 1 (style C également utilisable)
result = 5 <> 5
PRINT(result)  ' 0

' Supérieur
result = 10 > 5
PRINT(result)  ' 1

' Inférieur
result = 3 < 10
PRINT(result)  ' 1

' Supérieur ou égal
result = 5 >= 5
PRINT(result)  ' 1
result = 5 >= 6
PRINT(result)  ' 0

' Inférieur ou égal
result = 3 <= 10
PRINT(result)  ' 1
```

### Opérateurs logiques

| Opérateur | Description | Exemple | Résultat |
|-----------|-------------|---------|----------|
| AND | ET logique | `(5>3) AND (2<4)` | 1 (True) |
| OR | OU logique | `(5<3) OR (2<4)` | 1 (True) |
| NOT | NON logique | `NOT (5>3)` | 0 (False) |

**Exemples** :
```vba
' Opération AND
result = (5 > 3) AND (10 > 5)
PRINT(result)  ' 1
result = (5 > 3) AND (2 > 5)
PRINT(result)  ' 0

' Opération OR
result = (5 > 3) OR (2 > 5)
PRINT(result)  ' 1
result = (2 > 5) OR (1 > 3)
PRINT(result)  ' 0

' Opération NOT
result = NOT (5 > 3)
PRINT(result)  ' 0
result = NOT (2 > 5)
PRINT(result)  ' 1
```

### Opérateur de chaînes

| Opérateur | Description | Exemple | Résultat |
|-----------|-------------|---------|----------|
| & | Concaténation | `"Hello" & " " & "World"` | "Hello World" |

**Exemples** :
```vba
' Concaténation de chaînes (opérateur &)
greeting = "Hello" & " " & "World"
PRINT(greeting)  ' Hello World
result = "La valeur est " & VAL1 & " ."
PRINT(result)
```

---

## 🎮 Structures de contrôle

### Instruction IF (branchement conditionnel)

#### Forme de base : Instruction IF (forme de bloc)

```vba
IF VAL1 > 50 THEN
    RETURN1 = "Grand"
END IF
```

#### Instruction IF multiligne

```vba
IF VAL1 > 100 THEN
    RETURN1 = "Très grand"
    PRINT("Valeur: " & VAL1)
ELSE
    RETURN1 = "Standard"
END IF
```

#### Branchement multiple avec ELSEIF

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

#### Instructions IF imbriquées

```vba
IF TXT1 <> "" THEN
    IF LEN(TXT1) > 10 THEN
        IF INSTR(TXT1, "keyword") > 0 THEN
            RETURN1 = "Mot-clé trouvé (texte long)"
        ELSE
            RETURN1 = "Texte long (pas de mot-clé)"
        END IF
    ELSE
        RETURN1 = "Texte court"
    END IF
ELSE
    RETURN1 = "Pas d'entrée"
END IF
```

### Instruction FOR...NEXT (boucle avec compteur)

#### Forme de base

```vba
' Répéter de 1 à 10
FOR i = 1 TO 10
    PRINT("Compteur: " & i)
NEXT
```

#### Spécification STEP

```vba
' Augmenter de 2 (nombres pairs uniquement)
sum = 0
FOR i = 0 TO 20 STEP 2
    sum = sum + i
    PRINT(sum)
NEXT

' Ordre inverse (compte à rebours)
FOR i = 10 TO 1 STEP -1
    PRINT(i & "...")
NEXT
PRINT("Décollage !")
```

#### Boucles imbriquées

```vba
' Créer une table de multiplication
FOR i = 1 TO 9
    row = ""
    FOR j = 1 TO 9
        row = row & (i * j) & " "
    NEXT
    PRINT(row)
NEXT
```

### Instruction WHILE...WEND (boucle conditionnelle)

#### Forme de base

```vba
count = 0
WHILE count < 10
    count = count + 1
    PRINT("Compteur: " & count)
WEND
```

#### Boucle conditionnelle

```vba
' Rechercher un caractère spécifique dans la chaîne d'entrée
position = 1
found = 0
WHILE position <= LEN(TXT1) AND found = 0
    IF MID(TXT1, position, 1) = "X" THEN
        found = position
    END IF
    position = position + 1
WEND

IF found > 0 THEN
    RETURN1 = "X se trouve au " & found & "ème caractère"
    PRINT(RETURN1)
ELSE
    RETURN1 = "X n'a pas été trouvé"
    PRINT(RETURN1)
END IF
```

### Instruction SELECT CASE (branchement multiple)

L'instruction SELECT CASE de style VBA permet d'écrire de manière concise plusieurs branches conditionnelles. La première clause Case qui correspond est exécutée, et les évaluations suivantes ne sont pas effectuées.

#### Forme de base

```vba
SELECT CASE VAL1
    CASE 1
        RETURN1 = "Un"
    CASE 2
        RETURN1 = "Deux"
    CASE 3
        RETURN1 = "Trois"
    CASE ELSE
        RETURN1 = "Autre"
END SELECT
```

#### Instruction Case avec valeurs multiples

```vba
' Spécifier plusieurs valeurs séparées par des virgules
value = 5
SELECT CASE value
    CASE 1, 3, 5, 7, 9
        result = "Impair"
    CASE 2, 4, 6, 8, 10
        result = "Pair"
    CASE ELSE
        result = "Hors plage"
END SELECT
PRINT(result)  ' Impair
```

#### Instruction Case avec plage

```vba
' Spécifier une plage avec l'opérateur TO
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
        grade = "Invalide"
END SELECT
PRINT(grade)  ' C
```

#### Spécification multiple séparée par des virgules (exemple de jour de la semaine)

```vba
dayNum = WEEKDAY(NOW())
SELECT CASE dayNum
    CASE 1, 7
        dayType = "Week-end"
    CASE 2, 3, 4, 5, 6
        dayType = "Jour de semaine"
END SELECT
PRINT(dayType)
```

---

## 🔨 Fonctions définies par l'utilisateur (instruction FUNCTION)

Dans u5 EasyScripter, vous pouvez créer des fonctions définies par l'utilisateur en utilisant l'instruction Function de style VBA. Les fonctions fournissent une portée locale indépendante, empêchant les interférences avec les variables globales.

### Définition de fonction de base

```vba
' Fonction pour additionner deux nombres
FUNCTION add(a, b)
    add = a + b  ' Définir la valeur de retour en affectant au nom de la fonction
END FUNCTION

' Appel de la fonction
result = add(5, 3)
PRINT(result)  ' 8
```

### Fonction retournant le plus grand de deux nombres

```vba
' Fonction retournant le plus grand de deux nombres
FUNCTION maxValue(a, b)
    IF a > b THEN
        maxValue = a
    ELSE
        maxValue = b
    END IF
END FUNCTION

' Exemple d'utilisation
result = maxValue(10, 20)
PRINT(result)  ' 20
```

### Fonction avec plusieurs arguments

```vba
' Fonction pour décorer un prompt
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

' Exemple d'utilisation
finalPrompt = decoratePrompt("portrait", "high", "anime")
PRINT(finalPrompt)  ' portrait, masterpiece, best quality, anime style
```

### Fonction récursive

```vba
' Fonction récursive pour calculer la factorielle
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

## 💬 Notation des commentaires

Les commentaires commencent par un guillemet simple (`'`).

```vba
' Ceci est un commentaire
x = 10  ' Commentaire de fin de ligne également possible
PRINT(x)  ' 10

' Commentaire sur plusieurs lignes
' Mettre un guillemet simple au début de chaque ligne
```

---

## 📚 Prochaines étapes

- [Référence des fonctions intégrées](00_index.md) - Détails de 120 fonctions
- [Document principal](README.md) - Vue d'ensemble et méthode d'installation

---

**Dernière mise à jour** : 3 octobre 2024

---

[← Retour au document principal](README.md)
