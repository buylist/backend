from rest_framework import routers

from mainapp.viewsets import buyer, category, checklist, item, listitems

app_name = 'apiv1'

router = routers.DefaultRouter()
router.register(r'users', buyer.BuyerViewSet, 'buyer')
router.register(r'categories', category.CategoryViewSet, 'category')
router.register(r'lists', checklist.ChecklistViewSet, 'list')
router.register(r'items', item.ItemViewSet, 'item')
router.register(r'checklists', listitems.ItemlistViewSet, 'checklist')
