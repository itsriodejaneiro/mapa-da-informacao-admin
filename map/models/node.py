from django.db import models


class Node(models.Model):
    title = models.CharField(max_length=255, verbose_name='Título')
    label = models.CharField(max_length=255, verbose_name='Rótulo')
    text = models.TextField(null=True, blank=True, verbose_name='Texto')

    x_position = models.FloatField(null=True, blank=True, verbose_name='Posição X')
    y_position = models.FloatField(null=True, blank=True, verbose_name='Posição Y')

    namespace = models.CharField(max_length=255, null=True, blank=True)
    index = models.IntegerField(null=True, blank=True)

    button_icon = models.FileField(upload_to='node/button_icon', null=True, blank=True, verbose_name='Ícone do botão')
    button_text = models.CharField(max_length=255, null=True, blank=True, verbose_name='Texto do botão')
    button_link = models.CharField(max_length=255, null=True, blank=True, verbose_name='Link do botão')

    _id = models.CharField(max_length=255, null=True, blank=True, verbose_name='ID antigo') # todo remove
    def __str__(self) -> str:
        try:
            fields = self.namespace, self.label, self.index
            fields = list(filter(lambda s: s is not None and str(s).strip(), fields))
            return ' - '.join(fields)
        except:
            return self.title if self.title else super().__str__()

    class Meta:
        verbose_name = "Nó"
