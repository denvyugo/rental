from django.conf import settings
from django.db import models
from . import datetools

# Create your models here.

class OwnedModel(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    class Meta:
        abstract = True


class FriendQuerySet(models.QuerySet):
    def with_overdue(self):
        return self.annotate(
            ann_overdue=models.Case(
                models.When(
                    borrowed__when__lte=datetools.datesub_month(2),
                    then=True),
                default=models.Value(False),
                output_field=models.BooleanField()
            )
        )


class Friend(OwnedModel):
    name = models.CharField(max_length=100)

    objects = FriendQuerySet.as_manager()

    @property
    def has_overdue(self):
        if hasattr(self, 'ann_overdue'):
            return self.ann_overdue
        return self.borrowed_set.filter(
            returned__isnull=True, when=datetools.datesub_month(2)
            ).exists()


class Belonging(OwnedModel):
    name = models.CharField(max_length=100)


class Borrowed(OwnedModel):
    what = models.ForeignKey(Belonging, on_delete=models.CASCADE)
    to_who = models.ForeignKey(Friend, on_delete=models.CASCADE)
    when = models.DateTimeField(auto_now_add=True)
    returned = models.DateTimeField(null=True, blank=True)
