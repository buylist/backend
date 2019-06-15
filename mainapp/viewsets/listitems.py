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
        fields = ('url', 'quantity', 'unit', 'item_id', 'checklist_id', 'modified', 'deleted', 'value')


class ItemlistViewSet(viewsets.ModelViewSet):
    queryset = ItemInChecklist.objects.all()
    serializer_class = ChangeItemInChecklistSerializer
    lookup_field = 'pk'

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        try:
            item = Item.objects.filter(buyer_id=self.request.user.pk).filter(name=data['item']).first()
            checklist = Checklist.objects.filter(buyer_id=self.request.user.pk).filter(name=data['checklist']).first()

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            serializer.validated_data['item_id'] = item.id
            serializer.validated_data['checklist_id'] = checklist.id
            print(serializer.validated_data)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print('ОШИБКА ЗАПИСИ В БАЗУ ДАННЫХ')
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": f"{e}"})



