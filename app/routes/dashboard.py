from flask import Blueprint, render_template
from flask_login import login_required
from ..models import Chamado

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def dashboard():
    total_chamados = Chamado.query.count()

    chamados_abertos = Chamado.query.filter(Chamado.hora_tratativa == None, Chamado.hora_finalizacao == None).count()

    chamados_em_atendimento = Chamado.query.filter(Chamado.hora_tratativa != None, Chamado.hora_finalizacao == None).count()

    chamados_fechados = Chamado.query.filter(Chamado.hora_finalizacao != None).count()

    return render_template('dashboard.html', 
                           total_chamados=total_chamados,
                           chamados_abertos=chamados_abertos,
                           chamados_em_atendimento=chamados_em_atendimento,
                           chamados_fechados=chamados_fechados)
