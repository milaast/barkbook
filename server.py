""" Barkbook! """

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, User, Pet, PetInterest, Adoption, Species


app = Flask(__name__)
app.secret_key = "ABC"
# app.jinja_env.undefined = StrictUndefined


@app.route("/")
def show_homepage():

    return render_template('homepage.html')


@app.route("/", methods=["POST"])
def log_user_in():

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

    #redirect routes are temporary, until new templates are designed


@app.route('/puppy')
def see_puppy():

    return '<img src="static/pictures/dottie.jpg">'


if __name__ == '__main__':

    app.debug = True
    app.jinja_env.auto_reload = app.debug 

    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")