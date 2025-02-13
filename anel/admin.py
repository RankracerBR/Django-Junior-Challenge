from django.contrib import admin

from .models import Anel


@admin.register(Anel)
class AnelAdmin(admin.ModelAdmin):
    fields = (
        "nome_anel",
        "poder_anel",
        "portador_anel",
        "forjadoPor_anel",
        "imagem_anel",
    )
    list_display = [
        "nome_anel",
        "forjadoPor_anel",
    ]
