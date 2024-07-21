import graphene
from products.schema import Query as ProductsQuery
from users.schema import Query as UsersQuery
from admin_app.schema import Query as AdminQuery


class Query(
    ProductsQuery,
    UsersQuery,
    AdminQuery,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query)
