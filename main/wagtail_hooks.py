# emailing/wagtail_hooks.py
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from .models import SentEmail

class SentEmailAdmin(ModelAdmin):
    model = SentEmail
    menu_label = "Sent Emails"
    menu_icon = "mail"
    list_display = ("subject", "from_email", "to_email", "status", "sent_at")
    search_fields = ("to_email", "subject")

modeladmin_register(SentEmailAdmin)
