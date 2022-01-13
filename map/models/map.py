from django.db import models

class Map(models.Model):
    title = models.CharField(max_length=255)
    synopsis = models.TextField()
    project_cover = models.ImageField(upload_to='map/project_cover')
    
    # Drafting
    draft_password = models.CharField(max_length=30, blank=True, null=True)
    url_map = models.CharField(max_length=50, blank=True, null=True)
    
    # Seo
    title_seo = models.CharField(max_length=50, blank=True, null=True)
    description_seo = models.CharField(max_length=50, blank=True, null=True)
    site_name_seo = models.CharField(max_length=50, blank=True, null=True)
    image_seo = models.ImageField(upload_to='map/image_seo', blank=True, null=True)
    
    # todo:
    # categories
    # node_mapping

    def __str__(self) -> str:
        return self.title if self.title else super().__str__()


    class Meta:
        verbose_name = "Mapa"
