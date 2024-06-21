import graphene
from products.schema import Query as ProductsQuery
from users.schema import Query as UsersQuery


class Query(
    ProductsQuery,
    UsersQuery,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query)
