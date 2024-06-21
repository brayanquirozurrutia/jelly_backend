import graphene
import uuid
from graphene_django.types import DjangoObjectType
from users.models import User


class UserType(DjangoObjectType):
    fullname = graphene.String()

    class Meta:
        model = User

    def resolve_fullname(self, info):
        return self.get_full_name()


class Query(graphene.ObjectType):
    get_user = graphene.Field(UserType, id=graphene.ID(required=True))

    def resolve_get_user(self, info, id):
        try:
            return User.objects.get(pk=id)
        except (User.DoesNotExist, ValueError):
            return None