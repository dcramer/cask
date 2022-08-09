import graphene
from graphene_django.types import DjangoObjectType

from cask.accounts.models import Follower
from cask.utils import optimize_queryset

from .models import CheckIn


class CheckInScope(graphene.Enum):
    class Meta:
        name = "CheckInScope"

    public = "public"
    friends = "friends"


class CheckInNode(DjangoObjectType):
    class Meta:
        model = CheckIn
        name = "CheckIn"


class Query(object):
    checkins = graphene.List(
        CheckInNode,
        id=graphene.UUID(),
        scope=graphene.Argument(CheckInScope),
        created_by=graphene.UUID(),
    )

    def resolve_checkins(
        self, info, id: str = None, scope: str = None, created_by: str = None
    ):
        user = info.context.user

        qs = CheckIn.objects.all()

        if id:
            qs = qs.filter(id=id)

        if scope == "friends":
            if not user.is_authenticated:
                return qs.none()
            qs = qs.filter(created_by__in=Follower.objects.filter(from_user=user.id))
        # there's not yet privacy scope
        elif scope == "public":
            pass
        elif scope:
            raise NotImplementedError

        if created_by:
            qs = qs.filter(created_by=created_by)

        qs = qs.order_by("-created_at")

        qs = optimize_queryset(qs, info, "checkins")

        return qs
