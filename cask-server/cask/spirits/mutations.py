import graphene
from django.db import IntegrityError

from cask.world.models import Region

from .models import Bottle, Brand, Distillery, SpiritType
from .schema import BottleNode, BrandNode, DistilleryNode


class AddBottle(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        brand = graphene.UUID(required=True)
        distillery = graphene.UUID(required=True)
        spirit_type = graphene.UUID(required=False)
        abv = graphene.Float(required=False)
        age = graphene.Int(required=False)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)
    bottle = graphene.Field(BottleNode)

    def mutate(
        self,
        info,
        name: str = None,
        distillery: str = None,
        brand: str = None,
        spirit_type: str = None,
        abv: float = None,
        age: int = None,
    ):
        if not info.context.user.is_authenticated:
            return AddDistillery(ok=False, errors=["Authentication required"])

        bottle = Bottle.objects.create(
            name=name,
            distillery=Distillery.objects.get(id=distillery),
            brand=Brand.objects.get(id=brand),
            spirit_type=SpiritType.objects.get(id=spirit_type),
            abv=abv,
            age=age,
            created_by=info.context.user,
        )
        return AddBottle(ok=True, bottle=bottle, errors=None)


class AddBrand(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)
    brand = graphene.Field(BrandNode)

    def mutate(self, info, name: str = None, country: str = None, region: str = None):
        if not info.context.user.is_authenticated:
            return AddDistillery(ok=False, errors=["Authentication required"])

        try:
            result = Brand.objects.create(name=name, created_by=info.context.user)
        except IntegrityError:
            return AddBrand(ok=False, errors=["Brand already exists."])
        return AddBrand(ok=True, brand=result, errors=None)


class AddDistillery(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        region = graphene.UUID(required=True)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)
    distillery = graphene.Field(DistilleryNode)

    def mutate(self, info, name: str = None, region: str = None):
        if not info.context.user.is_authenticated:
            return AddDistillery(ok=False, errors=["Authentication required"])

        region = Region.objects.get(id=region)

        try:
            result = Distillery.objects.create(
                name=name,
                country_id=region.country_id,
                region=region,
                created_by=info.context.user,
            )
        except IntegrityError:
            return AddDistillery(ok=False, errors=["Distillery already exists."])
        return AddDistillery(ok=True, distillery=result, errors=None)


class Mutation(graphene.ObjectType):
    addBottle = AddBottle.Field()
    addBrand = AddBrand.Field()
    addDistillery = AddDistillery.Field()
