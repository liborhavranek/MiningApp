
from flask import Flask

from extensions import db
from models.recived_invoice_model import RecivedInvoiceVATPayer


app = Flask(__name__)

app.secret_key = "secret_key"
API_URL = "https://documents-ai.netglade.cz/process-document"  # URL pro API
UPLOAD_FOLDER = 'uploads'

# Konfigurace SQLAlchemy
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///invoices.db'  # Použijeme SQLite jako příklad
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()









#
# @app.route('/delete_invoice/<int:id>', methods=['POST'])
# def delete_invoice(id):
#     invoice_to_delete = Invoice.query.get_or_404(id)
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], invoice_to_delete.filename)
#     try:
#         if os.path.exists(file_path):
#             os.remove(file_path)
#         db.session.delete(invoice_to_delete)
#         db.session.commit()
#         flash('Faktura a související soubor byly úspěšně smazány!', 'success')
#     except Exception as e:
#         db.session.rollback()
#         flash('Nastala chyba při mazání faktury.', 'danger')
#         print(e)
#     return redirect(url_for('invoice_list'))
#
#
#
# @app.route('/editfakturu/<int:id>', methods=['GET', 'POST'])
# def edit_invoice(id):
#     invoice = Invoice.query.get_or_404(id)
#
#     if request.method == 'POST':
#         # Zpracování nahrávání souboru, pokud je přítomen
#         file = request.files.get('file')
#         if file:
#             # Získání původního názvu souboru
#             original_filename = secure_filename(file.filename)
#
#             # Vytvoření hash pomocí názvu souboru a aktuálního času
#             filename_hash = hashlib.sha256((original_filename + str(datetime.now())).encode()).hexdigest()
#
#             # Nový název souboru s hash
#             filename = f"{filename_hash}_{original_filename}"
#
#             # Uchováme soubor v paměti a odložíme jeho uložení na později
#             file_data = file.read()
#
#             # Po potvrzení uložení faktury uložíme i soubor na disk
#             with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'wb') as f:
#                 f.write(file_data)
#
#             # Aktualizace názvu souboru v databázi
#             invoice.filename = filename
#
#         # Získání údajů z formuláře
#         invoice.nazev_faktury = request.form.get('nazev-faktury', invoice.nazev_faktury)
#         invoice.evidencni_cislo = request.form.get('evidencni-cislo', invoice.evidencni_cislo)
#         invoice.typ_faktury = request.form.get('typ-faktury', invoice.typ_faktury)
#         invoice.jmeno_dodavatele = request.form.get('jmeno-dodavatele', invoice.jmeno_dodavatele)
#         invoice.ico_dodavatele = request.form.get('ico-dodavatele', invoice.ico_dodavatele)
#         invoice.dic_dodavatele = request.form.get('dic-dodavatele', invoice.dic_dodavatele)
#         invoice.jmeno_odberatele = request.form.get('jmeno-odberatele', invoice.jmeno_odberatele)
#         invoice.ico_odberatele = request.form.get('ico-odberatele', invoice.ico_odberatele)
#         invoice.dic_odberatele = request.form.get('dic-odberatele', invoice.dic_odberatele)
#         invoice.datum_vystaveni = convert_to_date(request.form.get('datum-vystaveni', invoice.datum_vystaveni))
#         invoice.datum_splatnosti = convert_to_date(request.form.get('datum-splatnosti', invoice.datum_splatnosti))
#         invoice.datum_uzp = convert_to_date(request.form.get('datum-uzp', invoice.datum_uzp))
#         invoice.cislo_uctu = request.form.get('cislo-uctu', invoice.cislo_uctu)
#         invoice.mena = request.form.get('mena', invoice.mena)
#         invoice.variabilni_symbol = request.form.get('variabilni-symbol', invoice.variabilni_symbol)
#         invoice.price = request.form.get('price', invoice.price)
#         invoice.dph_celkem = request.form.get('dph-celkem', invoice.dph_celkem)
#         invoice.zaokrouhleni = request.form.get('zaokrouhleni', invoice.zaokrouhleni)
#         invoice.cena_celkem = request.form.get('cena-celkem', invoice.cena_celkem)
#         invoice.rpdp = request.form.get('rpdp', invoice.rpdp)
#         invoice.vc_dph_21 = request.form.get('vc-dph-21', invoice.vc_dph_21)
#         invoice.bez_dph_21 = request.form.get('bez-dph-21', invoice.bez_dph_21)
#         invoice.dph_21 = request.form.get('dph-21', invoice.dph_21)
#         invoice.bez_dph_0 = request.form.get('bez-dph-0', invoice.bez_dph_0)
#         invoice.vc_dph_12 = request.form.get('vc-dph-12', invoice.vc_dph_12)
#         invoice.bez_dph_12 = request.form.get('bez-dph-12', invoice.bez_dph_12)
#         invoice.dph_12 = request.form.get('dph-12', invoice.dph_12)
#         invoice.dph_0 = request.form.get('dph-0', invoice.dph_0)
#
#         # Uložení aktualizovaných údajů do databáze
#         db.session.commit()
#
#         return redirect(url_for('invoice_list'))
#
#     return render_template("edit_invoice.html", invoice=invoice)
#
#
# @app.route('/testinvoice/<int:id>', methods=['GET', 'POST'])
# def test_invoice(id):
#     invoice = Invoice.query.get_or_404(id)
#
#     return render_template("test_invoice.html", invoice=invoice)
#
#
# @app.route('/send_file<int:id>', methods=['POST'])
# def send_file(id):
#     invoice = Invoice.query.get_or_404(id)
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
#
#
#
#
#             }
#             return render_template('results.html', json_data=result, key_descriptions=key_descriptions, invoice=invoice)
#         else:
#             return f"Error: {response.status_code}, {response.text}", response.status_code


from Blueprints.dashboard.dashboard import dashboard_blueprint
from Blueprints.load_invoices.load_invoices import load_invoice_blueprint
from Blueprints.invoice_list.invoice_list import invoice_list_blueprint
from Blueprints.edit_invoices.edit_invoices import edit_invoice_blueprint


app.register_blueprint(dashboard_blueprint)
app.register_blueprint(load_invoice_blueprint)
app.register_blueprint(invoice_list_blueprint)
app.register_blueprint(edit_invoice_blueprint)

if __name__ == '__main__':
    app.run(port=5003, debug=True)

