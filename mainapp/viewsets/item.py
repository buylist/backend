from django.conf import settings
from django.db import IntegrityError
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

    def get_category(self, category_name):
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

    def get_item_id(self, item_name):
        item = Item.objects.filter(buyer__in=(
            DEFAULT_USER, self.request.user,)).filter(name=item_name).order_by('-buyer').first()
        if item:
            item_id = item.item_id
        else:
            item = Item.objects.filter(buyer__in=(DEFAULT_USER, self.request.user, )).order_by('-item_id').first()
            item_id = item.item_id + 1
        return item_id

    def create(self, request, *args, **kwargs):
        category = self.get_category(request.data.get('category_name'))
        item_id = self.get_item_id(request.data.get('name'))

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data['buyer_id'] = request.user.pk
        serializer.validated_data['category_id'] = category.pk
        serializer.validated_data['item_id'] = item_id

        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError:
            instance = Item.objects.filter(buyer__in=(
                DEFAULT_USER, self.request.user,)).filter(item_id=item_id).order_by('-buyer').first()

            serializer = self.get_serializer(instance=instance, data=request.data)
            serializer.is_valid(raise_exception=True)

            serializer.validated_data['category_id'] = category.pk

            self.perform_update(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
