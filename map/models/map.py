from django.db import models

class Map(models.Model):
    title = models.CharField(max_length=255, verbose_name='Título')
    synopsis = models.TextField(verbose_name='Sinopse')
    project_cover = models.ImageField(upload_to='map/project_cover', verbose_name='Capa do projeto')
    
    # Drafting
    draft_password = models.CharField(max_length=255, blank=True, null=True, verbose_name='Senha de rascunho')
    url_map = models.CharField(max_length=255, blank=True, null=True, verbose_name='URL do mapa')
    
    # Seo
    title_seo = models.CharField(max_length=255, blank=True, null=True, verbose_name='Título SEO')
    description_seo = models.CharField(max_length=255, blank=True, null=True, verbose_name='Descrição SEO')
    site_name_seo = models.CharField(max_length=255, blank=True, null=True, verbose_name='Nome do site SEO')
    image_seo = models.ImageField(upload_to='map/image_seo', blank=True, null=True, verbose_name='Imagem SEO')
    

    def __str__(self) -> str:
        return self.title if self.title else super().__str__()


    class Meta:
        verbose_name = "Mapa"
