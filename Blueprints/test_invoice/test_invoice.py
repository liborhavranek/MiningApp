import os

import requests
from flask import Blueprint, render_template, request, current_app
from extensions import API_URL
from models.recived_invoice_model import RecivedInvoiceVATPayer

test_invoice_blueprint = Blueprint('test_invoice_blueprint', __name__, template_folder='templates')


@test_invoice_blueprint.route('/test_recieved_vat_payer_invoice/<int:id>', methods=['GET', 'POST'])
def test_recieved_vat_payer_invoice(id):
    invoice = RecivedInvoiceVATPayer.query.get_or_404(id)
    return render_template("test_invoices_templates/test_recieved_invoice_vat_payer.html", invoice=invoice)


@test_invoice_blueprint.route('/send_file_recieved_vat_payer_invoice/<int:id>', methods=['POST'])
def send_file_recieved_vat_payer_invoice(id):
    invoice = RecivedInvoiceVATPayer.query.get_or_404(id)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], invoice.filename)
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
                    "ACCOUNT_NUMBER": "76202231/0100",
                    "CURRENCY": "Kč",
                    "DIC_SUPPLIER": "CZ48207691",
                    "DUE_DATE": "29.08.2024",
                    "IC_SUPPLIER": "48207691",
                    "ID": "240735",
                    "IS_DEFERRED_TAX": "null",
                    "PAYMENT_METHOD": "Převodem",
                    "PUBLICATION_DATE": "15.08.2024",
                    "ROUNDING": "null",
                    "SUPPLIER_ADDRESS": "Husova tř. 1821/4 37001 České Budějovice Czech Republic",
                    "SUPPLIER_NAME": "PF Č.Budějovice spol. s r.o.",
                    "TAX_POINT": "15.08.2024",
                    "TYPE": "Faktura - daňoví doklad",
                    "VARIABLE_SYMBOL": "240735",
                    "VAT_TABLE": [
                        {
                            "PRICE_INCLUDING_VAT": "615.29",
                            "PRICE_WITHOUT_VAT": "508.5",
                            "VAT_AMOUNT": "106.79",
                            "VAT_RATE": "21%"
                        },
                        {
                            "PRICE_INCLUDING_VAT": "2406.32",
                            "PRICE_WITHOUT_VAT": "2148.5",
                            "VAT_AMOUNT": "257.82",
                            "VAT_RATE": "12%"
                        },
                    ]
                }
            }

        # Definujte slovník aliasů
        key_aliases = {
            'SUPPLIER_NAME': ['SUPPLIER_NAME', 'SUPP_NAME'],
            'SUPPLIER_ADDRESS': ['SUPPLIER_ADDRESS'],
            'IC_SUPPLIER': ['IC_SUPPLIER'],
            'DIC_SUPPLIER': ['DIC_SUPPLIER'],
            'ACCOUNT_NUMBER': ['ACCOUNT_NUMBER', 'BANK_ACCOUNT'],
            'VARIABLE_SYMBOL': ['VARIABLE_SYMBOL'],
            'PUBLICATION_DATE': ['PUBLICATION_DATE'],
            'TAX_POINT': ['TAX_POINT'],
            'DUE_DATE': ['DUE_DATE'],
            'PAYMENT_METHOD': ['PAYMENT_METHOD'],
            'CURRENCY': ['CURRENCY'],
            'TYPE': ['TYPE'],
            'IS_DEFERRED_TAX': ['IS_DEFERRED_TAX'],
            'ROUNDING': ['ROUNDING'],
            'ID': ['ID'],
            # VAT_TABLE items
            'VAT_RATE': ['VAT_RATE'],
            'PRICE_INCLUDING_VAT': ['PRICE_INCLUDING_VAT'],
            'PRICE_WITHOUT_VAT': ['PRICE_WITHOUT_VAT'],
            'VAT_AMOUNT': ['VAT_AMOUNT']
        }

        # Přiřazení hodnot z result do klíčů podle aliasů
        standardized_result = {}
        for main_key, aliases in key_aliases.items():
            for alias in aliases:
                if alias in result['result']:
                    standardized_result[main_key] = result['result'][alias]
                    break

        # Zpracování VAT_TABLE
        vat_table = []
        if 'VAT_TABLE' in result['result']:
            for vat_entry in result['result']['VAT_TABLE']:
                vat_standardized_entry = {}
                for main_key, aliases in key_aliases.items():
                    for alias in aliases:
                        if alias in vat_entry:
                            vat_standardized_entry[main_key] = vat_entry[alias]
                            break
                vat_table.append(vat_standardized_entry)
            standardized_result['VAT_TABLE'] = vat_table

        key_descriptions = {
            'ID': 'Číslo dokladu',
            'TYPE': 'Typ',
            'SUPPLIER_ADDRESS': 'Adresa Odběratele',
            'SUPPLIER_NAME': 'Jméno odběratele',
            'IC_SUPPLIER': 'IČO dodavatele',
            'DIC_SUPPLIER': 'DIČ dodavatele',
            'ACCOUNT_NUMBER': 'Číslo účtu',
            'VARIABLE_SYMBOL': 'Variabilní symbol',
            'PUBLICATION_DATE': 'Datum vystavení',
            'TAX_POINT': 'Datum UZP',
            'DUE_DATE': 'Datum splatnosti',
            'PAYMENT_METHOD': 'Platební metoda',
            'CURRENCY': 'Měna',
            'IS_DEFERRED_TAX': 'RPDP',
            'ROUNDING': 'Zaokrouhlení',
            # VAT_TABLE descriptions
            'VAT_RATE': 'Sazba DPH',
            'PRICE_INCLUDING_VAT': 'Cena včetně DPH',
            'PRICE_WITHOUT_VAT': 'Cena bez DPH',
            'VAT_AMOUNT': 'Výše DPH'
        }

        return render_template('results.html', result=result, json_data=standardized_result, key_descriptions=key_descriptions, invoice=invoice)
