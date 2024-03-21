import subprocess

# Liste des scripts à exécuter dans l'ordre
scripts = [
    'db_create_bcu.py',
    'seed_contact.py',
    'seed_commande.py',
    'seed_avis.py'
]

# Répertoire où se trouvent vos scripts
script_directory = 'src/cwsql/fixtures'

for script in scripts:
    script_path = f"{script_directory}/{script}"
    try:
        # Exécuter chaque script
        print(f"Exécution du script : {script}")
        subprocess.run(['python', script_path], check=True)
        print(f"Script {script} exécuté avec succès.\n")
    except subprocess.CalledProcessError:
        print(f"Échec de l'exécution du script : {script}")
        break  # Arrête d'exécuter les scripts suivants si l'un échoue
