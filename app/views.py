import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from .forms import PartnershipRequestForm, ContactMessageForm

logger = logging.getLogger(__name__)


def _send_email(subject, body):
    """
    Sends an email ONLY to settings.CONTACT_RECEIVER_EMAIL (infos@climares.com).
    Returns (success, error_message).
    """
    to_email = settings.CONTACT_RECEIVER_EMAIL
    from_email = settings.DEFAULT_FROM_EMAIL
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=body,
            from_email=from_email,
            to=[to_email],
        )
        email.send(fail_silently=False)
        logger.info("EMAIL OK  → %s | %s", to_email, subject)
        return True, None
    except Exception as exc:
        logger.exception("EMAIL FAIL → %s | %s", to_email, subject)
        return False, str(exc)


@require_POST
@csrf_protect
def become_partner(request):
    form = PartnershipRequestForm(request.POST)
    if not form.is_valid():
        return JsonResponse(
            {"ok": False, "errors": form.errors.get_json_data()},
            status=400,
        )

    instance = form.save()

    # Build the email body with ALL submitted data
    subject = (
        f"New partnership request [{instance.get_partnership_area_display()}] "
        f"— {instance.organization or instance.last_name}"
    )
    body = (
        "A new partnership request has been submitted.\n"
        "================================================\n\n"
        f"Name            : {instance.first_name} {instance.last_name}\n"
        f"Organization    : {instance.organization or '—'}\n"
        f"Position        : {instance.position or '—'}\n"
        f"Email           : {instance.email}\n"
        f"Phone / WhatsApp: {instance.phone or '—'}\n"
        f"Country         : {instance.country or '—'}\n"
        f"Partner type    : {instance.get_partner_type_display() or '—'}\n"
        f"Area            : {instance.get_partnership_area_display()}\n\n"
        "Message:\n"
        "------------------------------------------------\n"
        f"{instance.message}\n\n"
        "================================================\n"
        f"Submitted at: {instance.created_at:%Y-%m-%d %H:%M}\n"
    )

    ok, err = _send_email(subject=subject, body=body)

    if not ok:
        return JsonResponse(
            {
                "ok": False,
                "id": instance.id,
                "error": "Data saved, but email to infos@climares.com failed.",
                "smtp_error": err if settings.DEBUG else None,
            },
            status=500,
        )

    return JsonResponse({"ok": True, "id": instance.id})


@require_POST
@csrf_protect
def contact(request):
    form = ContactMessageForm(request.POST)
    if not form.is_valid():
        return JsonResponse(
            {"ok": False, "errors": form.errors.get_json_data()},
            status=400,
        )

    instance = form.save()

    # Build the email body with ALL submitted data
    subject = (
        f"New contact message [{instance.get_subject_display()}] "
        f"— {instance.full_name}"
    )
    body = (
        "A new contact message has been submitted.\n"
        "================================================\n\n"
        f"Name    : {instance.full_name}\n"
        f"Email   : {instance.email}\n"
        f"Phone   : {instance.phone or '—'}\n"
        f"Subject : {instance.get_subject_display()}\n\n"
        "Message:\n"
        "------------------------------------------------\n"
        f"{instance.message}\n\n"
        "================================================\n"
        f"Submitted at: {instance.created_at:%Y-%m-%d %H:%M}\n"
    )

    ok, err = _send_email(subject=subject, body=body)

    if not ok:
        return JsonResponse(
            {
                "ok": False,
                "id": instance.id,
                "error": "Data saved, but email to infos@climares.com failed.",
                "smtp_error": err if settings.DEBUG else None,
            },
            status=500,
        )

    return JsonResponse({"ok": True, "id": instance.id})