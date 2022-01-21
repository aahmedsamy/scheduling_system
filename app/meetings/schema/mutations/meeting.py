import graphene
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
        # Notice we return an instance of this mutation
        return MeetingCreateMutation(meeting=meeting)


class MeetingUpdateMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        meeting_id = graphene.String()
        attendance_email_address = graphene.String()
        attendance_full_name = graphene.String()
        slot_id = graphene.String()
        name = graphene.String()

    # The class attributes define the response of the mutation
    meeting = graphene.Field(MeetingNode)

    @classmethod
    def mutate(cls, root, info, meeting_id, **kwargs):
        try:
            meeting = Meeting.objects.get(id=from_global_id(meeting_id)[-1], slot__user_id=info.context.user.id)
        except Meeting.DoesNotExist:
            raise Meeting.DoesNotExist(f"Meeting with id({meeting_id}) Does not exist in our database")
        if kwargs.get('slot'):
            try:
                Slot.objects.get(id=from_global_id(kwargs.get('slot'))[-1])
            except Slot.DoesNotExist:
                raise Slot.DoesNotExist("Selected Slot is not available please select another Slot")
        meeting.name = kwargs.get('name') if kwargs.get('name') else meeting.name
        meeting.slot_id = from_global_id(kwargs.get('slot_id'))[-1] if kwargs.get('slot_id') else meeting.slot_id

        meeting.attendance_email_address = kwargs.get('attendance_email_address') if kwargs.get(
            'attendance_email_address') else meeting.attendance_email_address

        meeting.attendance_full_name = kwargs.get('attendance_full_name') if kwargs.get(
            'attendance_full_name') else meeting.attendance_full_name
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
