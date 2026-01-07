from django.test import TestCase
from .models import Paciente

class PacienteModelTest(TestCase):
    def setUp(self):
        Paciente.objects.create(
            nome_completo="João da Silva",
            idade=78,
            genero="M"
            # adicione outros campos obrigatórios do seu model com valores válidos
        )

    def test_paciente_criado(self):
        paciente = Paciente.objects.get(nome_completo="João da Silva")
        self.assertEqual(paciente.idade, 78)
        self.assertIsNotNone(paciente.data_cadastro)
