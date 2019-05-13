from django.conf import settings
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response

from mainapp.models import Item, Category


DEFAULT_USER = settings.CONFIG.get('DEFAULT_USER_ID', 0)


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="mainapp:item-detail", lookup_field='item_id')

    class Meta:
        model = Item
        # fields = ('url', 'name', 'quantity', 'unit', 'checklist', 'modified',)
        fields = ('url', 'name', 'modified',)


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    lookup_field = 'item_id'

    def get_queryset(self):
        user = self.request.user
        q = Item.objects.filter(buyer__in=(user, DEFAULT_USER, )).order_by('name', '-buyer').distinct('name')
        print(q.query)
        return q

    def get_category_id(self, category_name):
        category = Category.objects.filter(buyer__in=(
            DEFAULT_USER, self.request.user,)).filter(name=category_name).order_by('-buyer').first()
        if not category:
            category = Category()
            category.buyer = self.request.user
            category.name = category_name
            last_category = Category.objects.filter(buyer_id=category.buyer).order_by('-category_id').first()
            category.category_id = last_category.category_id + 1 if last_category else 1
            category.save()
        return category

    def get_item_id(self, item_name, category):
        item = Item.objects.filter(buyer__in=(
            DEFAULT_USER, self.request.user,)).filter(name=item_name).order_by('-buyer').first()
        print(item.category, category, item.category == category)
        if item.category != category:
            item = None
        if not item:
            item = Item()
            item.name = item_name
            item.buyer = self.request.user
            item.category = category
            last_item = Item.objects.filter(buyer_id=item.buyer).order_by('-item_id').first()
            item.item_id = last_item.item_id + 1 if last_item else 1
            item.save()
        return item

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['buyer_id'] = request.user.pk
        category = self.get_category_id(request.data.get('category_name'))
        serializer.validated_data['category_id'] = category.pk
        item = self.get_item_id(request.data.get('name'), category)
        serializer.validated_data['item_id'] = item.item_id
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
