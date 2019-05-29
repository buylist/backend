from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from mainapp.models import ItemInChecklist, Checklist, Category, Item
from mainapp.viewsets.category import CategoryViewSet
from mainapp.viewsets.item import ItemSerializer
from django.db.utils import IntegrityError


DEFAULT_USER = settings.CONFIG.get('DEFAULT_USER_ID', 0)


# Специальный класс, для чтения данных из базы, и выводе json с вложенными объектами
class ItemInChecklistSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="mainapp:checklist-detail", lookup_field='pk')
    item = ItemSerializer()

    class Meta:
        model = ItemInChecklist
        fields = ('url', 'quantity', 'unit', 'item', 'delete')
        depth = 1


# Специальный класс, для добавление/удаления/обновления новых позиций в списке покупок
class ChangeItemInChecklistSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="mainapp:checklist-detail", lookup_field='pk')

    class Meta:
        model = ItemInChecklist
        fields = ('url', 'quantity', 'unit', 'item_id', 'checklist_id', 'modified', 'delete')


class ItemlistViewSet(viewsets.ModelViewSet):
    serializer_class = ChangeItemInChecklistSerializer
    lookup_field = 'pk'

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        item = Item.objects.filter(buyer_id=self.request.user.pk).filter(name=data['item']).first()
        print(item.id, item.pk, item.name)
        checklist = Checklist.objects.filter(buyer_id=self.request.user.pk).filter(name=data['checklist']).first()
        print(checklist.id, checklist.pk, checklist.name)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        print(f'Cерилизатор => {serializer}')
        print(f'Валидатная дата => {serializer.validated_data}')
        serializer.validated_data['item_id'] = item.id
        serializer.validated_data['checklist_id'] = checklist.id

        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError as e:
            print('ОШИБКА ЗАПИСИ В БАЗУ ДАННЫХ')
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": f"{e}"})

    def partial_update(self, request, *args, **kwargs):
        print('*****МЕТОД АПДЕЙТ*****')
        print(kwargs)
        pk = kwargs.get('pk')
        instance = ItemInChecklist.objects.filter(pk=pk).first()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except IntegrityError as e:
            print('ОШИБКА ЗАПИСИ В БАЗУ ДАННЫХ')
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": f"{e}"})

