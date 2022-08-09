import graphene
from graphene_django.types import DjangoObjectType

from cask.utils import optimize_queryset

from .models import Follower, User


class UserScope(graphene.Enum):
    class Meta:
        name = "UserScope"

    followers = "followers"
    following = "following"


# TODO(dcramer): how do we return following/follower status efficiently here?
class UserNode(DjangoObjectType):
    email = graphene.String(required=False)
    following = graphene.Boolean()
    follower = graphene.Boolean()

    class Meta:
        model = User
        name = "User"
        only_fields = ("id", "email", "name")

    def resolve_email(self, info):
        user = info.context.user
        if user.is_authenticated and user.id == self.id:
            return self.email
        return None


class Query(object):
    me = graphene.Field(UserNode)
    users = graphene.List(
        UserNode,
        id=graphene.UUID(),
        query=graphene.String(),
        scope=graphene.Argument(UserScope),
    )

    def resolve_me(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user
        return None

    def resolve_users(
        self, info, id: str = None, query: str = None, scope: str = None, **kwargs
    ):
        user = info.context.user
        qs = User.objects.all()

        if id:
            qs = qs.filter(from_user_id=id)

        if query:
            qs = qs.filter(name__istartswith=query)

        if scope == "followers":
            if not user.is_authenticated:
                qs = qs.none()
            else:
                qs = qs.filter(
                    id__in=Follower.objects.filter(to_user_id=user.id).values_list(
                        "from_user_id"
                    )
                )
        elif scope == "following":
            if not user.is_authenticated:
                qs = qs.none()
            else:
                qs = qs.filter(
                    id__in=Follower.objects.filter(from_user_id=user.id).values_list(
                        "to_user_id"
                    )
                )
        elif scope:
            qs = qs.none()

        qs = optimize_queryset(qs, info, "users")

        return qs
