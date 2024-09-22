import base64
import binascii
from flask import (
    Flask,
    flash,
    render_template,
    request,
    jsonify,
    redirect,
    send_file,
    session,
)
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import json
from sqlalchemy.dialects.postgresql import UUID
import uuid
import os
from flask_ipfilter import IPFilter, Whitelist
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import datetime
import os


app = Flask(__name__)
app.app_context().push()
db = SQLAlchemy()
load_dotenv()
import os


database_url = os.getenv("DATABASE_URI")
secret_key = os.getenv("SECRET_KEY")
app.config["SECRET_KEY"] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
ip_filter = IPFilter(app, ruleset=Whitelist())
ip_filter.ruleset.permit("127.0.0.1")

db.init_app(app)
# hier maak ik de encypted key
key = os.getenv("DATABASE_KEY")
fernet = Fernet(key)


class applicaties(db.Model):
    __tablename__ = "applicaties"
    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(120), nullable=False)
    ip = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"('{self.id}', '{self.naam}','{self.ip}')"


class bestanden(db.Model):
    __tablename__ = "bestanden"

    id = db.Column(db.Integer, primary_key=True)
    bestand = db.Column(db.String(120), nullable=False)
    omgevingen_id = db.Column(db.Integer, db.ForeignKey("omgevingen.id"))
    uuid = db.Column(db.String(36), unique=True, default=str(uuid.uuid4()))
    omgevingen = db.relationship(
        "omgevingen", backref=db.backref("bestanden", lazy=True)
    )
    applicaties_id = db.Column(db.Integer, db.ForeignKey("applicaties.id"))
    applicatie = db.relationship(
        "applicaties", backref=db.backref("bestanden", lazy=True)
    )

    def __repr__(self):
        return f"('{self.id}', '{self.bestand}','{self.omgevingen_id},{self.applicaties_id}')"


class register(db.Model):
    __tablename__ = "register"
    id = db.Column(db.Integer, primary_key=True)
    u_name = db.Column((db.String(120)), nullable=False)
    pass_word = db.Column((db.String(120)), nullable=False)

    def __init__(self, u_name, pass_word):

        self.u_name = fernet.encrypt(u_name.encode("utf-8"))
        self.pass_word = fernet.encrypt(pass_word.encode("utf-8"))

        return f"('{self.u_name}', '{self.pass_word}')"


class omgevingen(db.Model):
    __tablename__ = "omgevingen"
    id = db.Column(db.Integer, primary_key=True)
    test_omgeving = db.Column(db.String(120), nullable=False)
    productie_omgeving = db.Column(db.String(120), nullable=False)
    applicaties_id = db.Column(db.Integer, db.ForeignKey("applicaties.id"))
    applicatie = db.relationship(
        "applicaties", backref=db.backref("omgevingen", lazy=True)
    )

    def __repr__(self):
        return f"('{self.id}', '{self.test_omgeving}','{self.productie_omgeving}', '{self.applicaties_id}')"


class admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    adminname = db.Column(db.String(120), nullable=False)
    admin_pass = db.Column(db.String(120), nullable=False)

    # hier wordt de password en username geencrypt

    def __init__(self, adminname, admin_pass):
        self.adminname = fernet.encrypt(adminname.encode("utf-8"))
        self.admin_pass = fernet.encrypt(admin_pass.encode("utf-8"))

        return f"( '{self.adminname}','{self.admin_pass}')"


class logging(db.Model):
    __tablename__ = "logging"
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(120), nullable=False)
    omgeving = db.Column(db.String(120), nullable=False)
    tijdstip = db.Column(db.DateTime())

    melding = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"('{self.ip}','{self.id}', '{self.omgeving}','{self.tijdstip}',{self.melding})"


@app.route("/")
@app.route("/login", methods=["POST", "GET"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    adminname = request.form.get("adminname")
    adminpass = request.form.get("admin_pass")
    if request.method == "POST":
        if user(username, password):

            return redirect("/testcorrect")

        if admins(adminname, adminpass):
            flash("are you an administrator")
            return redirect("/applicaties")
        else:
            return render_template("login.html")

    return render_template("login.html")


def user(username, password):
    for i in register.query.all():
        usersname = fernet.decrypt(i.u_name).decode("utf-8")
        passsword = fernet.decrypt(i.pass_word).decode("utf-8")

        if username == usersname and password == passsword:

            return True
        else:

            return False


def admins(adminname, adminpass):
    for i in admin.query.all():
        adminname1 = fernet.decrypt(i.adminname).decode("utf-8")
        adminpass1 = fernet.decrypt(i.admin_pass).decode("utf-8")
        if adminname == adminname1 and adminpass1 == adminpass:
            return True
        else:
            return False


@app.route("/register", methods=["POST", "GET"])
def register_user():
    u_name = request.form.get("u_name")
    pass_word = request.form.get("pass_word")
    if request.method == "POST":
        new_register = register(u_name=u_name, pass_word=pass_word)

        db.session.add(new_register)
        db.session.commit()
        # print(fernet.decrypt(pass_word.encode("utf-8")), u_name)
        return render_template(
            "register.html",
            u_name=u_name,
            pass_word=pass_word,
        )
    if request.method == "GET":
        print("lukte n iet")
        return render_template("register.html", u_name=u_name, pass_word=pass_word)
    else:
        return print("lukte niet")


@app.route("/admin", methods=["POST", "GET"])
def register_admin():
    adminname = request.form.get("adminname")
    admin_pass = request.form.get("admin_pass")
    if request.method == "POST":
        new_admin = admin(adminname=adminname, admin_pass=admin_pass)

        db.session.add(new_admin)
        db.session.commit()
        # print(fernet.decrypt(pass_word.encode("utf-8")), u_name)
        return render_template(
            "admin.html",
            adminname=adminname,
            admin_pass=admin_pass,
        )
    if request.method == "GET":
        print("jij bent admin")
        return render_template("admin.html", adminname=adminname, admin_pass=admin_pass)
    else:
        return print("jij bent geen admin")


@app.route("/index")
def index():
    return render_template("app1.html")


@app.route("/testcorrect")
def testCorrect():
    if request.method == "GET":
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM applicaties")
        applications = cur.fetchall()
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM omgevingen")
        omgevingen = cur.fetchall()
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM bestanden")
        bestanden = cur.fetchall()
        return render_template(
            "testcorrect.html",
            applications=applications,
            omgevingen=omgevingen,
            bestanden=bestanden,
        )
    return render_template("testcorrect.html")


ip_filter = IPFilter(app, ruleset=Whitelist())

ip_filter.ruleset.permit("127.0.0.1")


@app.route("/")
def route_test():
    if ip_filter == "127.0.0.1":
        return "Allowed"
    else:
        "Not allowed"


@app.route("/applicaties", methods=["POST", "GET"])
def scherm_applicaties():
    if request.method == "GET":
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM applicaties")
        applications = cur.fetchall()
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM omgevingen")
        omgevingen = cur.fetchall()
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM bestanden")
        bestanden = cur.fetchall()
        return render_template(
            "applicaties.html",
            applications=applications,
            omgevingen=omgevingen,
            bestanden=bestanden,
        )
    if request.method == "POST":
        naam = request.form.get("naam")
        ip = request.form.get("ip")

        new_app = applicaties(naam=naam, ip=ip)

        db.session.add(new_app)

        db.session.commit()

        return render_template("applicaties.html", naam=naam, ip=ip)

    else:
        return render_template("applicaties.html", naam=naam, ip=ip)


@app.route("/pygame")
def pygame():
    return render_template("pygame.html")


@app.route("/applicaties/<id>", methods=["GET", "POST"])
def apps(id):
    if request.method == "GET":
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM applicaties WHERE id =?", (id,))
        result = cur.fetchone()
        if result:
            app = {"id": result[0], "naam": result[1], "ip": result[2]}

            return render_template("applicatie.html", app=app)

    return render_template("applicatie.html", app={})

    # if request.method == "POST":
    #     naam = request.form.get("naam")
    #     ip = request.form.get("ip")

    #     new_app = applicaties(naam=naam, ip=ip)

    #     db.session.add(new_app)

    #     db.session.commit()

    #     return render_template("app2.html", naam=naam, ip=ip)

    # else:
    #     return render_template("app2.html", naam=naam, ip=ip)


@app.route("/applicaties/<applicaties_id>/omgevingen", methods=["GET", "POST"])
def saves_omgevingen(applicaties_id):
    omgeving = None
    if request.method == "GET":
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM omgevingen WHERE applicaties_id=?", (applicaties_id,)
        )
        result = cur.fetchone()
        if result:
            omgeving = {
                "id": result[0],
                "testomgeving": result[1],
                "productieomgeving": result[2],
                "applicaties_id": result[3],
            }
            return render_template("omgevingen.html", omgeving=omgeving)
        else:
            return render_template("omgevingen.html", omgeving={})

    if request.method == "POST":
        test_omgeving = request.form.get("test_omgeving")
        productie_omgeving = request.form.get("productie_omgeving")
        applicaties_id = request.form.get("applicaties_id")
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")
        cur.execute(
            " INSERT INTO omgevingen (test_omgeving,productie_omgeving, applicaties_id) VALUES (?,?,?);",
            (test_omgeving, productie_omgeving, applicaties_id),
        )

        cur.fetchone()
        conn.commit()
        cur.close()

        return redirect("/index")


@app.route(
    "/applicaties/<applicaties_id>/omgevingen/<omgevingen_id>", methods=["GET", "POST"]
)
def open_bestand(applicaties_id, omgevingen_id):
    bestand = None
    if request.method == "GET":
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM bestanden WHERE applicaties_id =?", (applicaties_id,)
        )
        result = cur.fetchone()
        if result:
            bestand = {
                "applicaties_id": result[0],
                "bestandnaam": result[1],
                "omgevingen_id": result[2],
            }
            return render_template("bestand.html", bestand=bestand)
        else:
            return render_template("bestand.html", bestand=bestand)

    if request.method == "POST":
        bestandnaam = request.form.get("bestandnaam")
        print(bestandnaam)
        omgevingen_id = request.form.get("omgevingen_id")
        applicaties_id = request.form.get("applicaties_id")
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")
        cur.execute(
            " INSERT INTO bestanden (bestand,omgevingen_id,applicaties_id) VALUES (?,?,?);",
            (bestandnaam, omgevingen_id, applicaties_id),
        )

        cur.fetchone()
        conn.commit()
        cur.close()
        return redirect("/index")


@app.route("/api/download/<applicatie_id>/<omgevingen_id>/<bestand_uuid>")
def download(applicatie_id, omgevingen_id, bestand_uuid):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT bestand FROM bestanden")
    bestandnaam = cursor.fetchall()
    cursor.execute("SELECT id FROM omgevingen WHERE id=?", (omgevingen_id,))
    omgeving = cursor.fetchall()
    cursor.execute("SELECT ip FROM applicaties Where id=?", (applicatie_id,))
    ip = cursor.fetchone()
    cursor.close()
    conn.close()
    data3 = {"ip": ip, "bestand": bestandnaam, "omgeving": omgeving}

    if ip == "127.0.0.1":
        with open("bestand.txt", "w") as f:
            f.write(str(data3["bestand"]))
        return send_file("bestand.txt", as_attachment=True)
    else:
        with open("bestand.txt", "w") as f:
            f.write(str(data3["bestand"]))
        return send_file("bestand.txt", as_attachment=True)


@app.route("/api/logging", methods=["GET", "POST"])
def api_logging():
    if request.method == "GET":
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM logging")
        id = cursor.fetchall()
        cursor.execute("SELECT ip FROM logging")
        ip = cursor.fetchall()
        cursor.execute("SELECT omgeving FROM logging")
        omgeving = cursor.fetchall()
        cursor.execute("SELECT tijdstip FROM logging")
        tijdstip = cursor.fetchall()
        cursor.execute("SELECT melding FROM logging")
        melding = cursor.fetchall()
        return [
            {
                "id": id,
                "ip": ip,
                "omgeving": omgeving,
                "tijdstip": tijdstip,
                "melding": melding,
            }
        ]
    if request.method == "POST":
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM logging")
        id = cursor.fetchall()
        cursor.execute("SELECT ip FROM logging")
        ip = cursor.fetchall()
        cursor.execute("SELECT omgeving FROM logging")
        omgeving = cursor.fetchall()
        cursor.execute("SELECT tijdstip FROM logging")
        tijdstip = cursor.fetchall()
        cursor.execute("SELECT melding FROM logging")
        melding = cursor.fetchall()
        return [
            {
                "id": id,
                "ip": ip,
                "omgeving": omgeving,
                "tijdstip": tijdstip,
                "melding": melding,
            }
        ]


@app.route("/naam", methods=["POST", "GET"])
def a():

    naam = request.form.get("naam")
    print(naam)
    return render_template("naam.html", naam=naam)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
