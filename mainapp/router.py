from rest_framework import routers

from mainapp import api_views

app_name = 'apiv1'

router = routers.DefaultRouter()
router.register(r'users', api_views.BuyerViewSet, 'buyer')
