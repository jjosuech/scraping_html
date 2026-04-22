from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import urlparse
import os

class CustomImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        # Obtén el nombre original del archivo desde la URL
        image_name = os.path.basename(urlparse(request.url).path)

        # Guarda el archivo en la carpeta 'imgvape' con el nombre original
        return f"imgvape/{image_name}"
