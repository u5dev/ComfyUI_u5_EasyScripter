# Référence des fonctions mathématiques

[日本語](../../docs/02_builtin_functions/01_math_functions.md) | [English](../en/01_math_functions.md) | [中文](../zh/01_math_functions.md) | [Español](../es/01_math_functions.md) | **Français** | [Deutsch](../de/01_math_functions.md)

---

[← Retour à l'index des fonctions intégrées](00_index.md)

---

Référence complète des fonctions mathématiques disponibles dans u5 EasyScripter.

## Liste des fonctions
24 fonctions mathématiques sont fournies.

---

## Fonctions mathématiques
Fournit des fonctionnalités de base liées aux mathématiques.
Dans les exemples attendus, les nombres à circulation infinie (0.9999...) sont arrondis pour plus de commodité.


### ABS(value)
**Description** : Retourne la valeur absolue
**Arguments** : value - Valeur numérique ou valeur convertible en nombre
**Retour** : Valeur absolue (float)
**Exemples** :
```vba
result = ABS(-5.5)
PRINT(result)  ' 5.5
result = ABS(10)
PRINT(result)  ' 10
result = ABS("-3.14")
PRINT(result)  ' 3.14
```

### INT(value)
**Description** : Retourne la partie entière (tronque les décimales)
**Arguments** : value - Valeur numérique
**Retour** : Partie entière (format float)
**Exemples** :
```vba
result = INT(5.9)
PRINT(result)  ' 5
result = INT(-2.3)
PRINT(result)  ' -2
result = INT("10.5")
PRINT(result)  ' 10
```

### ROUND(value, [digits])
**Description** : Retourne une valeur arrondie
**Arguments** :
- value - Valeur numérique
- digits - Nombre de décimales (par défaut : 0)
**Retour** : Valeur arrondie
**Exemples** :
```vba
result = ROUND(3.14159, 2)
PRINT(result)  ' 3.14
result = ROUND(5.5)
PRINT(result)  ' 6
result = ROUND(123.456, 1)
PRINT(result)  ' 123.5
```

### SQRT(value)
**Description** : Retourne la racine carrée
**Arguments** : value - Valeur numérique ≥ 0
**Retour** : Racine carrée
**Erreur** : Les valeurs négatives provoquent une erreur
**Exemples** :
```vba
result = SQRT(16)
PRINT(result)  ' 4
result = SQRT(2)
PRINT(result)  ' 1.4142135623730951
' result = SQRT(-1) ' Erreur !
```

### MIN(value1, value2, ...)
**Description** : Retourne la valeur minimale
**Arguments** : Plusieurs valeurs numériques
**Retour** : Valeur minimale
**Exemples** :
```vba
result = MIN(5, 2, 8, 1)
PRINT(result)  ' 1
result = MIN(VAL1, VAL2)
PRINT(result)  ' La plus petite des deux valeurs d'entrée
```

### MAX(value1, value2, ...)
**Description** : Retourne la valeur maximale
**Arguments** : Plusieurs valeurs numériques
**Retour** : Valeur maximale
**Exemples** :
```vba
result = MAX(5, 2, 8, 1)
PRINT(result)  ' 8
result = MAX(0, VAL1)
PRINT(result)  ' Limite à 0 minimum
```

### SIN(radians)
**Description** : Retourne le sinus
**Arguments** : radians - Angle en radians
**Retour** : Valeur entre -1 et 1
**Exemples** :
```vba
result = SIN(0)
PRINT(result)  ' 0
result = SIN(3.14159/2)
PRINT(result)  ' 0.9999999999991198 (environ 1)
result = SIN(RADIANS(30))
PRINT(result)  ' 0.49999999999999994 (environ 0.5)
```

### COS(radians)
**Description** : Retourne le cosinus
**Arguments** : radians - Angle en radians
**Retour** : Valeur entre -1 et 1
**Exemples** :
```vba
result = COS(0)
PRINT(result)  ' 1
result = COS(3.14159)
PRINT(result)  ' -0.9999999999964793 (environ -1)
result = COS(RADIANS(60))
PRINT(result)  ' 0.5000000000000001 (environ 0.5)
```

### TAN(radians)
**Description** : Retourne la tangente
**Arguments** : radians - Angle en radians
**Retour** : Valeur de la tangente
**Exemples** :
```vba
result = TAN(0)
PRINT(result)  ' 0
result = TAN(3.14159/4)
PRINT(result)  ' 0.9999986732059836 (environ 1)
result = TAN(RADIANS(45))
PRINT(result)  ' 0.9999999999999999 (environ 1)
```

### RADIANS(degrees)
**Description** : Convertit les degrés en radians
**Arguments** : degrees - Angle en degrés
**Retour** : Radians
**Exemples** :
```vba
result = RADIANS(180)
PRINT(result)  ' 3.141592653589793
result = RADIANS(90)
PRINT(result)  ' 1.5707963267948966
result = RADIANS(45)
PRINT(result)  ' 0.7853981633974483
```

### DEGREES(radians)
**Description** : Convertit les radians en degrés
**Arguments** : radians - Angle en radians
**Retour** : Degrés
**Exemples** :
```vba
result = DEGREES(3.14159)
PRINT(result)  ' 179.9998479605043 (environ 180)
result = DEGREES(1.5708)
PRINT(result)  ' 90.00021045914971 (environ 90)
result = DEGREES(0.7854)
PRINT(result)  ' 45.00010522957486 (environ 45)
```

### POW(base, exponent)
**Description** : Calcule la puissance (base^exponent)
**Arguments** :
- base - Base
- exponent - Exposant
**Retour** : Résultat de la puissance
**Exemples** :
```vba
result = POW(2, 10)
PRINT(result)  ' 1024
result = POW(5, 3)
PRINT(result)  ' 125
result = POW(10, -2)
PRINT(result)  ' 0.01
```

### LOG(value, [base])
**Description** : Retourne le logarithme

**Important** : La fonction LOG retourne par défaut le logarithme naturel (base e).

**Arguments** :
- value - Nombre positif
- base - Base (par défaut : logarithme naturel e)
**Retour** : Logarithme
**Exemples** :
```vba
result = LOG(2.718282)
PRINT(result)  ' 1.0000000631063886 (environ 1)
result = LOG(8, 2)
PRINT(result)  ' 3 (base 2)
result = LOG(1000, 10)
PRINT(result)  ' 2.9999999999999996 (environ 3)
```

### EXP(value)
**Description** : Puissance de e (base du logarithme naturel)
**Arguments** : value - Exposant
**Retour** : e^value
**Exemples** :
```vba
result = EXP(0)
PRINT(result)  ' 1
result = EXP(1)
PRINT(result)  ' 2.718281828459045
result = EXP(2)
PRINT(result)  ' 7.38905609893065
```

### AVG(value1, value2, ...)
**Description** : Calcule la moyenne
**Arguments** : Plusieurs valeurs numériques
**Retour** : Valeur moyenne
**Exemples** :
```vba
result = AVG(10, 20, 30)
PRINT(result)  ' 20
result = AVG(1, 2, 3, 4, 5)
PRINT(result)  ' 3
```

### SUM(value1, value2, ...)
**Description** : Calcule la somme
**Arguments** : Plusieurs valeurs numériques
**Retour** : Somme
**Exemples** :
```vba
result = SUM(10, 20, 30)
PRINT(result)  ' 60
result = SUM(1, 2, 3, 4, 5)
PRINT(result)  ' 15
```

---

[← Retour à l'index des fonctions intégrées](00_index.md)
