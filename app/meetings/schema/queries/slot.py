import graphene
from django.utils import timezone
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from meetings.models import Slot


class SlotNode(DjangoObjectType):
    class Meta:
        model = Slot
        fields = '__all__'
        filter_fields = {
            'scheduled_at': ['exact', 'gte', 'lte'],
            'id': ['exact'],
            'user__email': ['exact']
        }
        interfaces = (relay.Node,)
        convert_choices_to_enum = False

    slot_available = graphene.Boolean()

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter(scheduled_at__gte=timezone.now())

    def resolve_slot_available(self, info):
        return Slot.objects.filter(id=self.id, meeting__isnull=True).exists()


class SlotQuery(graphene.ObjectType):
    all_slots = DjangoFilterConnectionField(SlotNode, user_email=graphene.String(required=True))
