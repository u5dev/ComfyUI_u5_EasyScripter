# u5 EasyScripter Node

[日本語](../../README.md) | [English](../en/README.md) | [中文](../zh/README.md) | [Español](../es/README.md) | **Français** | [Deutsch](../de/README.md)

---

## Qu'est-ce que c'est ?
- Un nœud personnalisé pour ComfyUI qui permet d'exécuter des **scripts simples de style VBA**
- Permet diverses intégrations, notamment des branchements conditionnels, la formation de prompts, le traitement en boucle, et les appels d'API externes
- **Presque toutes les fonctions sont fournies avec des exemples prêts à copier-coller**, donc pas de problème même sans expérience en programmation
- Intègre également des nœuds séquentiels et des outils de libération de mémoire publiés ailleurs

```
Créé parce que la configuration devenait lourde avec les nœuds standard ou individuels, et qu'un contrôle fin était difficile
```

---

## Fonctionnalités recommandées et cas d'usage
- Vous pouvez glisser-déposer une capture d'écran du workflow dans ComfyUI et l'utiliser immédiatement

### Créer automatiquement de nombreuses variations
- C'est ennuyeux de penser au prompt à chaque fois. Produisez rapidement des variations en mode diaporama !
```vba
' Prompt de base + remplacer aléatoirement l'expression et la pose à chaque fois pour créer un prompt
' → "base prompt" & "," & RNDCSV("CSV des poses candidates") & "," & RNDCSV("CSV des expressions candidates")

RETURN1 = "woman, a girl, nurse, with a bandage, pale skin, green eyes, pink hair, blunt bangs,upper body, full body shot, masterpiece, best quality, high quality," & RNDCSV("looking at viewer, looking away, looking back, wink, making a peace sign, making a heart with hands, making a thumbs up, waving at the camera") & "," & RNDCSV("blush, smiling, embarrassed, sleepy, serious expression, fear")
```
<img src="../img/AUTO_SLIDESHOW.png" alt="Exemple de script de génération de prompt dans le nœud EasyScripter" width="80%"><br>
  ↓<br>
  En collant juste une ligne<br>
  ↓<br>
<img src="../img/SLIDES.png" alt="Diaporama d'images de variations générées automatiquement" width="100%">

### Ajustement automatique de la taille Latent optimale pour le modèle
- C'est SDXL donc la résolution est comme ça, etc., on n'a pas le temps de s'en occuper !
```vba
result = OPTIMAL_LATENT("SDXL", 4, 3) ' Ajusté automatiquement à 1152x896
RETURN1 = RESULT[0] '1152
RETURN2 = RESULT[1] '896
```
<img src="../img/OPTIMAL_LATENT.png" alt="Exemple d'ajustement automatique de résolution optimisée par modèle avec la fonction OPTIMAL_LATENT" width="80%"><br>

**Collez simplement dans la fenêtre de script en bas du nœud et il se transforme instantanément en un nœud professionnel avec des fonctionnalités spéciales**

---

## 📖 Documentation

Pour une documentation détaillée, veuillez consulter :

- **[📖 Référence du langage de script](01_syntax_reference.md)** - Guide complet de la grammaire et des structures de contrôle
- **[🔧 Référence des fonctions intégrées](00_index.md)** - Référence complète de plus de 100 fonctions intégrées
- **[🌟 Merci de votre soutien](CONTENTS.md)** - Exemples pratiques plus utiles, images de workflow riches, explications détaillées

---

## Solutions avec u5 EasyScripter

**Un nœud, des possibilités infinies** - u5 EasyScripter est un moteur de script générique fonctionnant sur ComfyUI :

- ✅ **Remplace plus de 10 nœuds dédiés** : traitement de texte, calculs mathématiques, logique conditionnelle, génération aléatoire
- ✅ **Accélère le traitement par lots** : balayage automatique de paramètres, génération intelligente de variations
- ✅ **Améliore l'ingénierie de prompts** : ajustement dynamique des poids, modifications par branchement conditionnel, variations intelligentes
- ✅ **Optimise le workflow** : graphiques propres, chargement rapide, partage facile
- ✅ **Évolutif** : des calculs simples aux algorithmes d'automatisation complexes
- ✅ **Protection contre l'exécution parallèle** : mise en file d'attente sûre sans blocage lors de l'exécution simultanée de plusieurs nœuds
- ✅ **Multilingue** : messages d'erreur et sortie de débogage en japonais et en anglais

---

## ⚡ Démarrage rapide

### Installation

```bash
# Cloner dans le répertoire custom_nodes de ComfyUI
git clone https://github.com/u5dev/ComfyUI_u5_EasyScripter.git
```

### Votre premier workflow intelligent
- Ajustement intelligent basé sur les règles de prompt requises par le type de modèle

```vba

model_type = TXT1  ' Connecter le nom du modèle ("sdxl" ou "Flux")
PRINT(model_type)  ' Vérifier le type de modèle
base_prompt = "beautiful landscape"

SELECT CASE model_type
    CASE "sdxl"
        RETURN1 = "(" & base_prompt & ", ultra-detailed wide landscape, crisp daylight photography, shot on full-frame DSLR, high dynamic range, 8k uhd, professional photography:1.2)"
        PRINT(RETURN1)  ' Vérifier le prompt SDXL
    CASE "flux"
        RETURN1 = "(" & base_prompt & "moody cinematic wide shot of a beautiful landscape at golden hour, dramatic backlight haze, soft volumetric light, cinematic lighting:1.1, subtle film grain)"
        PRINT(RETURN1)  ' Vérifier le prompt Flux
    CASE ELSE
        RETURN1 = base_prompt & ", high quality"
        PRINT(RETURN1)  ' Vérifier le prompt par défaut
END SELECT
```
<img src="../img/FIRST_WORFLOW.png" alt="Exemple de workflow d'ajustement de prompt par type de modèle" width="50%">

---

## 💡 Utilisation de base

### Configuration du nœud

Le **nœud EasyScripter** a la configuration suivante :

#### Entrées
- `script` : Écrire le script de style VBA (obligatoire)
- `VAL1_int`, `VAL1_float` : Entrée numérique 1 (utilisable comme `VAL1` après sommation)
- `VAL2_int`, `VAL2_float` : Entrée numérique 2 (utilisable comme `VAL2` après sommation)
- `TXT1`, `TXT2` : Entrées texte
- `any_input` : Entrée de type ANY (accepte MODEL, CLIP, VAE, etc.)

#### Sorties
- `RETURN1_int`, `RETURN1_float`, `RETURN1_text` : Valeur de retour principale (sortie simultanée en 3 formats)
- `RETURN2_int`, `RETURN2_float`, `RETURN2_text` : Valeur de retour secondaire (sortie simultanée en 3 formats)
- `relay_output` : Sortie de bypass complet de `any_input` (contrôlable par la variable RELAY_OUTPUT)

![Exemple de connexion de base du nœud EasyScripter](../img/SimpleConnection.png)

### Exemples simples
Essayez de copier-coller dans le workflow ci-dessus

#### Calcul de base
```vba
' Additionner deux valeurs et les retourner
result = VAL1 + VAL2
PRINT(result)  ' Vérifier le résultat du calcul
RETURN1 = result
```

#### Concaténation de chaînes
```vba
' Combiner deux textes
combined = TXT1 & " " & TXT2
PRINT(combined)  ' Vérifier le résultat de la combinaison
RETURN1 = combined
```

#### Branchement conditionnel
```vba
' Changer le message en fonction de la valeur
IF VAL1 > 10 THEN
    RETURN1 = "Grand"
    PRINT(RETURN1)  ' Vérifier le résultat du branchement
ELSE
    RETURN1 = "Petit"
    PRINT(RETURN1)  ' Vérifier le résultat du branchement
END IF
```

**Instruction IF sur une ligne et instruction EXIT** (v2.1.1 et ultérieures) :
```vba
' Retour anticipé dans une fonction
FUNCTION Validate(value)
    IF value < 0 THEN EXIT FUNCTION  ' Terminer immédiatement si valeur négative
    Validate = value * 2
END FUNCTION

' Sortie anticipée de boucle
FOR i = 1 TO 100
    IF i > 50 THEN EXIT FOR  ' Terminer la boucle si supérieur à 50
    sum = sum + i
NEXT

RETURN1 = sum
RETURN2 = i
```

#### Sélection aléatoire
```vba
' Sélectionner aléatoirement dans un CSV (index omis)
styles = "realistic, anime, oil painting, watercolor"
selected = PICKCSV(styles)  ' Sélection aléatoire
PRINT(selected)  ' Vérifier le résultat de la sélection
RETURN1 = selected

' Ou spécifier un index spécifique (base 1)
' selected = PICKCSV(styles, 2)  ' Sélectionner le 2ème "anime"
' PRINT(selected)  ' "anime"
```

---

## 🛠️ Série de chargeurs u5

Groupe de nœuds de chargeur avec fonction de sortie de nom de fichier, à utiliser en combinaison avec EasyScripter :

- **u5 Checkpoint Loader** - MODEL, CLIP, VAE + sortie de nom de fichier
- **u5 LoRA Loader** - Modèle + application LoRA + sortie de nom de fichier
- **u5 VAE Loader** - VAE + sortie de nom de fichier
- **u5 ControlNet Loader** - ControlNet + sortie de nom de fichier
- **u5 CLIP Vision Loader** - CLIP Vision + sortie de nom de fichier
- **u5 Style Model Loader** - StyleModel + sortie de nom de fichier
- **u5 GLIGEN Loader** - GLIGEN + sortie de nom de fichier
- **u5 UNET Loader** - UNET + sortie de nom de fichier
- **u5 CLIP Loader** - CLIP + sortie de nom de fichier

Tous les chargeurs u5 ont les fonctionnalités communes suivantes :
- Recherche et chargement de nom de fichier par le champ `text_input` (correspondance partielle)
- Sortie `filename` pour sortir le nom du fichier chargé en tant que texte

---

## 🔍 Dépannage

### Le script génère une erreur
- Pour vérifier la sortie de débogage avec la fonction PRINT, utilisez la forme de fonction avec parenthèses `PRINT("LOG", valeur)`
  - **Remarque** : La forme d'instruction VBA (`PRINT "LOG", valeur`) n'est pas prise en charge
- Vérifier les fautes de frappe et la casse des noms de variables

### Fonction introuvable
- Vérifiez l'orthographe du nom de fonction
- Vérifiez le nom de fonction correct dans l'[index des fonctions intégrées](00_index.md)

### La valeur de retour est différente de ce qui était attendu
- Pour vérifier les valeurs intermédiaires avec la fonction PRINT, appelez également avec la forme avec parenthèses (`PRINT("Valeur intermédiaire:", variable)`)
- Vérifier si une conversion de type (CINT, CDBL, CSTR) est nécessaire

### Apparence étrange
- Essayez d'enregistrer le workflow et de rafraîchir avec F5

---

## 📜 Licence

MIT License

Copyright (c) 2025 u5dev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 📝 Historique des mises à jour

Pour l'historique détaillé des versions, consultez [CHANGELOG.md](CHANGELOG.md).

---

## 🙏 Remerciements

Merci à tous les membres de la communauté ComfyUI.
