from logging import getLogger
from rest_framework_simplejwt.authentication import JWTAuthentication, api_settings, InvalidToken, User, AuthenticationFailed
from sahha_service.utils import exceptions
from django.utils.translation import gettext_lazy as _

logger = getLogger(__name__)


class CustomMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        return response

    def process_exception(self, request, exception):
        logger.error(exception)


class CustomJWTAuthentication(JWTAuthentication):
    
    def get_validated_token(self, raw_token):
        try:
            response = JWTAuthentication.get_validated_token(self, raw_token)
            return response
        except Exception:
            raise exceptions.invalidToken()

    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(_('Token contained no recognizable user identification'))

        user = User.objects.filter(**{api_settings.USER_ID_FIELD: user_id}).select_related('sahha_user').first()
        if not user:
            raise AuthenticationFailed(_('User not found'), code='user_not_found')

        if not user.is_active:
            raise AuthenticationFailed(_('User is inactive'), code='user_inactive')

        return user
