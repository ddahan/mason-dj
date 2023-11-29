from django.contrib.auth import authenticate, get_user_model
from django.db import transaction

from ninja import Router

from profiles.exceptions import EmailAlreadyExists, InvalidLogin, UnexistingUser

from .exceptions import MagicLinkNotFound
from .models.magic_link_token import MagicLinkToken, MagicLinkUsage
from .schemas import (
    EmailSchemaIn,
    ResetPasswordSchemaIn,
    UserSchemaInCreate,
    UserSchemaInLogin,
    UserSchemaOut,
)

User = get_user_model()
router = Router()


@router.post("signup", response=UserSchemaOut, auth=None)
def signup(request, payload: UserSchemaInCreate):
    if User.objects.filter(email=payload.email).exists():
        raise EmailAlreadyExists()

    new_user = User.objects.create_user(**payload.dict(exclude_unset=True))
    return new_user


@router.post("login", response=UserSchemaOut, auth=None)
def login(request, payload: UserSchemaInLogin):
    """NOTE: logout does not require an endpoint, as it's just a front-end operation"""
    user = authenticate(request, email=payload.email, password=payload.password)
    if user is not None:
        return user
    else:
        raise InvalidLogin()


@router.post("send-reset-password-link", auth=None)
def send_reset_password_link(request, payload: EmailSchemaIn):
    try:
        user = User.objects.get(email=payload.email)
    except User.DoesNotExist:
        raise UnexistingUser()
    else:
        user.send_reset_password_magic_link()


@router.post("reset-password", auth=None)
def reset_password(request, payload: ResetPasswordSchemaIn):
    try:
        magic_link = MagicLinkToken.objects.get(key=payload.key)
    except MagicLinkToken.DoesNotExist:
        raise MagicLinkNotFound()
    else:
        assert magic_link.usage == MagicLinkUsage.RESET_PASSWORD
        user = magic_link.user
        with transaction.atomic():
            user.set_password(payload.new_password)  # WARN: unchecked
            user.save()
            magic_link.consume()
