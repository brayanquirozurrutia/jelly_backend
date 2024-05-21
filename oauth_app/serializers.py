from rest_framework import serializers


class CreateOAuthApplicationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    client_type = serializers.ChoiceField(choices=['confidential', 'public'], default='confidential')
    authorization_grant_type = serializers.ChoiceField(
        choices=['authorization-code', 'implicit', 'password', 'client-credentials'],
        default='password'
    )
    redirect_uris = serializers.CharField(required=False, allow_blank=True)
