from django.conf import settings
from rest_framework import serializers, viewsets

from mainapp.models import Category


DEFAULT_USER = settings.CONFIG.get('DEFAULT_USER_ID', 0)


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='mainapp:category-detail', lookup_field='category_id')

    class Meta:
        model = Category
        fields = ('url', 'name', 'modified')


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    lookup_field = 'category_id'

    def get_queryset(self):
        return Category.objects.filter(
            buyer__in=(self.request.user, DEFAULT_USER,)
        ).order_by('name', '-buyer').distinct('name')
