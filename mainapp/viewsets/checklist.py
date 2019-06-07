from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.utils import IntegrityError
from mainapp.models import Checklist, ItemInChecklist
from mainapp.viewsets.listitems import ItemInChecklistSerializer


class ChecklistSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="mainapp:list-detail", lookup_field='pk')
    items = ItemInChecklistSerializer(many=True, required=False)

    class Meta:
        model = Checklist
        fields = ('url', 'name', 'items')
        # depth = 1


class ChecklistViewSet(viewsets.ModelViewSet):
    serializer_class = ChecklistSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        chek = Checklist.objects.all().prefetch_related('items').filter(buyer_id=self.request.user.id)
        return chek

    def create(self, request, *args, **kwargs):
        print(request.data)
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            print(serializer.validated_data)
            serializer.validated_data['buyer_id'] = request.user.pk
            serializer.validated_data['checklist_id'] = request.data['checklist_id']

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError as e:
            print('ОШИБКА ЗАПИСИ В БАЗУ ДАННЫХ')
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": f"{e}"})

