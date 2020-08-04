from rest_framework import viewsets

from vinegar_cellar.models import BarrelSet, Barrel
from .serializers import BarrelSetSerializer

class BarrelSetViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = BarrelSetSerializer
    queryset = BarrelSet.objects.all()


#from rest_framework.generics import (
#    ListAPIView,
#    RetrieveAPIView,
#    CreateAPIView,
#    DestroyAPIView,
#    UpdateAPIView
#    )


#class ArticleListView(ListAPIView):
#    queryset = Article.objects.all()
#    serializer_class = ArticleSerializer


#class ArticleDetailView(RetrieveAPIView):
#    queryset = Article.objects.all()
#    serializer_class = ArticleSerializer


#class ArticleCreateView(CreateAPIView):
#    queryset = Article.objects.all()
#    serializer_class = ArticleSerializer

#class ArticleUpdateView(UpdateAPIView):
#    queryset = Article.objects.all()
#    serializer_class = ArticleSerializer

#class ArticleDeleteView(DestroyAPIView):
#    queryset = Article.objects.all()
#    serializer_class = ArticleSerializer
