from rest_framework import serializers, viewsets

from mainapp.models import Buyer


class BuyerSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="mainapp:buyer-detail")

    class Meta:
        model = Buyer
        fields = ('url', 'username', 'is_active', 'created', 'modified')


class BuyerViewSet(viewsets.ModelViewSet):
    serializer_class = BuyerSerializer

    def get_queryset(self):
        # this gets user according to token
        # in this model it is useless, but in other it can be used to filter data
        user = self.request.user
        assert user
        return Buyer.objects.all().order_by('-modified')
