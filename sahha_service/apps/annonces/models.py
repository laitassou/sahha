from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Agence(models.Model):
    name = models.CharField(max_length=100, unique=True)  # agence name
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    address = models.CharField(max_length=250, unique=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    phone_number = models.CharField(max_length=20)

    class Meta:
        ordering = ("country", "city", "name", "address")

    def __str__(self):
        return self.name


class Categorie(models.Model):
    name = models.CharField(max_length=250, unique=True)
    count = models.IntegerField(default=0)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Annonce(models.Model):
    title = models.CharField(max_length=100, blank=True, default="")
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    based_location = models.ForeignKey(
        Agence, related_name="location", on_delete=models.CASCADE, default="", null=True
    )

    based_category = models.ForeignKey(
        Categorie,
        related_name="category_id",
        on_delete=models.CASCADE,
        default="",
        null=True,
    )

    addresse = models.CharField(max_length=200, blank=True, default="")

    gps_latitude = models.FloatField(null=True, default=0)
    gps_longitude = models.FloatField(null=True, default=0)

    is_validated = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return str(self.title + "-" + self.addresse)


class TimeSlot(models.Model):
    Daily = "Jour"
    Weekly = "Semaine"
    CHOICES = (
        (Daily, Daily),
        (Weekly, Weekly),
    )
    annonce_id = models.ForeignKey(Annonce, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, blank=True, default="")
    time_slot_intervenant = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    is_periodic = models.BooleanField(default=False)
    periodicity = models.CharField(
        max_length=120, default=Weekly, choices=CHOICES)

    class Meta:
        unique_together = ("annonce_id", "start_time", "end_time")

    def __str__(self):
        return str(self.start_time) + "-" + str(self.end_time)


class Intervention(models.Model):
    slot_id = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    intervenant = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )
    reporting = models.TextField()
    done = models.BooleanField(default=False)
    gps_latitude = models.FloatField(null=True)
    gps_longitude = models.FloatField(null=True)
    score = models.IntegerField(
        default=1, validators=[MaxValueValidator(10), MinValueValidator(1)]
    )

    class Meta:
        unique_together = ("id", "slot_id", "intervenant")

    def __str__(self):
        return (
            str(self.slot_id.annonce_id)
            + "-"
            + str(self.slot_id.annonce_id.title)
            + "-"
            + str(self.intervenant.last_name)
        )
