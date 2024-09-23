from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
from ..models import db, Chamado, Categoria, Servico, Historico, Cliente, User
from datetime import datetime
import pytz  

chamados_bp = Blueprint('chamados', __name__, url_prefix='/chamados')

@chamados_bp.route('/')
@login_required
def listar_chamados():
    chamados = Chamado.query.all()
    return render_template('listar_chamados.html', chamados=chamados)




@chamados_bp.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def tratar_chamado(id):
    chamado = Chamado.query.get_or_404(id)
    historico = Historico.query.filter_by(chamado_id=id).all()
    
    brasilia_tz = pytz.timezone('America/Sao_Paulo')

    if not chamado.operador_tratativa:
        chamado.operador_tratativa = current_user.username
        chamado.hora_tratativa = datetime.now(brasilia_tz)


        historico_tratativa = Historico(
            chamado_id=id,
            usuario_id=current_user.id,  
            comentario='Início da tratativa',
            data_interacao=chamado.hora_tratativa
        )
        db.session.add(historico_tratativa)
        db.session.commit()

    if request.method == 'POST':
        comentario = request.form.get('comentario', '').strip()

  
        if comentario:
            usuario = User.query.get(current_user.id)
            if not usuario:
                flash('Usuário inválido, por favor, verifique as credenciais.', 'danger')
                return redirect(url_for('chamados.tratar_chamado', id=id))

            try:
                # Adiciona o comentário ao histórico
                novo_historico = Historico(
                    chamado_id=id,
                    usuario_id=current_user.id,
                    comentario=comentario,
                    data_interacao=datetime.now(brasilia_tz)
                )
                db.session.add(novo_historico)
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao adicionar comentário: {e}', 'danger')

        
        if 'finalizar' in request.form:
            if not chamado.operador_finalizacao:
                chamado.operador_finalizacao = current_user.username
                chamado.hora_finalizacao = datetime.now(brasilia_tz)
                chamado.status = 'Fechado'
                historico_finalizacao = Historico(
                    chamado_id=id,
                    usuario_id=current_user.id,
                    comentario='Chamado finalizado',
                    data_interacao=chamado.hora_finalizacao
                )
                db.session.add(historico_finalizacao)
                flash('Chamado finalizado com sucesso!', 'success')
            else:
                flash('Chamado já está finalizado!', 'warning')

        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            flash('Erro ao salvar o comentário ou finalizar o chamado. Verifique se os dados são válidos e tente novamente.', 'danger')
            print(e)  # Para debugging no console

        return redirect(url_for('chamados.tratar_chamado', id=id))

    return render_template('tratar_chamado.html', chamado=chamado, historico=historico)


@chamados_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo_chamado():
    categorias = Categoria.query.all()
    clientes = Cliente.query.all()

    # Calcula o próximo ID de solicitação
    solicitacao_id = Chamado.query.count() + 1  # Gera um novo ID de solicitação

    # Define o fuso horário de Brasília
    brasilia_tz = pytz.timezone('America/Sao_Paulo')
    data_hora_abertura = datetime.now(brasilia_tz).strftime('%Y-%m-%d %H:%M:%S')

    if request.method == 'POST':
        titulo = f"N°{solicitacao_id}"  
        descricao = request.form['descricao']
        categoria_id = request.form['categoria']
        servico_id = request.form['servico']
        cliente_id = request.form['cliente']

        novo_chamado = Chamado(
            titulo=titulo,
            descricao=descricao,
            categoria_id=categoria_id,
            servico_id=servico_id,
            cliente_id=cliente_id,
            operador_tratativa=current_user.username  
        )
        db.session.add(novo_chamado)
        db.session.commit()
        flash('Chamado criado com sucesso!', 'success')
        return redirect(url_for('chamados.listar_chamados'))
    
    return render_template('novo_chamado.html', categorias=categorias, clientes=clientes, solicitacao_id=solicitacao_id, data_hora_abertura=data_hora_abertura)

@chamados_bp.route('/finalizar/<int:id>', methods=['POST'])
@login_required
def finalizar_chamado(id):
    chamado = Chamado.query.get_or_404(id)
    
    #horário de Brasília
    brasilia_tz = pytz.timezone('America/Sao_Paulo')

    chamado.status = 'Fechado'
    chamado.operador_finalizacao = current_user.username
    chamado.hora_finalizacao = datetime.now(brasilia_tz)

    historico_finalizacao = Historico(
        chamado_id=id,
        usuario_id=current_user.id,
        comentario='Chamado finalizado',
        data_interacao=chamado.hora_finalizacao
    )
    db.session.add(historico_finalizacao)

    try:
        db.session.commit()
        flash('Chamado finalizado com sucesso.', 'success')
    except IntegrityError as e:
        db.session.rollback()
        flash('Erro ao finalizar o chamado. Verifique se os dados são válidos e tente novamente.', 'danger')
        print(e)  #dbug

    return redirect(url_for('chamados.listar_chamados'))
