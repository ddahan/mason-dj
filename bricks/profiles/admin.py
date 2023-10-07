from django.contrib import admin

from .models.user import User

admin.site.register([User])
