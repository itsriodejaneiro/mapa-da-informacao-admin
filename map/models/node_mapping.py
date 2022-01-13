from django.db import models


class NodeMapping(models.Model):
    source = models.ForeignKey('Node', on_delete=models.CASCADE, verbose_name='Nó de origem', related_name='source_mappings')
    target = models.ForeignKey('Node', on_delete=models.CASCADE, verbose_name='Nó de destino', related_name='target_mappings')
    context = models.CharField(max_length=255, null=True, blank=True, verbose_name='Contexto')
    map = models.ForeignKey('Map', on_delete=models.CASCADE, verbose_name='Mapa', related_name='node_mappings')

    def __str__(self) -> str:
        if self.source and self.target:
            return f"{self.source.title} -> {self.target.title} ({self.context})"
        return super().__str__()

    class Meta:
        verbose_name = "Mapeamento de nós"
        verbose_name_plural = "Mapeamentos de nós"
