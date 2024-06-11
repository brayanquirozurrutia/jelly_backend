import graphene
from graphene_django.types import DjangoObjectType
from products.models import Product, Group, Category


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class GroupType(DjangoObjectType):
    class Meta:
        model = Group


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class Query(graphene.ObjectType):
    list_products = graphene.List(ProductType)
    list_groups = graphene.List(GroupType)
    list_categories = graphene.List(CategoryType)

    def resolve_list_products(self, info):
        return Product.objects.all()

    def resolve_list_groups(self, info):
        return Group.objects.all()

    def resolve_list_categories(self, info):
        return Category.objects.all()
