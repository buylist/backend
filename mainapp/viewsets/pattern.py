from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from django.db.utils import IntegrityError
from mainapp.models import Pattern
from mainapp.viewsets.pattern_items import ItemInPatternSerializer


class PatternSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="mainapp:pattern-detail", lookup_field='pk')
    items_pattern = ItemInPatternSerializer(many=True, required=False)

    class Meta:
        model = Pattern
        fields = ('url', 'name', 'items_pattern')
        # depth = 1


class PatternViewSet(viewsets.ModelViewSet):
    serializer_class = PatternSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        chek = Pattern.objects.all().prefetch_related('items_pattern').filter(buyer_id=self.request.user.id)
        return chek

    def create(self, request, *args, **kwargs):
        print(request.data)
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            print(serializer.validated_data)
            serializer.validated_data['buyer_id'] = request.user.pk
            serializer.validated_data['mobile_id'] = request.data['mobile_id']

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError as e:
            print('ОШИБКА ЗАПИСИ В БАЗУ ДАННЫХ')
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": f"{e}"})

