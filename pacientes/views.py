from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PacienteForm, ReceitaForm
from .models import Paciente
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm
import io
import json  # ← Novo import necessário
from django.db.models import Count, Avg  # ← Movido para o topo para ficar organizado

# Suas views existentes (mantidas exatamente como estavam)
def home(request):
    return render(request, 'pacientes/home.html')

def cadastro_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pacientes')
    else:
        form = PacienteForm()
    return render(request, 'pacientes/cadastro.html', {'form': form})

def lista_pacientes(request):
    pacientes = Paciente.objects.all().order_by('-data_cadastro')
    return render(request, 'pacientes/lista.html', {'pacientes': pacientes})

def gerar_receita(request):
    if request.method == 'POST':
        form = ReceitaForm(request.POST)
        if form.is_valid():
            # Criar o PDF
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=A4)
            width, height = A4

            # Cabeçalho com fundo azul
            p.setFillColor(colors.darkblue)
            p.rect(0, height - 3*cm, width, 3*cm, fill=1)
            p.setFillColor(colors.white)
            p.setFont("Helvetica-Bold", 20)
            p.drawCentredString(width/2, height - 2*cm, "Receita Médica")

            # Linha divisória
            p.setLineWidth(1)
            p.setStrokeColor(colors.grey)
            p.line(2*cm, height - 3.5*cm, width - 2*cm, height - 3.5*cm)

            # Informações do paciente e médico
            p.setFillColor(colors.black)
            p.setFont("Helvetica-Bold", 12)
            p.drawString(2*cm, height - 5*cm, "Paciente:")
            p.setFont("Helvetica", 12)
            p.drawString(7*cm, height - 5*cm, form.cleaned_data['paciente'].nome_completo)

            p.setFont("Helvetica-Bold", 12)
            p.drawString(2*cm, height - 6*cm, "Médico:")
            p.setFont("Helvetica", 12)
            p.drawString(7*cm, height - 6*cm, form.cleaned_data['medico'])

            # Adicionar CRM do médico
            p.setFont("Helvetica-Bold", 12)
            p.drawString(2*cm, height - 7*cm, "CRM:")
            p.setFont("Helvetica", 12)
            p.drawString(7*cm, height - 7*cm, form.cleaned_data['crm'])

            # Data ajustada para a linha seguinte
            p.setFont("Helvetica-Bold", 12)
            p.drawString(2*cm, height - 8*cm, "Data:")
            p.setFont("Helvetica", 12)
            p.drawString(7*cm, height - 8*cm, form.cleaned_data['data_receita'].strftime('%d/%m/%Y'))

            # Seção de prescrição
            p.setFillColor(colors.darkblue)
            p.setFont("Helvetica-Bold", 14)
            p.drawString(2*cm, height - 10*cm, "Prescrição")
            p.setLineWidth(0.5)
            p.setStrokeColor(colors.darkgrey)
            p.line(2*cm, height - 10.3*cm, width - 2*cm, height - 10.3*cm)

            # Texto da prescrição com bullets
            p.setFillColor(colors.black)
            p.setFont("Helvetica", 11)
            y = height - 11.5*cm
            for line in form.cleaned_data['prescricao'].split('\n'):
                p.drawString(2.5*cm, y, f"• {line}")
                y -= 0.6*cm
                if y < 2*cm:  # Nova página se necessário
                    p.showPage()
                    y = height - 2*cm

            # Rodapé
            p.setFillColor(colors.grey)
            p.setFont("Helvetica-Oblique", 9)
            p.drawCentredString(width/2, 1*cm, "Sistema de Gerenciamento do Recanto dos Idosos São Vicente de Paulo")
            p.setLineWidth(1)
            p.setStrokeColor(colors.grey)
            p.line(2*cm, 1.5*cm, width - 2*cm, 1.5*cm)

            # Finalizar PDF
            p.showPage()
            p.save()

            # Enviar o PDF como resposta
            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="receita_medica.pdf"'
            return response
    else:
        form = ReceitaForm()
    return render(request, 'pacientes/gerar_receita.html', {'form': form})

def remover_paciente(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)
    if request.method == 'POST':
        paciente.delete()
        return redirect('lista_pacientes')
    return render(request, 'pacientes/confirmar_remocao.html', {'paciente': paciente})


# --------- Passo 4: API REST Framework ----------
from rest_framework import viewsets
from .serializers import PacienteSerializer

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer


# ============ NOVA VIEW: DASHBOARD DE ANÁLISES DE DADOS (VERSÃO CORRIGIDA) ============
def dashboard(request):
    """
    View que exibe o dashboard com análises estatísticas dos pacientes.
    Dados preparados em JSON para uso seguro no JavaScript.
    """
    # Total de pacientes
    total_pacientes = Paciente.objects.count()

    # Idade média
    idade_media_agg = Paciente.objects.aggregate(Avg('idade'))
    idade_media = round(idade_media_agg['idade__avg'], 1) if idade_media_agg['idade__avg'] else 0

    # Distribuição por faixa etária (lista na ordem certa para o gráfico)
    faixas_etarias = [
        Paciente.objects.filter(idade__gte=60, idade__lte=69).count(),
        Paciente.objects.filter(idade__gte=70, idade__lte=79).count(),
        Paciente.objects.filter(idade__gte=80, idade__lte=89).count(),
        Paciente.objects.filter(idade__gte=90).count(),
    ]

    # Distribuição por gênero
    genero_dist = Paciente.objects.values('genero') \
                                 .annotate(count=Count('genero')) \
                                 .order_by('-count')

    # Preparar labels e dados do gênero para o JavaScript
    genero_labels = [item['genero'] or 'Não informado' for item in genero_dist]
    genero_dados = [item['count'] for item in genero_dist]

    context = {
        'total_pacientes': total_pacientes,
        'idade_media': idade_media,
        'faixas_etarias_json': json.dumps(faixas_etarias),
        'genero_labels_json': json.dumps(genero_labels),
        'genero_dados_json': json.dumps(genero_dados),
    }

    return render(request, 'pacientes/dashboard.html', context)
# ===================================================================