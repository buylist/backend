from django.conf import settings
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from django.db.utils import IntegrityError
from mainapp.models import Category

DEFAULT_USER = settings.CONFIG.get('DEFAULT_USER_ID', 0)


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='mainapp:category-detail', lookup_field='pk')

    class Meta:
        model = Category
        fields = ('url', 'name', 'modified', 'color')


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Category.objects.filter(
            buyer__in=(self.request.user, DEFAULT_USER,)
        ).order_by('name', '-buyer').distinct('name')

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer)
        serializer.validated_data['buyer_id'] = request.user.pk
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError as e:
            print('ОШИБКА ЗАПИСИ В БАЗУ ДАННЫХ')
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": f"{e}"})








