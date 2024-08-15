import os
import hashlib
from extensions import db
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Blueprint, current_app, render_template, request
from models.recived_invoice_model import RecivedInvoiceVATPayer

load_invoice_blueprint = Blueprint('load_invoice_blueprint', __name__, template_folder='templates')




def convert_to_date(date_string):
    if date_string:
        return datetime.strptime(date_string, '%Y-%m-%d').date()  # Předpokládám, že používáš formát 'YYYY-MM-DD'
    return None


@load_invoice_blueprint.route('/loadinvoice')
def load_invoice_dashboard():
    return render_template("load_invoice_dashboard.html")


@load_invoice_blueprint.route('/load_recived_inovice_vat_payer', methods=['GET', 'POST'])
def upload_recived_invoice_vat_payer():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            original_filename = secure_filename(file.filename)
            filename_hash = hashlib.sha256((original_filename + str(datetime.now())).encode()).hexdigest()
            filename = f"{filename_hash}_{original_filename}"
            file_data = file.read()
            nazev_faktury = request.form.get('nazev-faktury')

            evidencni_cislo = request.form.get('evidencni-cislo')
            typ_faktury = request.form.get('typ-faktury')

            jmeno_dodavatele = request.form.get('jmeno-dodavatele')
            adresa_dodavatele = request.form.get('adresa-dodavatele')
            ico_dodavatele = request.form.get('ico-dodavatele')
            dic_dodavatele = request.form.get('dic-dodavatele')

            cislo_uctu = request.form.get('cislo-uctu')

            datum_vystaveni = convert_to_date(request.form.get('datum-vystaveni'))
            datum_splatnosti = convert_to_date(request.form.get('datum-splatnosti'))
            datum_uzp = convert_to_date(request.form.get('datum-uzp'))

            mena = request.form.get('mena')
            variabilni_symbol = request.form.get('variabilni-symbol')
            platebni_metoda = request.form.get('platebni-metoda')

            zaokrouhleni = request.form.get('zaokrouhleni')
            rpdp = request.form.get('rpdp')

            vc_dph_21 = request.form.get('vc-dph-21')
            bez_dph_21 = request.form.get('bez-dph-21')
            dph_21 = request.form.get('dph-21')
            bez_dph_0 = request.form.get('bez-dph-0')
            vc_dph_12 = request.form.get('vc-dph-12')
            bez_dph_12 = request.form.get('bez-dph-12')
            dph_12 = request.form.get('dph-12')

            # Uložení do databáze
            new_invoice = RecivedInvoiceVATPayer(
                filename=filename,
                nazev_faktury=nazev_faktury,
                evidencni_cislo=evidencni_cislo,
                typ_faktury=typ_faktury,
                jmeno_dodavatele=jmeno_dodavatele,
                adresa_dodavatele=adresa_dodavatele,
                ico_dodavatele=ico_dodavatele,
                dic_dodavatele=dic_dodavatele,
                datum_vystaveni=datum_vystaveni,
                datum_splatnosti=datum_splatnosti,
                datum_uzp=datum_uzp,
                cislo_uctu=cislo_uctu,
                mena=mena,
                variabilni_symbol=variabilni_symbol,
                platebni_metoda=platebni_metoda,
                zaokrouhleni=zaokrouhleni,
                rpdp=rpdp,
                vc_dph_21=vc_dph_21,
                bez_dph_21=bez_dph_21,
                dph_21=dph_21,
                bez_dph_0=bez_dph_0,
                vc_dph_12=vc_dph_12,
                bez_dph_12=bez_dph_12,
                dph_12=dph_12,
            )
            db.session.add(new_invoice)
            db.session.commit()

            with open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), 'wb') as f:
                f.write(file_data)

            return render_template("index.html")

    return render_template("load_invoices_forms_templates/load_recived_invoice_vat_payer.html")
