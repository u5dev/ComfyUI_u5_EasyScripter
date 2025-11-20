# Référence des fonctions d'expressions régulières

[← Retour à l'index des fonctions intégrées](00_index.md)

## Vue d'ensemble

Les fonctions d'expressions régulières permettent un traitement de texte avancé tel que la correspondance de motifs, la recherche, le remplacement et l'extraction. Elles utilisent le moteur d'expressions régulières Python et fournissent des fonctionnalités puissantes de correspondance de motifs.

---

## REGEX(pattern, text)

**Description** : Teste la correspondance de motif

**Arguments** :
- pattern - Motif d'expression régulière
- text - Chaîne de recherche cible

**Retour** : 1 (correspondance) ou 0

**Exemples** :
```vba
result = REGEX("\\d+", "abc123def")
PRINT(result)  ' 1 (contient des chiffres)

result = REGEX("^[A-Z]", "Hello")
PRINT(result)  ' 1 (commence par une majuscule)

result = REGEX("\\.(jpg|png)$", "a.gif")
PRINT(result)  ' 0 (pas jpg ou png)
```

---

## REGEXMATCH(pattern, text)

**Description** : Récupère la première correspondance

**Arguments** :
- pattern - Motif d'expression régulière
- text - Chaîne de recherche cible

**Retour** : Chaîne correspondante (vide si aucune)

**Exemples** :
```vba
result = REGEXMATCH("\\d+", "abc123def456")
PRINT(result)  ' "123"

result = REGEXMATCH("[A-Z]+", "helloWORLD")
PRINT(result)  ' "WORLD"
```

---

## REGEXREPLACE(pattern, text, replacement)

**Description** : Remplace le motif

**Arguments** :
- pattern - Motif d'expression régulière
- text - Chaîne cible
- replacement - Chaîne de remplacement

**Retour** : Chaîne après remplacement

**Exemples** :
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

**Description** : Extrait un groupe

**Arguments** :
- pattern - Motif d'expression régulière (avec groupes)
- text - Chaîne cible
- group - Numéro de groupe (par défaut : 0=tout)

**Retour** : Chaîne extraite

**Exemples** :
```vba
result = REGEXEXTRACT("(\\d{4})-(\\d{2})", "2024-01-15", 1)
PRINT(result)  ' "2024"

result = REGEXEXTRACT("(\\w+)@(\\w+)", "user@domain", 2)
PRINT(result)  ' "domain"
```

---

## REGEXCOUNT(pattern, text)

**Description** : Compte le nombre de correspondances

**Arguments** :
- pattern - Motif d'expression régulière
- text - Chaîne cible

**Retour** : Nombre de correspondances

**Exemples** :
```vba
count = REGEXCOUNT("\\d", "a1b2c3d4")
PRINT(count)  ' 4

count = REGEXCOUNT("\\w+", "hello world")
PRINT(count)  ' 2
```

---

## REGEXMATCHES(pattern, text)

**Description** : Récupère toutes les correspondances sous forme de tableau

**Arguments** :
- pattern - Motif d'expression régulière
- text - Chaîne cible

**Retour** : Liste de correspondances

**Exemples** :
```vba
matches = REGEXMATCHES("\\d+", "a10b20c30")
PRINT(matches)  ' ["10", "20", "30"]
```

---

## REGEXSPLIT(pattern, text)

**Description** : Divise par motif

**Arguments** :
- pattern - Motif de séparateur
- text - Chaîne cible

**Retour** : Liste divisée

**Exemples** :
```vba
parts = REGEXSPLIT("[,;]", "a,b;c,d")
PRINT(parts)  ' ["a", "b", "c", "d"]
PRINT(parts[0]) ' a

parts = REGEXSPLIT("\\s+", "one  two  three")
PRINT(parts)  ' ["one", "two", "three"]
PRINT(parts[1]) ' two
```

---

[← Retour à l'index des fonctions intégrées](00_index.md)
