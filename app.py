import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Konfigurace SQLAlchemy
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///invoices.db'  # Použijeme SQLite jako příklad
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Model pro databázi
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    price = db.Column(db.String(120), nullable=False)


# Vytvoření databázových tabulek
with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/nahratfakturu', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Zpracování nahrávání souboru
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Získání ceny
            price = request.form['price']

            # Uložení do databáze
            new_invoice = Invoice(filename=filename, price=price)
            db.session.add(new_invoice)
            db.session.commit()

            return redirect(url_for('hello_world'))

    return render_template("load_invoice.html")


if __name__ == '__main__':
    app.run(port=5002, debug=True)
