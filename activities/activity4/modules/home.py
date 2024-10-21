# app/modules/home/routes.py
from flask import session, render_template


def register(app):
    @app.route("/")
    def landing_page():
        return render_template("landing_page.html")

    