import graphene
from graphene_django.types import DjangoObjectType
from products.models import Product, Group, Category, ProductImageFile, Version

from jelly_backend.decorators import validate_token


class ProductType(DjangoObjectType):
    images = graphene.List(lambda: ProductImageFileType)
    product_version = graphene.List(lambda: VersionType)

    class Meta:
        model = Product

    def resolve_images(self, info):
        return ProductImageFile.objects.filter(product=self)

    def resolve_product_version(self, info):
        return Version.objects.filter(product=self)


class GroupType(DjangoObjectType):
    class Meta:
        model = Group


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class ProductImageFileType(DjangoObjectType):
    class Meta:
        model = ProductImageFile


class VersionType(DjangoObjectType):
    class Meta:
        model = Version


class Query(graphene.ObjectType):
    # --- Products ---
    list_products_without_pagination = graphene.List(ProductType)
    get_product = graphene.Field(ProductType, id=graphene.ID(required=True))
    total_products = graphene.Int(search=graphene.String())
    list_products = graphene.List(
        ProductType,
        search=graphene.String(),
        page=graphene.Int(),
        page_size=graphene.Int()
    )

    # --- Groups ---
    total_groups = graphene.Int(search=graphene.String())
    list_groups = graphene.List(
        GroupType,
        search=graphene.String(),
        page=graphene.Int(),
        page_size=graphene.Int()
    )
    list_groups_without_pagination = graphene.List(GroupType)

    # --- Categories ---
    total_categories = graphene.Int(search=graphene.String())
    list_categories = graphene.List(
        CategoryType,
        search=graphene.String(),
        page=graphene.Int(),
        page_size=graphene.Int()
    )
    list_categories_without_pagination = graphene.List(CategoryType)

    def resolve_list_products_without_pagination(self, info):
        try:
            return Product.objects.all()
        except Product.DoesNotExist:
            return None

    def resolve_get_product(self, info, id):
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return None

    def resolve_total_products(self, info, search=None):
        products = Product.objects.all()
        if search:
            products = products.filter(name__icontains=search)
        return products.count()

    def resolve_list_products(self, info, search=None, page=None, page_size=None):
        products = Product.objects.all()

        if search:
            products = products.filter(name__icontains=search)
        if page is not None and page_size is not None:
            offset = (page - 1) * page_size
            products = products[offset:offset + page_size]

        return list(products)

    #@validate_token
    def resolve_total_groups(self, info, search=None):
        groups = Group.objects.all()
        if search:
            groups = groups.filter(name__icontains=search)
        return groups.count()

    #@validate_token
    def resolve_list_groups(self, info, search=None, page=None, page_size=None):
        groups = Group.objects.all()

        if search:
            groups = groups.filter(name__icontains=search)
        if page is not None and page_size is not None:
            offset = (page - 1) * page_size
            groups = groups[offset:offset + page_size]

        return list(groups)

    def resolve_list_groups_without_pagination(self, info):
        try:
            return Group.objects.all()
        except Group.DoesNotExist:
            return None

    #@validate_token
    def resolve_total_categories(self, info, search=None):
        categories = Category.objects.all()
        if search:
            categories = categories.filter(name__icontains=search)
        return categories.count()

    #@validate_token
    def resolve_list_categories(self, info, search=None, page=None, page_size=None):
        categories = Category.objects.all()

        if search:
            categories = categories.filter(name__icontains=search)
        if page is not None and page_size is not None:
            offset = (page - 1) * page_size
            categories = categories[offset:offset + page_size]

        return list(categories)

    def resolve_list_categories_without_pagination(self, info):
        try:
            return Category.objects.all()
        except Category.DoesNotExist:
            return None
