from django.conf import settings
from django.db.utils import IntegrityError
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
import json
from mainapp.models import Item, Category
from mainapp.viewsets.category import CategorySerializer


DEFAULT_USER = settings.CONFIG.get('DEFAULT_USER_ID', 0)


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="mainapp:item-detail", lookup_field='pk')
    # category = CategorySerializer(many=False, required=False)
    # buyer_id = serializers.IntegerField()  #  По умолчанию эти поля только для чтения и не дает в них ниче записать
    # category_id = serializers.IntegerField() # А если их переопределить таким образом, то нормльно записывает...
    category = serializers.CharField(required=False)
    mob_cat_id = serializers.IntegerField(required=False)
    item_id = serializers.IntegerField(required=True)

    class Meta:
        model = Item
        fields = ('url', 'name', 'category', 'mob_cat_id', 'item_id')


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        q = Item.objects.filter(buyer_id=self.request.user.pk)
        # q = Item.objects.filter(buyer__in=(user, DEFAULT_USER,)).order_by('name', '-buyer').distinct('name')
        print(q.query)
        return q

    def get_category(self, category_name, mob_cat_id):
        category, _ = Category.objects.get_or_create(buyer_id=self.request.user.pk, name=category_name,
                                                     mobile_category_id=mob_cat_id)
        # category = Category.objects.filter(buyer__in=(
        #     DEFAULT_USER, self.request.user,)).filter(name=category_name, ).order_by('-buyer').first()
        # if not category:
        #     category = Category()
        #     category.buyer = self.request.user
        #     category.name = category_name
        #     last_category = Category.objects.filter(buyer_id=category.buyer).order_by('-category_id').first()
        #     category.category_id = last_category.category_id + 1 if last_category else 1
        #     category.save()
        return category

    def get_item_id(self, item_name):
        item = Item.objects.filter(buyer__in=(
            DEFAULT_USER, self.request.user,)).filter(name=item_name).order_by('-buyer').first()
        if item:
            item_id = item.item_id
        else:
            item = Item.objects.filter(buyer__in=(DEFAULT_USER, self.request.user, )).order_by('-item_id').first()
            item_id = item.item_id + 1
        return item_id

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['buyer_id'] = request.user.pk

            category_obj = self.get_category(serializer.validated_data['category'],
                                             serializer.validated_data['mob_cat_id'])

            serializer.validated_data['category'] = category_obj
            serializer.validated_data.pop('mob_cat_id')

            self.perform_create(serializer)
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
        serializer.validated_data['buyer_id'] = request.user.pk

        category_obj = self.get_category(serializer.validated_data['category'],
                                         serializer.validated_data['mob_cat_id'])

        serializer.validated_data['category'] = category_obj
        serializer.validated_data.pop('mob_cat_id')

        self.perform_update(serializer)

        return Response(serializer.data)

    # def partial_update(self, request, *args, **kwargs):
    #     print('*****МЕТОД АПДЕЙТ*****')
    #     print(kwargs)
    #     pk = kwargs.get('item_id')
    #     instance = Item.objects.filter(pk=pk).first()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #
    #     try:
    #         self.perform_update(serializer)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #
    #     except IntegrityError as e:
    #         print('ОШИБКА ЗАПИСИ В БАЗУ ДАННЫХ')
    #         return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": f"{e}"})
