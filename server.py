""" Barkbook! """

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, User, Pet, PetInterest, Adoption, Species, db


app = Flask(__name__)
app.secret_key = "ABC"
# app.jinja_env.undefined = StrictUndefined


@app.route("/")
def show_homepage_login():
    """ Shows user the homepage and the login form. """

    return render_template("homepage.html")


@app.route("/", methods=["POST"])
def log_user_in():
    """ Takes information from form and validates against database.

        """

    email = request.form.get("email")
    form_password = request.form.get("password")

    existing_user = User.query.filter(User.email == email).first() 

    if existing_user is None:

        flash("You must create an account first")
        return redirect("/")

    else:

        user_id = existing_user.user_id
        user_password = existing_user.password

        if form_password != user_password:

            flash("The password you entered does not match your account")
            return redirect("/")

        else:

            session["user_id"] = user_id

            flash("You're successfully logged in")
            return redirect("/" + str(user_id))
            # the person's profile. Use jinja to fill in URL

    #redirect routes are temporary, until new templates are designed

# create a link on the navbar to logout
@app.route("/logout")
def log_user_out():

    session.clear()
    flash("You've successfully logged out")

    return redirect("/")



@app.route("/<user_id>")
def show_profile(user_id):

    user = User.query.get(user_id)

    return render_template("user_profile.html", user=user)


@app.route("/register")
def reg_form():
    """Shows user account registration form."""

    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_user():
    """ Create user account.
        Checks database and, if e-mail does not exist there yet, creates a
        new user account.

        """
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")    
    password = request.form.get("password")
    zipcode = request.form.get("zipcode")
    city = request.form.get("city")
    phone = request.form.get("phone")
    dob = request.form.get("dob")

    existing_user = User.query.filter(User.email == email).first()

    if not existing_user:

        new_user = User(first_name=first_name,
                        last_name=last_name,
                        email=email,
                        password=password,
                        zipcode=zipcode,
                        city=city,
                        phone=phone,
                        dob=dob)

        db.session.add(new_user)
        db.session.commit()

        # none of this worked
        # user = User.query.filter(User.email==email).one()
        # session["user_id"] = user.user_id

        # session["user_id"] = user_id ; query database to get the user_id for
        # this user and start a session, so you can pass i over to the pet profile.
        flash("You successfully created an account")
        return redirect("/pet_profile")


    else:
        flash("That e-mail address is already in use!")
        return redirect("/register")


@app.route("/pet_profile")
def pet_profile():
    """Shows user account registration form."""

    return render_template("create_pet_profile.html")


@app.route("/pet_profile", methods=["POST"])
def add_pet_profile():
    """ Create pet profile.
        Adds pet profile to database and, if available for adoption, 
        adds pet to adoption table.
         """
         
    # also not working
    # user_id = User.query.get(user) 
    name = request.form.get("name")
    species = request.form.get("species")
    age = request.form.get("age")
    breed = request.form.get("breed")
    gender = request.form.get("gender")
    details = request.form.get("details")
    adoptable = request.form.get("adoptable")

    pet = Pet(user_id=user_id,
              name=name,
              species=species,
              age=age,
              breed=breed,
              gender=gender,
              details=details)

    db.session.add(pet)
    db.session.commit()

    if adoptable == "yes": 
        
        pet_id = Pet.query.filter(Pet.name==name)
        owner_id = user_id

        adoption = Adoption(pet_id=pet_id,
                            owner_id=owner_id)

        db.session.add(adoption)
        db.session.commit()
        flash("Your pet is now available for adoption!")

    flash("Your pet's profile has been created!")
    redirect("/")

@app.route('/puppy')
def see_puppy():

    return '<img src="static/pictures/dottie.jpg">'


if __name__ == '__main__':

    app.debug = True
    app.jinja_env.auto_reload = app.debug 

    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")