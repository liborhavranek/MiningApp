from extensions import db


class RecivedInvoiceVATPayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    nazev_faktury = db.Column(db.String(520), nullable=True)

    evidencni_cislo = db.Column(db.String(120), nullable=True)
    typ_faktury = db.Column(db.String(120), nullable=True)

    jmeno_dodavatele = db.Column(db.String(120), nullable=True)
    adresa_dodavatele = db.Column(db.String(120), nullable=True)
    ico_dodavatele = db.Column(db.String(120), nullable=True)
    dic_dodavatele = db.Column(db.String(120), nullable=True)

    cislo_uctu = db.Column(db.String(120), nullable=True)

    datum_vystaveni = db.Column(db.Date, nullable=True)
    datum_splatnosti = db.Column(db.Date, nullable=True)
    datum_uzp = db.Column(db.Date, nullable=True)

    mena = db.Column(db.String(10), nullable=True)
    variabilni_symbol = db.Column(db.String(120), nullable=True)
    platebni_metoda = db.Column(db.String(120), nullable=True)

    zaokrouhleni = db.Column(db.String(120), nullable=True)
    rpdp = db.Column(db.String(120), nullable=True)

    vc_dph_21 = db.Column(db.String(120), nullable=True)
    bez_dph_21 = db.Column(db.String(120), nullable=True)
    dph_21 = db.Column(db.String(120), nullable=True)
    vc_dph_12 = db.Column(db.String(120), nullable=True)
    bez_dph_12 = db.Column(db.String(120), nullable=True)
    dph_12 = db.Column(db.String(120), nullable=True)
    bez_dph_0 = db.Column(db.String(120), nullable=True)
