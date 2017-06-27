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

    phone = db.Column(db.Integer, 
                      nullable=True)

    dob = db.Column(db.DateTime,
                    nullable=True)

    picture = db.Column(db.String,
                        nullable=True)


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

    picture = db.Column(db.String,
                        nullable=True)

    details = db.Column(db.Text,
                        nullable=True)


class PetInterest(db.Model):
    """Movie on ratings website."""

    __tablename__ = "pet_interest"

    # this is the table that will be queried and dispalyed on the users page
    # that shows users interested in pets up for adoption and the pets a user
    # has interest on

    # def __repr__(self):
    #     """Provide helpful representation when printed."""

    #     the_m_rep = "<Movie movie_id=%s title=%s>"
    #     return the_m_rep % (self.movie_id, self.title)

    interest_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)

    adoption_id = db.Column(db.Integer,
                  db.ForeignKey("adoptions.adoption_id"),
                  nullable=False)


class Adoption(db.Model):
    """Identify pets that are available for adoption."""

    __tablename__ = "adoptions"

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Pet's owner ID: owner_id=%i pet's name: name=%s>" % (self.owner_id, 
                                                                      pets.name)

    pet_id = db.Column(db.Integer,
                       db.ForeignKey("pets.pet_id"),
                       nullable=False)

    owner_id = db.Column(db.ForeignKey("users.user_id"),
                         nullable=False)


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


##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."