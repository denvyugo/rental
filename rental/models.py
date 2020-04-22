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
        ann_overdue = Borrowed.objects.filter(to_who=models.OuterRef('pk'),
                                              when__lte=datetools.datesub_month(2))
        return self.annotate(ann_overdue=models.Exists(ann_overdue))


class Friend(OwnedModel):
    name = models.CharField(max_length=100)

    objects = FriendQuerySet.as_manager()

    @property
    def has_overdue(self):
        if hasattr(self, 'ann_overdue'):
            return self.ann_overdue
        return self.borrowed_set.filter(
            returned__isnull=True, when__lte=datetools.datesub_month(2)
            ).exists()

    def __str__(self):
        return self.name


class BelongingQuerySet(models.QuerySet):
    def with_borrowed(self):
        has_borrowed = Borrowed.objects.filter(what=models.OuterRef('pk'),
                                               to_who__isnull=False, returned__isnull=True)
        return self.annotate(ann_borrowed=models.Exists(has_borrowed))


class Belonging(OwnedModel):
    name = models.CharField(max_length=100)

    objects = BelongingQuerySet.as_manager()

    @property
    def is_borrowed(self):
        if hasattr(self, 'ann_borrowed'):
            return self.ann_borrowed
        return self.borrowed_set.filter(
            returned__isnull=True, to_who__isnull=False).exists()

    def __str__(self):
        return self.name


class BorrowedQuerySet(models.QuerySet):
    def overdue(self):
        return self.filter(when__lte=datetools.datesub_month(2), returned__isnull=True)


class Borrowed(OwnedModel):
    what = models.ForeignKey(Belonging, on_delete=models.CASCADE)
    to_who = models.ForeignKey(Friend, on_delete=models.CASCADE)
    when = models.DateTimeField()
    returned = models.DateTimeField(null=True, blank=True)

    objects = BorrowedQuerySet.as_manager()

    def __str__(self):
        return f'{self.what} to {self.to_who}'
