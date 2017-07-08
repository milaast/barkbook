"""Utility file to seed Barbkbook database"""

from sqlalchemy import func
from model import User, Pet

from model import connect_to_db, db
from server import app


def load_users():
    """Load users from users_data into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("data/users_data"):
        row = row.rstrip()
        user_id, first_name, last_name, email, password, zipcode, city, state = row.split("|")

        user = User(user_id=user_id,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    zipcode=zipcode,
                    city=city,
                    state=state)

        # Add to the session or it won't ever be stored
        db.session.add(user)
    # Commit session to save to database
    db.session.commit()


def load_pets():
    """Load pets from pets_data into database."""

    print "Pets"

    Pet.query.delete()

    for row in open("data/pets_data"):
        row = row.rstrip()
        user_id, name, species, age, breed, gender, details, picture = row.split("|")

        pet = Pet(user_id=user_id,
                  name=name,
                  species=species,
                  age=age,
                  breed=breed,
                  gender=gender,
                  details=details,
                  picture=picture)

        db.session.add(pet)

    db.session.commit()


# def load_species():
#     """Load species from species_data into database."""

#     print "Species"

#     Species.query.delete()

#     for row in open("data/species_data"):
#         row = row.rstrip()
#         species_id, name = row.split("|")

#         species = Species(species_id=species_id,
#                           name=name)

#         db.session.add(species)

#     db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_pets()
    set_val_user_id()