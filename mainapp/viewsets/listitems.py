from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from django.conf import settings
from mainapp.models import ItemInChecklist, Checklist, Item, FromWebProdFields
from mainapp.parser.parser import Parser
from mainapp.viewsets.item import ItemSerializer


DEFAULT_USER = settings.CONFIG.get('DEFAULT_USER_ID', 0)


# Специальный класс, для чтения данных из базы, и выводе json с вложенными объектами
class ItemInChecklistSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="mainapp:checklist-detail", lookup_field='pk')
    item = ItemSerializer()

    class Meta:
        model = ItemInChecklist
        fields = ('url', 'quantity', 'unit', 'deleted', 'item')
        depth = 1


# Специальный класс, для добавление/удаления/обновления новых позиций в списке покупок
# Прописывание lookup_field  в данном случае не обязательно, так как по умолчанию ссылается на pk
class ChangeItemInChecklistSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="mainapp:checklist-detail", lookup_field='pk')
    item_name = serializers.CharField(required=False)
    checklist_name = serializers.CharField(required=False)
    mob_item_id = serializers.IntegerField(required=False)
    mob_check_id = serializers.IntegerField(required=False)

    class Meta:
        model = ItemInChecklist
        fields = (
            'url',
            'mob_item_id',
            'item_name',
            'mob_check_id',
            'checklist_name',
            'deleted',
            'quantity',
            'unit'
        )


class ItemlistViewSet(viewsets.ModelViewSet):
    queryset = ItemInChecklist.objects.all()
    serializer_class = ChangeItemInChecklistSerializer
    # lookup_field  в данном случае не обязательно, так как по умолчанию ссылается на pk
    lookup_field = 'pk'

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        try:
            item, _ = Item.objects.get_or_create(buyer_id=self.request.user.pk, name=data['item_name'],
                                       mobile_id=data['mob_item_id'])
            checklist = Checklist.objects.filter(buyer_id=self.request.user.pk, name=data['checklist_name'],
                                                 mobile_id=data['mob_check_id']).first()

            data.pop('item_name')
            data.pop('checklist_name')
            data.pop('mob_item_id')
            data.pop('mob_check_id')

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)

            serializer.validated_data['item_id'] = item.id
            serializer.validated_data['checklist_id'] = checklist.id

            self.perform_create(serializer)

            Parser.django_value_field_update(FromWebProdFields, self.get_queryset().filter(item=item,
                                                                                           checklist=checklist))

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print('ОШИБКА ЗАПИСИ В БАЗУ ДАННЫХ')
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": f"{e}"})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        data = request.data
        data.pop('item_name', False)
        data.pop('checklist_name', False)
        data.pop('mob_item_id', False)
        data.pop('mob_check_id', False)

        items_in_checklist = [instance]

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        Parser.django_value_field_update(FromWebProdFields, items_in_checklist)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
