from cwsql.db.db_connect import connect_to_db

# Établir la connexion à la base de données
conn = connect_to_db(dbname='postgres', set_autocommit=True)
cur = conn.cursor()

# Suppression de la base de données si elle existe déjà, puis création
cur.execute(f"DROP DATABASE IF EXISTS bcu;")
cur.execute(f"CREATE DATABASE bcu;")

# Fermeture de la connexion initiale
cur.close()
conn.close()

conn = connect_to_db()
cur = conn.cursor()

# Création des tables
cur.execute("""
    CREATE TABLE contact (
        id SERIAL PRIMARY KEY,
        nom VARCHAR(255),
        prenom VARCHAR(255),
        date_anniversaire DATE,
        telephone VARCHAR(20),
        adresse VARCHAR(255),
        profession VARCHAR(100),
        age INT,
        sexe CHAR(1)
    );
""")

cur.execute("""
    CREATE TABLE commande (
        id SERIAL PRIMARY KEY,
        contact_id INT,
        prix DECIMAL(10, 2),
        date_debut DATE,
        date_fin DATE,
        duree INT,
        pays VARCHAR(255),
        nombre_passagers INT,
        FOREIGN KEY (contact_id) REFERENCES contact(id)
    );
""")

cur.execute("""
    CREATE TABLE avis_voyageur (
        id SERIAL PRIMARY KEY,
        commande_id INT,
        contact_id INT,
        avis TEXT,
        note INT,
        date_avis DATE,
        FOREIGN KEY (commande_id) REFERENCES commande(id),
        FOREIGN KEY (contact_id) REFERENCES contact(id)
    );
""")

# Valider les changements
conn.commit()

# Fermeture de la connexion
cur.close()
conn.close()

print("La base de données a été créée et initialisée avec succès.")
