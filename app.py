from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__, template_folder='templates')


# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pessoa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

# Settings for migrations
migrate = Migrate(app, db)

class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String, nullable=False)
    telefone = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    endereco = db.Column(db.String, nullable=False)

    def __init__(self, nome, telefone, email, endereco):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.endereco = endereco

@app.route("/")
def home():
    pessoa = Pessoa.query.all()
    return render_template("home.html", pessoa=pessoa)

#CREATE - CADASTRAR CLIENTE
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        add_pessoa = Pessoa(request.form['nome'], request.form['telefone'], request.form['email'], request.form['endereco'])
        db.session.add(add_pessoa)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")

#READ - VISUALIZAR CLIENTE
@app.route("/visualizar")
def visualizar():
    pessoa = Pessoa.query.all()
    return render_template("visualizar.html", pessoa=pessoa)

#UPDATE - ATUALIZAR CLIENTE
@app.route("/editar/<int:pessoa_id>", methods=["GET", "POST"])
def editar(pessoa_id):
    pessoa = Pessoa.query.get(pessoa_id)
    if request.method == "POST":
        pessoa.nome = request.form['nome']
        pessoa.telefone = request.form['telefone']
        pessoa.email = request.form['email']
        pessoa.endereco = request.form['endereco']
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("editar.html", pessoa=pessoa)

#DELETE - DELETAR CLIENTE
@app.route("/delete/<int:pessoa_id>")
def delete(pessoa_id):
    nome = Pessoa.query.filter_by(id=pessoa_id).first()
    db.session.delete(nome)
    db.session.commit()
    return redirect(url_for("home"))

with app.app_context():
    if __name__ == "__main__":
        app.run(debug=True)
        db.create_all()
