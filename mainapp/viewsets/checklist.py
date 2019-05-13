from rest_framework import serializers, viewsets, status
from rest_framework.response import Response

from mainapp.models import Checklist


class ChecklistSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="mainapp:list-detail", lookup_field='checklist_id')

    class Meta:
        model = Checklist
        fields = ('url', 'name', 'modified')


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
