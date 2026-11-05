from django.db import models


class PartnershipRequest(models.Model):
    """Stores submissions from the 'Become a partner' form (B1)."""

    PARTNER_TYPE_CHOICES = [
        ("un", "UN agency"),
        ("university", "University"),
        ("financial", "Financial institution"),
        ("ngo", "NGO / Civil society"),
        ("gov", "Government"),
        ("private", "Private sector"),
        ("other", "Individual / other"),
    ]

    AREA_CHOICES = [
        ("research", "Research & Studies"),
        ("innovation", "Innovation & Incubation"),
        ("hydrology", "Hydrology & Water Resources"),
        ("climate", "Climate & Climate Services"),
        ("drr", "Disaster Risk Reduction"),
        ("digital", "Digital Transformation & AI"),
        ("training", "Training & Capacity Building"),
        ("funding", "Project Funding / Sponsorship"),
        ("other", "Other"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    organization = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=150, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=100, blank=True)
    partner_type = models.CharField(max_length=30, choices=PARTNER_TYPE_CHOICES, blank=True)
    partnership_area = models.CharField(max_length=30, choices=AREA_CHOICES)
    message = models.TextField()
    consent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Partnership Request"
        verbose_name_plural = "Partnership Requests"

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.get_partnership_area_display()}"


class ContactMessage(models.Model):
    """Stores submissions from the Contact form (B3)."""

    SUBJECT_CHOICES = [
        ("general", "General information"),
        ("partnership", "Partnership"),
        ("training", "Training"),
        ("incubation", "Incubation"),
        ("press", "Press"),
        ("other", "Other"),
    ]

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=30, choices=SUBJECT_CHOICES)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.full_name} — {self.get_subject_display()} ({self.created_at:%Y-%m-%d})"