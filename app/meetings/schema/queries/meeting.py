import graphene
from django.utils import timezone
from graphene import relay
from graphene_django import DjangoObjectType
from meetings.models import Meeting


class MeetingNode(DjangoObjectType):
    class Meta:
        model = Meeting
        fields = '__all__'
        interfaces = (relay.Node,)
        convert_choices_to_enum = False


class MeetingQuery(graphene.ObjectType):
    my_upcoming_meetings = graphene.List(MeetingNode)

    def resolve_my_upcoming_meetings(self, info, **kwargs):
        return Meeting.objects.select_related("slot"). \
            filter(slot__user_id=info.context.user.id, slot__scheduled_at__gte=timezone.now())
