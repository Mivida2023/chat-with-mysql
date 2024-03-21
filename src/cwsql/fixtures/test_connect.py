from cwsql.db.db_connect import connect_to_db


# Établir la connexion à la base de données
conn = connect_to_db()


#remplace le code ci-dessous

# import psycopg2

# try:
#     # Remplacez 'ma_base_de_donnees', 'postgres', et 'votre_mot_de_passe' par vos informations
#     conn = psycopg2.connect(s
#         dbname='bcu',
#         user='francois',
#         password='240365',
#         host='localhost'
#     )
#     print("Connexion établie à la base de données")
#     # Vous pouvez ajouter votre code ici pour interagir avec la base de données
    
# except psycopg2.Error as e:
#     print("Erreur lors de la connexion à la base de données : ", e)
# finally:
#     if conn is not None:
#         conn.close()
