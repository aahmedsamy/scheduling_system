import graphene

import meetings.schema


class Query(meetings.schema.SlotQuery, meetings.schema.MeetingQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(meetings.schema.MeetingMutation, meetings.schema.SlotMutation, graphene.ObjectType):
    # This class will inherit from multiple Mutations
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
