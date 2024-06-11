from PIL import Image

nom_image = "file_name"

chemin_image = "directory file"
image = Image.open(chemin_image + nom_image + ".bmp")

# Obtenir les dimensions de l'image
largeur, hauteur = image.size

def rgb_to_rgb565(r, g, b):
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

# Ouvrir un fichier en écriture pour stocker les instructions
with open(nom_image + ".txt", "w") as fichier:
    # Parcourir chaque ligne de l'image
    for y in range(hauteur):
        x_start = 0
        couleur_start = image.getpixel((0, y))

        # Si l'image est en niveaux de gris, convertir la couleur en RGB
        if isinstance(couleur_start, int):
            couleur_start = (couleur_start, couleur_start, couleur_start)

        rouge_start, vert_start, bleu_start = couleur_start
        couleur_hex_start = rgb_to_rgb565(rouge_start, vert_start, bleu_start)

        for x in range(1, largeur):
            couleur = image.getpixel((x, y))

            # Si l'image est en niveaux de gris, convertir la couleur en RGB
            if isinstance(couleur, int):
                couleur = (couleur, couleur, couleur)

            rouge, vert, bleu = couleur
            couleur_hex = rgb_to_rgb565(rouge, vert, bleu)

            # Si la couleur change, écrire l'instruction drawLine ou drawPixel
            if couleur_hex != couleur_hex_start:
                if couleur_hex_start != 0x0000:  # Ignorer les lignes noires
                    if x_start == x - 1:
                        fichier.write(f"tft.drawPixel(_x + {x_start}, _y + {y}, 0x{couleur_hex_start:04X});\n")
                    else:
                        fichier.write(f"tft.drawLine(_x + {x_start}, _y + {y}, _x + {x - 1}, _y + {y}, 0x{couleur_hex_start:04X});\n")
                x_start = x
                couleur_hex_start = couleur_hex
                rouge_start, vert_start, bleu_start = rouge, vert, bleu

        # Écrire la dernière ligne de la rangée si elle n'est pas noire
        if couleur_hex_start != 0x0000:  # Ignorer les lignes noires
            if x_start == largeur - 1:
                fichier.write(f"tft.drawPixel(_x + {x_start}, _y + {y}, 0x{couleur_hex_start:04X});\n")
            else:
                fichier.write(f"tft.drawLine(_x + {x_start}, _y + {y}, _x + {largeur - 1}, _y + {y}, 0x{couleur_hex_start:04X});\n")

print("Le fichier output.txt a été généré avec succès.")
