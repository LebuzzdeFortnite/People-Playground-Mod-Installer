import subprocess
import os
import shutil
from zipfile import ZipFile
import importlib
import time

libs = ["os", "subprocess", "shutil", "zipfile", "importlib", "time"]

for lib in libs:
    try:
        importlib.import_module(lib)
        print(f"Library {lib} ✅ OK")
    except ImportError:
        print(f"Library {lib} ❌ Non installé")
    time.sleep(0.5)

liste_games = {
    "People Playground": "1118200",
    "transport fever 2": "1066780",
    "project zomboid": "108600",
}

print("Jeux disponibles :")
for i, game in enumerate(liste_games.keys(), 1):
    print(f"{i}. {game}")

#Demande les emplacelent des apps
id_jeux = list(liste_games.values())[int(input("Entrer le numéro du jeu pour lequel vous voulez installer un mod : ")) - 1]
path_steamcmd = input("Entrer l'emplacement de l'executable de steamCMD, si vous n'avez pas steamCMD, metter rien pour le telecharger automatiquement : ")
path_People_Playground = input("Entrer le path du dossier mod du jeu sélectionné : ")

if path_steamcmd == "":
    os.system("curl https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip -o steamcmd.zip")
    with ZipFile("steamcmd.zip", 'r') as zip: 
        # extraire tous les fichiers vers un autre répertoire
        zip.extractall("steamcmd")
        path_steamcmd = "steamcmd\steamcmd.exe"

print (f"L'executable de steamCMD est : {path_steamcmd}")
print (f"L'emplacement du dossier mod de people playground est : {path_People_Playground}")

id_workshop = input("Entrer l'id du mod (fin de l'url apres id=xxxxx) : ")

steamcmd_dir = os.path.dirname(path_steamcmd)

print (f"Le dir de steamcmd est : {steamcmd_dir}")

#Se connecte et installe le mod
command_steamcmd = [
    "login anonymous",
    f"workshop_download_item {id_jeux} {id_workshop}",
    "quit"
]

#Prepare le lancement de steamcmd
steamcmd_arg = [path_steamcmd] + [f"+{cmd}" for cmd in command_steamcmd]

#lance steamcmd avec les argument obligatoire
subprocess.run(steamcmd_arg)

mod_path = os.path.join(steamcmd_dir, "steamapps", "workshop", "content", id_jeux, id_workshop)

print (f"mod telecharge dans : {mod_path}")

dest_path = os.path.join(path_People_Playground, id_workshop)

if os.path.exists(mod_path):
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)  # supprime ancienne version du mod
    shutil.copytree(mod_path, dest_path)
    print(f"✅ Mod {id_workshop} installé !")
else:
    print("❌ Erreur : mod non trouvé après téléchargement.")