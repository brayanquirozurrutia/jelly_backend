import graphene
from graphene_django.types import DjangoObjectType

from admin_app.models import BannerPhrase
from django.core.cache import cache


class BannerPhraseType(DjangoObjectType):
    class Meta:
        model = BannerPhrase
        fields = ('id', 'phrase')


class Query(graphene.ObjectType):
    banner_phrases = graphene.List(BannerPhraseType)

    def resolve_banner_phrases(self, info):
        cached_data = cache.get('banner_phrases')
        if cached_data:
            return cached_data

        phrases = BannerPhrase.objects.all()
        cache.set('banner_phrases', phrases, timeout=3600)
        return phrases
