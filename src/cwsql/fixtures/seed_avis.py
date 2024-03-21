from faker import Faker
import random
from cwsql.db.db_connect import connect_to_db

fake = Faker('fr_FR')

conn = connect_to_db()
cur = conn.cursor()

# Liste des avis prédéfinis
avis_et_notes = [
    ("Incroyable voyage, service impeccable ! Je recommande à tous.", 5),
    ("Plutôt déçu de l'hôtel, mais les paysages étaient magnifiques.", 3),
    ("Expérience inoubliable, je reviendrai !", 5),
    ("Service médiocre, je ne recommande pas.", 2),
    ("Voyage de rêve, tout était parfait du début à la fin.", 5),
    ("Nourriture décevante, mais guides très compétents.", 3),
    ("Magnifique séjour, mais un peu trop court à mon goût.", 4),
    ("Pire expérience de ma vie, je suis outré !", 1),
    ("Très bon rapport qualité-prix, vacances réussies.", 4),
    ("Des vacances reposantes, exactement ce dont j'avais besoin.", 5),
    ("Guide désagréable, mais paysages à couper le souffle.", 2),
    ("Voyage moyen, beaucoup de retard dans les transports.", 3),
    ("Je n'ai jamais autant ri, guide très drôle !", 5),
    ("Très déçu, rien n'était comme prévu.", 2),
    ("Fantastique ! J'ai adoré chaque minute.", 5),
    ("Pourquoi le guide ne connaissait-il pas la région ? Inacceptable.", 1),
    ("Hôtel de luxe à un prix abordable, quelle trouvaille !", 5),
    ("Repas sublimes, j'ai découvert de nouvelles saveurs.", 4),
    ("Je me suis ennuyé, pas assez d'activités proposées.", 2),
    ("Incroyable expérience sous-marine, plongée top !", 5),
    ("Accueil froid, on ne m'y reprendra plus.", 2),
    ("Voyage organisé au millimètre, chapeau !", 5),
    ("Je m'attendais à mieux vu le prix payé.", 3),
    ("Charmant petit hôtel, personnel très accueillant.", 4),
    ("Le vol était inconfortable, compagnie à éviter.", 2),
    ("Un vrai conte de fées, je suis sous le charme.", 5),
    ("Safari incroyable, j'ai vu tant d'animaux !", 5),
    ("La chambre d'hôtel était sale, très déçu.", 1),
    ("Croisière de rêve, paysages époustouflants.", 5),
    ("Le guide était plus perdu que nous... dommage.", 2),
    ("Des moments magiques, je n'oublierai jamais.", 5),
    ("Le camping était une blague, rien à voir avec les photos.", 1),
    ("Excellente cuisine, un voyage culinaire inattendu.", 4),
    ("Trop de monde partout, pas de repos possible.", 2),
    ("Aventure inoubliable, je me suis découvert une passion pour la randonnée.", 5),
    ("Horrible expérience, l'organisation était un désastre.", 1),
    ("Le personnel de l'hôtel a rendu notre séjour exceptionnel.", 5),
    ("Visites culturelles enrichissantes, guides bien informés.", 4),
    ("Transport désorganisé, nous avons manqué une excursion.", 2),
    ("Le paradis sur terre, je reviens l'année prochaine !", 5),
    ("La climatisation était en panne, nuits infernales.", 2),
    ("Équipe au top, vacances réussies grâce à eux.", 5),
    ("Manque de variété dans les repas, assez monotone.", 3),
    ("Émerveillé par la faune et la flore, randonnées superbes.", 5),
    ("La ville était surpeuplée, difficile d'apprécier les sites.", 2),
    ("Excursions bien organisées, nous avons vu tant de lieux incroyables !", 5),
    ("Le prix ne justifie pas la qualité, très décevant.", 2),
    ("Petit déjeuner de roi, un large choix chaque matin.", 4),
    ("Panne d'électricité, une soirée à la bougie, ambiance romantique imprévue !", 4),
    ("Le site était en rénovation, visite gâchée, très frustrant.", 1)
]

# Sélectionnez tous les IDs des commandes existantes
cur.execute("SELECT id FROM commande")
commande_ids = cur.fetchall()

# Générez un avis pour chaque commande
for (commande_id,) in commande_ids:
    # Sélectionnez un avis aléatoire de la liste
    avis, note = random.choice(avis_et_notes)
    
    # Associez chaque avis à une commande et à un contact existants
    cur.execute(
        "INSERT INTO avis_voyageur (commande_id, contact_id, avis, note, date_avis) VALUES (%s, (SELECT contact_id FROM commande WHERE id = %s), %s, %s, %s)",
        (commande_id, commande_id, avis, note, fake.date_between(start_date='-1y', end_date='today'))
    )

# Valider les changements et fermer la connexion
conn.commit()
cur.close()
conn.close()

print("Les avis ont été générés et insérés dans la base de données avec succès.")