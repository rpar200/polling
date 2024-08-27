from django.contrib import admin
from .models import Question

## We're telling django that Question objects have an admin interface!
admin.site.register(Question)