from rest_framework import routers

from mainapp.viewsets import (
    buyer, category, checklist, reciept, reciept_items,
    item, listitems, pattern, pattern_items)

app_name = 'apiv1'

router = routers.DefaultRouter()
router.register(r'users', buyer.BuyerViewSet, 'buyer')
router.register(r'categories', category.CategoryViewSet, 'category')
router.register(r'lists', checklist.ChecklistViewSet, 'list')
router.register(r'items', item.ItemViewSet, 'item')
router.register(r'checklists', listitems.ItemlistViewSet, 'checklist')
router.register(r'pattern', pattern.PatternViewSet, 'pattern')
router.register(r'pattern_item', pattern_items.ItemPatternViewSet, 'pattern_item')
router.register(r'reciept', reciept.RecieptViewSet, 'reciept')
router.register(r'reciept_item', reciept_items.ItemRecieptViewSet, 'reciept_item')
