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