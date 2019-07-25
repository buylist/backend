from django.urls import path, include
from django.contrib.auth.decorators import login_required
import mainapp.views as mainapp

from mainapp import router

app_name = 'mainapp'

urlpatterns = [
    path('api/v1/', include(router.router.urls)),
    path('', mainapp.Entrance.as_view(), name='entrance_page'),
    path('registration/', mainapp.register, name='registration_page'),
    path('web/', login_required(mainapp.MyProfile.as_view()), name='main_web_page'),
    path('web/checklists/', login_required(mainapp.WebChecklists.as_view()), name='checklists_web_page'),
    path('web/checklists/items/<pk>', login_required(mainapp.ItemsInChecklist.as_view()), name='items_web_page'),
    path('web/checklists/upd_check/<pk>', login_required(mainapp.ItemsInChecklist.upd_check), name='upd_check'),
    path('web/checklists/shared/<pk>/', mainapp.SharedItemsInChecklist.as_view(), name='shared_items'),
    path('web/checklists/share/<pk>/', login_required(mainapp.SharedItemsInChecklist.share), name='share'),
    path('web/checklists/noshare/<pk>/', login_required(mainapp.SharedItemsInChecklist.noshare), name='noshare'),
    path('web/checklists/pull_to_origin/<pk>/', login_required(mainapp.SharedItemsInChecklist.pull_shared_to_original),
         name='pull_to_origin'),
    path('web/checklists/share/save/<pk>/', mainapp.SharedItemsInChecklist.save_shared,
         name='save_shared'),
    path('web/patterns/', login_required(mainapp.Patterns.as_view()), name='patterns_web_page'),
]
