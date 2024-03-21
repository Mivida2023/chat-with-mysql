import psycopg2
from faker import Faker
from cwsql.db.db_connect import connect_to_db


fake = Faker('fr_FR')

conn = connect_to_db()

cur = conn.cursor()

for _ in range(3000):
    nom = fake.last_name()
    prenom = fake.first_name()
    date_anniversaire = fake.date_of_birth(minimum_age=18, maximum_age=80)
    telephone = fake.phone_number()[:20]
    adresse = fake.address().replace('\n', ', ')[:255]
    profession = fake.job()[:100]
    age = fake.random_int(min=18, max=80)
    sexe = fake.random_element(elements=('M', 'F', 'A'))
    cur.execute(
        "INSERT INTO contact (nom, prenom, date_anniversaire, telephone, adresse, profession, age, sexe) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (nom, prenom, date_anniversaire, telephone, adresse, profession, age, sexe)
    )

conn.commit()
cur.close()
conn.close()
