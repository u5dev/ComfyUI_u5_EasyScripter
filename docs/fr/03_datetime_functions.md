# Référence des fonctions de date et heure

[← Retour à l'index des fonctions intégrées](00_index.md)

Référence complète des fonctions de date et heure disponibles dans u5 EasyScripter.

## Liste des fonctions
12 fonctions de date et heure sont fournies.

---

### NOW()
**Description** : Obtient la date et l'heure actuelles
**Arguments** : Aucun
**Retour** : Chaîne de date et heure (YYYY-MM-DD HH:MM:SS)
**Exemples** :
```vba
currentTime = NOW()
PRINT(currentTime)    ' "2024-01-15 14:30:45"
PRINT("Heure actuelle: " & NOW())
```

### DATE()
**Description** : Obtient la date d'aujourd'hui
**Arguments** : Aucun
**Retour** : Chaîne de date (YYYY-MM-DD)
**Exemples** :
```vba
today = DATE()
PRINT(today)    ' "2024-01-15"
```

### TIME()
**Description** : Obtient l'heure actuelle
**Arguments** : Aucun
**Retour** : Chaîne d'heure (HH:MM:SS)
**Exemples** :
```vba
currentTime = TIME()
PRINT(currentTime)    ' "14:30:45"
```

### YEAR([date])
**Description** : Obtient l'année
**Arguments** : date - Chaîne de date (par défaut : aujourd'hui)
**Retour** : Année (numérique)
**Exemples** :
```vba
result = YEAR()
PRINT(result)              ' 2024 (année en cours)
result = YEAR("2023-12-25")
PRINT(result)              ' 2023
```

### MONTH([date])
**Description** : Obtient le mois
**Arguments** : date - Chaîne de date (par défaut : aujourd'hui)
**Retour** : Mois (1-12)
**Exemples** :
```vba
result = MONTH()
PRINT(result)             ' 1 (mois en cours)
result = MONTH("2023-12-25")
PRINT(result)             ' 12
```

### DAY([date])
**Description** : Obtient le jour
**Arguments** : date - Chaîne de date (par défaut : aujourd'hui)
**Retour** : Jour (1-31)
**Exemples** :
```vba
result = DAY()
PRINT(result)               ' 15 (aujourd'hui)
result = DAY("2023-12-25")
PRINT(result)               ' 25
```

### HOUR([time])
**Description** : Obtient l'heure
**Arguments** : time - Chaîne d'heure (par défaut : maintenant)
**Retour** : Heure (0-23)
**Exemples** :
```vba
result = HOUR()
PRINT(result)              ' 14 (heure actuelle)
result = HOUR("15:30:45")
PRINT(result)              ' 15
```

### MINUTE([time])
**Description** : Obtient les minutes
**Arguments** : time - Chaîne d'heure (par défaut : maintenant)
**Retour** : Minutes (0-59)
**Exemples** :
```vba
result = MINUTE()
PRINT(result)            ' 30 (minutes actuelles)
result = MINUTE("15:30:45")
PRINT(result)            ' 30
```

### SECOND([time])
**Description** : Obtient les secondes
**Arguments** : time - Chaîne d'heure (par défaut : maintenant)
**Retour** : Secondes (0-59)
**Exemples** :
```vba
result = SECOND()
PRINT(result)            ' 45 (secondes actuelles)
result = SECOND("15:30:45")
PRINT(result)            ' 45
```

### DATEADD(interval, number, [date])
**Description** : Ajoute/soustrait à une date
**Arguments** :
- interval - Unité ("d"=jour, "m"=mois, "y"=année, "h"=heure, "n"=minute, "s"=seconde)
- number - Nombre à ajouter
- date - Date de référence (par défaut : maintenant)
**Retour** : Date et heure calculées (format YYYY/MM/DD HH:MM:SS)
**Exemples** :
```vba
tomorrow = DATEADD("d", 1, DATE())
PRINT(tomorrow)        ' Demain (ex: "2025/10/23 00:00:00")
nextMonth = DATEADD("m", 1, "2024-01-15")
PRINT(nextMonth)       ' "2024/02/15 00:00:00"
inOneHour = DATEADD("h", 1, NOW())
PRINT(inOneHour)       ' Dans 1 heure (ex: "2025/10/22 15:30:00")
```

### DATEDIFF(interval, date1, [date2])
**Description** : Calcule la différence entre deux dates
**Arguments** :
- interval - Unité ("d"=jour, "m"=mois, "y"=année, "h"=heure, "n"=minute, "s"=seconde)
- date1 - Date de début
- date2 - Date de fin (par défaut : maintenant)
**Retour** : Différence (numérique)
**Exemples** :
```vba
days = DATEDIFF("d", "2024-01-01", "2024-01-15")
PRINT(days)  ' 14
age = DATEDIFF("y", "1990-01-01", DATE())
PRINT(age)   ' Âge
hours = DATEDIFF("h", "2024-01-15 10:00:00", NOW())
PRINT(hours) ' Temps écoulé
```

### CDATE(date_string)
**Description** : Convertit une chaîne de date en type date (compatible VBA)
**Arguments** : date_string - Chaîne représentant une date
**Retour** : Chaîne de date (format YYYY/MM/DD HH:MM:SS)
**Support de format flexible** :
- Date et heure complètes : `"2025/11/05 15:39:49"` → `2025/11/05 15:39:49`
- Date uniquement : `"2025/11/05"` → `2025/11/05 00:00:00` (heure 00:00:00)
- Année et mois : `"2025/11"` → `2025/11/01 00:00:00` (jour=1, heure=00:00:00)
- Année uniquement : `"2025"` → `2025/01/01 00:00:00` (mois/jour=1/1, heure=00:00:00)
- Heure uniquement : `"2025/11/05 15"` → `2025/11/05 15:00:00` (min/sec=00)
- Heure et minutes : `"2025/11/05 15:39"` → `2025/11/05 15:39:00` (sec=00)

**Flexibilité des séparateurs** :
- Mixte de `/` et `-` et `:` et espaces autorisés
- `"2025-11-05-15-39-49"`, `"2025-11-05 15-39-49"`, `"2025-11-05 15:39:49"` tous traités de la même manière

**Exemples** :
```vba
' Date et heure complètes
result = CDATE("2025/11/05 15:39:49")
PRINT(result)  ' "2025/11/05 15:39:49"

' Date uniquement (heure devient 00:00:00)
result = CDATE("2025/11/05")
PRINT(result)  ' "2025/11/05 00:00:00"

' Séparateurs mixtes OK
result = CDATE("2025-11-05 15:39:49")
PRINT(result)  ' "2025/11/05 15:39:49"

' Date partielle (parties manquantes complétées)
result = CDATE("2025/11")
PRINT(result)  ' "2025/11/01 00:00:00"
```

---

[← Retour à l'index des fonctions intégrées](00_index.md)
