import graphene
from graphql import GraphQLError
from graphql_relay import from_global_id

from meetings.models import Meeting, Slot
from meetings.schema.queries import MeetingNode


class MeetingCreateMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        attendance_email_address = graphene.String(required=True)
        attendance_full_name = graphene.String(required=True)
        slot_id = graphene.String(required=True)
        name = graphene.String()

    # The class attributes define the response of the mutation
    meeting = graphene.Field(MeetingNode)

    @classmethod
    def mutate(cls, root, info, slot_id, attendance_full_name, attendance_email_address, name=''):
        slot_id = from_global_id(slot_id)[-1]
        try:
            Slot.objects.get(id=slot_id, meeting__isnull=True)
        except Slot.DoesNotExist:
            raise Slot.DoesNotExist("Selected Slot is not available please select another Slot")
        meeting = Meeting(
            slot_id=slot_id,
            attendance_full_name=attendance_full_name,
            attendance_email_address=attendance_email_address,
            name=name
        )
        meeting.save()
        # Notice we return an instance of this mutation
        return MeetingCreateMutation(meeting=meeting)


class MeetingUpdateMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        meeting_id = graphene.String(required=True)
        slot_id = graphene.String(required=True)

    # The class attributes define the response of the mutation
    meeting = graphene.Field(MeetingNode)

    @classmethod
    def mutate(cls, root, info, meeting_id, slot_id):
        if info.context.user.is_anonymous:
            raise GraphQLError('You must be logged !')
        meeting_id = from_global_id(meeting_id)[-1]
        slot_id = from_global_id(slot_id)[-1]
        try:
            meeting = Meeting.objects.get(id=meeting_id, slot__user_id=info.context.user.id)
        except Meeting.DoesNotExist:
            raise Meeting.DoesNotExist(f"Meeting with id({meeting_id}) Does not exist in our database")
        try:
            Slot.objects.get(id=slot_id)
        except Slot.DoesNotExist:
            raise Slot.DoesNotExist("Selected Slot is not available please select another Slot")
        meeting.slot_id = slot_id
        meeting.save()
        # Notice we return an instance of this mutation
        return MeetingUpdateMutation(meeting=meeting)


class MeetingDeleteMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        meeting_id = graphene.String()

    # The class attributes define the response of the mutation
    meeting = graphene.Field(MeetingNode)

    @classmethod
    def mutate(cls, root, info, meeting_id, **kwargs):
        if info.context.user.is_anonymous:
            raise GraphQLError('You must be logged !')
        try:
            meeting = Meeting.objects.get(id=from_global_id(meeting_id)[-1], slot__user_id=info.context.user.id)
        except Meeting.DoesNotExist:
            raise Meeting.DoesNotExist(f"Meeting with id({meeting_id}) Does not exist in our database")
        meeting.delete()
        # Notice we return an instance of this mutation
        return


class MeetingMutation(graphene.ObjectType):
    create_meeting = MeetingCreateMutation.Field()
    update_meeting = MeetingUpdateMutation.Field()
    delete_meeting = MeetingDeleteMutation.Field()
