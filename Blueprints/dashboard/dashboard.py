from flask import Blueprint, render_template

# Vytvoření blueprintu
dashboard_blueprint = Blueprint('dashboard_blueprint', __name__, template_folder='templates')


@dashboard_blueprint.route('/')
def dashboard():
    return render_template("index.html")
