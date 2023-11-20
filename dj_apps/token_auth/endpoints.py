from django.contrib.auth import authenticate, get_user_model

from ninja import Router

from profiles.exceptions import EmailAlreadyExists, InvalidLogin

from .schemas import UserSchemaInCreate, UserSchemaInLogin, UserSchemaOut

User = get_user_model()
router = Router()


@router.post("signup", response=UserSchemaOut, auth=None)
def signup(request, payload: UserSchemaInCreate):
    if User.objects.filter(email=payload.email).exists():
        raise EmailAlreadyExists(
            message="This email already exists.",
            error_level="field",
            field_name="email",
        )

    new_user = User.objects.create_user(**payload.dict(exclude_unset=True))
    return new_user


@router.post("login", response=UserSchemaOut, auth=None)
def login(request, payload: UserSchemaInLogin):
    """NOTE: logout does not require an endpoint, as it's just a front-end operation"""
    user = authenticate(request, email=payload.email, password=payload.password)
    if user is not None:
        return user
    else:
        raise InvalidLogin(
            message="Wrong given credentials. Please try again.", error_level="non_field"
        )


@router.post("reset-password")
def reset_password(request):
    return {"reset": "ok"}
