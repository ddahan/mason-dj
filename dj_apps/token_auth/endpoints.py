from django.contrib.auth import get_user_model

from ninja import Router

from profiles.exceptions import EmailAlreadyExists

from .schemas import UserSchemaInCreate, UserSchemaOut

User = get_user_model()
router = Router()


@router.post("signup", response=UserSchemaOut)
def signup(request, payload: UserSchemaInCreate):
    if User.objects.filter(email=payload.email).exists():
        raise EmailAlreadyExists(
            message="Cette adresse e-mail est déjà utilisée.",
            error_level="field",
            field_name="email",
        )

    new_user = User.objects.create_user(**payload.dict(exclude_unset=True))
    return new_user


@router.post("login")
def login(request):
    return {"login": "ok"}


@router.post("reset-password")
def reset_password(request):
    return {"reset": "ok"}
