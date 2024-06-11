import graphene
from products.schema import Query as ProductsQuery


class Query(
    ProductsQuery,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query)
