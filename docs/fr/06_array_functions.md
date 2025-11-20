# Référence des fonctions de tableaux

[← Retour à l'index des fonctions intégrées](00_index.md)

## Vue d'ensemble

Les fonctions de tableaux fournissent des opérations telles que l'initialisation, le redimensionnement et l'obtention des limites des tableaux. Dans u5 EasyScripter, les tableaux utilisent un indexage base 0 et sont accessibles avec la notation `[]`.

**Nombre de fonctions dans cette catégorie** : 3

## Liste des fonctions

### UBOUND(array)

**Description** : Obtient l'index de limite supérieure du tableau

**Arguments** :
- array - Variable de tableau

**Retour** : Index de limite supérieure (base 0)

**Traitement spécial** : Fonction spéciale traitée par script_engine.py

**Exemples** :
```vba
' Obtenir la limite supérieure du tableau
REDIM ARR, 5
upper = UBOUND(ARR[])
PRINT(upper)   ' 4 (5 éléments de 0 à 4)

' Traiter tout le tableau en boucle
ARRAY data[], 10, 20, 30, 40, 50
FOR I = 0 TO UBOUND(data[])
    PRINT(data[I])
NEXT

' Vérifier la taille du tableau
ARRAY items[], "apple", "banana", "orange"
size = UBOUND(items[]) + 1
PRINT(size)  ' 3 éléments
```

---

### ARRAY(variable_name, value1, value2, ...)

**Description** : Initialise un tableau et définit les valeurs

**Arguments** :
- variable_name - Nom de variable du tableau
- value1, value2, ... - Valeurs initiales

**Traitement spécial** : Fonction spéciale traitée par script_engine.py

**Exemples** :
```vba
' Initialiser un tableau de chaînes
ARRAY items[], "apple", "banana", "orange"
' items[0] = "apple", items[1] = "banana", items[2] = "orange"

' Initialiser un tableau numérique
ARRAY numbers[], 10, 20, 30, 40, 50
' numbers[0] = 10, numbers[1] = 20, ...

' Accéder aux éléments du tableau
ARRAY colors[], "red", "green", "blue"
favoriteColor = colors[1]
PRINT(favoriteColor)  ' "green"

' Traiter un tableau en boucle
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

**Description** : Redimensionne (redéfinit) le tableau

**Arguments** :
- array_name - Nom du tableau (chaîne)
- size - Nouvelle taille

**Traitement spécial** : Fonction spéciale traitée par script_engine.py

**Attention** : REDIM efface les éléments existants du tableau

**Exemples** :
```vba
' Initialiser le tableau
REDIM ARR, 10        ' Redéfinir le tableau ARR avec 10 éléments
REDIM DATA, 100      ' Redéfinir le tableau DATA avec 100 éléments

' Redimensionnement dynamique
size = VAL1
PRINT(size)
REDIM MyArray, size  ' Redimensionner selon la valeur de VAL1

' Traitement de données dynamiques avec tableau
itemCount = CSVCOUNT(TXT1)
PRINT(itemCount)
REDIM items, itemCount
FOR I = 0 TO itemCount - 1
    items[I] = CSVREAD(TXT1, I + 1)
NEXT
```

## Exemples d'utilisation de tableaux

### Opérations de tableaux de base
```vba
' Créer un tableau et définir des valeurs
ARRAY names[], "Alice", "Bob", "Charlie", "David"

' Vérifier la taille du tableau
count = UBOUND(names[]) + 1
PRINT(count)
PRINT("Nombre d'éléments: " & count)  ' "Nombre d'éléments: 4"

' Traiter le tableau dans l'ordre
FOR I = 0 TO UBOUND(names[])
    PRINT("Nom[" & I & "]: " & names[I])
NEXT
```

### Redimensionnement dynamique de tableau
```vba
' Créer un tableau avec taille initiale
REDIM buffer, 5
FOR I = 0 TO 4
    buffer[I] = I * 10
NEXT

' Redimensionner si nécessaire
newSize = 10
PRINT(newSize)
REDIM buffer, newSize
' Attention : REDIM efface les données existantes
```

### Combinaison de tableaux et CSV
```vba
' Convertir des données CSV en tableau
csvData = "apple,banana,orange,grape,melon"
PRINT(csvData)
itemCount = CSVCOUNT(csvData)
PRINT(itemCount)
REDIM fruits, itemCount

FOR I = 0 TO itemCount - 1
    fruits[I] = CSVREAD(csvData, I + 1)
NEXT

' Vérifier le contenu du tableau
FOR I = 0 TO UBOUND(fruits[])
    PRINT("Fruit[" & I & "]: " & fruits[I])
NEXT
```

### Traitement d'agrégation de tableaux
```vba
' Initialiser un tableau numérique
ARRAY scores[], 85, 92, 78, 95, 88, 91

' Calculer la somme
total = 0
FOR I = 0 TO UBOUND(scores[])
    total = total + scores[I]
NEXT
PRINT(total)

' Calculer la moyenne
count = UBOUND(scores[]) + 1
PRINT(count)
average = total / count
PRINT(average)

' Rechercher le maximum
maxScore = scores[0]
PRINT(maxScore)
FOR I = 1 TO UBOUND(scores[])
    IF scores[I] > maxScore THEN
        maxScore = scores[I]
        PRINT(maxScore)
    END IF
NEXT

PRINT("Somme: " & total)
PRINT("Moyenne: " & ROUND(average, 2))
PRINT("Score maximum: " & maxScore)
```

---

[← Retour à l'index des fonctions intégrées](00_index.md)
