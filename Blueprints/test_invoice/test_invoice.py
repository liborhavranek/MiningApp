import os

import requests
from flask import Blueprint, render_template, request

from app import UPLOAD_FOLDER, API_URL
from models.recived_invoice_model import RecivedInvoiceVATPayer

test_invoice_blueprint = Blueprint('test_invoice_blueprint', __name__, template_folder='templates')


@test_invoice_blueprint.route('/test_recieved_vat_payer_invoice/<int:id>', methods=['GET', 'POST'])
def test_recieved_vat_payer_invoice(id):
    invoice = RecivedInvoiceVATPayer.query.get_or_404(id)
    return render_template("test_invoices_templates/test_recieved_invoice_vat_payer.html", invoice=invoice)


# @test_invoice_blueprint.route('/send_file_recieved_vat_payer_invoice/<int:id>', methods=['POST'])
# def send_file_recieved_vat_payer_invoice(id):
#     invoice = RecivedInvoiceVATPayer.query.get_or_404(id)
#     file_path = os.path.join(UPLOAD_FOLDER, invoice.filename)
#     if not os.path.exists(file_path):
#         return "File not found", 404
#
#     with open(file_path, 'rb') as file:
#         prompt = request.form['prompt']
#         model = request.form['model']
#         files = {
#             'prompt': (None, prompt),
#             'model': (None, model),
#             'file': (invoice.filename, file, 'application/octet-stream')
#         }
#         response = requests.post(API_URL, files=files)
#
#         if response.status_code == 200:
#             result = response.json()
#             key_descriptions = {
#                 'ID': 'Číslo dokladu',
#                 'TYPE': 'Typ',
#                 'IC_SUPPLIER': 'IČO dodavatele',
#                 'DIC_SUPPLIER': 'DIC dodavatele',
#                 'IC_CUSTOMER': 'IČO odběratele',
#                 'DIC_CUSTOMER': 'DIC odběratele',
#                 'VARIABLE_SYMBOL': 'Variabilní symbol ',
#                 'PUBLICATION_DATE': 'Datum vystavení',
#                 'TAX_POINT': 'Datum UZP',
#                 'DUE_DATE': 'Datum splatnosti',
#                 'ACCOUNT_NUMBER': 'Číslo účtu',
#
#                 'PRICE_INCLUDING_VAT': 'Cena včetně DPH',
#                 'PRICE_WITHOUT_VAT': 'Cena bez DPH',
#                 'VAT_AMOUNT': 'DPH',
#
#                 'CURRENCY': 'Měna',
#                 'SUPPLIER_EVIDENCE_NUMBER': 'Evidenční číslo odběratele',
#                 'IS_DEFERRED_TAX': 'RPDP',
#                 'BANK_ACCOUNT': 'Číslo účtu',
#
#                 'ICO_SUPPLIER': 'IČO dodavatele',
#                 'CIN_SUPPLIER': 'IČO dodavatele',
#
#             }
#             return render_template('results.html', json_data=result, key_descriptions=key_descriptions, invoice=invoice)
#         else:
#             return f"Error: {response.status_code}, {response.text}", response.status_code

@test_invoice_blueprint.route('/send_file_recieved_vat_payer_invoice/<int:id>', methods=['POST'])
def send_file_recieved_vat_payer_invoice(id):
    invoice = RecivedInvoiceVATPayer.query.get_or_404(id)
    file_path = os.path.join(UPLOAD_FOLDER, invoice.filename)
    if not os.path.exists(file_path):
        return "File not found", 404

    with open(file_path, 'rb') as file:
        prompt = request.form['prompt']
        model = request.form['model']
        files = {
            'prompt': (None, prompt),
            'model': (None, model),
            'file': (invoice.filename, file, 'application/octet-stream')
        }

        try:
            response = requests.post(API_URL, files=files)
            response.raise_for_status()  # Raises an exception for 4xx/5xx errors
            result = response.json()
        except (requests.exceptions.RequestException, ValueError):
            # Fallback JSON data for testing when the API call fails
            result = {
  "metadata": {
    "inputTokens": 1964,
    "outputTokens": 318,
    "priceUsd": 0.0107,
    "pages": [
      {
        "type": "pdfFullscreenImage",
        "width": 1242,
        "height": 1920,
        "rescaledWidth": 862,
        "rescaledHeight": 1333
      }
    ]
  },
  "result": {
    "SUPPLIER_NAME": "Polívka Libor - POLI",
    "SUPPLIER_ADDRESS": "U Trojice 13, 370 04 České Budějovice",
    "IC_SUPPLIER": "47228881",
    "DIC_SUPPLIER": "CZ7401281294",
    "ACCOUNT_NUMBER": "273077329 / 0300",
    "PUBLICATION_DATE": "04.07.2024",
    "TAX_POINT": "04.07.2024",
    "DUE_DATE": "18.07.2024",
    "VARIABLE_SYMBOL": "2244996",
    "PAYMENT_METHOD": "Převodem",
    "CURRENCY": "Kč",
    "TYPE": "FAKTURA - DAŇOVÝ",
    "IS_DEFERRED_TAX": "null",
    "ROUNDING": "null",
    "ID": "2244996",
    "VAT_TABLE": [
      {
        "VAT_RATE": "12%",
        "PRICE_INCLUDING_VAT": 15071,
        "PRICE_WITHOUT_VAT": 13456.25,
        "VAT_AMOUNT": 1614.75
      }
    ]
  }
}

        key_descriptions = {
            'ID': 'Číslo dokladu',
            'TYPE': 'Typ',
            'IC_SUPPLIER': 'IČO dodavatele',
            'DIC_SUPPLIER': 'DIČ dodavatele',
            'IC_CUSTOMER': 'IČO odběratele',
            'DIC_CUSTOMER': 'DIČ odběratele',
            'VARIABLE_SYMBOL': 'Variabilní symbol ',
            'PUBLICATION_DATE': 'Datum vystavení',
            'TAX_POINT': 'Datum UZP',
            'DUE_DATE': 'Datum splatnosti',
            'ACCOUNT_NUMBER': 'Číslo účtu',
            'PRICE_INCLUDING_VAT': 'Cena včetně DPH',
            'PRICE_WITHOUT_VAT': 'Cena bez DPH',
            'VAT_AMOUNT': 'DPH',
            'CURRENCY': 'Měna',
            'SUPPLIER_EVIDENCE_NUMBER': 'Evidenční číslo odběratele',
            'IS_DEFERRED_TAX': 'RPDP',
            'BANK_ACCOUNT': 'Číslo účtu',
            'ICO_SUPPLIER': 'IČO dodavatele',
            'CIN_SUPPLIER': 'IČO dodavatele',
        }

        return render_template('results.html', json_data=result, key_descriptions=key_descriptions, invoice=invoice)