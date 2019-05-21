from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from mainapp.models import Checklist, ItemInChecklist


class ChecklistSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="mainapp:list-detail", lookup_field='checklist_id')

    class Meta:
        model = Checklist
        fields = ('url', 'name', 'modified')


class ItemInChecklistSerializer(serializers.HyperlinkedIdentityField):

    class Meta:
        model = ItemInChecklist
        fields = ('quantity', 'unit')


class ChecklistViewSet(viewsets.ModelViewSet):
    serializer_class = ChecklistSerializer
    lookup_field = 'checklist_id'

    def get_queryset(self):
        return Checklist.objects.filter(buyer=self.request.user).order_by('-modified')

    def update(self, request, *args, **kwargs):
        serializer_context = {
            'request': request,
        }
        checklist_id = int(kwargs.get('checklist_id', None))
        try:
            instance = Checklist.objects.get(checklist_id=checklist_id)
            serializer = ChecklistSerializer(instance=instance, data=request.data, context=serializer_context)
        except Checklist.DoesNotExist:
            serializer = ChecklistSerializer(data=request.data, context=serializer_context)
        if serializer.is_valid():
            serializer.validated_data['checklist_id'] = checklist_id
            serializer.validated_data['buyer_id'] = request.user.pk
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('we made an error here')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated], url_name='items', url_path='items')
    def list_items(self, request, checklist_id=None):

        checklist = self.get_object()
        items = checklist.iteminchecklist_set.prefetch_related('item__name').values()
        print(items)
        print(checklist, checklist.checklist_id, checklist.pk, checklist.name)
        print('Checklist ID', checklist_id, request.data)

        context = {'request': request}

        serializer = ItemInChecklistSerializer(instance=items, many=True, context=context)

        # print('here', serializer.initial_data)

        return Response(serializer)

    @action(methods=[], detail=True, url_name='add', url_path='add')
    def add_item(self, request):
        pass

    @action(methods=[], detail=True, url_name='remove', url_path='remove')
    def remove_item(self, request):
        pass
