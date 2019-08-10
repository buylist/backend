from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.http import Http404, JsonResponse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.views.generic.edit import FormView, CreateView
from rest_framework.authentication import TokenAuthentication
from mainapp.models.checklists import Checklist, ItemInChecklist, ItemsInShared
from mainapp.models.parser import FromWebProdFields
from mainapp.models.users import Buyer
from mainapp.models.patterns import Pattern, ItemInPattern
from mainapp.models.reciepts import Reciept, ItemInReciept
from socializer.forms import LoginForm, RegisterForm
from mainapp.parser.parser import Parser
from decimal import Decimal
import hashlib
import os
import json

# Create your views here.


class Entrance(FormView):
    template_name = 'web_templates/entrance.html'
    form_class = LoginForm
    success_url = reverse_lazy('socializer:login')

    def get(self, request, *args, **kwargs):

        if request.user in Buyer.objects.filter(email='anonymous@anonymous.ru'):
            auth.logout(request)

        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            buyer = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
            if buyer and buyer.is_active:
                auth.login(request, buyer)
                request.session.set_expiry(0)
            return self.form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('mainapp:entrance_page'))
        else:
            print(form.errors)

    else:
        form = RegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'web_templates/register_form.html', context)


class MyProfile(ListView):
    model = Checklist
    template_name = 'web_templates/main_page.html'
    context_object_name = 'checklists'

    def get(self, request, *args, **kwargs):

        if request.user in Buyer.objects.filter(email='anonymous@anonymous.ru'):
            auth.logout(request)

        self.object_list = self.get_queryset().filter(buyer=request.user)
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })

        patterns = Pattern.objects.filter(buyer=request.user)
        reciepts = Reciept.objects.filter(buyer=request.user)

        context = self.get_context_data(**kwargs)
        context['user'] = request.user
        context['page_title'] = 'BuyList for you'
        context['patterns'] = patterns
        context['reciepts'] = reciepts
        return self.render_to_response(context)


# class WebChecklists(ListView):
#     model = Checklist
#     template_name = 'web_templates/checklists.html'
#     context_object_name = 'checklists'
#     # paginate_by = 100
#
#     def get(self, request, *args, **kwargs):
#
#         if request.user in Buyer.objects.filter(email='anonymous@anonymous.ru'):
#             auth.logout(request)
#
#         self.object_list = self.get_queryset().filter(buyer=request.user)
#         allow_empty = self.get_allow_empty()
#
#         if not allow_empty:
#             if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
#                 is_empty = not self.object_list.exists()
#             else:
#                 is_empty = not self.object_list
#             if is_empty:
#                 raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
#                     'class_name': self.__class__.__name__,
#                 })
#         context = self.get_context_data()
#         context['user'] = request.user
#         return self.render_to_response(context)


class ItemsInChecklist(ListView):
    model = ItemInChecklist
    template_name = 'web_templates/items_in_check.html'
    context_object_name = 'items_in_checklist'

    @classmethod
    def upd_check(cls, request, pk):
        check = Checklist.objects.filter(pk=pk).first()

        items_in_checklist = []

        for obj in ItemInChecklist.objects.filter(checklist=check):
            if obj.quantity != Decimal(request.POST['quantity_' + str(obj.item.pk)]):
                obj.quantity = Decimal(request.POST['quantity_' + str(obj.item.pk)])
                obj.save()
            if obj.unit != request.POST['unit_' + str(obj.item.pk)]:
                obj.unit = request.POST['unit_' + str(obj.item.pk)]
                obj.save()

            items_in_checklist.append(obj)

        Parser.django_value_field_update(FromWebProdFields, items_in_checklist)

        return HttpResponseRedirect(request.headers['Referer'])

    def get(self, request, pk=0, **kwargs):

        if request.user in Buyer.objects.filter(email='anonymous@anonymous.ru'):
            auth.logout(request)

        check = Checklist.objects.get(pk=pk, buyer=request.user)
        self.object_list = self.get_queryset().filter(checklist=check)
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        context['user'] = request.user
        context['checklist'] = check

        return self.render_to_response(context)


class SharedItemsInChecklist(ListView):
    model = ItemsInShared
    template_name = 'web_templates/shared_items_in_check.html'
    context_object_name = 'items_in_checklist'

    @classmethod
    @csrf_exempt
    def share_api(cls, request):
        def create_shared_link(pk, buyer):
            obj_to_share = Checklist.objects.get(pk=pk, buyer=buyer)
            obj_to_share.share = hashlib.sha256(os.urandom(1024)).hexdigest()
            obj_to_share.save()

            for_bulk = []

            for item in ItemInChecklist.objects.filter(checklist=obj_to_share):
                for_bulk.append(
                    ItemsInShared(item=item.item, checklist=obj_to_share, quantity=item.quantity, unit=item.unit))

            ItemsInShared.objects.filter(checklist=obj_to_share).delete()
            ItemsInShared.objects.bulk_create(for_bulk)

            print(f'SHARE Created ItemsInShare {ItemsInShared.objects.filter(checklist=obj_to_share)}')

            return obj_to_share.share

        if request.method != 'POST':
            return HttpResponse(status=400)
        else:
            token_auth = TokenAuthentication()
            buyer, _ = token_auth.authenticate(request)
            data = json.loads(request.body)

            pk = Checklist.objects.get(mobile_id=data['mobile_id'], buyer=buyer).pk

            code = create_shared_link(pk, buyer)

            return HttpResponse(JsonResponse({"uri": reverse('mainapp:shared_items', args=(pk,))+'?share='+code}))

    @classmethod
    @csrf_exempt
    def noshare_api(cls, request):
        def del_shared_link(pk, buyer):
            if 'return' in request.GET and request.GET['return'] == 'yes':
                redirect_uri = request.headers['Referer']

            obj_to_share = Checklist.objects.get(pk=pk, buyer=buyer)
            obj_to_share.share = ''
            obj_to_share.save()

            ItemsInShared.objects.filter(checklist=obj_to_share).delete()

            print(f'NOSHARE Deleted from ItemsInShare {ItemsInShared.objects.filter(checklist=obj_to_share)}')

        if request.method != 'POST':
            return HttpResponse(status=400)
        else:
            token_auth = TokenAuthentication()
            buyer, _ = token_auth.authenticate(request)
            data = json.loads(request.body)

            pk = Checklist.objects.get(mobile_id=data['mobile_id'], buyer=buyer).pk

            del_shared_link(pk, buyer)

            return HttpResponse(JsonResponse({"uri": "deleted"}))

    @classmethod
    @csrf_exempt
    def pull_shared_to_original_api(cls, request):
        if request.method == "POST":
            token_auth = TokenAuthentication()
            buyer, _ = token_auth.authenticate(request)

            data = json.loads(request.body)
            print(f" data {data}")

            check = Checklist.objects.get(mobile_id=data['mobile_id'], buyer=buyer)

            original_objects = ItemInChecklist.objects.filter(checklist=check)
            shared_objects = ItemsInShared.objects.filter(checklist=check)
            if len(shared_objects) == 0:
                return HttpResponse(JsonResponse({'response': 'no shared objects to merge'}), status=400)

            for item in original_objects:
                setattr(item, 'quantity', shared_objects.get(item=item.item).quantity)
                setattr(item, 'unit', shared_objects.get(item=item.item).unit)
                item.save()

            return HttpResponse(JsonResponse({'response': 'shared merged with origin'}))
        return HttpResponse(JsonResponse({'response': 'incorrect request'}), status=400)

    @classmethod
    def pull_shared_to_original(cls, request, pk=0):
        check = Checklist.objects.get(pk=pk)

        if request.user == check.buyer:

            original_objects = ItemInChecklist.objects.filter(checklist=check)
            shared_objects = ItemsInShared.objects.filter(checklist=check)

            for item in original_objects:
                setattr(item, 'quantity', shared_objects.get(item=item.item).quantity)
                setattr(item, 'unit', shared_objects.get(item=item.item).unit)
                item.save()

        return HttpResponseRedirect(reverse('mainapp:items_web_page', args=(pk,)))

    @classmethod
    def share_web(cls, request, pk=0):
        def create_shared_link(pk, buyer):
            obj_to_share = Checklist.objects.get(pk=pk, buyer=buyer)
            obj_to_share.share = hashlib.sha256(os.urandom(1024)).hexdigest()
            obj_to_share.save()

            for_bulk = []

            for item in ItemInChecklist.objects.filter(checklist=obj_to_share):
                for_bulk.append(
                    ItemsInShared(item=item.item, checklist=obj_to_share, quantity=item.quantity, unit=item.unit))

            ItemsInShared.objects.filter(checklist=obj_to_share).delete()
            ItemsInShared.objects.bulk_create(for_bulk)

            print(f'SHARE Created ItemsInShare {ItemsInShared.objects.filter(checklist=obj_to_share)}')

            return obj_to_share.share

        if request.method == "GET" and pk != 0:
            redirect_uri = reverse('mainapp:checklists_web_page')

            if 'return' in request.GET and request.GET['return'] == 'yes':
                redirect_uri = request.headers['Referer']

            create_shared_link(pk, request.user)

            return HttpResponseRedirect(redirect_uri)
        return HttpResponse(JsonResponse({'response': 'incorrect request'}), status=400)

    @classmethod
    def noshare_web(cls, request, pk=0):
        def del_shared_link(pk, buyer):
            if 'return' in request.GET and request.GET['return'] == 'yes':
                redirect_uri = request.headers['Referer']

            obj_to_share = Checklist.objects.get(pk=pk, buyer=buyer)
            obj_to_share.share = ''
            obj_to_share.save()

            ItemsInShared.objects.filter(checklist=obj_to_share).delete()

            print(f'NOSHARE Deleted from ItemsInShare {ItemsInShared.objects.filter(checklist=obj_to_share)}')

        if request.method == "GET" and pk != 0:
            redirect_uri = reverse('mainapp:checklists_web_page')

            if 'return' in request.GET and request.GET['return'] == 'yes':
                redirect_uri = request.headers['Referer']

            del_shared_link(pk, request.user)

            return HttpResponseRedirect(redirect_uri)
        return HttpResponse(JsonResponse({'response': 'incorrect request'}), status=400)

    @classmethod
    def save_shared(cls, request, pk=0):
        shared_check = Checklist.objects.get(pk=pk)
        if shared_check.share and shared_check.share == request.GET['share']:
            shared_objects = ItemsInShared.objects.filter(checklist=shared_check)
            for obj in shared_objects:
                if obj.quantity != Decimal(request.POST['quantity_' + str(obj.item.pk)]):
                    obj.quantity = Decimal(request.POST['quantity_' + str(obj.item.pk)])
                    obj.save()
                if obj.unit != request.POST['unit_' + str(obj.item.pk)]:
                    obj.unit = request.POST['unit_' + str(obj.item.pk)]
                    obj.save()
            print(f' SAVED changes in ItemsInShare \n{shared_objects.values_list()}\n')
        return HttpResponseRedirect(request.headers['Referer'])

    def get(self, request, pk=0, **kwargs):

        if request.user not in Buyer.objects.all():
            if not Buyer.objects.filter(email='anonymous@anonymous.ru'):
                anonymous = Buyer.objects.create(email='anonymous@anonymous.ru', username='anonymous',
                                                 password=os.urandom(10))
            else:
                anonymous = Buyer.objects.filter(email='anonymous@anonymous.ru').first()

            auth.login(request, anonymous)

        obj_to_share = Checklist.objects.get(pk=pk)

        if request.GET['share'] and request.GET['share'] == obj_to_share.share and obj_to_share.share:
            self.object_list = self.get_queryset().filter(checklist_id=pk)
            allow_empty = self.get_allow_empty()

            if not allow_empty:
                if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                    is_empty = not self.object_list.exists()
                else:
                    is_empty = not self.object_list
                if is_empty:
                    raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                        'class_name': self.__class__.__name__,
                    })
            context = self.get_context_data()
            context['user'] = request.user
            context['checklist'] = obj_to_share
            return self.render_to_response(context)
        else:
            return HttpResponse('you have no perms for this page', status=401)


# class Patterns(ListView):
#     model = Pattern
#     template_name = 'web_templates/patterns.html'
#     # paginate_by = 100
#
#     def get(self, request, *args, **kwargs):
#         self.object_list = self.get_queryset().filter(buyer=request.user)
#         allow_empty = self.get_allow_empty()
#
#         if not allow_empty:
#             if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
#                 is_empty = not self.object_list.exists()
#             else:
#                 is_empty = not self.object_list
#             if is_empty:
#                 raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
#                     'class_name': self.__class__.__name__,
#                 })
#         context = self.get_context_data()
#         context['user'] = request.user
#         return self.render_to_response(context)
