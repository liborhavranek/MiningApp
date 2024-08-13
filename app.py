import os
import hashlib
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename


app = Flask(__name__)

# Konfigurace SQLAlchemy
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///invoices.db'  # Použijeme SQLite jako příklad
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def convert_to_date(date_string):
    if date_string:
        return datetime.strptime(date_string, '%Y-%m-%d').date()  # Předpokládám, že používáš formát 'YYYY-MM-DD'
    return None

# Model pro databázi
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    evidencni_cislo = db.Column(db.String(120), nullable=True)
    typ_faktury = db.Column(db.String(120), nullable=True)
    jmeno_dodavatele = db.Column(db.String(120), nullable=True)
    ico_dodavatele = db.Column(db.String(120), nullable=True)
    dic_dodavatele = db.Column(db.String(120), nullable=True)
    jmeno_odberatele = db.Column(db.String(120), nullable=True)
    ico_odberatele = db.Column(db.String(120), nullable=True)
    dic_odberatele = db.Column(db.String(120), nullable=True)
    datum_vystaveni = db.Column(db.Date, nullable=True)
    datum_splatnosti = db.Column(db.Date, nullable=True)
    datum_uzp = db.Column(db.Date, nullable=True)
    cislo_uctu = db.Column(db.String(120), nullable=True)
    mena = db.Column(db.String(10), nullable=True)
    variabilni_symbol = db.Column(db.String(120), nullable=True)
    price = db.Column(db.String(120), nullable=True)
    dph_celkem = db.Column(db.String(120), nullable=True)
    zaokrouhleni = db.Column(db.String(120), nullable=True)
    cena_celkem = db.Column(db.String(120), nullable=True)
    rpdp = db.Column(db.String(120), nullable=True)
    vc_dph_21 = db.Column(db.String(120), nullable=True)
    bez_dph_21 = db.Column(db.String(120), nullable=True)
    dph_21 = db.Column(db.String(120), nullable=True)
    bez_dph_0 = db.Column(db.String(120), nullable=True)
    vc_dph_12 = db.Column(db.String(120), nullable=True)
    bez_dph_12 = db.Column(db.String(120), nullable=True)
    dph_12 = db.Column(db.String(120), nullable=True)
    dph_0 = db.Column(db.String(120), nullable=True)


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
            # Získání původního názvu souboru
            original_filename = secure_filename(file.filename)

            # Vytvoření hash pomocí názvu souboru a aktuálního času
            filename_hash = hashlib.sha256((original_filename + str(datetime.now())).encode()).hexdigest()

            # Nový název souboru s hash
            filename = f"{filename_hash}_{original_filename}"

            # Uložení souboru
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Získání údajů z formuláře
            evidencni_cislo = request.form.get('evidencni-cislo')
            typ_faktury = request.form.get('typ-faktury')
            jmeno_dodavatele = request.form.get('jmeno-dodavatele')
            ico_dodavatele = request.form.get('ico-dodavatele')
            dic_dodavatele = request.form.get('dic-dodavatele')
            jmeno_odberatele = request.form.get('jmeno-odberatele')
            ico_odberatele = request.form.get('ico-odberatele')
            dic_odberatele = request.form.get('dic-odberatele')
            datum_vystaveni = convert_to_date(request.form.get('datum-vystaveni'))
            datum_splatnosti = convert_to_date(request.form.get('datum-splatnosti'))
            datum_uzp = convert_to_date(request.form.get('datum-uzp'))
            cislo_uctu = request.form.get('cislo-uctu')
            mena = request.form.get('mena')
            variabilni_symbol = request.form.get('variabilni-symbol')
            price = request.form.get('price')
            dph_celkem = request.form.get('dph-celkem')
            zaokrouhleni = request.form.get('zaokrouhleni')
            cena_celkem = request.form.get('cena-celkem')
            rpdp = request.form.get('rpdp')
            vc_dph_21 = request.form.get('vc-dph-21')
            bez_dph_21 = request.form.get('bez-dph-21')
            dph_21 = request.form.get('dph-21')
            bez_dph_0 = request.form.get('bez-dph-0')
            vc_dph_12 = request.form.get('vc-dph-12')
            bez_dph_12 = request.form.get('bez-dph-12')
            dph_12 = request.form.get('dph-12')
            dph_0 = request.form.get('dph-0')

            # Uložení do databáze
            new_invoice = Invoice(
                filename=filename,
                evidencni_cislo=evidencni_cislo,
                typ_faktury=typ_faktury,
                jmeno_dodavatele=jmeno_dodavatele,
                ico_dodavatele=ico_dodavatele,
                dic_dodavatele=dic_dodavatele,
                jmeno_odberatele=jmeno_odberatele,
                ico_odberatele=ico_odberatele,
                dic_odberatele=dic_odberatele,
                datum_vystaveni=datum_vystaveni,
                datum_splatnosti=datum_splatnosti,
                datum_uzp=datum_uzp,
                cislo_uctu=cislo_uctu,
                mena=mena,
                variabilni_symbol=variabilni_symbol,
                price=price,
                dph_celkem=dph_celkem,
                zaokrouhleni=zaokrouhleni,
                cena_celkem=cena_celkem,
                rpdp=rpdp,
                vc_dph_21=vc_dph_21,
                bez_dph_21=bez_dph_21,
                dph_21=dph_21,
                bez_dph_0=bez_dph_0,
                vc_dph_12=vc_dph_12,
                bez_dph_12=bez_dph_12,
                dph_12=dph_12,
                dph_0=dph_0
            )
            db.session.add(new_invoice)
            db.session.commit()

            return redirect(url_for('hello_world'))

    return render_template("load_invoice.html")


if __name__ == '__main__':
    app.run(port=5002, debug=True)

