from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from mainapp.models import Reciept, ItemInReciept, Item
from mainapp.viewsets.item import ItemSerializer


class ItemInRecieptSerializer(serializers.HyperlinkedModelSerializer):
    """
    Специальный класс, для чтения данных из базы,
    и выводе json с вложенными объектами
    """
    url = serializers.HyperlinkedIdentityField(view_name="mainapp:reciept_item-detail", lookup_field='pk')
    item = ItemSerializer()

    class Meta:
        model = ItemInReciept
        fields = ('url', 'quantity', 'unit', 'item', 'deleted')
        depth = 1


class ChangeItemInRecieptSerializer(serializers.HyperlinkedModelSerializer):
    """
    Специальный класс, для
    добавление/удаления/обновления новых позиций в шаблоне покупок
    """
    url = serializers.HyperlinkedIdentityField(
        view_name="mainapp:reciept_item-detail", lookup_field='pk')

    class Meta:
        model = ItemInReciept
        fields = (
            'url', 'quantity', 'unit', 'item_id',
            'reciept_id', 'modified', 'deleted', 'value')


class ItemRecieptViewSet(viewsets.ModelViewSet):
    queryset = ItemInReciept.objects.all()
    serializer_class = ChangeItemInRecieptSerializer
    lookup_field = 'pk'

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)

        try:
            item = Item.objects.filter(buyer_id=self.request.user.pk).filter(name=data['item']).first()
            pattern = Reciept.objects.filter(
                buyer_id=self.request.user.pk).filter(
                name=data['reciept']).first()

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            serializer.validated_data['item_id'] = item.id
            serializer.validated_data['reciept_id'] = pattern.id
            print(serializer.validated_data)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers)

        except Exception as e:
            print('ОШИБКА ЗАПИСИ В БАЗУ ДАННЫХ')
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data={"error": f"{e}"})


