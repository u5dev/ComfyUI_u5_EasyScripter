# Historique des mises à jour (CHANGELOG)

[日本語](../CHANGELOG.md) | [English](../en/CHANGELOG.md) | [中文](../zh/CHANGELOG.md) | [Español](../es/CHANGELOG.md) | **Français** | [Deutsch](../de/CHANGELOG.md)

---

Historique des principales mises à jour de version de u5 EasyScripter.

---

## 📝 Historique des mises à jour

### v3.1.2 (2025-11-18) - Corrections de formatage de la documentation

#### Fixed
- **Correction des références croisées du nombre de fonctions** : Nombre de fonctions dans docs/02_builtin_functions/00_index.md corrigé pour correspondre au nombre réel d'implémentations
  - Fonctions mathématiques : 24 → 16
  - Fonctions CSV : 11 → 9
  - Fonctions de tableaux : 7 → 3
  - Fonctions de modèle : 3 → 1
  - Fonctions utilitaires : 21 → 18
  - Fonctions de contrôle de boucle : 9 → 1
  - Fonctions de communication HTTP : 17 → 9
  - Exécution de fonctions Python : 3 → 4
- **Correction du tableau de référence rapide** : Tableau de référence rapide dans 00_index.md corrigé
  - 8 fonctions inexistantes supprimées du tableau des fonctions mathématiques (RND, RANDOMIZE, FIX, SGN, ASIN, ACOS, ATAN, ATAN2)
  - Arguments de la fonction CSVDIFF corrigés : CSVDIFF(csv1, csv2) → CSVDIFF(array_name, csv1, csv2)
  - Fonction PYDECODE ajoutée au tableau des fonctions Python
- **Correction du nombre de fonctions de chaînes** : Nombre de fonctions dans docs/02_builtin_functions/02_string_functions.md corrigé de 29 → 28
- **Correction des liens d'ancrage de la table des matières** : Traits d'union initiaux supprimés des liens d'ancrage de la table des matières dans docs/01_syntax_reference.md (conformité avec la spécification Markdown GitHub)

### v3.1.1 (2025-11-17) - Ajout de documentation des fonctions de chaînes

#### Added
- **Documentation des fonctions de chaînes ajoutée** : Documentation de 7 fonctions de chaînes déjà implémentées
  - **ESCAPEPATHSTR(path, [replacement])** : Remplacer ou supprimer les caractères interdits dans les chemins de fichiers
  - **URLENCODE(text, [encoding])** : Encodage URL (encodage en pourcentage)
  - **URLDECODE(text, [encoding])** : Décodage URL
  - **PROPER(text)** : Convertir en casse de titre (première lettre de chaque mot en majuscule)
  - **CHR(code)** : Conversion code de caractère → caractère (plage ASCII)
  - **ASC(char)** : Conversion caractère → code de caractère
  - **STR(value)** : Conversion nombre → chaîne
  - Documentation : docs/02_builtin_functions/02_string_functions.md
  - Nombre de fonctions : corrigé de 21 → 23

#### Changed
- **Nombre total de fonctions intégrées** : Mis à jour de 135 entrées → 137 entrées
  - 135 fonctions uniques (133 fonctions + 2 alias)
  - README.md, docs/02_builtin_functions/00_index.md mis à jour

### v3.1.0 (2025-11-17) - Support de l'opérateur !=

#### Added
- **Opérateur !=** : Ajout de l'opérateur d'inégalité de style C
  - Fonctionne exactement comme l'opérateur `<>` (les deux peuvent être utilisés)
  - Implémentation : script_parser.py (ajouté au tableau TOKEN_PATTERNS)
  - Test : tests/test_neq_operator.py
  - Documentation : docs/01_syntax_reference.md

### v3.0.0 (2025-11-13) - Améliorations du socket d'entrée any_input et autres

### Added
- **Fonction IMAGETOBASE64** : Fonction pour convertir un tensor IMAGE ou un chemin de fichier image en encodage Base64 (ou format data URL)
  - Prise en charge de la génération de données pour l'envoi à l'API Vision d'OpenAI, etc.
  - Prise en charge des entrées de tensor IMAGE (connexion de nœud ComfyUI) et de chemin de fichier
  - Fonctionnalités : redimensionnement, compression JPEG (quality=85), conversion RGBA→RGB, retour Base64/data URL
  - Implémentation : functions/misc_functions.py (MiscFunctions.IMAGETOBASE64)
  - Documentation : docs/02_builtin_functions/09_utility_functions.md

- **Fonction IMAGETOBYTEARRAY** : Fonction pour convertir un tensor IMAGE ou un chemin de fichier image en tableau JSON (ou tableau d'octets)
  - Prise en charge de la génération de données pour l'envoi à l'API REST de Cloudflare Workers AI, etc.
  - Prise en charge des entrées de tensor IMAGE (connexion de nœud ComfyUI) et de chemin de fichier
  - Fonctionnalités : redimensionnement, compression JPEG, conversion RGBA→RGB, retour tableau JSON/type bytes
  - Implémentation : functions/misc_functions.py (MiscFunctions.IMAGETOBYTEARRAY)
  - Documentation : docs/02_builtin_functions/09_utility_functions.md

- **Fonction FORMAT** : Fonction pour formater des nombres/dates dans un format spécifié (compatible VBA)
  - Prise en charge du format VBA ("0", "0.0", "0.00", "#.##"), format Python, format strftime pour les dates
  - Implémentation : functions/misc_functions.py (MiscFunctions.FORMAT)
  - Documentation : docs/02_builtin_functions/07_type_functions.md

- **Fonction GETANYTYPE** : Fonction pour déterminer le nom du type de données de type ANY
  - Détermine les types de base (int, float, string) et les types ComfyUI (image, latent, model, vae, clip, etc.)
  - Récupération automatique depuis le socket d'entrée any_input ou spécification explicite des données possible
  - Implémentation : functions/misc_functions.py (MiscFunctions.GETANYTYPE)
  - Documentation : docs/02_builtin_functions/09_utility_functions.md

- **Fonction GETANYVALUEINT** : Fonction pour obtenir une valeur entière à partir de données de type ANY
  - Récupération automatique depuis le socket d'entrée any_input ou spécification explicite des données possible
  - Renvoie 0 si impossible à obtenir
  - Implémentation : functions/misc_functions.py (MiscFunctions.GETANYVALUEINT)
  - Documentation : docs/02_builtin_functions/09_utility_functions.md

- **Fonction GETANYVALUEFLOAT** : Fonction pour obtenir une valeur à virgule flottante à partir de données de type ANY
  - Récupération automatique depuis le socket d'entrée any_input ou spécification explicite des données possible
  - Renvoie 0.0 si impossible à obtenir
  - Implémentation : functions/misc_functions.py (MiscFunctions.GETANYVALUEFLOAT)
  - Documentation : docs/02_builtin_functions/09_utility_functions.md

- **Fonction GETANYSTRING** : Fonction pour obtenir une chaîne à partir de données de type ANY
  - Récupération automatique depuis le socket d'entrée any_input ou spécification explicite des données possible
  - Renvoie une chaîne vide si impossible à obtenir
  - Implémentation : functions/misc_functions.py (MiscFunctions.GETANYSTRING)
  - Documentation : docs/02_builtin_functions/09_utility_functions.md

---

**Pour l'historique complet**, veuillez consulter [CHANGELOG.md](../CHANGELOG.md) en japonais.
