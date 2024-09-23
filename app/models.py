from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  # Importa db corretamente depois de inicializado no contexto do app


class Chamado(db.Model):
    __tablename__ = 'chamados'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey('servicos.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    data_abertura = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    data_atendimento = db.Column(db.DateTime)
    data_fechamento = db.Column(db.DateTime)
    
    
    operador_tratativa = db.Column(db.String(100))  
    hora_tratativa = db.Column(db.DateTime)         
    operador_finalizacao = db.Column(db.String(100)) 
    hora_finalizacao = db.Column(db.DateTime)        

    categoria = db.relationship('Categoria', backref='chamados')
    servico = db.relationship('Servico', backref='chamados')
    cliente = db.relationship('Cliente', backref='chamados')

    def __repr__(self):
        return f'<Chamado {self.titulo}>'




class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    descricao = db.Column(db.String(200))

    def __repr__(self):
        return f'<Categoria {self.nome}>'

class Servico(db.Model):
    __tablename__ = 'servicos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(200))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    categoria = db.relationship('Categoria', backref=db.backref('servicos', lazy=True))

    def __repr__(self):
        return f'<Servico {self.nome}>'



class Historico(db.Model):
    __tablename__ = 'historicos'
    id = db.Column(db.Integer, primary_key=True)
    chamado_id = db.Column(db.Integer, db.ForeignKey('chamados.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    data_interacao = db.Column(db.DateTime, default=datetime.utcnow)
    comentario = db.Column(db.Text)

    chamado = db.relationship('Chamado', backref='historico')
    usuario = db.relationship('User', backref='historico')  



class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200))
    cnpj = db.Column(db.String(20), unique=True, nullable=False)
    conta_sigma = db.Column(db.String(50))
    cep = db.Column(db.String(10))
    equipamentos = db.relationship('Equipamento', backref='cliente', lazy=True)

    def __repr__(self):
        return f'<Cliente {self.nome}>'

class Equipamento(db.Model):
    __tablename__ = 'equipamentos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)

    def __repr__(self):
        return f'<Equipamento {self.nome}>'


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    perfil = db.Column(db.String(20), nullable=False)

    @property
    def password(self):
        raise AttributeError('Senha não pode ser lida diretamente!')

    @password.setter
    def password(self, password):
        print(f"[INFO] Gerando hash para a senha: {password}")  
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        print(f"[INFO] Verificando senha para o usuário {self.username}")  
        print(f"[INFO] Hash armazenado: {self.password_hash}")  
        print(f"[INFO] Senha fornecida: {password}")  
        result = check_password_hash(self.password_hash, password)
        print(f"[INFO] Resultado da verificação: {result}") 
        return result

    def is_admin(self):
        return self.perfil == 'admin'

    def is_analista(self):
        return self.perfil == 'analista'

    def is_tecnico(self):
        return self.perfil == 'tecnico'

    def is_cliente(self):
        return self.perfil == 'cliente'

    def __repr__(self):
        return f'<User {self.username}>'