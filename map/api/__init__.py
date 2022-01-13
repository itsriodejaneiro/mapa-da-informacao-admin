
from contrib.router import HybridRouter
from .map import MapViewSet
MapHybridRouter = HybridRouter()

MapHybridRouter.register('maps', MapViewSet, basename='maps')
