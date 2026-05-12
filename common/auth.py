import base64
import json

from i_dot_ai_utilities.auth.auth_api import UserAuthorisationResult

from common.services.exceptions import MissingAuthTokenError
from common.settings import get_settings, get_structured_logger

settings = get_settings()
logger = get_structured_logger()


def __load_dummy_user_info() -> UserAuthorisationResult:
    """
    Returns a dummy UserAuthorisationResult, as one would be received from the Auth API's /token/authorise endpoint.
    Used for local testing.
    """
    return UserAuthorisationResult(
        email="test@test.co.uk",
        is_authorised=True,
        auth_reason="LOCAL_TESTING",
    )


def get_user_info(auth_token: str | None) -> UserAuthorisationResult:
    """
    Retrieve user metadata, including the user email and whether they should have access to the app.
    Decodes ALB OIDC JWT token directly.
    """
    if settings.ENVIRONMENT == "local":
        return __load_dummy_user_info()

    if not auth_token:
        raise MissingAuthTokenError

    try:
        # Decode JWT token from ALB OIDC
        parts = auth_token.split('.')
        if len(parts) != 3:
            logger.error("Invalid JWT token format")
            raise ValueError("Invalid JWT token format")
        
        payload = json.loads(base64.b64decode(parts[1] + '==').decode('utf-8'))
        email = payload.get('email')
        
        if not email:
            logger.error("No email found in JWT token payload")
            raise ValueError("No email in token")
        
        logger.info(f"Successfully parsed token for user: {email}")
        
        return UserAuthorisationResult(
            email=email,
            is_authorised=True,
            auth_reason="ALB_OIDC_AUTHENTICATED",
        )
    except Exception:
        logger.exception("Error occurred when authorising user")
        raise


def is_authorised_user(auth_token: str) -> bool:
    """
    A simple wrapper function to call the Auth API and check the user is permitted to access the resource.
    """
    try:
        return get_user_info(auth_token).is_authorised
    except Exception:
        logger.exception("Error occurred when authorising user")
        return False
