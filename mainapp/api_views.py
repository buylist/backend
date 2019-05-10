from rest_framework import viewsets

from mainapp.models import Buyer
from mainapp.serializers import BuyerSerializer


class BuyerViewSet(viewsets.ModelViewSet):
    serializer_class = BuyerSerializer

    def get_queryset(self):
        # this gets user according to token
        # in this model it is useless, but in other it can be used to filter data
        user = self.request.user
        assert user
        return Buyer.objects.all().order_by('-modified')
