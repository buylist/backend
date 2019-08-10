from django.urls import path, include
from django.contrib.auth.decorators import login_required
import mainapp.views as mainapp

from mainapp import router

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.Entrance.as_view(), name='entrance_page'),
    path('web/registration/', mainapp.register, name='registration_page'),
    path('web/', login_required(mainapp.MyProfile.as_view()), name='main_web_page'),
    # path('web/checklists/', login_required(mainapp.WebChecklists.as_view()), name='checklists_web_page'),
    path('web/checklists/items/<pk>', login_required(mainapp.ItemsInChecklist.as_view()), name='items_web_page'),
    path('web/checklists/upd_check/<pk>', login_required(mainapp.ItemsInChecklist.upd_check), name='upd_check'),
    path('web/checklists/shared/<pk>/', mainapp.SharedItemsInChecklist.as_view(), name='shared_items'),
    path('web/checklists/share/<pk>/', mainapp.SharedItemsInChecklist.share_web, name='share'),
    path('web/checklists/noshare/<pk>/', mainapp.SharedItemsInChecklist.noshare_web, name='noshare'),
    path('web/checklists/pull_to_origin/<pk>/', login_required(mainapp.SharedItemsInChecklist.pull_shared_to_original),
         name='pull_to_origin'),
    path('web/checklists/share/save/<pk>/', mainapp.SharedItemsInChecklist.save_shared,
         name='save_shared'),
    # path('web/patterns/', login_required(mainapp.Patterns.as_view()), name='patterns_web_page'),
    path('api/v1/', include(router.router.urls)),
    path('api/checklists/share/', mainapp.SharedItemsInChecklist.share_api, name='share_api'),
    path('api/checklists/noshare/', mainapp.SharedItemsInChecklist.noshare_api, name='noshare_api'),
    path('api/checklists/pull_to_origin/', mainapp.SharedItemsInChecklist.pull_shared_to_original_api,
         name='pull_to_origin_api'),
]
