from django.test import TestCase
from datetime import date
from .models import Paciente

class PacienteTestCase(TestCase):
    def test_criacao_paciente_e_calculo_idade(self):
        # Cria um paciente de teste
        paciente = Paciente.objects.create(
            nome_completo="Antônio Teste",
            data_nascimento=date(1950, 1, 15),  # 76 anos em 2026
            genero="M",
            cpf="111.111.111-11",
            telefone="(11) 11111-1111",
            condicao_medica="Nenhuma",
            medicamentos="Nenhum"
        )
        # Verifica se foi criado corretamente
        self.assertEqual(paciente.nome_completo, "Antônio Teste")
        self.assertGreaterEqual(paciente.idade, 75)
        self.assertLess(paciente.idade, 80)