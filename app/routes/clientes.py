from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from app.models import Cliente, Equipamento
from app import db

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes/novo', methods=['GET', 'POST'])
def novo_cliente():
    if request.method == 'POST':
        nome = request.form.get('nome')
        endereco = request.form.get('endereco')
        cnpj = request.form.get('cnpj')
        conta_sigma = request.form.get('conta_sigma')
        equipamentos_nomes = request.form.getlist('equipamentos')

        # Verifica se o CNPJ já está cadastrado
        if Cliente.query.filter_by(cnpj=cnpj).first():
            flash('CNPJ já cadastrado!', 'danger')
            return redirect(url_for('clientes.novo_cliente'))

        novo_cliente = Cliente(nome=nome, endereco=endereco, cnpj=cnpj, conta_sigma=conta_sigma)
        db.session.add(novo_cliente)
        db.session.commit()

        # Adiciona os equipamentos associados
        for equipamento_nome in equipamentos_nomes:
            if equipamento_nome.strip():  # Ignora equipamentos vazios
                equipamento = Equipamento(nome=equipamento_nome.strip(), cliente_id=novo_cliente.id)
                db.session.add(equipamento)
        
        db.session.commit()
        flash('Cliente criado com sucesso!', 'success')
        return redirect(url_for('clientes.listar_clientes'))
    
    # Carregar todos os clientes para a seleção
    clientes = Cliente.query.all()
    return render_template('novo_cliente.html', clientes=clientes)




@clientes_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()  # Recupera todos os clientes do banco de dados
    return render_template('listar_clientes.html', clientes=clientes)


@clientes_bp.route('/clientes/editar/<int:cliente_id>', methods=['GET', 'POST'])
def editar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    if request.method == 'POST':
        cliente.nome = request.form.get('nome')
        cliente.endereco = request.form.get('endereco')
        cliente.cep = request.form.get('cep')
        cliente.cnpj = request.form.get('cnpj')
        cliente.conta_sigma = request.form.get('conta_sigma')
        
        db.session.commit()
        flash('Cliente atualizado com sucesso!', 'success')
        return redirect(url_for('clientes.listar_clientes'))
    
    return render_template('editar_cliente.html', cliente=cliente)

@clientes_bp.route('/clientes/excluir/<int:cliente_id>', methods=['GET', 'POST'])
def excluir_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente excluído com sucesso!', 'success')
    return redirect(url_for('clientes.listar_clientes'))


@clientes_bp.route('/<int:cliente_id>', methods=['GET'])
def obter_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)
    if cliente:
        cliente_data = {
            "id": cliente.id,
            "nome": cliente.nome,
            "cnpj": cliente.cnpj,
            "endereco": cliente.endereco,
            "conta_sigma": cliente.conta_sigma
        }
        return jsonify(cliente_data)
    else:
        return jsonify({"error": "Cliente não encontrado"}), 404