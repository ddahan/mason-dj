from django.contrib import admin

from .models.badge import Badge
from .models.user import User

admin.site.register([User, Badge])
