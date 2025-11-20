# Référence des fonctions de modèles

[← Retour à l'index des fonctions intégrées](00_index.md)

## Vue d'ensemble

Les fonctions de modèles fournissent une fonctionnalité pour déterminer automatiquement la résolution optimale pour divers modèles génératifs utilisés dans ComfyUI. À partir du nom du modèle et du rapport d'aspect, elles calculent automatiquement la taille optimale de l'espace Latent pour ce modèle.

Modèles supportés : Stable Diffusion 1.5/2.1/XL, SD3/3.5, FLUX.1, Hunyuan-DiT, Kandinsky, PixArt, Playground, etc. (plus de 30 types)

---

## Liste des fonctions de modèles

### OPTIMAL_LATENT(model_hint, width, height)

**Description** : Détermine automatiquement la taille Latent optimale à partir du nom du modèle et du rapport d'aspect

**Arguments** :
- model_hint - Indice du nom du modèle (chaîne)
  - Ex : "SDXL", "SD 1.5", "Flux", "Hunyuan"
- width - Largeur souhaitée (entier)
- height - Hauteur souhaitée (entier)

**Retour** : Tableau de taille Latent optimale [width, height]

**Modèles supportés** : SD1.5, SD2.1, SDXL, SD3/3.5, Hunyuan-DiT, FLUX.1, Kandinsky, PixArt, Playground, etc. (30+ modèles)

**Exemples** :
```vba
' Obtenir la résolution optimale 4:3 pour SDXL
DIM result
result = OPTIMAL_LATENT("SDXL", 4, 3)
PRINT(result)  ' Vérification du résultat intermédiaire
PRINT("Taille optimale: " & result(0) & "x" & result(1))
' Sortie: "Model: SDXL 1.0 (base) | Optimal: 1152x896 (4:3)"
' Sortie: "{0: 1152, 1: 896}"
' Sortie: "Taille optimale: 1152x896"

' Obtenir 16:9 pour Stable Diffusion 1.5
result = OPTIMAL_LATENT("SD 1.5", 16, 9)
PRINT(result)  ' Vérification du résultat intermédiaire
PRINT(result(0) & "x" & result(1))
' Sortie: "Model: blue_pencil (SD1.5) | Optimal: 704x384 (11:6)"
' Sortie: "{0: 704, 1: 384}"
' Sortie: "704x384"

' Carré pour FLUX.1
result = OPTIMAL_LATENT("Flux", 256, 256)
PRINT(result)  ' Vérification du résultat intermédiaire
' Sortie: "Model: FLUX.1 (dev/pro) | Optimal: 1024x1024 (1:1)"
' Sortie: "{0: 1024, 1: 1024}"
```

---

## Mise à jour des données de modèles

Pour ajouter de nouveaux modèles, modifiez `data/model_resolutions.csv`.

**Format CSV** :
```csv
model_key,model_display_name,aliases,version,width,height,aspect_ratio,description
new_model,New Model v1.0,newmodel|new,1.0,1024,1024,1:1,description
```

**Attention** : Les nouvelles données seront reflétées après le redémarrage de ComfyUI.

---

## Exemples d'utilisation

### Détermination de résolution optimale dans un workflow SDXL

```vba
' Calculer automatiquement la résolution optimale pour SDXL à partir de la résolution d'entrée utilisateur
DIM user_width
DIM user_height
user_width = 1920  ' Largeur Full HD
PRINT(user_width)  ' Vérification du résultat intermédiaire
' Sortie: "1920"
user_height = 1080 ' Hauteur Full HD
PRINT(user_height)  ' Vérification du résultat intermédiaire
' Sortie: "1080"

DIM optimal
optimal = OPTIMAL_LATENT("SDXL", user_width, user_height)
PRINT(optimal)  ' Vérification du résultat intermédiaire
' Sortie: "Model: SDXL 1.0 (base) | Optimal: 1344x768 (16:9)"
' Sortie: "{0: 1344, 1: 768}"

' Obtenir la largeur et hauteur optimales depuis le tableau optimal
DIM final_width
DIM final_height
final_width = optimal(0)
PRINT(final_width)  ' Vérification du résultat intermédiaire
' Sortie: "1344"
final_height = optimal(1)
PRINT(final_height)  ' Vérification du résultat intermédiaire
' Sortie: "768"

PRINT("Entrée: " & user_width & "x" & user_height)
PRINT("SDXL optimal: " & final_width & "x" & final_height)
' Sortie: "Entrée: 1920x1080"
' Sortie: "SDXL optimal: 1344x768"
```

### Script générique prenant en charge plusieurs modèles

```vba
' Obtenir la résolution optimale pour chaque modèle en changeant simplement le nom du modèle
DIM model_name
DIM aspect_width
DIM aspect_height

model_name = "Flux"
PRINT(model_name)  ' Vérification du résultat intermédiaire
' Sortie: "Flux"
aspect_width = 1024
PRINT(aspect_width)  ' Vérification du résultat intermédiaire
' Sortie: "1024"
aspect_height = 1024
PRINT(aspect_height)  ' Vérification du résultat intermédiaire
' Sortie: "1024"

DIM result
result = OPTIMAL_LATENT(model_name, aspect_width, aspect_height)
PRINT(result)  ' Vérification du résultat intermédiaire
' Sortie: "Model: FLUX.1 (dev/pro) | Optimal: 1024x1024 (1:1)"
' Sortie: "{0: 1024, 1: 1024}"
PRINT(model_name & " -> " & result(0) & "x" & result(1))
' Sortie: "Flux -> 1024x1024"

' Changer en SD1.5
model_name = "SD 1.5"
PRINT(model_name)  ' Vérification du résultat intermédiaire
' Sortie: "SD 1.5"
result = OPTIMAL_LATENT(model_name, aspect_width, aspect_height)
PRINT(result)  ' Vérification du résultat intermédiaire
' Sortie: "Model: blue_pencil (SD1.5) | Optimal: 512x512 (1:1)"
' Sortie: "{0: 512, 1: 512}"
PRINT(model_name & " -> " & result(0) & "x" & result(1))
' Sortie: "SD 1.5 -> 512x512"
```

---

[← Retour à l'index des fonctions intégrées](00_index.md)
