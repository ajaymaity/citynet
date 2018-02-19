"""TODO."""

from django.contrib import admin
from .models import DublinBikesStation


# Register your models here.
class StationAdmin(admin.ModelAdmin):
    """Create the admin view of the stations."""

    list_display = [field.name for field in
                    DublinBikesStation._meta.get_fields()]


admin.site.register(DublinBikesStation, StationAdmin)
