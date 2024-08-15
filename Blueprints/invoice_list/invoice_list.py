from flask import Blueprint, render_template
from models.recived_invoice_model import RecivedInvoiceVATPayer

invoice_list_blueprint = Blueprint('invoice_list_blueprint', __name__, template_folder='templates')


@invoice_list_blueprint.route('/invoice_list_dashboard')
def dashboard():
    return render_template("invoice_list_dashboard.html")


@invoice_list_blueprint.route('/recived_invoice_vat_payer_list')
def recived_invoices_vat_payer_list():
    invoices = RecivedInvoiceVATPayer.query.all()
    return render_template("invoice_list_templates/recieved_invoice_vat_payer.html", invoices=invoices)
