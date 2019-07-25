from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from django.db.utils import IntegrityError
from mainapp.models import Checklist, ItemInChecklist, FromWebProdFields, Category, Item
from mainapp.parser.parser import Parser
from mainapp.viewsets.listitems import ItemInChecklistSerializer


class ChecklistSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="mainapp:list-detail", lookup_field='pk')
    items = ItemInChecklistSerializer(many=True, required=False)

    class Meta:
        model = Checklist
        fields = ('url', 'name', 'mobile_id', 'items')
        depth = 2


class ChecklistViewSet(viewsets.ModelViewSet):
    serializer_class = ChecklistSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        chek = Checklist.objects.filter(buyer_id=self.request.user.pk).all()
        return chek

    def create(self, request, *args, **kwargs):
        print(f'request.data: {request.data}')
        try:
            exist_checklist = Checklist.objects.filter(buyer_id=self.request.user.pk,
                                                       name=self.request.data['name']).first()
            if exist_checklist:
                serializer = self.get_serializer(exist_checklist, data=request.data, partial=True)
                self.get_queryset().filter(name=self.request.data['name'])[0].items.all().delete()
            else:
                serializer = self.get_serializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            validated_items_in_list = serializer.validated_data.pop('items', False)
            serializer.validated_data['buyer_id'] = request.user.pk

            self.perform_create(serializer)

            checklist_obj = self.get_queryset().first()

            if validated_items_in_list:
                items_in_checklist = []
                for item_in_list in validated_items_in_list:
                    item = item_in_list.pop('item')
                    item['buyer_id'] = request.user.pk
                    item['category'], _ = Category.objects.update_or_create(mobile_id=item['mob_cat_id'],
                                                                            buyer_id=item['buyer_id'],
                                                                            defaults={'name': item['category']})
                    item.pop('mob_cat_id', False)

                    # если в БД не существует передаваемого в чек-лист товара, мы его передаём на создание,
                    # иначе обновляем
                    item_in_list['item'], _ = Item.objects.update_or_create(buyer_id=item['buyer_id'],
                                                                            mobile_id=item['mobile_id'],
                                                                            defaults=item)
                    item_in_list['checklist'] = checklist_obj

                    # передаем на создание в БД товары в чек-листе
                    items_in_checklist.append(ItemInChecklist(**item_in_list))

                ItemInChecklist.objects.bulk_create(items_in_checklist)

                Parser.django_value_field_update(FromWebProdFields, items_in_checklist)

            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError as e:
            print('ОШИБКА ЗАПИСИ В БАЗУ ДАННЫХ')
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": f"{e}"})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        print(f"\nобъект {instance}\n")
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        validated_items_in_list = serializer.validated_data.pop('items', False)
        serializer.validated_data['buyer_id'] = request.user.pk

        self.perform_update(serializer)

        checklist_obj = instance

        if validated_items_in_list:
            items_in_checklist = []
            for item_in_list in validated_items_in_list:
                item = item_in_list.pop('item')
                item['buyer_id'] = request.user.pk
                item['category'], _ = Category.objects.update_or_create(mobile_id=item['mob_cat_id'],
                                                                        buyer_id=item['buyer_id'],
                                                                        defaults={'name': item['category']})
                item.pop('mob_cat_id', False)

                # если в БД не существует передаваемого в чек-лист товара, мы его передаём на создание, иначе обновляем
                item_in_list['item'], _ = Item.objects.update_or_create(buyer_id=item['buyer_id'],
                                                                        mobile_id=item['mobile_id'],
                                                                        defaults=item)
                item_in_list['checklist'] = checklist_obj

                obj_to_update = ItemInChecklist.objects.filter(item=item_in_list['item'],
                                                               checklist=item_in_list['checklist']).first()

                for attr, value in item_in_list.items():
                    setattr(obj_to_update, attr, value)

                # передаем на создание в БД товары в чек-листе
                items_in_checklist.append(obj_to_update)

            ItemInChecklist.objects.bulk_update(items_in_checklist,
                                                [field for field in validated_items_in_list[0].keys()])

            Parser.django_value_field_update(FromWebProdFields, items_in_checklist)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
