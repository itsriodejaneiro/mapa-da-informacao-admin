from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Título')
    description = models.TextField( verbose_name='Descrição')
    node_color = models.CharField(max_length=255, verbose_name='Cor do nó')
    order = models.IntegerField(default=0, verbose_name='Ordem')

    min_size = models.FloatField(null=True, blank=True, verbose_name='Tamanho mínimo')
    max_size = models.FloatField(null=True, blank=True, verbose_name='Tamanho máximo')
    height_area = models.FloatField(null=True, blank=True, verbose_name='Altura da área')
    show = models.BooleanField(default=True, verbose_name='Exibir')
    
    # todo:
    # nodes

    def __str__(self) -> str:
        return self.title if self.title else super().__str__()

    class Meta:
        verbose_name = "Categoria"