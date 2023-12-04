from django.contrib.auth import authenticate, get_user_model
from django.db import transaction

from ninja import Router

from profiles.exceptions import EmailAlreadyExists, InvalidLogin, UnexistingUser

from .exceptions import CodeNotFound, MagicLinkNotFound
from .models.api_token import APIAccessToken
from .models.magic_link_token import MagicLinkToken, MagicLinkUsage
from .models.password_less_token import LoginPasswordLessToken, SignupPasswordLessToken
from .schemas import (
    EmailSchemaIn,
    EnterVerificationCodeSchemaIn,
    ResetPasswordSchemaIn,
    UserSchemaInCreate,
    UserSchemaInLogin,
    UserSchemaOut,
)

User = get_user_model()
router = Router()

##########################################################################################
# Base Authentication
##########################################################################################


@router.get("check")
def check(request):
    """This is the most basic credentials check for current access token validity.
    Example of usage: on homepage if there is no other backend check, it will help to
    log out the user from the front-end.
    """
    pass  # will return a 401 if a valid token can't be found.


@router.get("revoque-access-tokens")
def revoque_access_tokens(request):
    """Logout operation requires a back-end part to revoque all user access tokens. This implies the user will be logged out from all devices. This favors safety over experience, and can be changed accordingly."""
    APIAccessToken.revoque_all_for_user(request.auth)


##########################################################################################
# Classical Authentication
##########################################################################################


@router.post("classic/login", response=UserSchemaOut, auth=None)
def login(request, payload: UserSchemaInLogin):
    """Log a user in from a given email/password"""

    user = authenticate(request, email=payload.email, password=payload.password)
    if user is not None:
        api_access_token = APIAccessToken.objects.create(user=user)
        return dict(sid=user.sid, email=user.email, api_token_key=api_access_token.key)
    else:
        raise InvalidLogin()


@router.post("classic/signup", response=UserSchemaOut, auth=None)
def signup(request, payload: UserSchemaInCreate):
    """Create a new user and acts as a login too (2-in-1)"""

    if User.objects.filter(email=payload.email).exists():
        raise EmailAlreadyExists()

    new_user = User.objects.create_user(**payload.dict(exclude_unset=True))
    api_access_token = APIAccessToken.objects.create(user=new_user)

    return dict(
        sid=new_user.sid, email=new_user.email, api_token_key=api_access_token.key
    )


@router.post("classic/send-reset-password-link", auth=None)
def send_reset_password_link(request, payload: EmailSchemaIn):
    try:
        user = User.objects.get(email=payload.email)
    except User.DoesNotExist:
        raise UnexistingUser()
    else:
        MagicLinkToken.send_new_to(user=user, usage=MagicLinkUsage.RESET_PASSWORD)


@router.post("classic/reset-password", auth=None)
def reset_password(request, payload: ResetPasswordSchemaIn):
    try:
        magic_link = MagicLinkToken.objects.get(key=payload.key)
    except MagicLinkToken.DoesNotExist:
        raise MagicLinkNotFound()
    else:
        assert magic_link.usage == MagicLinkUsage.RESET_PASSWORD
        user = magic_link.user
        with transaction.atomic():
            user.set_password(payload.new_password)
            user.save()
            magic_link.consume()
            # NOTE: in front-end, logout() will be called to clear access tokens


##########################################################################################
# Passwordless Authentication
##########################################################################################


@router.post("passwordless/enter-email", auth=None)
def enter_email(request, payload: EmailSchemaIn):
    """Verify identity to know if the given email must lead to a login or signup"""
    # WARN: until the user is not signed up, someone can sign up.
    try:
        user = User.objects.get(email=payload.email)
    except User.DoesNotExist:
        usage = "signup"
        SignupPasswordLessToken.send_new_to(email=payload.email)
    else:
        usage = "login"
        LoginPasswordLessToken.send_new_to(user=user)

    return {"usage": usage}  # front-end needs this information


@router.post("passwordless/enter-signup-verif-code", auth=None)
def enter_verif_signup_code(request, payload: EnterVerificationCodeSchemaIn):
    # This should not happen but tested as extra security
    if User.objects.filter(email=payload.email).exists():
        raise EmailAlreadyExists()

    if (
        SignupPasswordLessToken.challenge(
            input_code=payload.code,
            email=payload.email,
            # token will be consumed on next screen. Act as a verification only.
            consume=False,
        )
        is False
    ):
        raise CodeNotFound()


@router.post("passwordless/enter-login-verif-code", response=UserSchemaOut, auth=None)
def enter_verif_login_code(request, payload: EnterVerificationCodeSchemaIn):
    try:
        user = User.objects.get(email=payload.email)
    except User.DoesNotExist:
        raise UnexistingUser()

    if LoginPasswordLessToken.challenge(input_code=payload.code, user=user) is True:
        api_access_token = APIAccessToken.objects.create(user=user)
    else:
        raise CodeNotFound()

    return dict(sid=user.sid, email=user.email, api_token_key=api_access_token.key)
