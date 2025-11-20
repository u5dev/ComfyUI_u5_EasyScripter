# Référence des fonctions utilitaires

[← Retour à l'index des fonctions intégrées](00_index.md)

Les fonctions utilitaires sont un groupe de fonctions pratiques qui assistent le développement de scripts, telles que la sortie de débogage, le jugement de type et le traitement d'entrée.

---

## Fonctions de sortie

### PRINT(message, ...)

**Description** : Affiche des valeurs dans la zone de texte (pour le débogage)

**Arguments** :
- message - Valeur à afficher (plusieurs spécifications possibles)

**Retour** : Aucun (ajouté à la variable PRINT)

**Exemples** :
```vba
' Suivre la valeur de la variable
value = VAL1 * 2
PRINT("value after multiplication: " & value)

' Progression de la boucle
FOR i = 1 TO 10
    PRINT("Itération de la boucle: " & i)
    ' Traitement...
NEXT

' Vérification du branchement conditionnel
condition = VAL1 > 100
IF condition THEN
    PRINT("La condition était VRAIE")
ELSE
    PRINT("La condition était FAUSSE")
END IF

' Afficher plusieurs valeurs simultanément
PRINT("VAL1:", VAL1, "VAL2:", VAL2)
result = VAL1 + VAL2
PRINT("Résultat du calcul:", result)
```

**Attention** :
- Le contenu affiché par la fonction PRINT est affiché dans la zone de texte en bas du nœud
- Pratique pour vérifier les valeurs de variables lors du débogage

---

### OUTPUT(arg, [path], [flg])

**Description** : Sortie de texte, nombres, tableaux, images, données binaires vers un fichier

**Arguments** :
- arg (Any) - Valeur à sortir (chaîne, nombre, tableau, torch.Tensor, bytes)
- path (str, optionnel) - Chemin de sortie (chemin relatif, par défaut="")
- flg (str, optionnel) - Mode d'opération ("NEW"=nouveau/éviter les doublons, "ADD"=ajouter, par défaut="NEW")

**Retour** : str - Chemin absolu du fichier sorti (chaîne vide en cas d'échec)

**Fonctionnalités** :
1. **Sortie de texte** : Sortie de chaînes, nombres, tableaux comme fichier texte
2. **Sortie d'image** : Sortie de torch.Tensor (données d'image ComfyUI) comme PNG/JPEG, etc.
3. **Sortie binaire** : Sortie de données de type bytes comme fichier binaire
4. **Mode NEW** : Ajoute automatiquement `_0001`, `_0002`... en cas de doublon
5. **Mode ADD** : Ajoute au fichier existant
6. **Sécurité** : Refuse les chemins absolus/UNC (seuls les chemins relatifs sont autorisés)
7. **Sous-répertoires** : Création récursive automatique
8. **Complément d'extension** : `.txt` (texte), `.png` (image)

**Support de variables réservées** :
- `OUTPUT("TXT1", "output.txt")` → Sortie de la valeur du socket d'entrée TXT1
- Compatible avec TXT1, TXT2, ANY_INPUT

**Exemples** :
```vba
' Sortie de texte
path = OUTPUT("Hello World", "output.txt", "NEW")
PRINT("Destination de sortie: " & path)

' Sortie de nombre
path = OUTPUT(12345, "number.txt")
PRINT("Destination de sortie: " & path)

' Sortie de tableau
ARR = ARRAY("apple", "banana", "cherry")
path = OUTPUT(ARR, "fruits.txt")
PRINT("Destination de sortie: " & path)

' Sortie depuis variable réservée
path = OUTPUT("TXT1", "user_input.txt")
PRINT("Sortie de la valeur TXT1: " & path)

' Mode ajout
path1 = OUTPUT("First Line", "log.txt", "NEW")
PRINT("Nouveau: " & path1)
path2 = OUTPUT("Second Line", "log.txt", "ADD")
PRINT("Ajout: " & path2)

' Création de sous-répertoire
path = OUTPUT("data", "subdir/data.txt")
PRINT("Créé avec sous-répertoire: " & path)

' Éviter les doublons
path1 = OUTPUT("content", "file.txt", "NEW")
PRINT("1ère fois: " & path1)  ' file.txt
path2 = OUTPUT("content", "file.txt", "NEW")
PRINT("2ème fois: " & path2)  ' file_0001.txt
```

**Restrictions de sécurité** :
- Chemins absolus (`C:\...`, `/...`) refusés
- Chemins UNC (`\\server\...`) refusés
- Seuls les chemins relatifs autorisés

**Répertoire de sortie** :
- Environnement ComfyUI : Sous `ComfyUI/output/`
- Environnement de test : Sous le répertoire courant

---

### INPUT(path)

**Description** : Lit un fichier depuis le dossier de sortie ComfyUI (fonction symétrique de la fonction OUTPUT)

**Arguments** :
- path (str, requis) - Chemin relatif depuis le dossier de sortie ComfyUI
  - Chemins absolus (`C:\...`, `/...`) interdits
  - Chemins UNC (`\\server\...`) interdits
  - Seuls les chemins relatifs autorisés

**Retour** : Type dynamique (détection automatique selon le format de fichier)
- Fichiers texte (`.txt`, `.md`) → type str
- Nombre JSON → type float
- Tableau JSON → type list
- Fichiers image (`.png`, `.jpg`, `.jpeg`, `.bmp`, `.webp`) → type torch.Tensor (compatible ComfyUI)
- Autres → type bytes (binaire)

**Fonctionnalités** :
1. **Détection automatique de type** : Lecture avec le type optimal selon le format de fichier
2. **Support de données d'image** : Connexion directe possible aux nœuds d'image ComfyUI au format torch.Tensor
3. **Support JSON** : Analyse automatique des nombres et tableaux JSON
4. **Sécurité** : Refuse les chemins absolus/UNC (seuls les chemins relatifs autorisés)
5. **Gestion d'erreurs** : Retourne None avec avertissement PRINT si fichier introuvable

**Répertoire de lecture source** :
- Environnement ComfyUI : Sous `ComfyUI/output/`
- Environnement de test : Sous le répertoire courant

**Exemples** :
```vba
' Lecture de fichier texte
prompt = INPUT("prompts/positive.txt")
PRINT("Prompt lu: " & prompt)
RETURN1 = prompt

' Lecture de tableau JSON
dataArray = INPUT("data_array.json")
PRINT("Nombre d'éléments du tableau: " & (UBOUND(dataArray[]) + 1))

' Lecture d'image (format torch.Tensor)
refImage = INPUT("reference_images/style_sample.png")
' refImage peut se connecter directement au nœud d'entrée d'image ComfyUI

' Lecture depuis sous-répertoire
configText = INPUT("configs/model_settings.txt")
PRINT("Contenu de configuration: " & configText)
```

**Restrictions de sécurité** :
- Chemins absolus (`C:\...`, `/...`) refusés
- Chemins UNC (`\\server\...`) refusés
- Seuls les chemins relatifs autorisés

**Répertoire source de sortie** :
- Environnement ComfyUI : Sous `ComfyUI/output/`
- Environnement de test : Sous le répertoire courant

**Symétrie avec la fonction OUTPUT** :
- OUTPUT : Données → Sauvegarde de fichier
- INPUT : Lecture de fichier → Données
- Les deux fonctions n'autorisent que les chemins relatifs, refusent les chemins absolus/UNC

#### Coordination de la fonction INPUT et RELAY_OUTPUT

Pour transmettre l'image ou les données lues par la fonction INPUT au nœud suivant, utilisez la variable RELAY_OUTPUT.

```vba
' Lire le prompt depuis fichier texte, le transmettre au CLIPTextEncode suivant
PROMPT_TEXT = INPUT("prompts/positive.txt")
RELAY_OUTPUT = PROMPT_TEXT

' Ou lire un fichier image, le transmettre au LoadImage suivant
IMG1 = INPUT("reference_images/base.png")
RELAY_OUTPUT = IMG1
```

**RETURN1/RETURN2 vs RELAY_OUTPUT** :
- RETURN1/RETURN2 : Exclusif aux types primitifs (INT, FLOAT, STRING)
- RELAY_OUTPUT : Compatible type ANY (objets comme torch.Tensor, list, dict aussi possibles)

**Attention** :
- Si le fichier n'existe pas, affiche un message d'avertissement avec PRINT et retourne None
- La lecture de gros fichiers (images, etc.) peut prendre du temps

---

### ISFILEEXIST(path, [flg])

**Description** : Vérification d'existence de fichier dans le dossier de sortie ComfyUI et obtention d'informations étendues

**Arguments** :
- path (str, requis) - Chemin relatif depuis le dossier de sortie ComfyUI
  - Chemins absolus (`C:\...`, `/...`) interdits
  - Chemins UNC (`\\server\...`) interdits
  - Seuls les chemins relatifs autorisés
- flg (str, optionnel) - Drapeau d'option (par défaut : "")
  - `""` (par défaut) : Vérification d'existence seulement
  - `"NNNN"` : Recherche du chemin de fichier _NNNN avec numéro maximum
  - `"PIXEL"` : Obtention de la taille d'image (largeur/hauteur)
  - `"SIZE"` : Obtention de la taille de fichier (octets)

**Retour** : Type dynamique (change selon flg)
- **flg=""** : `"TRUE"` ou `"FALSE"` (type str)
- **flg="NNNN"** : Chemin de fichier avec numéro maximum (chemin relatif, type str), `"FALSE"` si inexistant
- **flg="PIXEL"** : Chaîne de tableau au format `"[width, height]"` (type str), `"FALSE"` si pas une image/inexistant
- **flg="SIZE"** : Taille de fichier en octets (type str), `"FALSE"` si inexistant

**Fonctionnalités** :
1. **Vérification d'existence** : Confirme la présence du fichier
2. **Recherche _NNNN** : Recherche le numéro maximum de fichiers numérotés (ex : `output_0003.png`)
3. **Obtention de taille d'image** : Obtient la résolution des fichiers image PNG/JPEG/WEBP, etc.
4. **Obtention de taille de fichier** : Obtient la taille de fichier en octets
5. **Sécurité** : Refuse les chemins absolus/UNC (seuls les chemins relatifs autorisés)

**Répertoire cible** :
- Environnement ComfyUI : Sous `ComfyUI/output/`
- Environnement de test : Sous le répertoire courant

**Exemples** :
```vba
' Vérification d'existence de base
exists = ISFILEEXIST("output.txt")
PRINT("exists = " & exists)
IF exists = "TRUE" THEN
    PRINT("Le fichier existe")
ELSE
    PRINT("Le fichier n'existe pas")
END IF

' Recherche du numéro maximum de fichier avec _NNNN
latestFile = ISFILEEXIST("ComfyUI_00001_.png", "NNNN")
PRINT("latestFile = " & latestFile)
IF latestFile <> "FALSE" THEN
    PRINT("Dernier fichier: " & latestFile)
    ' Ex : "ComfyUI_00005_.png"
ELSE
    PRINT("Aucun fichier correspondant")
END IF

' Obtention de taille d'image
imageSize = ISFILEEXIST("sample_image.png", "PIXEL")
PRINT("imageSize = " & imageSize)
IF imageSize <> "FALSE" THEN
    PRINT("Taille d'image: " & imageSize)
    ' Ex : "[512, 768]"
ELSE
    PRINT("N'est pas un fichier image")
END IF

' Obtention de taille de fichier
fileSize = ISFILEEXIST("data.txt", "SIZE")
PRINT("fileSize = " & fileSize)
IF fileSize <> "FALSE" THEN
    PRINT("Taille de fichier: " & fileSize & " octets")
ELSE
    PRINT("Fichier introuvable")
END IF
```

**Restrictions de sécurité** :
- Chemins absolus (`C:\...`, `/...`) refusés
- Chemins UNC (`\\server\...`) refusés
- Seuls les chemins relatifs autorisés

**Spécifications de la recherche _NNNN** :
- Motif de nom de fichier : format `{base}_{number}.{ext}`
- Numéro avec 4 chiffres zéro padding (ex : `_0001`, `_0002`)
- Retourne le chemin de fichier avec numéro maximum
- Retourne `"FALSE"` si aucun fichier correspondant

**Formats supportés pour l'obtention de taille d'image** :
- PNG, JPEG, JPG, BMP, WEBP
- Retourne `"FALSE"` si pas un fichier image

**Attention** :
- Toutes les valeurs de retour sont de type chaîne (str)
- Modes autres que vérification d'existence retournent aussi `"FALSE"` en cas d'erreur
- La taille d'image est une chaîne au format `"[width, height]"` (pas de type tableau)

---

### VRAMFREE([min_free_vram_gb])

**Description** : Fonction pour libérer VRAM et RAM. Exécute le déchargement de modèles, l'effacement de cache et la collecte des ordures.

**⚠️ AVERTISSEMENT** : Le déchargement de modèles est une opération délicate. Selon le timing d'exécution, il peut provoquer un comportement inattendu pendant l'exécution du workflow. Utilisez avec une attention suffisante.

**Syntaxe** :
```vba
result = VRAMFREE(min_free_vram_gb)
```

**Paramètres** :
- `min_free_vram_gb` (float, optionnel) : Seuil d'exécution (en GB)
  - Si la VRAM libre actuelle est égale ou supérieure à cette valeur, le traitement est ignoré
  - Par défaut : 0.0 (toujours exécuté)

**Retour** :
dict (informations détaillées du résultat d'exécution)
- `success` : Drapeau de succès d'exécution (bool)
- `message` : Message de résultat d'exécution (str)
- `freed_vram_gb` : Quantité de VRAM libérée (float)
- `freed_ram_gb` : Quantité de RAM libérée (float)
- `initial_status` : État de mémoire avant exécution (dict)
- `final_status` : État de mémoire après exécution (dict)
- `actions_performed` : Liste d'actions exécutées (list)

**Exemples d'utilisation** :
```vba
' Toujours exécuté (sans seuil)
result = VRAMFREE(0.0)
PRINT("VRAM libérée: " & result["freed_vram_gb"] & " GB")

' Exécuté seulement si VRAM libre < 2GB
result = VRAMFREE(2.0)
IF result["success"] = TRUE THEN
    PRINT("Nettoyage terminé")
ELSE
    PRINT("Échec du nettoyage")
END IF
```

**Contenu d'exécution** :
1. Obtention de l'état de mémoire initial
2. Vérification du seuil (jugement d'ignore)
3. Déchargement des modèles ComfyUI
4. Effacement du soft cache ComfyUI
5. Effacement du cache GPU PyTorch
6. Collecte des ordures Python (GC)
7. Paramétrage de drapeau vers prompt_queue ComfyUI
8. Surveillance du flush asynchrone (3 secondes)
9. Calcul de la quantité de mémoire libérée

**Précautions** :
- En dehors de l'environnement ComfyUI, les fonctionnalités disponibles sont limitées (mode limité)
- Dans les environnements non compatibles CUDA, les informations VRAM peuvent ne pas être obtenues
- En raison du traitement asynchrone, la mémoire peut être libérée avec un léger délai après la fin de l'exécution

---

### SLEEP([milliseconds])

**Description** : Suspend temporairement le traitement pendant les millisecondes spécifiées (sleep). Utilisé pour le contrôle de vitesse des boucles WHILE() et la synchronisation des traitements.

**Arguments** :
- milliseconds (FLOAT, optionnel) : Durée du sleep (millisecondes), par défaut : 10ms

**Retour** : Aucun (retourne 0.0 en interne)

**Syntaxe** :
```vba
SLEEP(milliseconds)
```

**Exemples d'utilisation** :
```vba
' Sleep par défaut de 10ms
SLEEP()

' Sleep de 0.5 seconde
SLEEP(500)

' Contrôle de vitesse de boucle WHILE() (réduction de l'utilisation CPU)
VAL1 = 0
WHILE VAL1 < 100
    VAL1 = VAL1 + 1
    SLEEP(100)  ' Attente de 100ms
WEND
PRINT("Boucle terminée: " & VAL1)
RETURN1 = VAL1

' Synchronisation des traitements
PRINT("Début du traitement")
result = VAL1 * 2
SLEEP(1000)  ' Attente de 1 seconde
PRINT("Traitement terminé: " & result)
RETURN1 = result
```

**Utilisations principales** :
1. **Contrôle de vitesse de boucle WHILE()** : Réduit l'utilisation CPU, allège la charge système
2. **Synchronisation des traitements** : Attente de réponse de systèmes externes, traitement de retard intentionnel
3. **Débogage** : Suspension temporaire pour observer le flux de traitement

**Intégration ComfyUI** :
- Fonctionne en coordination avec le contrôle de queuing basé thread de ComfyUI (ScriptExecutionQueue)
- Exécution de blocage synchrone par time.sleep()
- La sécurité lors de l'exécution simultanée de plusieurs nœuds EasyScripter est garantie par ScriptExecutionQueue

**Précautions** :
- SLEEP() bloque le thread actuel (les autres traitements ne s'exécutent pas)
- N'utilise pas de traitement asynchrone (asyncio) (ComfyUI n'est pas piloté par boucle d'événements)
- Les longs sleeps augmentent le temps d'exécution total du workflow

---

## Fonctions de traitement d'images

### IMAGETOBYTEARRAY(image_input, [max_size], [format], [return_format])

**Description** : Reçoit un IMAGE tensor ou un chemin de fichier image, le redimensionne/compresse et le convertit en tableau d'octets ou tableau JSON. Principalement utilisé comme données d'envoi pour les API REST.

**Arguments** :
- image_input (str | torch.Tensor, requis) - Source d'image
  - Chaîne : Chemin de fichier image (ex : `"C:/path/to/image.png"`)
  - torch.Tensor : Format IMAGE ComfyUI `[batch, height, width, channels]`
- max_size (int, optionnel) - Taille maximale après redimensionnement (côté long, pixels), par défaut : 336
- format (str, optionnel) - Format d'image de sortie ("PNG", "JPEG", etc.), par défaut : "PNG"
- return_format (str, optionnel) - Format de retour ("bytes" ou "json"), par défaut : "bytes"

**Retour** : Type dynamique (change selon return_format)
- **return_format="bytes"** : type bytes (données binaires brutes)
- **return_format="json"** : type str (chaîne au format tableau JSON, ex : `"[137, 80, 78, 71, ...]"`)

**Fonctionnalités** :
1. **Support IMAGE tensor** : Peut recevoir directement le type IMAGE depuis les nœuds ComfyUI
2. **Support chemin de fichier** : Spécification de chemin de fichier image conventionnelle également possible
3. **Redimensionnement automatique** : Redimensionne à la taille spécifiée en conservant le rapport d'aspect
4. **Compression JPEG** : Lors de la spécification format="JPEG", compression avec quality=50 (réduction de taille de fichier)
5. **Conversion RGBA→RGB** : Lors de la sortie JPEG, conversion automatique du fond transparent en fond blanc
6. **Conversion tableau JSON** : Format de tableau d'entiers directement utilisable dans Cloudflare API, etc.

**Spécifications d'encodage** :
- Pas Base64
- Pas d'encodage MIME
- return_format="bytes" : Retourne les données binaires brutes en type bytes
- return_format="json" : Retourne une chaîne JSON de tableau d'entiers [0-255]
- Dans Cloudflare API, le format de tableau JSON peut être utilisé directement

**Exemples** :
```vba
' Entrée de chemin de fichier (méthode conventionnelle)
json_array = IMAGETOBYTEARRAY("C:/path/to/image.png", 336, "JPEG", "json")
PRINT("Longueur du tableau JSON: " & LEN(json_array))

' Entrée IMAGE tensor (depuis connexion de nœud ComfyUI)
' Le type IMAGE est passé à VAL1 depuis LoadImage node, etc.
json_array = IMAGETOBYTEARRAY(VAL1, 336, "JPEG", "json")
RETURN1 = json_array

' Exemple d'envoi à Cloudflare Workers AI Image-to-Text API
```

**Restrictions de sécurité** :
Aucune (FileNotFoundError si fichier inexistant lors de spécification de chemin)

**Gestion d'erreurs** :
- FileNotFoundError : Fichier image inexistant (lors d'entrée de chaîne)
- RuntimeError : PIL (Pillow) non installé, erreur de traitement d'image
- ValueError : return_format invalide, ou taille d'image incorrecte
- TypeError : Type d'entrée invalide (autre que str/torch.Tensor)

**Précautions** :
- La bibliothèque PIL (Pillow) est nécessaire (`pip install Pillow`)
- Pour manipuler torch.Tensor, PyTorch est nécessaire (généralement déjà installé dans l'environnement ComfyUI)
- Le format JPEG est compressé avec quality=50, priorité à la taille de fichier plutôt qu'à la qualité
- La conversion JSON de grandes images (4K, etc.) sans redimensionnement peut rendre la chaîne JSON énorme

---

### IMAGETOBASE64(image_input, [max_size], [format], [return_format])

**Description** : Reçoit un IMAGE tensor ou un chemin de fichier image, le redimensionne/compresse et le convertit en encodage Base64 ou format data URL. Principalement utilisé comme données d'envoi pour les API REST.

**Arguments** :
- image_input (str | torch.Tensor, requis) - Source d'image
  - Chaîne : Chemin de fichier image (ex : `"C:/path/to/image.png"`)
  - torch.Tensor : Format IMAGE ComfyUI `[batch, height, width, channels]`
- max_size (int, optionnel) - Taille maximale après redimensionnement (côté long, pixels), par défaut : 512
- format (str, optionnel) - Format d'image de sortie ("PNG", "JPEG", etc.), par défaut : "PNG"
- return_format (str, optionnel) - Format de retour ("base64" ou "data_url"), par défaut : "base64"

**Retour** : type str (change selon return_format)
- **return_format="base64"** : Chaîne encodée Base64 (ex : `"iVBORw0KGgoAAAANSUhEUgAA..."`)
- **return_format="data_url"** : Chaîne au format data URL (ex : `"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."`)

**Fonctionnalités** :
1. **Support IMAGE tensor** : Peut recevoir directement le type IMAGE depuis les nœuds ComfyUI
2. **Support chemin de fichier** : Spécification de chemin de fichier image conventionnelle également possible
3. **Redimensionnement automatique** : Redimensionne à la taille spécifiée en conservant le rapport d'aspect
4. **Compression JPEG** : Lors de la spécification format="JPEG", compression avec quality=85 (équilibre qualité et taille)
5. **Conversion RGBA→RGB** : Lors de la sortie JPEG, conversion automatique du fond transparent en fond blanc
6. **Encodage Base64** : Encodage Base64 standard, support également du format data URL

**Spécifications d'encodage** :
- Encodage standard Base64
- return_format="base64" : Retourne uniquement la chaîne Base64
- return_format="data_url" : Retourne au format data URL (`"data:image/png;base64,..."`)
- Directement utilisable dans Vision API

**Exemples** :
```vba
' Entrée de chemin de fichier (chaîne Base64)
base64_str = IMAGETOBASE64("C:/path/to/image.png", 512, "PNG", "base64")
PRINT("Longueur Base64: " & LEN(base64_str))

' Entrée IMAGE tensor (format data URL)
' Le type IMAGE est passé à ANY_INPUT depuis LoadImage node, etc.
data_url = IMAGETOBASE64(ANY_INPUT, 512, "PNG", "data_url")
RETURN1 = data_url
```

**Restrictions de sécurité** :
Aucune (FileNotFoundError si fichier inexistant lors de spécification de chemin)

**Gestion d'erreurs** :
- FileNotFoundError : Fichier image inexistant (lors d'entrée de chaîne)
- RuntimeError : PIL (Pillow) non installé, erreur de traitement d'image
- ValueError : return_format invalide, ou taille d'image incorrecte
- TypeError : Type d'entrée invalide (autre que str/torch.Tensor)

**Précautions** :
- La bibliothèque PIL (Pillow) est nécessaire (`pip install Pillow`)
- Pour manipuler torch.Tensor, PyTorch est nécessaire (généralement déjà installé dans l'environnement ComfyUI)
- Le format JPEG est compressé avec quality=85 (équilibre haute qualité et taille de fichier)
- La conversion Base64 de grandes images (4K, etc.) sans redimensionnement peut rendre la chaîne énorme
- Le format data URL inclut toutes les données d'image dans la chaîne, donc le corps JSON devient volumineux

---

## Fonctions d'obtention de données Image/Latent

### GETANYWIDTH([any_data])

**Description** : Obtient la largeur (nombre de pixels) de données de type IMAGE/LATENT

**Arguments** :
- any_data (torch.Tensor, optionnel) - Données IMAGE/LATENT
  - Sans argument, utilise automatiquement les données du socket d'entrée any_input

**Retour** : float - Largeur (nombre de pixels, 0.0 si impossible d'obtenir)

**Formats supportés** :
- Type IMAGE : format torch.Tensor `[batch, height, width, channels]`
- Type LATENT : format torch.Tensor `[batch, channels, height, width]`

**Exemples** :
```vba
' Obtention automatique depuis le socket d'entrée any_input
width = GETANYWIDTH()
PRINT("Largeur: " & width)
RETURN1 = width

' Spécifier explicitement les données
imageData = INPUT("sample.png")
w = GETANYWIDTH(imageData)
PRINT("Largeur d'image: " & w)
```

---

### GETANYHEIGHT([any_data])

**Description** : Obtient la hauteur (nombre de pixels) de données de type IMAGE/LATENT

**Arguments** :
- any_data (torch.Tensor, optionnel) - Données IMAGE/LATENT
  - Sans argument, utilise automatiquement les données du socket d'entrée any_input

**Retour** : float - Hauteur (nombre de pixels, 0.0 si impossible d'obtenir)

**Formats supportés** :
- Type IMAGE : format torch.Tensor `[batch, height, width, channels]`
- Type LATENT : format torch.Tensor `[batch, channels, height, width]`

**Exemples** :
```vba
' Obtention automatique depuis le socket d'entrée any_input
height = GETANYHEIGHT()
PRINT("Hauteur: " & height)
RETURN2 = height

' Branchement conditionnel selon la résolution
w = GETANYWIDTH()
h = GETANYHEIGHT()
IF w >= 1024 AND h >= 1024 THEN
    PRINT("Image haute résolution")
    scale = 1.0
ELSE
    PRINT("Image résolution standard")
    scale = 2.0
END IF
RETURN1 = scale
```

---

### GETANYTYPE([any_data])

**Description** : Juge le nom de type de données de type ANY

**Arguments** :
- any_data (Any, optionnel) - Données cibles de jugement de type
  - Sans argument, utilise automatiquement les données du socket d'entrée any_input

**Retour** : str - Nom de type
- "int", "float", "string" - Types de base
- "image", "latent" - Image/Latent
- "model", "vae", "clip" - Types de modèles ComfyUI
- "conditioning", "control_net", "clip_vision", "style_model", "gligen", "lora" - Types spécifiques ComfyUI
- "none" - Valeur None
- "unknown" - Impossible de juger

**Exemples** :
```vba
' Jugement automatique depuis le socket d'entrée any_input
type_name = GETANYTYPE()
PRINT("Type: " & type_name)

SELECT CASE type_name
    CASE "image"
        w = GETANYWIDTH()
        h = GETANYHEIGHT()
        PRINT("Type IMAGE: " & w & "x" & h)
    CASE "latent"
        PRINT("Type LATENT")
    CASE "model"
        PRINT("Type MODEL")
    CASE "string"
        PRINT("Type STRING")
    CASE ELSE
        PRINT("Autre type: " & type_name)
END SELECT
```

---

### GETANYVALUEINT([any_data])

**Description** : Obtient une valeur entière depuis des données de type ANY

**Arguments** :
- any_data (Any, optionnel) - Données
  - Sans argument, utilise automatiquement les données du socket d'entrée any_input

**Retour** : int - Valeur entière (0 si impossible d'obtenir)

**Exemples** :
```vba
' Obtention de valeur entière depuis le socket d'entrée any_input
int_value = GETANYVALUEINT()
PRINT("Valeur entière: " & int_value)
RETURN1 = int_value
```

---

### GETANYVALUEFLOAT([any_data])

**Description** : Obtient une valeur à virgule flottante depuis des données de type ANY

**Arguments** :
- any_data (Any, optionnel) - Données
  - Sans argument, utilise automatiquement les données du socket d'entrée any_input

**Retour** : float - Valeur à virgule flottante (0.0 si impossible d'obtenir)

**Exemples** :
```vba
' Obtention de valeur à virgule flottante depuis le socket d'entrée any_input
float_value = GETANYVALUEFLOAT()
PRINT("Valeur à virgule flottante: " & float_value)
RETURN1 = float_value
```

---

### GETANYSTRING([any_data])

**Description** : Obtient une chaîne depuis des données de type ANY

**Arguments** :
- any_data (Any, optionnel) - Données
  - Sans argument, utilise automatiquement les données du socket d'entrée any_input

**Retour** : str - Chaîne (chaîne vide si impossible d'obtenir)

**Exemples** :
```vba
' Obtention de chaîne depuis le socket d'entrée any_input
str_value = GETANYSTRING()
PRINT("Chaîne: " & str_value)
RETURN1 = str_value
```

---

## Fonctions de jugement de type

### ISNUMERIC(value)

**Description** : Juge si la valeur est numérique

**Arguments** :
- value - Valeur à examiner

**Retour** : 1 (numérique) ou 0 (non numérique)

**Exemples** :
```vba
result = ISNUMERIC("123")      ' 1
PRINT("ISNUMERIC('123') = " & result)
result = ISNUMERIC("12.34")    ' 1
PRINT("ISNUMERIC('12.34') = " & result)
result = ISNUMERIC("abc")      ' 0
PRINT("ISNUMERIC('abc') = " & result)
result = ISNUMERIC("")         ' 0
PRINT("ISNUMERIC('') = " & result)

' Exemple pratique : Validation de valeur d'entrée
IF ISNUMERIC(TXT1) THEN
    value = CDBL(TXT1)
    PRINT("Traité comme nombre: " & value)
ELSE
    PRINT("Erreur: Pas un nombre")
END IF
```

---

### ISDATE(value)

**Description** : Juge si analysable comme date

**Arguments** :
- value - Valeur à examiner

**Retour** : 1 (date) ou 0 (non date)

**Exemples** :
```vba
result = ISDATE("2024-01-15")     ' 1
PRINT("ISDATE('2024-01-15') = " & result)
result = ISDATE("2024/01/15")     ' 1
PRINT("ISDATE('2024/01/15') = " & result)
result = ISDATE("15:30:00")       ' 1 (l'heure peut aussi être jugée)
PRINT("ISDATE('15:30:00') = " & result)
result = ISDATE("hello")          ' 0
PRINT("ISDATE('hello') = " & result)

' Exemple pratique : Validation de date
IF ISDATE(TXT1) THEN
    dateVal = DATEVALUE(TXT1)
    PRINT("Traité comme date: " & dateVal)
ELSE
    PRINT("Erreur: Pas un format de date")
END IF
```

**Formats supportés** :
- `YYYY/MM/DD HH:MM:SS`
- `YYYY/MM/DD`
- `YYYY-MM-DD HH:MM:SS`
- `YYYY-MM-DD`
- `MM/DD/YYYY`
- `DD/MM/YYYY`
- `HH:MM:SS`
- `HH:MM`

---

### ISARRAY(variable_name)

**Description** : Juge si la variable est un tableau

**Arguments** :
- variable_name - Nom de variable (chaîne) ou référence de variable de tableau (notation ARR[])

**Retour** : 1 (tableau) ou 0 (non tableau)

**Exemples** :
```vba
REDIM arr, 10
result = ISARRAY(arr[])      ' 1 (référence de tableau)
PRINT("ISARRAY(arr[]) = " & result)
result = ISARRAY("arr")      ' 1 (chaîne de nom de tableau)
PRINT("ISARRAY('arr') = " & result)
result = ISARRAY("VAL1")     ' 0 (variable ordinaire)
PRINT("ISARRAY('VAL1') = " & result)

' Exemple pratique : Vérification de type de variable
REDIM myData, 5
myData[0] = "a"
myData[1] = "b"
IF ISARRAY(myData[]) THEN
    PRINT("C'est un tableau. Nombre d'éléments: " & (UBOUND(myData[]) + 1))
ELSE
    PRINT("Ce n'est pas un tableau")
END IF
```

**Attention** :
- Passez le nom du tableau comme chaîne ou passez une référence de variable de tableau avec la notation ARR[]

---

### TYPE(value)

**Description** : Retourne le type de variable comme chaîne

**Arguments** :
- value - Valeur dont on veut connaître le type

**Retour** : Nom de type ("NUMBER", "STRING", "BOOLEAN", "ARRAY", "NULL", "OBJECT")

**Exemples** :
```vba
typeName = TYPE(123)           ' "NUMBER"
PRINT("TYPE(123) = " & typeName)
typeName = TYPE("hello")       ' "STRING"
PRINT("TYPE('hello') = " & typeName)
typeName = TYPE(1 > 0)         ' "NUMBER"
PRINT("TYPE(1 > 0) = " & typeName)

REDIM arr, 5
typeName = TYPE(arr[])         ' "OBJECT"
PRINT("TYPE(arr[]) = " & typeName)

' Exemple pratique : Traitement de type générique
myValue = VAL1
dataType = TYPE(myValue)
PRINT("TYPE(myValue) = " & dataType)
SELECT CASE dataType
    CASE "NUMBER"
        PRINT("Nombre: " & myValue)
    CASE "STRING"
        PRINT("Chaîne: " & myValue)
    CASE "ARRAY"
        PRINT("Tableau (nombre d'éléments: " & (UBOUND(myValue[]) + 1) & ")")
    CASE "NULL"
        PRINT("Pas de valeur")
END SELECT
```

---

## Exemples pratiques

### Utilisation de la sortie de débogage

```vba
' Vérifier les valeurs à chaque étape du traitement
originalValue = VAL1
PRINT("Valeur originale: " & originalValue)

processedValue = originalValue * 2
PRINT("Après multiplication par 2: " & processedValue)

finalValue = processedValue + 10
PRINT("Valeur finale: " & finalValue)

RETURN1 = finalValue
PRINT("Affecté à RETURN1: " & RETURN1)
```

### Validation de valeur d'entrée

```vba
' Vérifier si numérique avant traitement
IF ISNUMERIC(TXT1) THEN
    number = CDBL(TXT1)
    PRINT("TXT1 converti en nombre: " & number)
    result = number * VAL1
    PRINT("Résultat du calcul: " & result)
    RETURN1 = result
    PRINT("Affecté à RETURN1: " & RETURN1)
ELSE
    PRINT("Erreur: TXT1 n'est pas un nombre")
    RETURN1 = 0
    PRINT("Valeur par défaut affectée à RETURN1: " & RETURN1)
END IF
```

### Branchement de traitement selon le type

```vba
' Changer le traitement selon le type de données
myData = VAL1
dataType = TYPE(myData)
PRINT("TYPE(myData) = " & dataType)

IF dataType = "NUMBER" THEN
    result = myData * 2
    PRINT("Traitement numérique: " & result)
ELSEIF dataType = "STRING" THEN
    result = UCASE(myData)
    PRINT("Traitement de chaîne: " & result)
ELSEIF dataType = "ARRAY" THEN
    count = UBOUND(myData[]) + 1
    PRINT("Traitement de tableau: nombre d'éléments=" & count)
    FOR i = 0 TO UBOUND(myData[])
        PRINT("  [" & i & "] = " & myData[i])
    NEXT
ELSE
    PRINT("Type non supporté: " & dataType)
END IF
```

---

[← Retour à l'index des fonctions intégrées](00_index.md)
