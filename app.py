from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# /// = relative path, //// = absolute path

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    telefone = db.Column(db.String, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    endereco = db.Column(db.String, nullable=False)

    def __init__(self, nome, telefone, data_nascimento, email, endereco):
        self.nome = nome
        self.telefone = telefone
        self.data_nascimento = data_nascimento
        self.email = email
        self.endereco = endereco

@app.route("/")
def home():
    pessoa = Pessoa.query.all()
    return render_template("base.html", pessoa=pessoa)

#CREATE - CADASTRAR CLIENTE
@app.route("/add", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        nova_pessoa = Pessoa(request.form['nome'], request.form['telefone'], request.form['data_nascimento'], request.form['email'], request.form['endereco'])
        db.session.add(nova_pessoa)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("adicionar.html")

#READ - VISUALIZAR CLIENTE
@app.route("/visualizar")
def read():
    pessoa = Pessoa.query.all()
    return render_template("visualizar.html", pessoa=pessoa)

#UPDATE - ATUALIZAR CLIENTE
@app.route("/update/<int:pessoa_id>", methods=["GET", "POST"])
def update(pessoa_id):
    pessoa = Pessoa.query.get(pessoa_id)
    if request.method == "POST":
        pessoa.nome = request.form['nome']
        pessoa.telefone = request.form['telefone']
        pessoa.data_nascimento = request.form['data_nascimento']
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