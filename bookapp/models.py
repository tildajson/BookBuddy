from django.db import models
from django.conf import settings
from django.urls import reverse


class AllBooks(models.Model):
    """Model for all books."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             blank=True, null=True, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("myList", args=None)


class Book(models.Model):
    """Model for individual books."""
    title = models.TextField(blank=False)
    current_page = models.IntegerField(blank=False)
    total_pages = models.IntegerField(blank=False)
    all_books = models.ForeignKey(
        AllBooks, default=None, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("all_books", "title")
