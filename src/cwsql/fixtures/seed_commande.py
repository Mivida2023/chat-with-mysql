import psycopg2
from faker import Faker
import random
from cwsql.db.db_connect import connect_to_db

fake = Faker('fr_FR')

conn = connect_to_db()

cur = conn.cursor()

for contact_id in range(1, 3001):  # Assumant 3000 contacts
    for _ in range(random.randint(2, 5)):  # Entre 2 et 5 commandes par contact
        prix = round(random.uniform(100, 2000), 2)
        date_debut = fake.date_between(start_date='-1y', end_date='today')
        date_fin = fake.date_between(start_date=date_debut, end_date='+30d')
        duree = (date_fin - date_debut).days
        pays = fake.country()
        nombre_passagers = random.randint(1, 5)
        cur.execute(
            "INSERT INTO commande (contact_id, prix, date_debut, date_fin, duree, pays, nombre_passagers) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (contact_id, prix, date_debut, date_fin, duree, pays, nombre_passagers)
        )

conn.commit()
cur.close()
conn.close()