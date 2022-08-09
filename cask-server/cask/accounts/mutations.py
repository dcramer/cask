from typing import Optional

import facebook
import graphene
from django.contrib.auth import authenticate
from django.db import IntegrityError, transaction

from .models import Follower, Identity, User
from .schema import UserNode
from .utils import generate_token


def get_user_from_facebook_token(token: str = None) -> Optional[User]:
    graph = facebook.GraphAPI(access_token=token)

    try:
        profile = graph.get_object("me", fields="id,name,email")
    except facebook.GraphAPIError as e:
        if "Invalid OAuth access token" in str(e):
            return None
        raise

    external_id = str(profile["id"])
    for i in range(2):
        identity = (
            Identity.objects.filter(provider="facebook", external_id=external_id)
            .select_related("user")
            .first()
        )
        if identity:
            return identity.user
        try:
            with transaction.atomic():
                user = User.objects.create(email=profile["email"], name=profile["name"])
                identity = Identity.objects.create(
                    user=user, provider="facebook", external_id=external_id
                )
                return user
        except IntegrityError:
            pass
    return user


class Login(graphene.Mutation):
    """
    Mutation to login a user
    """

    class Arguments:
        email = graphene.String(required=False)
        password = graphene.String(required=False)
        facebook_token = graphene.String(required=False)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)
    token = graphene.String()
    user = graphene.Field(UserNode)

    def mutate(
        self, info, email: str = None, password: str = None, facebook_token: str = None
    ):
        if facebook_token:
            user = get_user_from_facebook_token(facebook_token)
        elif email and password:
            user = authenticate(email=email, password=password)
        else:
            user = None

        if not user:
            return Login(
                ok=False, errors=["Unable to login with provided credentials."]
            )
        # we stuff the user into the current request so they can serialize sensitive attributes
        info.context.user = user
        return Login(ok=True, user=user, token=generate_token(user))


class Follow(graphene.Mutation):
    """
    Follow a user
    """

    class Arguments:
        user = graphene.UUID(required=True)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)
    token = graphene.String()
    user = graphene.Field(UserNode)

    def mutate(self, info, user: str):
        current_user = info.context.user
        if not current_user.is_authenticated:
            return Follow(ok=False, errors=["Requires authentication"])

        user = User.objects.exclude(id=info.context.user.id).get(id=user)
        Follower.objects.create(from_user=current_user, to_user=user)
        return Follow(ok=True, user=user)


class Unfollow(graphene.Mutation):
    """
    Unfollow a user
    """

    class Arguments:
        user = graphene.UUID(required=True)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)
    token = graphene.String()
    user = graphene.Field(UserNode)

    def mutate(self, info, user: str):
        current_user = info.context.user
        if not current_user.is_authenticated:
            return Follow(ok=False, errors=["Requires authentication"])

        user = User.objects.exclude(id=info.context.user.id).get(id=user)
        Follower.objects.filter(from_user=current_user, to_user=user).delete()
        return Unfollow(ok=True, user=user)


class Mutation(graphene.ObjectType):
    login = Login.Field()
    follow = Follow.Field()
    unfollow = Unfollow.Field()
