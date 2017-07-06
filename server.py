""" Barkbook! """

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, User, Pet, PetInterest, Adoption, Species, db


app = Flask(__name__)
app.secret_key = "ABC"
# app.jinja_env.undefined = StrictUndefined


@app.route("/")
def show_homepage():

    return render_template('homepage.html')


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
            return redirect("/")
            # the person's profile. Use jinja to fill in URL

    #redirect routes are temporary, until new templates are designed


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

        flash("You successfully created an account")
        return redirect("/")
        # redirect to their profile, where they will be able to add pictures
        # add pets, or look for pets


    else:
        flash("That e-mail address is already in use!")
        return redirect("/register")


@app.route("/login")
def show_login():

    return render_template("login.html")



@app.route('/puppy')
def see_puppy():

    return '<img src="static/pictures/dottie.jpg">'


if __name__ == '__main__':

    app.debug = True
    app.jinja_env.auto_reload = app.debug 

    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")