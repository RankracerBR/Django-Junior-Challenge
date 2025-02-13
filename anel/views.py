from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from .models import Anel
from .serializers import AnelSerializer


class AnelGeral(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    def get(self, request):
        aneis = Anel.objects.all()
        serializer = AnelSerializer(aneis, many=True)
        return Response({'aneis': serializer.data})


class CriarAnelView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'form.html'

    def get(self, request):
        return Response()

    def post(self, request):
        data = {
            'nome_anel': request.POST.get('nome_anel'),
            'poder_anel': request.POST.get('poder_anel'),
            'portador_anel': request.POST.get('portador_anel'),
            'forjadoPor_anel': request.POST.get('forjadoPor_anel'),
            'imagem_anel': request.POST.get('imagem_anel'),
        }

        print("Request Data:", data)  # Debugging

        serializer = AnelSerializer(data=data)
        if serializer.is_valid():
            forjador = serializer.validated_data['forjadoPor_anel']
            limite = {
                'Elfos': 3,
                'Anões': 7,
                'Homens': 9,
                'Sauron': 1,
            }.get(forjador, 0)

            if Anel.objects.filter(forjadoPor_anel=forjador).count() >= limite:
                return Response(
                    {'error': f'Limite de anéis para {forjador} atingido.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()
            return redirect('anel-listagem')
        print("Serializer Errors:", serializer.errors)  # Debugging
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetalheAnelView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'detalhe_anel.html'

    def get_object(self, pk):
        try:
            return Anel.objects.get(pk=pk)
        except Anel.DoesNotExist:
            return None
    
    def get(self, request, pk):
        anel = self.get_object(pk)
        if anel:
            serializer = AnelSerializer(anel)
            return Response({'anel': serializer.data})
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        anel = self.get_object(pk)
        if anel:
            print("Request Data:", request.data)  # Debugging
            serializer = AnelSerializer(anel, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            print("Serializer Errors:", serializer.errors)  # Debugging
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        anel = self.get_object(pk)
        if anel:
            anel.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
