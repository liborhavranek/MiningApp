from flask import Flask
from extensions import db
from models.recived_invoice_model import RecivedInvoiceVATPayer


app = Flask(__name__)

app.secret_key = "secret_key"
UPLOAD_FOLDER = 'uploads'

# Konfigurace SQLAlchemy
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///invoices.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


from Blueprints.dashboard.dashboard import dashboard_blueprint
from Blueprints.load_invoices.load_invoices import load_invoice_blueprint
from Blueprints.invoice_list.invoice_list import invoice_list_blueprint
from Blueprints.edit_invoices.edit_invoices import edit_invoice_blueprint
from Blueprints.delete_invoice.delte_invoices import delete_invoice_blueprint
from Blueprints.test_invoice.test_invoice import test_invoice_blueprint


app.register_blueprint(dashboard_blueprint)
app.register_blueprint(load_invoice_blueprint)
app.register_blueprint(invoice_list_blueprint)
app.register_blueprint(edit_invoice_blueprint)
app.register_blueprint(delete_invoice_blueprint)
app.register_blueprint(test_invoice_blueprint)

if __name__ == '__main__':
    app.run(port=5003, debug=True)

