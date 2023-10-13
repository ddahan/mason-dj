from django.contrib import admin

from .models.app_parameters import AppParameters

admin.site.register([AppParameters])
