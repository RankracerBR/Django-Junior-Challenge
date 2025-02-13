from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Anel
from .serializers import AnelSerializer


class AnelGeralTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.anel1 = Anel.objects.create(
            nome_anel="Anel do Poder",
            poder_anel="Invisibilidade",
            portador_anel="Frodo",
            forjadoPor_anel="Elfos",
            imagem_anel="imagem1.jpg",
        )
        self.anel2 = Anel.objects.create(
            nome_anel="Anel Único",
            poder_anel="Dominação",
            portador_anel="Sauron",
            forjadoPor_anel="Sauron",
            imagem_anel="imagem2.jpg",
        )

    def test_get_all_aneis(self):
        response = self.client.get(reverse("anel-listagem"))
        aneis = Anel.objects.all()
        serializer = AnelSerializer(aneis, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["aneis"], serializer.data)


class CriarAnelViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {
            "nome_anel": "Anel do Poder",
            "poder_anel": "Invisibilidade",
            "portador_anel": "Frodo",
            "forjadoPor_anel": "Elfos",
            "imagem_anel": "http://example.com/imagem1.jpg",
        }
        self.invalid_payload = {
            "nome_anel": "",
            "poder_anel": "",
            "portador_anel": "",
            "forjadoPor_anel": "",
            "imagem_anel": "",
        }

    def test_create_valid_anel(self):
        response = self.client.post(
            reverse("criar-anel"), data=self.valid_payload, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Anel.objects.count(), 1)

    def test_create_invalid_anel(self):
        response = self.client.post(
            reverse("criar-anel"), data=self.invalid_payload, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Anel.objects.count(), 0)

    def test_create_anel_exceeds_limit(self):
        for _ in range(3):
            Anel.objects.create(
                nome_anel="Anel do Poder",
                poder_anel="Invisibilidade",
                portador_anel="Frodo",
                forjadoPor_anel="Elfos",
                imagem_anel="imagem1.jpg",
            )
        response = self.client.post(
            reverse("criar-anel"), data=self.valid_payload, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Anel.objects.count(), 3)


class DetalheAnelViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.anel = Anel.objects.create(
            nome_anel="Anel do Poder",
            poder_anel="Invisibilidade",
            portador_anel="Frodo",
            forjadoPor_anel="Elfos",
            imagem_anel="imagem1.jpg",
        )
        self.valid_payload = {
            "nome_anel": "Anel Único",
            "poder_anel": "Dominação",
            "portador_anel": "Sauron",
            "forjadoPor_anel": "Sauron",
            "imagem_anel": "http://example.com/imagem2.jpg",
        }

        self.invalid_payload = {
            "nome_anel": "",
            "poder_anel": "",
            "portador_anel": "",
            "forjadoPor_anel": "",
            "imagem_anel": "",
        }

    def test_get_valid_single_anel(self):
        response = self.client.get(reverse("detalhe-anel", kwargs={"pk": self.anel.pk}))
        anel = Anel.objects.get(pk=self.anel.pk)
        serializer = AnelSerializer(anel)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["anel"], serializer.data)

    def test_get_invalid_single_anel(self):
        response = self.client.get(reverse("detalhe-anel", kwargs={"pk": 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_update_anel(self):
        response = self.client.put(
            reverse("detalhe-anel", kwargs={"pk": self.anel.pk}),
            data=self.valid_payload,
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_anel(self):
        response = self.client.put(
            reverse("detalhe-anel", kwargs={"pk": self.anel.pk}),
            data=self.invalid_payload,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_valid_anel(self):
        response = self.client.delete(
            reverse("detalhe-anel", kwargs={"pk": self.anel.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_anel(self):
        response = self.client.delete(reverse("detalhe-anel", kwargs={"pk": 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
