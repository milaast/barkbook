"""Models and database functions for Barkbook."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)


db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of Barkbook."""

    __tablename__ = "users"

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User: first_name=%s last_name=%s E-mail: email=%s>" % (self.first_name,
                                                                        self.last_name,
                                                                        self.email)

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)

    first_name = db.Column(db.String(64),
                           nullable=False)

    last_name = db.Column(db.String(64),
                          nullable=False)

    email = db.Column(db.String(64), 
                      nullable=False)

    password = db.Column(db.String(64),
                         nullable=False)

    zipcode = db.Column(db.String(10), 
                        nullable=False)

    city = db.Column(db.String(64),
                     nullable=False)

    state = db.Column(db.String(2),
                      nullable=False)

    phone = db.Column(db.String(12), 
                      nullable=True)

    dob = db.Column(db.DateTime,
                    nullable=True)

    picture = db.Column(db.String,
                        nullable=True)

    # Relationships:
    pets = db.relationship("Pet")
    adoptions = db.relationship("Adoption")



class Pet(db.Model):
    """Pet profiles on Barkbook."""

    __tablename__ = "pets"

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Pet's owner ID: owner_id=%i pet's name: name=%s>" % (self.owner_id, 
                                                                      self.name)

    pet_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False)

    name = db.Column(db.String(64),
                     nullable=False)

    species = db.Column(db.Integer,
                        db.ForeignKey("species.species_id"),
                        nullable=False)

    age = db.Column(db.Integer,
                    nullable=True)

    breed = db.Column(db.String(64),
                      nullable=True)

    gender = db.Column(db.String(20),
                       nullable=True)

    details = db.Column(db.Text,
                        nullable=True)

    picture = db.Column(db.String,
                        nullable=True)

    # Relationships: 
    species_relationship = db.relationship("Species")
    adoption = db.relationship("Adoption")
    user = db.relationship("User")

class PetInterest(db.Model):
    """Pets that have users interested in them."""

    __tablename__ = "pet_interest"

    # this is the table that will be queried and dispalyed on the users page
    # that shows users interested in pets up for adoption and the pets a user
    # has interest on

    interest_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)

    adoption_id = db.Column(db.Integer,
                  db.ForeignKey("adoptions.adoption_id"),
                  nullable=False)

    interested_person_id = db.Column(db.Integer,
                           db.ForeignKey("users.user_id"),
                           nullable=False)

    adoption = db.relationship('Adoption')


class Adoption(db.Model):
    """Identify pets that are available for adoption."""

    __tablename__ = "adoptions"

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Pet's owner ID: owner_id=%i pet's name: name=%s>" % (self.owner_id, 
                                                                      self.pet.name)
    adoption_id = db.Column(db.Integer, 
                            autoincrement=True,
                            primary_key=True)

    pet_id = db.Column(db.Integer,
                       db.ForeignKey("pets.pet_id"),
                       nullable=False)

    owner_id = db.Column(db.ForeignKey("users.user_id"),
                         nullable=False)

    # Relationships: 
    pet = db.relationship('Pet')
    owner = db.relationship('User')


class Species(db.Model):
    """Animal species on the website."""

    __tablename__ = "species"

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Species: species_id=%s name=%s>" & (self.species_id, 
                                                 self.name)

    species_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True)

    name = db.Column(db.String,
                      nullable=False)

    # Relationships: 
    pets = db.relationship('Pet')

##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///barkbook'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."