from rest_framework import serializers

from mainapp.models import Buyer, Checklist, Category, Item


class BuyerSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="mainapp:buyer-detail")

    class Meta:
        model = Buyer
        fields = ('url', 'username', 'is_active', 'created', 'modified')


class ChecklistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Checklist


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="mainapp:item-detail")
    buyer = serializers.HyperlinkedIdentityField(view_name='mainapp:buyer-detail')

    class Meta:
        model = Item
        fields = ('url', 'item_id', 'buyer', 'name', 'created', 'modified')
