from django import forms
from .models import PartnershipRequest, ContactMessage


class PartnershipRequestForm(forms.ModelForm):
    class Meta:
        model = PartnershipRequest
        fields = [
            "first_name", "last_name", "organization", "position",
            "email", "phone", "country", "partner_type",
            "partnership_area", "message", "consent",
        ]

    def clean_message(self):
        message = self.cleaned_data.get("message", "")
        if len(message.strip()) < 500:
            raise forms.ValidationError(
                "Message must be at least 500 characters long."
            )
        return message

    def clean_consent(self):
        consent = self.cleaned_data.get("consent")
        if not consent:
            raise forms.ValidationError("You must accept the privacy policy.")
        return consent


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["full_name", "email", "phone", "subject", "message"]