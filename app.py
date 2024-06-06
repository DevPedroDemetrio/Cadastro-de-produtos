
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cadastros'

db = SQLAlchemy(app)

#criando tabelas no banco de dados
class cadastros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto = db.Column(db.String(50))
    categoria = db.Column(db.String(50))
    quantidade = db.Column(db.Integer)

    def __init__(self, produto, categoria, quantidade):
        self.produto = produto
        self.categoria = categoria
        self.quantidade = quantidade

@app.route("/")
def index():
    return render_template("index.html")
    

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':  
        produto = request.form.get('produto')
        categoria = request.form.get('categoria')
        quantidade = request.form.get('quantidade')
        
        dados = cadastros(produto = produto,
                         categoria = categoria,
                         quantidade = quantidade)
        db.session.add(dados)
        db.session.commit()
        return redirect(url_for('lista'))
    

    return render_template("cadastro.html")

@app.route("/<int:id>/atualizar", methods=['GET', 'POST'])
def atualizar(id):
    dados = cadastros.query.filter_by(id=id).first()
    if request.method == 'POST':  
        produto = request.form.get('produto')
        categoria = request.form.get('categoria')
        quantidade = request.form.get('quantidade')

        cadastros.query.filter_by(id=id).update({"produto": produto,
            "categoria": categoria, "quantidade": quantidade})
        db.session.commit()    
        return redirect(url_for('lista')) 
        
    return render_template("atualizar.html", dado=dados)

@app.route("/lista")
def lista():
    return render_template("lista.html", cadastro=cadastros.query.all())

@app.route("/<int:id>/excluir")
def excluir(id):
    dados = cadastros.query.filter_by(id=id).first()
    db.session.delete(dados)
    db.session.commit()
    return redirect(url_for('lista'))
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)