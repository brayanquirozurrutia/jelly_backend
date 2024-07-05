import graphene
from graphene_django.types import DjangoObjectType
from products.models import Product, Group, Category

from jelly_backend.decorators import validate_token


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
    get_product = graphene.Field(ProductType, id=graphene.ID(required=True))
    total_groups = graphene.Int(search=graphene.String())
    list_groups = graphene.List(
        GroupType,
        search=graphene.String(),
        page=graphene.Int(),
        page_size=graphene.Int()
    )
    list_categories = graphene.List(CategoryType)

    def resolve_list_products(self, info):
        return Product.objects.all()

    def resolve_get_product(self, info, id):
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return None

    @validate_token
    def resolve_total_groups(self, info, search=None):
        groups = Group.objects.all()
        if search:
            groups = groups.filter(name__icontains=search)
        return groups.count()

    @validate_token
    def resolve_list_groups(self, info, search=None, page=None, page_size=None):
        groups = Group.objects.all()

        if search:
            groups = groups.filter(name__icontains=search)
        if page is not None and page_size is not None:
            offset = (page - 1) * page_size
            groups = groups[offset:offset + page_size]

        return list(groups)

    def resolve_list_categories(self, info):
        return Category.objects.all()
