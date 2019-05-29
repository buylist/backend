from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.utils import IntegrityError
from mainapp.models import Checklist, ItemInChecklist
from mainapp.viewsets.listitems import ItemInChecklistSerializer


class ChecklistSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="mainapp:list-detail", lookup_field='checklist_id')
    items = ItemInChecklistSerializer(many=True, required=False)

    class Meta:
        model = Checklist
        fields = ('url', 'name', 'items')
        # depth = 1


class ChecklistViewSet(viewsets.ModelViewSet):
    serializer_class = ChecklistSerializer
    lookup_field = 'checklist_id'

    def get_queryset(self):
        chek = Checklist.objects.all().prefetch_related('items').filter(buyer_id=self.request.user.id)
        return chek

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

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.validated_data['buyer_id'] = request.user.pk
        serializer.validated_data['checklist_id'] = request.data['checklist_id']
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError as e:
            print('ОШИБКА ЗАПИСИ В БАЗУ ДАННЫХ')
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": f"{e}"})

