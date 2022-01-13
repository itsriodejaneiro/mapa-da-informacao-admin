from django.db import models


class Node(models.Model):
    title = models.CharField(max_length=255, verbose_name='Título')
    label = models.CharField(max_length=255, verbose_name='Rótulo')
    text = models.TextField(verbose_name='Texto')

    x_position = models.FloatField(null=True, blank=True, verbose_name='Posição X')
    y_position = models.FloatField(null=True, blank=True, verbose_name='Posição Y')

    namespace = models.CharField(max_length=255, null=True, blank=True)
    index = models.IntegerField(null=True, blank=True)

    button_icon = models.FileField(upload_to='node/button_icon', null=True, blank=True, verbose_name='Ícone do botão')
    button_text = models.CharField(max_length=255, null=True, blank=True, verbose_name='Texto do botão')
    button_link = models.CharField(max_length=255, null=True, blank=True, verbose_name='Link do botão')

    def __str__(self) -> str:
        return self.title if self.title else super().__str__()

    class Meta:
        verbose_name = "Nó"
