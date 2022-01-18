
from contrib.router import HybridRouter
from .map import MapViewSet, mini_maps
MapHybridRouter = HybridRouter()

MapHybridRouter.register('maps', MapViewSet, basename='maps')
