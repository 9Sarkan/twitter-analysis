from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.validators import MaxValueValidator


class Tweet(models.Model):
    search_item = models.CharField(max_length=256)
    excepted_words = ArrayField(
        models.CharField(max_length=256), size=256, null=True, blank=True
    )

    id = models.IntegerField(primary_key=True)
    author = models.JSONField()
    created_date = models.DateTimeField()
    entities = models.JSONField(blank=True, null=True)
    source = models.CharField(max_length=256)
    lang = models.CharField(max_length=64)
    text = models.TextField()


class Tag(models.Model):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    tag = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)
    collection = ArrayField(models.CharField(max_length=256), size=256)
    lang = models.CharField(_("Language"), max_length=10, default="en")
    collect_size = models.PositiveIntegerField(
        _("Collect size"), default=1000, validators=[MaxValueValidator(18000)]
    )
    get_data = models.BooleanField(_("Get Data"), default=False)

    def __str__(self):
        return f"tag: {self.tag}"
