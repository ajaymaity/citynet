"""TODO."""

from django.contrib import admin
from .models import DublinBikesStation, DublinBikesStationRealTimeUpdate


# Register your models here.
class StationAdmin(admin.ModelAdmin):
    """Create the admin view of the stations."""

    list_display = [field.name for field in
                    DublinBikesStation._meta.get_fields()]

class RTStationAdmin(admin.ModelAdmin):
    """Create the admin view of the stations."""

    list_display = [field.name for field in
                    DublinBikesStationRealTimeUpdate._meta.get_fields()]


admin.site.register(DublinBikesStation, StationAdmin)
admin.site.register(DublinBikesStationRealTimeUpdate, RTStationAdmin)

# modelLists = [DublinBikesStation, DublinBikesStationRealTimeUpdate]
# admin.site.register(modelLists, StationAdmin)