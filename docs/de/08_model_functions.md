# Modellfunktionen-Referenz

[← Zurück zum Index der integrierten Funktionen](00_index.md)

## Übersicht

Modellfunktionen bieten die Möglichkeit, die optimale Auflösung für verschiedene in ComfyUI verwendete Generierungsmodelle automatisch zu bestimmen. Sie berechnet automatisch die optimale Latent-Raumgröße für dieses Modell basierend auf Modellname und Seitenverhältnis.

Unterstützte Modelle: Stable Diffusion 1.5/2.1/XL, SD3/3.5, FLUX.1, Hunyuan-DiT, Kandinsky, PixArt, Playground etc. (über 30 Arten)

---

## Modellfunktionsliste

### OPTIMAL_LATENT(model_hint, width, height)

**Beschreibung**: Automatische Bestimmung der optimalen Latent-Größe aus Modellname und Seitenverhältnis

**Argumente**:
- model_hint - Modellname-Hinweis (Zeichenkette)
  - Beispiele: "SDXL", "SD 1.5", "Flux", "Hunyuan"
- width - Gewünschte Breite (Ganzzahl)
- height - Gewünschte Höhe (Ganzzahl)

**Rückgabewert**: Array der optimalen Latent-Größe [width, height]

**Unterstützte Modelle**: SD1.5, SD2.1, SDXL, SD3/3.5, Hunyuan-DiT, FLUX.1, Kandinsky, PixArt, Playground etc. (30+ Modelle)

**Beispiele**:
```vba
' Optimale 4:3-Auflösung für SDXL abrufen
DIM result
result = OPTIMAL_LATENT("SDXL", 4, 3)
PRINT(result)  ' Zwischenergebnis bestätigen
PRINT("Optimal Size: " & result(0) & "x" & result(1))
' Ausgabe: "Model: SDXL 1.0 (base) | Optimal: 1152x896 (4:3)"
' Ausgabe: "{0: 1152, 1: 896}"
' Ausgabe: "Optimal Size: 1152x896"

' 16:9 für Stable Diffusion 1.5 abrufen
result = OPTIMAL_LATENT("SD 1.5", 16, 9)
PRINT(result)  ' Zwischenergebnis bestätigen
PRINT(result(0) & "x" & result(1))
' Ausgabe: "Model: blue_pencil(SD1.5) | Optimal: 704x384 (11:6)"
' Ausgabe: "{0: 704, 1: 384}"
' Ausgabe: "704x384"

' Quadratisch für FLUX.1
result = OPTIMAL_LATENT("Flux", 256, 256)
PRINT(result)  ' Zwischenergebnis bestätigen
' Ausgabe: "Model: FLUX.1 (dev/pro) | Optimal: 1024x1024 (1:1)"
' Ausgabe: "{0: 1024, 1: 1024}"
```

---

## Aktualisierung der Modelldaten

Um neue Modelle hinzuzufügen, bearbeiten Sie `data/model_resolutions.csv`.

**CSV-Format**:
```csv
model_key,model_display_name,aliases,version,width,height,aspect_ratio,description
new_model,New Model v1.0,newmodel|new,1.0,1024,1024,1:1,Beschreibung
```

**Hinweis**: Neue Daten werden nach Neustart von ComfyUI wirksam.

---

## Verwendungsbeispiele

### Optimale Auflösungsbestimmung im SDXL-Workflow

```vba
' Automatische Berechnung der optimalen Auflösung für SDXL aus Benutzereingabe-Auflösung
DIM user_width
DIM user_height
user_width = 1920  ' Full HD-Breite
PRINT(user_width)  ' Zwischenergebnis bestätigen
' Ausgabe: "1920"
user_height = 1080 ' Full HD-Höhe
PRINT(user_height)  ' Zwischenergebnis bestätigen
' Ausgabe: "1080"

DIM optimal
optimal = OPTIMAL_LATENT("SDXL", user_width, user_height)
PRINT(optimal)  ' Zwischenergebnis bestätigen
' Ausgabe: "Model: SDXL 1.0 (base) | Optimal: 1344x768 (16:9)"
' Ausgabe: "{0: 1344, 1: 768}"

' Optimale Breite und Höhe aus optimal-Array abrufen
DIM final_width
DIM final_height
final_width = optimal(0)
PRINT(final_width)  ' Zwischenergebnis bestätigen
' Ausgabe: "1344"
final_height = optimal(1)
PRINT(final_height)  ' Zwischenergebnis bestätigen
' Ausgabe: "768"

PRINT("Input: " & user_width & "x" & user_height)
PRINT("SDXL Optimal: " & final_width & "x" & final_height)
' Ausgabe: "Input: 1920x1080"
' Ausgabe: "SDXL Optimal: 1344x768"
```

### Universalskript für mehrere Modelle

```vba
' Optimale Auflösung für jedes Modell durch einfache Änderung des Modellnamens abrufen
DIM model_name
DIM aspect_width
DIM aspect_height

model_name = "Flux"
PRINT(model_name)  ' Zwischenergebnis bestätigen
' Ausgabe: "Flux"
aspect_width = 1024
PRINT(aspect_width)  ' Zwischenergebnis bestätigen
' Ausgabe: "1024"
aspect_height = 1024
PRINT(aspect_height)  ' Zwischenergebnis bestätigen
' Ausgabe: "1024"

DIM result
result = OPTIMAL_LATENT(model_name, aspect_width, aspect_height)
PRINT(result)  ' Zwischenergebnis bestätigen
' Ausgabe: "Model: FLUX.1 (dev/pro) | Optimal: 1024x1024 (1:1)"
' Ausgabe: "{0: 1024, 1: 1024}"
PRINT(model_name & " -> " & result(0) & "x" & result(1))
' Ausgabe: "Flux -> 1024x1024"

' Auf SD1.5 ändern
model_name = "SD 1.5"
PRINT(model_name)  ' Zwischenergebnis bestätigen
' Ausgabe: "SD 1.5"
result = OPTIMAL_LATENT(model_name, aspect_width, aspect_height)
PRINT(result)  ' Zwischenergebnis bestätigen
' Ausgabe: "Model: blue_pencil(SD1.5) | Optimal: 512x512 (1:1)"
' Ausgabe: "{0: 512, 1: 512}"
PRINT(model_name & " -> " & result(0) & "x" & result(1))
' Ausgabe: "SD 1.5 -> 512x512"
```

---

[← Zurück zum Index der integrierten Funktionen](00_index.md)
