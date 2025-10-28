from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.models import APIKey

class GenerateAPIKeyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        api_key, key = APIKey.objects.create_key(name=f"{request.user.username}-api-key")
        return Response({'api_key': key})
