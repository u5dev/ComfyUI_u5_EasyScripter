# Référence des fonctions CSV

[← Retour à l'index des fonctions intégrées](00_index.md)

## Vue d'ensemble

Groupe de fonctions pour manipuler les chaînes CSV (valeurs séparées par des virgules). Pratique pour la génération de prompts et la gestion des valeurs de configuration.

- Comptage et récupération d'éléments CSV
- Génération de prompts par sélection aléatoire
- Suppression des doublons et obtention de différences
- Conversion entre tableaux et CSV

---

## Liste des fonctions

### CSVCOUNT(csv_text)

**Description** : Compte le nombre d'éléments CSV

**Arguments** :
- csv_text - Chaîne séparée par des virgules

**Retour** : Nombre d'éléments (entier)

**Exemples** :
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

**Description** : Récupère un élément à un index spécifié dans une chaîne CSV

**Arguments** :
- csv_text - Chaîne séparée par des virgules
- index - Index de l'élément à récupérer (base 1)

**Retour** : Élément à la position spécifiée (chaîne). Chaîne vide si hors limites

**Exemples** :
```vba
element = CSVREAD("apple,banana,orange", 2)
PRINT(element)    ' banana
element = CSVREAD("a,b,c,d", 1)
PRINT(element)    ' a
element = CSVREAD("x,y,z", 10)
PRINT(element)    ' (chaîne vide si hors limites)
```

---

### CSVUNIQUE(csv_text)

**Description** : Supprime les doublons

**Arguments** :
- csv_text - Chaîne séparée par des virgules

**Retour** : Chaîne CSV après suppression des doublons

**Exemples** :
```vba
result = CSVUNIQUE("a,b,a,c,b")
PRINT(result)    ' a,b,c
result = CSVUNIQUE("1,2,3,2,1")
PRINT(result)    ' 1,2,3
```

---

### CSVMERGE(csv1, csv2, ...)

**Description** : Fusionne plusieurs CSV

**Arguments** :
- csv1, csv2, ... - Plusieurs chaînes CSV (arguments variadiques)

**Retour** : Chaîne CSV fusionnée

**Exemples** :
```vba
result = CSVMERGE("a,b", "c,d")
PRINT(result)        ' a,b,c,d
result = CSVMERGE("1,2", "3", "4,5")
PRINT(result)        ' 1,2,3,4,5
```

---

### CSVDIFF(array_name, csv1, csv2)

**Description** : Stocke dans un tableau les différences entre deux chaînes CSV (éléments n'existant que dans l'une ou l'autre)

**Arguments** :
- array_name - Nom de variable du tableau pour stocker le résultat
- csv1 - Chaîne CSV 1
- csv2 - Chaîne CSV 2

**Retour** : Nombre d'éléments de différence (entier)

**Exemples** :
```vba
' Récupère les éléments dans csv1 mais pas csv2, et les éléments dans csv2 mais pas csv1
DIM diff_array
count = CSVDIFF(diff_array, "a,b,c,d", "b,d,e")
PRINT(count)           ' 3
PRINT(diff_array(0))   ' a
PRINT(diff_array(1))   ' c
PRINT(diff_array(2))   ' e
```

---

### PICKCSV(csv_text, [index])

**Description** : Sélectionne un élément CSV

**Arguments** :
- csv_text - Chaîne CSV
- index - Index (par défaut : sélection aléatoire)

**Retour** : Élément sélectionné (chaîne)

**Exemples** :
```vba
result = PICKCSV("red,green,blue", 2)
PRINT(result)     ' green
result = PICKCSV("A,B,C,D")
PRINT(result)     ' A, B, C, ou D
```

---

### RNDCSV(csv_text, [count])

**Description** : Sélection aléatoire depuis CSV (récupération de tableau d'éléments multiples également possible)

**Arguments** :
- csv_text - Chaîne CSV
- count - Nombre d'éléments à sélectionner (par défaut, retourne une chaîne unique)

**Retour** :
- count non spécifié : Un élément sélectionné aléatoirement (chaîne)
- count=1 : Un élément sélectionné aléatoirement (chaîne)
- count≥2 : Liste d'éléments sélectionnés aléatoirement
- count >= nombre d'éléments : Tableau complet conservant l'ordre de tri original

**Exemples** :
```vba
' Sélectionner un élément (comme avant)
style = RNDCSV("realistic,anime,cartoon,abstract")
PRINT(style)
color = RNDCSV("red,blue,green,yellow,purple")
PRINT(color)

' Récupérer plusieurs éléments sous forme de tableau (avec doublons possibles)
DIM selected[3]
selected = RNDCSV("A,B,B,B,C,C,D", 3)
PRINT(selected)  ' Ex: ["B", "B", "D"]

' Si count dépasse le nombre d'éléments, tous les éléments dans l'ordre original
DIM all[3]
all = RNDCSV("X,Y,Z", 5)
PRINT(all)  ' ["X", "Y", "Z"] (conserve l'ordre original)

' Coordination avec RANDOMIZE (graine fixe)
RANDOMIZE(12345)
result = RNDCSV("1,2,3,4,5", 3)
PRINT(result)  ' Sélection aléatoire reproductible
```

---

### CSVJOIN(array, [delimiter])

**Description** : Joint un tableau en chaîne CSV

**Arguments** :
- array - Tableau
- delimiter - Séparateur (par défaut : virgule)

**Retour** : Chaîne CSV jointe

**Exemples** :
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

**Description** : Trie les éléments CSV

**Arguments** :
- csv_text - Texte séparé par un délimiteur
- delimiter - Séparateur (par défaut : ",")
- descending - Indicateur de tri décroissant (par défaut : False, 0=croissant, 1 ou True=décroissant)

**Retour** : Chaîne CSV triée

**Exemples** :
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

## Exemples pratiques

### Sélection aléatoire pour la génération de prompts

```vba
' Sélectionner un style aléatoirement (un seul)
style = RNDCSV("photorealistic,anime,oil painting,watercolor")
PRINT(style)
' Sélectionner une tonalité aléatoirement
tone = RNDCSV("warm,cool,vivid,muted,monochrome")
PRINT(tone)
' Sélectionner une heure de la journée aléatoirement
time = RNDCSV("morning,noon,sunset,night")
PRINT(time)

PRINT("1girl, " & style & ", " & tone & " tone, " & time)

' Mélanger plusieurs styles (sélection de tableau)
DIM styles[3]
styles = RNDCSV("realistic,anime,3d,sketch,oil,watercolor,digital", 3)
PRINT(styles)
stylePrompt = CSVJOIN(styles, ", ")
PRINT(stylePrompt)
PRINT("1girl, " & stylePrompt)
```


### Suppression des doublons et fusion de listes

```vba
' Fusionner plusieurs listes de tags
tags1 = "girl,outdoor,sunny,smile"
PRINT(tags1)
tags2 = "outdoor,happy,smile,park"
PRINT(tags2)
tags3 = "girl,smile,nature"
PRINT(tags3)

' Fusion
allTags = CSVMERGE(tags1, tags2, tags3)
PRINT(allTags)
' "girl,outdoor,sunny,smile,happy,smile,park,girl,smile,nature"

' Supprimer les doublons
uniqueTags = CSVUNIQUE(allTags)
PRINT(uniqueTags)
' "girl,outdoor,sunny,smile,happy,park,nature"
```

---

[← Retour à l'index des fonctions intégrées](00_index.md)
