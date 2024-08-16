import os

from flask import Blueprint, current_app, flash, redirect, url_for

from extensions import db
from models.recived_invoice_model import RecivedInvoiceVATPayer

delete_invoice_blueprint = Blueprint('delete_invoice_blueprint', __name__, template_folder='templates')

@delete_invoice_blueprint.route('/delete_invoice_recieved_invoice_vat_payer/<int:id>', methods=['GET', 'POST'])
def delete_invoice_recieved_invoice_vat_payer(id):
    invoice_to_delete = RecivedInvoiceVATPayer.query.get_or_404(id)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], invoice_to_delete.filename)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        db.session.delete(invoice_to_delete)
        db.session.commit()
        flash('Faktura a související soubor byly úspěšně smazány!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Nastala chyba při mazání faktury.', 'danger')
        print(e)
    return redirect(url_for('invoice_list_blueprint.recived_invoices_vat_payer_list'))

