import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from .forms import PartnershipRequestForm, ContactMessageForm

logger = logging.getLogger(__name__)


def _send_email(subject, body, to_email, reply_to=None):
    """Helper: send a plain-text email via the configured SMTP backend."""
    from_email = settings.DEFAULT_FROM_EMAIL
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=body,
            from_email=from_email,
            to=[to_email],
            reply_to=reply_to or [],
        )
        email.send(fail_silently=False)
        return True
    except Exception as exc:
        logger.exception("Email sending failed: %s", exc)
        return False


@require_POST
@csrf_protect
def become_partner(request):
    """
    Handle the B1 'Become a partner' form.
    Saves to DB, then emails infos@climares.com via vovotacompany@gmail.com.
    """
    form = PartnershipRequestForm(request.POST)

    if not form.is_valid():
        return JsonResponse(
            {"ok": False, "errors": form.errors.get_json_data()},
            status=400,
        )

    instance = form.save()

    # ---- Build & send the email to CLIMARES ----
    subject = f"New partnership request [{instance.get_partnership_area_display()}] — {instance.organization or instance.last_name}"
    body = (
        "A new partnership request has been submitted.\n\n"
        f"Name            : {instance.first_name} {instance.last_name}\n"
        f"Organization    : {instance.organization or '—'}\n"
        f"Position        : {instance.position or '—'}\n"
        f"Email           : {instance.email}\n"
        f"Phone / WhatsApp: {instance.phone or '—'}\n"
        f"Country         : {instance.country or '—'}\n"
        f"Partner type    : {instance.get_partner_type_display() or '—'}\n"
        f"Area            : {instance.get_partnership_area_display()}\n\n"
        "Message:\n"
        f"{instance.message}\n\n"
        f"Submitted at: {instance.created_at:%Y-%m-%d %H:%M}\n"
    )
    _send_email(
        subject=subject,
        body=body,
        to_email=settings.CONTACT_RECEIVER_EMAIL,
        reply_to=[instance.email],
    )

    # ---- Auto-acknowledge to the visitor ----
    ack_body = (
        f"Dear {instance.first_name},\n\n"
        "Thank you for your partnership request to CLIMARES.\n"
        "Our team will contact you within 5 working days.\n\n"
        "Best regards,\n"
        "The CLIMARES Team\n"
        "infos@climares.com\n"
    )
    _send_email(
        subject="Thank you for your partnership request — CLIMARES",
        body=ack_body,
        to_email=instance.email,
    )

    return JsonResponse({"ok": True, "id": instance.id})


@require_POST
@csrf_protect
def contact(request):
    """
    Handle the B3 'Contact us' form.
    Saves to DB, then emails infos@climares.com via vovotacompany@gmail.com.
    """
    form = ContactMessageForm(request.POST)

    if not form.is_valid():
        return JsonResponse(
            {"ok": False, "errors": form.errors.get_json_data()},
            status=400,
        )

    instance = form.save()

    subject = f"New contact message [{instance.get_subject_display()}] — {instance.full_name}"
    body = (
        "A new contact message has been submitted.\n\n"
        f"Name    : {instance.full_name}\n"
        f"Email   : {instance.email}\n"
        f"Phone   : {instance.phone or '—'}\n"
        f"Subject : {instance.get_subject_display()}\n\n"
        "Message:\n"
        f"{instance.message}\n\n"
        f"Submitted at: {instance.created_at:%Y-%m-%d %H:%M}\n"
    )
    _send_email(
        subject=subject,
        body=body,
        to_email=settings.CONTACT_RECEIVER_EMAIL,
        reply_to=[instance.email],
    )

    ack_body = (
        f"Dear {instance.full_name},\n\n"
        "Thank you for reaching out to CLIMARES.\n"
        "We have received your message and will reply shortly.\n\n"
        "Best regards,\n"
        "The CLIMARES Team\n"
        "infos@climares.com\n"
    )
    _send_email(
        subject="We received your message — CLIMARES",
        body=ack_body,
        to_email=instance.email,
    )

    return JsonResponse({"ok": True, "id": instance.id})