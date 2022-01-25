from django.db import models

class Category(models.Model):
    map = models.ForeignKey('Map', on_delete=models.CASCADE, verbose_name='Mapa', related_name='categories')
    title = models.CharField(max_length=255, verbose_name='Título')
    description = models.TextField( verbose_name='Descrição')
    node_color = models.CharField(max_length=255, verbose_name='Cor do nó')
    order = models.IntegerField(default=0, null=True, blank=True, verbose_name='Ordem')

    min_size = models.FloatField(null=True, blank=True, verbose_name='Tamanho mínimo')
    max_size = models.FloatField(null=True, blank=True, verbose_name='Tamanho máximo')
    height_area = models.FloatField(null=True, blank=True, verbose_name='Altura da área')
    show = models.BooleanField(default=True, verbose_name='Exibir')
    
    nodes = models.ManyToManyField('Node', blank=True, verbose_name='Nós', related_name='categories')

    def __str__(self) -> str:
        return self.title if self.title else super().__str__()

    class Meta:
        verbose_name = "Camada"