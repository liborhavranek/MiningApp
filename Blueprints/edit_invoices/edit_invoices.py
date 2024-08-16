import os
import hashlib
from extensions import db
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Blueprint, current_app, render_template, request, redirect, url_for
from models.recived_invoice_model import RecivedInvoiceVATPayer

edit_invoice_blueprint = Blueprint('edit_invoice_blueprint', __name__, template_folder='templates')


def convert_to_date(date_string):
    if date_string:
        return datetime.strptime(date_string, '%Y-%m-%d').date()
    return None


@edit_invoice_blueprint.route('/edit_recived_invoice_vat_payer/<int:id>', methods=['GET', 'POST'])
def edit_recived_invoice_vat_payer(id):
    invoice = RecivedInvoiceVATPayer.query.get_or_404(id)

    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            original_filename = secure_filename(file.filename)
            filename_hash = hashlib.sha256((original_filename + str(datetime.now())).encode()).hexdigest()
            filename = f"{filename_hash}_{original_filename}"
            file_data = file.read()
            with open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), 'wb') as f:
                f.write(file_data)
            invoice.filename = filename

        invoice.nazev_faktury = request.form.get('nazev-faktury', invoice.nazev_faktury)
        invoice.evidencni_cislo = request.form.get('evidencni-cislo', invoice.evidencni_cislo)
        invoice.typ_faktury = request.form.get('typ-faktury', invoice.typ_faktury)

        invoice.jmeno_dodavatele = request.form.get('jmeno-dodavatele', invoice.jmeno_dodavatele)
        invoice.adresa_dodavatele = request.form.get('adresa-dodavatele', invoice.adresa_dodavatele)
        invoice.ico_dodavatele = request.form.get('ico-dodavatele', invoice.ico_dodavatele)
        invoice.dic_dodavatele = request.form.get('dic-dodavatele', invoice.dic_dodavatele)

        invoice.datum_vystaveni = convert_to_date(request.form.get('datum-vystaveni', invoice.datum_vystaveni))
        invoice.datum_splatnosti = convert_to_date(request.form.get('datum-splatnosti', invoice.datum_splatnosti))
        invoice.datum_uzp = convert_to_date(request.form.get('datum-uzp', invoice.datum_uzp))

        invoice.cislo_uctu = request.form.get('cislo-uctu', invoice.cislo_uctu)
        invoice.mena = request.form.get('mena', invoice.mena)
        invoice.variabilni_symbol = request.form.get('variabilni-symbol', invoice.variabilni_symbol)

        invoice.zaokrouhleni = request.form.get('zaokrouhleni', invoice.zaokrouhleni)
        invoice.platebni_metoda = request.form.get('platebni-metoda', invoice.platebni_metoda)
        invoice.rpdp = request.form.get('rpdp', invoice.rpdp)

        invoice.vc_dph_21 = request.form.get('vc-dph-21', invoice.vc_dph_21)
        invoice.bez_dph_21 = request.form.get('bez-dph-21', invoice.bez_dph_21)
        invoice.dph_21 = request.form.get('dph-21', invoice.dph_21)

        invoice.vc_dph_12 = request.form.get('vc-dph-12', invoice.vc_dph_12)
        invoice.bez_dph_12 = request.form.get('bez-dph-12', invoice.bez_dph_12)
        invoice.dph_12 = request.form.get('dph-12', invoice.dph_12)

        invoice.bez_dph_0 = request.form.get('bez-dph-0', invoice.bez_dph_0)

        db.session.commit()

        return redirect(url_for('invoice_list_blueprint.recived_invoices_vat_payer_list'))

    return render_template("edit_invoices_templates/edit_recieved_invoice_vat_payer.html", invoice=invoice)
