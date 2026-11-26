
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


# ============================================================
# 1. NOTIFICATIONS
# ============================================================

class Notification(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    message = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Notification for {self.user}: {self.message[:50]}"


# ============================================================
# 2. USER ACTIVITIES
# ============================================================

class Activity(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activities"
    )

    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        related_name="activities"
    )

    message = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Activity for {self.user} on {self.project.title}"


# ============================================================
# 3. INVESTMENT PROJECTS
# ============================================================

class Project(models.Model):

    SECTOR_CHOICES = [
        ("Agriculture", "Agriculture"),
        ("Energy", "Energy"),
        ("Mining", "Mining"),
        ("Education", "Education"),
        ("Tourism", "Tourism"),
        ("Irrigation", "Irrigation"),
        ("Technology", "Technology"),
        ("Healthcare", "Healthcare"),
        ("Finance", "Finance"),
        ("Robotics", "Robotics"),
        ("Artificial_Intelligence", "Artificial Intelligence"),
        ("Manufacturing", "Manufacturing"),
        ("Retail", "Retail"),
        ("Real_Estate", "Real Estate"),
        ("Transportation", "Transportation"),
        ("Logistics", "Logistics"),
        ("Media", "Media"),
        ("Entertainment", "Entertainment"),
        ("Sports", "Sports"),
        ("Aerospace", "Aerospace"),
        ("Defense", "Defense"),
        ("Environment", "Environment"),
        ("Water_Resources", "Water Resources"),
        ("Food_Processing", "Food Processing"),
        ("Pharmaceuticals", "Pharmaceuticals"),
        ("Biotechnology", "Biotechnology"),
        ("Telecommunications", "Telecommunications"),
        ("E_Commerce", "E-Commerce"),
        ("Consulting", "Consulting"),
        ("Fashion", "Fashion"),
        ("Automotive", "Automotive"),
        ("Non_Profit", "Non-Profit"),
        ("Public_Administration", "Public Administration"),
    ]

    STATUS_CHOICES = [
        ("Open", "Open"),
        ("In Progress", "In Progress"),
        ("Closed", "Closed"),
    ]

    title = models.CharField(max_length=200)

    description = models.TextField()

    sector = models.CharField(
        max_length=100,
        choices=SECTOR_CHOICES
    )

    country = models.CharField(max_length=100)

    investment_required = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    contact_information = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Provide an email or phone number to be contacted.")
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    collaborators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="collaborations",
        blank=True
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES
    )

    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


# ============================================================
# 4. INVESTMENT APPLICATIONS
# ============================================================

class InvestmentApplication(models.Model):

    APPLICATION_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="investment_applications"
    )

    title = models.CharField(
        max_length=200,
        default="Untitled Investment"
    )

    sector = models.CharField(
        max_length=100,
        choices=Project.SECTOR_CHOICES,
        default="Agriculture"
    )

    country = models.CharField(
        max_length=100,
        default="Not specified"
    )

    investment_required = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        default=0.01
    )

    contact_information = models.CharField(
        max_length=255,
        default="Not provided"
    )

    message = models.TextField()

    submitted_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=APPLICATION_STATUS_CHOICES,
        default="Pending"
    )

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"Application by {self.user} for {self.title}"


# ============================================================
# 5. USER PROFILES
# ============================================================

class UserProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    bio = models.TextField(
        blank=True,
        default="No bio available."
    )

    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        blank=True,
        default="profile_pics/default_profile.jpg"
    )

    country = models.CharField(
        max_length=50,
        blank=True,
        default="Not Specified"
    )

    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}'s Profile"
