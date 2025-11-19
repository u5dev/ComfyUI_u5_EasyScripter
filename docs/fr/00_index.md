# Index complet des fonctions intégrées

[日本語](../../docs/02_builtin_functions/00_index.md) | [English](../en/00_index.md) | [中文](../zh/00_index.md) | [Español](../es/00_index.md) | **Français** | [Deutsch](../de/00_index.md)

---

[← Retour au document principal](README.md)

**Cette page est l'index de référence des fonctions intégrées de u5 EasyScripter.**

u5 EasyScripter propose une riche bibliothèque de fonctions intégrées utilisables dans des scripts de style VBA.

## Liste des catégories de fonctions

### [Référence des fonctions mathématiques](01_math_functions.md)
16 fonctions mathématiques - Opérations de base, fonctions trigonométriques, logarithmes, fonctions statistiques, etc.

### [Référence des fonctions de chaînes](02_string_functions.md)
28 fonctions de chaînes - Manipulation de chaînes, recherche, remplacement, formatage, etc.

### [Référence des fonctions de date/heure](03_datetime_functions.md)
12 fonctions de date/heure - Date et heure actuelles, calculs de dates, extraction de composants de date/heure, conversion de dates, etc.

### [Référence des fonctions CSV](04_csv_functions.md)
9 fonctions CSV - Manipulation CSV, sélection aléatoire, suppression de doublons, etc.

### [Référence des fonctions d'expressions régulières](05_regex_functions.md)
7 fonctions d'expressions régulières - Correspondance de motifs, remplacement, extraction, etc.

### [Référence des fonctions de tableaux](06_array_functions.md)
3 fonctions de tableaux - Initialisation de tableaux, redimensionnement, obtention de l'index supérieur, etc.

### [Référence des fonctions de conversion et détection de types](07_type_functions.md)
7 fonctions de conversion et détection de types - Conversion de types, vérification de types, formatage, etc.

### [Référence des fonctions de modèle](08_model_functions.md)
1 fonction de modèle - Détermination de la résolution optimale pour les modèles de génération AI

### [Référence des fonctions utilitaires](09_utility_functions.md)
18 fonctions utilitaires - Sortie de débogage, détection de types, entrée/sortie de fichiers, vérification d'existence de fichiers, libération de mémoire, veille, traitement d'images (conversion IMAGE→tableau JSON/Base64), acquisition de données image/Latent, acquisition de données de type ANY, etc.

---

## Tableau de référence rapide

### Fonctions mathématiques (16)

| Nom de fonction | Aperçu |
|-----------------|---------|
| **ABS(value)** | Renvoie la valeur absolue |
| **INT(value)** | Renvoie la partie entière (troncature des décimales) |
| **ROUND(value, [digits])** | Renvoie la valeur arrondie |
| **SQRT(value)** | Renvoie la racine carrée |
| **MIN(value1, value2, ...)** | Renvoie la valeur minimale |
| **MAX(value1, value2, ...)** | Renvoie la valeur maximale |
| **SIN(radians)** | Renvoie le sinus |
| **COS(radians)** | Renvoie le cosinus |
| **TAN(radians)** | Renvoie la tangente |
| **RADIANS(degrees)** | Convertit les degrés en radians |
| **DEGREES(radians)** | Convertit les radians en degrés |
| **POW(base, exponent)** | Calcule la puissance (base^exposant) |
| **LOG(value, [base])** | Renvoie le logarithme (par défaut : logarithme naturel) |
| **EXP(value)** | Puissance de e (base du logarithme naturel) |
| **AVG(value1, value2, ...)** | Calcule la moyenne |
| **SUM(value1, value2, ...)** | Calcule la somme |

### Fonctions de chaînes (28)

| Nom de fonction | Aperçu |
|-----------------|---------|
| **LEN(text)** | Renvoie la longueur de la chaîne |
| **LEFT(text, length)** | Obtient le nombre spécifié de caractères depuis la gauche |
| **RIGHT(text, length)** | Obtient le nombre spécifié de caractères depuis la droite |
| **MID(text, start, length)** | Obtient une sous-chaîne depuis la position spécifiée |
| **UPPER(text)** | Convertit en majuscules |
| **LOWER(text)** | Convertit en minuscules |
| **TRIM(text)** | Supprime les espaces au début et à la fin |
| **REPLACE(text, old, new)** | Remplace une chaîne |
| **INSTR([start,] text, search)** | Recherche une chaîne (renvoie la position) |
| **INSTRREV(text, search, [start])** | Recherche une chaîne depuis la fin |
| **STRREVERSE(text)** | Inverse une chaîne |
| **STRCOMP(text1, text2, [compare])** | Compare des chaînes |
| **SPACE(number)** | Génère le nombre spécifié d'espaces |
| **STRING(number, character)** | Répète un caractère |
| **FORMAT(value, format_string)** | Formate une valeur |
| **SPLIT(text, [delimiter])** | Divise une chaîne en tableau |
| **JOIN(array, [delimiter])** | Joint un tableau en chaîne |
| **LTRIM(text)** | Supprime les espaces à gauche |
| **RTRIM(text)** | Supprime les espaces à droite |
| **UCASE(text)** | Convertit en majuscules (alias de UPPER) |
| **LCASE(text)** | Convertit en minuscules (alias de LOWER) |
| **PROPER(text)** | Convertit en casse de titre |
| **CHR(code)** | Conversion code de caractère → caractère |
| **ASC(char)** | Conversion caractère → code de caractère |
| **STR(value)** | Conversion nombre → chaîne |
| **URLENCODE(text, [encoding])** | Encodage URL |
| **URLDECODE(text, [encoding])** | Décodage URL |
| **ESCAPEPATHSTR(path, [replacement])** | Traite les caractères interdits dans les chemins de fichiers |

### Fonctions de date/heure (12)

| Nom de fonction | Aperçu |
|-----------------|---------|
| **NOW()** | Obtient la date et l'heure actuelles |
| **DATE()** | Obtient la date d'aujourd'hui |
| **TIME()** | Obtient l'heure actuelle |
| **YEAR([date])** | Obtient l'année |
| **MONTH([date])** | Obtient le mois |
| **DAY([date])** | Obtient le jour |
| **HOUR([time])** | Obtient l'heure |
| **MINUTE([time])** | Obtient les minutes |
| **SECOND([time])** | Obtient les secondes |
| **DATEADD(interval, number, [date])** | Ajoute/soustrait à une date |
| **DATEDIFF(interval, date1, [date2])** | Calcule la différence entre dates |
| **WEEKDAY([date], [firstday])** | Renvoie le jour de la semaine (1=dimanche) |

### Fonctions CSV (9)

| Nom de fonction | Aperçu |
|-----------------|---------|
| **CSVCOUNT(csv_text)** | Compte le nombre d'éléments CSV |
| **CSVREAD(csv_text, index)** | Obtient l'élément à l'index spécifié d'une chaîne CSV |
| **CSVUNIQUE(csv_text)** | Supprime les doublons |
| **CSVMERGE(csv1, csv2, ...)** | Fusionne plusieurs CSV |
| **CSVDIFF(array_name, csv1, csv2)** | Obtient la différence entre CSV |
| **PICKCSV(csv_text, [index])** | Sélectionne un élément CSV (omis : aléatoire) |
| **RNDCSV(csv_text)** | Sélection aléatoire dans CSV (identique à PICKCSV) |
| **CSVJOIN(array, [delimiter])** | Joint un tableau en chaîne CSV |
| **CSVSORT(csv_text, [delimiter], [reverse])** | Trie les éléments CSV |

### Fonctions d'expressions régulières (7)

| Nom de fonction | Aperçu |
|-----------------|---------|
| **REGEX(pattern, text)** | Teste la correspondance de motif |
| **REGEXMATCH(pattern, text)** | Obtient la première correspondance |
| **REGEXREPLACE(pattern, text, replacement)** | Remplace un motif |
| **REGEXEXTRACT(pattern, text, [group])** | Extrait un groupe |
| **REGEXCOUNT(pattern, text)** | Compte le nombre de correspondances |
| **REGEXMATCHES(pattern, text)** | Obtient toutes les correspondances en tableau |
| **REGEXSPLIT(pattern, text)** | Divise par motif |

### Fonctions de tableaux (3)

| Nom de fonction | Aperçu |
|-----------------|---------|
| **UBOUND(array)** | Obtient l'index supérieur du tableau |
| **ARRAY(variable_name, value1, value2, ...)** | Initialise le tableau et définit les valeurs |
| **REDIM(array_name, size)** | Modifie la taille du tableau (redéfinition) |

### Fonctions de conversion et détection de types (7)

| Nom de fonction | Aperçu |
|-----------------|---------|
| **CSTR(value)** | Convertit en chaîne |
| **CINT(value)** | Convertit en entier |
| **CDBL(value)** | Convertit en nombre à virgule flottante |
| **FORMAT(value, [format_string])** | Formate nombre/date dans le format spécifié (compatible VBA) |
| **ISNUMERIC(value)** | Détermine si c'est un nombre |
| **ISDATE(value)** | Détermine si c'est une date |
| **ISARRAY(variable_name)** | Détermine si c'est un tableau |

### Fonctions de modèle (1)

| Nom de fonction | Aperçu |
|-----------------|---------|
| **OPTIMAL_LATENT(model_hint, width, height)** | Détermine automatiquement la taille optimale de l'espace Latent à partir du nom du modèle et du rapport d'aspect |

### Fonctions utilitaires (18)

| Nom de fonction | Aperçu |
|-----------------|---------|
| **PRINT(message, ...)** | Affiche des valeurs dans la zone de texte (pour le débogage) |
| **OUTPUT(arg, [path], [flg])** | Affiche texte, nombres, tableaux, images, données binaires dans un fichier |
| **INPUT(path)** | Lit un fichier depuis le dossier de sortie ComfyUI (détection dynamique du type) |
| **ISFILEEXIST(path, [flg])** | Vérification de l'existence du fichier et obtention d'informations étendues (recherche _NNNN, taille d'image, taille de fichier) |
| **VRAMFREE([min_free_vram_gb])** | Libère la VRAM et la RAM (déchargement de modèle, effacement du cache, GC) |
| **SLEEP([milliseconds])** | Met en pause le traitement pour le nombre spécifié de millisecondes (par défaut : 10ms) |
| **IMAGETOBYTEARRAY(image_input, [max_size], [format], [return_format])** | Convertit IMAGE/chemin de fichier en tableau JSON d'image |
| **IMAGETOBASE64(image_input, [max_size], [format], [return_format])** | Encode IMAGE/chemin de fichier en Base64 (pour API Vision) |
| **GETANYWIDTH([any_data])** | Obtient la largeur (nombre de pixels) de données de type IMAGE/LATENT |
| **GETANYHEIGHT([any_data])** | Obtient la hauteur (nombre de pixels) de données de type IMAGE/LATENT |
| **GETANYTYPE([any_data])** | Détermine le nom du type de données de type ANY |
| **GETANYVALUEINT([any_data])** | Obtient une valeur entière à partir de données de type ANY |
| **GETANYVALUEFLOAT([any_data])** | Obtient une valeur à virgule flottante à partir de données de type ANY |
| **GETANYSTRING([any_data])** | Obtient une chaîne à partir de données de type ANY |
| **ISNUMERIC(value)** | Détermine si une valeur est un nombre |
| **ISDATE(value)** | Détermine si une valeur peut être analysée comme une date |
| **ISARRAY(variable_name)** | Détermine si une variable est un tableau |
| **TYPE(value)** | Renvoie le type de la variable sous forme de chaîne |

---

[← Retour au document principal](README.md)
