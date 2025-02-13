# ProjetoAneisPoder(Documentação)

### Esse projeto consiste em um CRUD, onde o usuário pode adicionar, ver, alterar e deletar aneis, uma certa inspiração em alguns conceitos de RPG

## Tecnologias utilizadas 

#### Django 

<img src="https://1000logos.net/wp-content/uploads/2020/08/Django-Logo.png" height="100px">

#### Django Rest Framework

<img src="https://www.django-rest-framework.org/img/logo.png"
height="100px">

#### Docker-Compose 

<img src="https://cdn4.iconfinder.com/data/icons/logos-and-brands/512/97_Docker_logo_logos-512.png"
height="100px">

#### Postgresql 

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Postgresql_elephant.svg/993px-Postgresql_elephant.svg.png"
height="100px">


#### Front-End

<img src="https://www.pikpng.com/pngl/b/597-5977109_html5-logo-png.png" 
height="100px">

### Estilização

<img src="https://techsparx.com/img/Bootstrap-Logo.png"
height="200px" width="300px">


 Além dessas linguagens houve a adição do <b>pre-commit</b>, uma ferramenta voltada a área de Dev-Ops, onde ela facilita e corrige erros a nível de código, extremamente importante quando se trabalha com mais desenvolvedores em um único repositório

# Informações Técnicas

## Parte 1: Como rodar o projeto?

#### primeiro abra o seu terminal e rode o seguinte comando primeiro(obs: para rodar os comandos abaixo, é necessário que o usuário tenha o docker-compose e python instalado na sua máquina):

```bash
docker compose up # Criar o container para o postgres

source bin/activate # ativa o ambiente virtual

# Caso dê errado o comando acima, tente esses seguintes comandos abaixo

python -m venv ProjetoAneisPoder

./Scripts/activate # Se estiver no windows

source bin/activate # Caso esteja em alguma distro linux



pip install -r requirements.txt # Instalar as depêndencias

python3 manage.py migrate # Migrar para o banco de dados as migrações

python3 manage.py runserver # Rodar a aplicação localmente
```

## Parte 2: Back-End

#### A estrutura base do projeto foi feita da seguinte maneira: foi criado o módulo 'anel' para configurações das views, ORM, rotas, serializer e renderização dos templates, segue o código abaixo da 'anel/models.py' e em sequência 'anel/views.py', 'anel/urls.py', 'anel/serializers.py' e 'anel/admin.py':

```python
from django.db import models


class Anel(models.Model):
    FORJADOR_CHOICES = [
        ('Elfos', 'Elfos'),
        ('Anões', 'Anões'),
        ('Homens', 'Homens'),
        ('Sauron', 'Sauron'),
    ]
    
    nome_anel = models.CharField(max_length=255) # Narya, o anel do fogo
    poder_anel = models.TextField() # Seu portador ganha resistência ao fogo
    portador_anel = models.CharField(max_length=255) # Gandalf
    forjadoPor_anel = models.CharField(max_length=50, choices=FORJADOR_CHOICES) # Elfos, Anões, Homens, Sauron
    imagem_anel = models.URLField(max_length=255)

    class Meta:
        verbose_name = "Anel"
        verbose_name_plural = "Aneis"
    
    def __str__(self):
        return self.nome_anel
```

```python
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
        # Extract data from request.POST
        data = {
            'nome_anel': request.POST.get('nome_anel'),
            'poder_anel': request.POST.get('poder_anel'),
            'portador_anel': request.POST.get('portador_anel'),
            'forjadoPor_anel': request.POST.get('forjadoPor_anel'),
            'imagem_anel': request.POST.get('imagem_anel'),
        }

        serializer = AnelSerializer(data=data)
        if serializer.is_valid():
            # Limite forjador
            forjador = serializer.validated_data['forjadoPor_anel']
            limite = {
                'Elfos': 3,
                'Anões': 7,
                'Homens': 9,
                'Sauron': 1,
            }.get(forjador, 0)  # if forjador mostra os valores, se não 0
            
            if Anel.objects.filter(forjadoPor_anel=forjador).count() >= limite:
                return Response(
                    {'error': f'Limite de anéis para {forjador} atingido.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save()
            return redirect('anel-listagem') 
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
            serializer = AnelSerializer(anel, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        anel = self.get_object(pk)
        if anel:
            anel.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
```

```python
from django.urls import path
from .views import AnelGeral, CriarAnelView, DetalheAnelView


urlpatterns = [
    path('aneis/', AnelGeral.as_view(), name='anel-listagem'),
    path('aneis/criar_anel/', CriarAnelView.as_view(), name='criar-anel'),
    path('aneis/<int:pk>/', DetalheAnelView.as_view(), name='detalhe-anel'),
]
```

```python

from rest_framework import serializers
from .models import Anel


class AnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anel
        fields = ['id', 'nome_anel', 'poder_anel', 'portador_anel', 'forjadoPor_anel', 'imagem_anel']

```

```python
from django.contrib import admin
from .models import Anel


@admin.register(Anel)
class AnelAdmin(admin.ModelAdmin):
    fields = ('nome_anel', 'poder_anel', 'portador_anel' ,  'forjadoPor_anel' , 'imagem_anel')
    list_display = ['nome_anel', 'forjadoPor_anel',]

```


## Parte 3: Front-end

#### O front-end base foi usado com HTML, CSS e JavaScript, os códigos em sequência são: 'index.html', 'form.html', 'detalhe_anel.html', após os templates, os arquivos estáticos em sequência são: 'script.js', 'anel_actions.js' e 'styles.css'

```html
{% load static %}
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Anéis do Poder</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="shortcut icon" type="image/png" href="{% static 'favi/favicon.ico' %}"/>
    <style>
        .carousel-item img {
            max-height: 400px;
            object-fit: cover;
        }
        .carousel-caption {
            background-color: rgba(0, 0, 0, 0.5);
            padding: 10px;
            border-radius: 5px;
        }

        .carousel-control-prev-icon,
        .carousel-control-next-icon {
            background-color: black;
            border-radius: 50%;
            padding: 10px;
        }

        .carousel-control-prev,
        .carousel-control-next {
            width: 5%;
        }
    </style>
</head>
<body>
    <div class="container mt-5">
        <h1>Anéis do Poder</h1>
        <a href="{% url 'criar-anel' %}" class="btn btn-primary mb-3">Criar Novo Anel</a>

        <!-- Bootstrap Carousel -->
        <div id="aneisCarousel" class="carousel slide" data-bs-ride="carousel">
            <div class="carousel-inner">
                {% for anel in aneis %}
                <div class="carousel-item {% if forloop.first %}active{% endif %}">
                    <!-- Clickable Image -->
                    <a href="{% url 'detalhe-anel' anel.id %}">
                        <img src="{{ anel.imagem_anel }}" class="d-block w-100" alt="{{ anel.nome_anel }}">
                    </a>
                    <!-- Carousel Caption -->
                    <div class="carousel-caption d-none d-md-block">
                        <h5>{{ anel.nome_anel }}</h5>
                        <p>
                            <strong>Poder:</strong> {{ anel.poder_anel }}<br>
                            <strong>Portador:</strong> {{ anel.portador_anel }}<br>
                            <strong>Forjado por:</strong> {{ anel.forjadoPor_anel }}
                        </p>
                    </div>
                </div>
                {% endfor %}
            </div>
            <!-- Carousel Controls -->
            <button class="carousel-control-prev" type="button" data-bs-target="#aneisCarousel" data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Anterior</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#aneisCarousel" data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Próximo</span>
            </button>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

```html
{% load static %}

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Criar Anel</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="shortcut icon" type="image/png" href="{% static 'favi/favicon.ico' %}"/>
</head>
<body>
    <div class="container mt-3">
        <a class="btn btn-primary mb-1" href="{% url 'anel-listagem' %}">Voltar</a>
    </div>
    <div class="container mt-4">
        <h1>Criar Anel</h1>
        <form method="post" enctype="multipart/form-data" id="anelForm">
            {% csrf_token %}
            <div class="mb-3">
                <label for="nome_anel" class="form-label">Nome</label>
                <input type="text" class="form-control" id="nome_anel" name="nome_anel" required>
            </div>
            <div class="mb-3">
                <label for="poder_anel" class="form-label">Poder</label>
                <textarea class="form-control" id="poder_anel" name="poder_anel" required></textarea>
            </div>
            <div class="mb-3">
                <label for="portador_anel" class="form-label">Portador</label>
                <input type="text" class="form-control" id="portador_anel" name="portador_anel" required>
            </div>
            <div class="mb-3">
                <label for="forjadoPor_anel" class="form-label">Forjado Por</label>
                <select class="form-select" id="forjadoPor_anel" name="forjadoPor_anel" required>
                    <option value="Elfos">Elfos</option>
                    <option value="Anões">Anões</option>
                    <option value="Homens">Homens</option>
                    <option value="Sauron">Sauron</option>
                </select>
            </div>
            <div class="mb-3">
                <label for="imagem_anel" class="form-label">Imagem (URL)</label>
                <input type="url" class="form-control" id="imagem_anel" name="imagem_anel" required>
            </div>
            <button type="submit" class="btn btn-success">Salvar</button>
        </form>
    </div>
    <script src="{% static 'js/script.js' %}"></script>
</body>
</html>
```

```html
{% load static %}

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Detalhe do Anel</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="shortcut icon" type="image/png" href="{% static 'favi/favicon.ico' %}"/>
</head>
<body>
    <div class="container mt-3">
        <a class="btn btn-primary mb-3" href="{% url 'anel-listagem' %}">Voltar</a>
    </div>
    <div class="container mt-5">
        <div class="card">
            <div class="card-header text-center">
                <h1 class="card-title">{{ anel.nome_anel }}</h1>
            </div>
            <div class="card-body">
                <form id="update-form">
                    {% csrf_token %}
                    <div class="mb-3">
                        <label for="nome_anel" class="form-label">Nome</label>
                        <input type="text" class="form-control" id="nome_anel" value="{{ anel.nome_anel }}">
                    </div>
                    <div class="mb-3">
                        <label for="poder_anel" class="form-label">Poder</label>
                        <textarea class="form-control" id="poder_anel">{{ anel.poder_anel }}</textarea>
                    </div>
                    <div class="mb-3">
                        <label for="portador_anel" class="form-label">Portador</label>
                        <input type="text" class="form-control" id="portador_anel" value="{{ anel.portador_anel }}">
                    </div>
                    <div class="mb-3">
                        <label for="forjadoPor_anel" class="form-label">Forjado Por</label>
                        <select class="form-select" id="forjadoPor_anel">
                            <option value="Elfos" {% if anel.forjadoPor_anel == 'Elfos' %}selected{% endif %}>Elfos</option>
                            <option value="Anões" {% if anel.forjadoPor_anel == 'Anões' %}selected{% endif %}>Anões</option>
                            <option value="Homens" {% if anel.forjadoPor_anel == 'Homens' %}selected{% endif %}>Homens</option>
                            <option value="Sauron" {% if anel.forjadoPor_anel == 'Sauron' %}selected{% endif %}>Sauron</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="imagem_anel" class="form-label">Imagem (URL)</label>
                        <input type="url" class="form-control" id="imagem_anel" value="{{ anel.imagem_anel }}">
                        <img src="{{ anel.imagem_anel }}" alt="{{ anel.nome_anel }}" class="img-fluid rounded" style="max-width: 300px;">
                    </div>
                    <button type="button" id="update-button" data-anel-id="{{ anel.id }}" class="btn btn-primary">Atualizar</button>
                    <button type="button" id="delete-button" data-anel-id="{{ anel.id }}" class="btn btn-danger">Deletar</button>
                </form>
            </div>
        </div>
    </div>
    <script src="{% static 'js/anel_actions.js' %}"></script>
</body>
</html>
```

```javascript
const API_URL = 'http://localhost:8000/aneis/';

async function loadAneis(){
    const response = await fetch(API_URL);
    const aneis = await response.json();
    const carouselInner = document.getElementById('carousel-inner');

    aneis.forEach((anel, index) => {
        const item = document.createElement('div');
        item.classList.add('carousel-item');

        if (index === 0) item.classList.add('active');

        item.innerHTML = `
                    <img src="${anel.imagem_anel}" class="d-block w-100" alt="${anel.nome_anel}">
            <div class="carousel-caption d-none d-md-block">
                <h5>${anel.nome_anel}</h5>
                <p>${anel.poder_anel}</p>
                <p>Portador: ${anel.portador_anel}</p>
                <p>Forjado por: ${anel.forjadoPor_anel}</p>
            </div>
        `;
        carouselInner.appendChild(item);
    })
}

document.addEventListener('DOMContentLoaded', loadAneis);
```

```javascript
async function updateAnel(anelId, updatedData) {
    try {
        const response = await fetch(`/aneis/${anelId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(updatedData),
        });

        if (response.ok) {
            alert('Anel atualizado com sucesso!');
            window.location.reload();
        } else {
            const errorData = await response.json();
            alert(`Erro ao atualizar: ${errorData.error || 'Erro desconhecido'}`);
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao atualizar o anel.');
    }
}

async function deleteAnel(anelId) {
    try {
        const response = await fetch(`/aneis/${anelId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        });

        if (response.ok) {
            alert('Anel deletado com sucesso!');
            window.location.href = '/aneis/';
        } else {
            const errorData = await response.json();
            alert(`Erro ao deletar: ${errorData.error || 'Erro desconhecido'}`);
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao deletar o anel.');
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
    const deleteButton = document.getElementById('delete-button');
    if (deleteButton) {
        deleteButton.addEventListener('click', function () {
            const anelId = this.dataset.anelId;
            if (confirm('Tem certeza que deseja deletar este anel?')) {
                deleteAnel(anelId);
            }
        });
    }

    const updateButton = document.getElementById('update-button');
    if (updateButton) {
        updateButton.addEventListener('click', function () {
            const anelId = this.dataset.anelId;
            const updatedData = {
                nome_anel: document.getElementById('nome_anel').value,
                poder_anel: document.getElementById('poder_anel').value,
                portador_anel: document.getElementById('portador_anel').value,
                forjadoPor_anel: document.getElementById('forjadoPor_anel').value,
                imagem_anel: document.getElementById('imagem_anel').value,
            };
            updateAnel(anelId, updatedData);
        });
    }
});
```

```css
.carousel-teim img {
    max-height: 500px;
    object-fit: cover;
}
```

## Parte 4: Testes Unitários

#### Sabe-se que testes unitários são extremamente importantes para testar a aplicação de ponta a ponta, o código abaixo mostra como foram feito os testes unitários, mas caso queira rodar os testes na sua máquina, apenas digite:

```bash
python manage.py test
```

#### Abaixo está o código dos testes unitários:

```python
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
            nome_anel='Anel do Poder',
            poder_anel='Invisibilidade',
            portador_anel='Frodo',
            forjadoPor_anel='Elfos',
            imagem_anel='imagem1.jpg'
        )
        self.anel2 = Anel.objects.create(
            nome_anel='Anel Único',
            poder_anel='Dominação',
            portador_anel='Sauron',
            forjadoPor_anel='Sauron',
            imagem_anel='imagem2.jpg'
        )

    def test_get_all_aneis(self):
        response = self.client.get(reverse('anel-listagem'))
        aneis = Anel.objects.all()
        serializer = AnelSerializer(aneis, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['aneis'], serializer.data)


class CriarAnelViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {
            'nome_anel': 'Anel do Poder',
            'poder_anel': 'Invisibilidade',
            'portador_anel': 'Frodo',
            'forjadoPor_anel': 'Elfos',
            'imagem_anel': 'http://example.com/imagem1.jpg'
        }
        self.invalid_payload = {
            'nome_anel': '',
            'poder_anel': '',
            'portador_anel': '',
            'forjadoPor_anel': '',
            'imagem_anel': ''
        }

    def test_create_valid_anel(self):
        response = self.client.post(reverse('criar-anel'), data=self.valid_payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Anel.objects.count(), 1)

    def test_create_invalid_anel(self):
        response = self.client.post(reverse('criar-anel'), data=self.invalid_payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Anel.objects.count(), 0)

    def test_create_anel_exceeds_limit(self):
        for _ in range(3):
            Anel.objects.create(
                nome_anel='Anel do Poder',
                poder_anel='Invisibilidade',
                portador_anel='Frodo',
                forjadoPor_anel='Elfos',
                imagem_anel='imagem1.jpg'
            )
        response = self.client.post(reverse('criar-anel'), data=self.valid_payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Anel.objects.count(), 3)


class DetalheAnelViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.anel = Anel.objects.create(
            nome_anel='Anel do Poder',
            poder_anel='Invisibilidade',
            portador_anel='Frodo',
            forjadoPor_anel='Elfos',
            imagem_anel='imagem1.jpg'
        )
        self.valid_payload = {
            'nome_anel': 'Anel Único',
            'poder_anel': 'Dominação',
            'portador_anel': 'Sauron',
            'forjadoPor_anel': 'Sauron',
            'imagem_anel': 'http://example.com/imagem2.jpg'
        }
    
        self.invalid_payload = {
            'nome_anel': '',
            'poder_anel': '',
            'portador_anel': '',
            'forjadoPor_anel': '',
            'imagem_anel': ''
        }

    def test_get_valid_single_anel(self):
        response = self.client.get(reverse('detalhe-anel', kwargs={'pk': self.anel.pk}))
        anel = Anel.objects.get(pk=self.anel.pk)
        serializer = AnelSerializer(anel)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['anel'], serializer.data)

    def test_get_invalid_single_anel(self):
        response = self.client.get(reverse('detalhe-anel', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_update_anel(self):
        response = self.client.put(
            reverse('detalhe-anel', kwargs={'pk': self.anel.pk}),
            data=self.valid_payload,
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_anel(self):
        response = self.client.put(
            reverse('detalhe-anel', kwargs={'pk': self.anel.pk}),
            data=self.invalid_payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_valid_anel(self):
        response = self.client.delete(
            reverse('detalhe-anel', kwargs={'pk': self.anel.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_anel(self):
        response = self.client.delete(
            reverse('detalhe-anel', kwargs={'pk': 30})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
```

## Parte 5(Opcional): Pre-Commit

#### Caso queira rodar na sua máquina o pre-commit, apenas digite esse código abaixo que ele irá fazer as correções no projeto:

```bash
pre-commit run --all-files
```

## Parte 6(Opcional): Painel Admin do Django

#### Caso queira analisar o painel do admin, primeiro digite o comando para criar um perfil de super usuário:

```bash
python manage.py createsuperuser
```

#### Após a criação irá aparecer algumas mensagens no terminal para você digitar o nome, email e senha, isso fica a seu critério

#### Após a criação do perfil, é necessário acessar a url: http/localhost:8000/admin/ para acessar a tela de login do admin, e então logar a conta do super usuário criada anteriormente, para então ter acesso ao painel