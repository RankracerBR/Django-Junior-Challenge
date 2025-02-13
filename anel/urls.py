from django.urls import path

from .views import AnelGeral, CriarAnelView, DetalheAnelView

urlpatterns = [
    path("", AnelGeral.as_view(), name="anel-listagem"),
    path("aneis/criar_anel/", CriarAnelView.as_view(), name="criar-anel"),
    path("aneis/<int:pk>/", DetalheAnelView.as_view(), name="detalhe-anel"),
]
