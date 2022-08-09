import graphene
from graphene_django.types import DjangoObjectType

from cask.utils import optimize_queryset

from .models import Bottle, Brand, Distillery, FlavorProfile, SpiritType


class BottleNode(DjangoObjectType):
    class Meta:
        name = "Bottle"
        model = Bottle


class BrandNode(DjangoObjectType):
    class Meta:
        name = "Brand"
        model = Brand


class DistilleryNode(DjangoObjectType):
    class Meta:
        name = "Distillery"
        model = Distillery


class FlavorProfileNode(DjangoObjectType):
    class Meta:
        name = "FlavorProfile"
        model = FlavorProfile


class SpiritTypeNode(DjangoObjectType):
    class Meta:
        name = "SpiritType"
        model = SpiritType


class Query(object):
    brands = graphene.List(BrandNode, id=graphene.UUID(), query=graphene.String())
    bottles = graphene.List(BottleNode, id=graphene.UUID(), query=graphene.String())
    distilleries = graphene.List(
        DistilleryNode, id=graphene.UUID(), query=graphene.String()
    )
    flavor_profiles = graphene.List(
        FlavorProfileNode, id=graphene.UUID(), query=graphene.String()
    )
    spirit_types = graphene.List(
        SpiritTypeNode, id=graphene.UUID(), query=graphene.String()
    )

    def resolve_brands(self, info, id: str = None, query: str = None):
        qs = Brand.objects.all()
        if id:
            qs = qs.filter(id=id)
        if query:
            qs = qs.filter(name__istartswith=query)
        qs = optimize_queryset(qs, info, "brands")
        return qs.order_by("name")

    def resolve_bottles(self, info, id: str = None, query: str = None):
        qs = Bottle.objects.all()
        if id:
            qs = qs.filter(id=id)
        if query:
            qs = qs.filter(name__istartswith=query)
        qs = optimize_queryset(qs, info, "bottles")
        return qs.order_by("name")

    def resolve_distilleries(self, info, id: str = None, query: str = None):
        qs = Distillery.objects.all()
        if id:
            qs = qs.filter(id=id)
        if query:
            qs = qs.filter(name__istartswith=query)
        qs = optimize_queryset(qs, info, "distilleries")
        return qs.order_by("name")

    def resolve_flavor_profiles(self, info, id: str = None, query: str = None):
        qs = FlavorProfile.objects.all()
        if id:
            qs = qs.filter(id=id)
        if query:
            qs = qs.filter(name__istartswith=query)
        qs = optimize_queryset(qs, info, "flavor_profiles")
        return qs.order_by("name")

    def resolve_spirit_types(self, info, id: str = None, query: str = None):
        qs = SpiritType.objects.all()
        if id:
            qs = qs.filter(id=id)
        if query:
            qs = qs.filter(name__istartswith=query)
        qs = optimize_queryset(qs, info, "spirit_types")
        return qs.order_by("name")
