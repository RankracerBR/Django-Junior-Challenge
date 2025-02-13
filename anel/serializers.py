from rest_framework import serializers
from .models import Anel


class AnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anel
        fields = ['id', 'nome_anel', 'poder_anel', 'portador_anel', 'forjadoPor_anel', 'imagem_anel']
