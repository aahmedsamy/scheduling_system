import graphene
from django.forms import ModelForm
from graphene_django.forms.mutation import DjangoModelFormMutation, _set_errors_flag_to_context
from graphene_django.types import ErrorType
from graphql import GraphQLError
from graphql_relay import from_global_id

from meetings.models import Slot
from meetings.schema.queries import SlotNode

DURATION_ENUM = graphene.Enum.from_enum(Slot.DurationChoices)


class SlotMutationBase(graphene.Mutation):
    # The class attributes define the response of the mutation
    slot = graphene.Field(SlotNode)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        pass


class SlotCreateMutation(SlotMutationBase):
    class Arguments:
        # The input arguments for this mutation
        scheduled_at = graphene.DateTime(required=True)
        duration = DURATION_ENUM(required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        if info.context.user.is_anonymous:
            raise GraphQLError('You must be logged !')
        slot = Slot(
            user_id=info.context.user.id,
            scheduled_at=kwargs['scheduled_at'],
            duration=kwargs['duration'],
        )
        slot.clean()
        slot.save()
        # Notice we return an instance of this mutation
        return SlotCreateMutation(slot=slot)


class SlotUpdateMutation(SlotMutationBase):
    class Arguments:
        # The input arguments for this mutation
        scheduled_at = graphene.DateTime()
        duration = DURATION_ENUM()
        slot_id = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        if info.context.user.is_anonymous:
            raise GraphQLError('You must be logged !')
        slot_id = from_global_id(kwargs['slot_id'])[-1]
        try:
            slot = Slot.objects.get(id=slot_id, user_id=info.context.user.id)
        except Slot.DoesNotExist:
            raise Slot.DoesNotExist(f"Slot with id({slot_id}) Does not exist in our database")
        slot.scheduled_at = kwargs.get('scheduled_at') if kwargs.get('scheduled_at') else slot.scheduled_at

        slot.duration = kwargs.get('duration') if kwargs.get('duration') else slot.attendance_email_address

        slot.clean()
        slot.save()
        # Notice we return an instance of this mutation
        return SlotUpdateMutation(slot=slot)


class SlotDeleteMutation(SlotMutationBase):
    class Arguments:
        # The input arguments for this mutation
        slot_id = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        if info.context.user.is_anonymous:
            raise GraphQLError('You must be logged !')
        slot_id = from_global_id(kwargs['slot_id'])[-1]
        try:
            slot = Slot.objects.get(id=slot_id, user_id=info.context.user.id)
        except Slot.DoesNotExist:
            raise Slot.DoesNotExist(f"Slot with id({slot_id}) Does not exist in our database")
        slot.delete()
        # Notice we return an instance of this mutation
        return


class SlotMutation(graphene.ObjectType):
    create_slot = SlotCreateMutation.Field()
    update_slot = SlotUpdateMutation.Field()
    delete_slot = SlotDeleteMutation.Field()
