import graphene

import cask.accounts.mutations
import cask.accounts.schema
import cask.cask.mutations
import cask.cask.schema
import cask.spirits.mutations
import cask.spirits.schema
import cask.world.schema


class RootQuery(
    cask.accounts.schema.Query,
    cask.cask.schema.Query,
    cask.spirits.schema.Query,
    cask.world.schema.Query,
    graphene.ObjectType,
):
    pass


class RootMutation(
    cask.accounts.mutations.Mutation,
    cask.cask.mutations.Mutation,
    cask.spirits.mutations.Mutation,
):
    pass


schema = graphene.Schema(query=RootQuery, mutation=RootMutation)
