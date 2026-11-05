from django.contrib import admin
from .models import PartnershipRequest, ContactMessage


@admin.register(PartnershipRequest)
class PartnershipRequestAdmin(admin.ModelAdmin):
    list_display = (
        "first_name", "last_name", "organization",
        "email", "partnership_area", "partner_type", "created_at",
    )
    list_filter = ("partnership_area", "partner_type", "created_at")
    search_fields = ("first_name", "last_name", "organization", "email", "message")
    readonly_fields = ("created_at",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "subject", "created_at")
    list_filter = ("subject", "created_at")
    search_fields = ("full_name", "email", "message")
    readonly_fields = ("created_at",)