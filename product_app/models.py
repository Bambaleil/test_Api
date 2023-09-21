from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Product(models.Model):
    """ Model product """

    title = models.CharField(
        max_length=128,
    )
    description = models.TextField(
        null=False,
        blank=True,
    )
    user_id = models.ForeignKey(
        to=User,
        related_name="products",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    archived = models.BooleanField(
        default=False,
    )

    def get_all_lesson(self):
        return self.lessons.filter(archived=False)

    def get_total_lessons_viewed(self):
        return LessonView.objects.filter(lesson__products=self).count()

    def get_total_view_time(self):
        return LessonView.objects.filter(lesson__products=self).aggregate(total_view_time=Sum('view_time_seconds'))[
            'total_view_time'] or 0

    def get_total_students(self):
        return self.user_id.products.count()

    def get_acquisition_percentage(self):
        total_users = User.objects.count()
        if total_users == 0:
            return 0
        return (self.get_total_students() / total_users) * 100


class Lesson(models.Model):
    """ Model Lesson"""

    title = models.CharField(
        max_length=128,
    )
    description = models.TextField(
        null=False,
        blank=True,
    )
    products = models.ManyToManyField(
        to=Product,
        related_name="lessons"
    )
    link_video = models.URLField()
    durations_second = models.PositiveIntegerField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    archived = models.BooleanField(
        default=False,
    )

    class Meta:
        pass

    def get_all_product(self):
        return self.products.objects.all()

    def __str__(self):
        return self.title


class LessonView(models.Model):
    """ Model LessonView"""

    lesson = models.ForeignKey(
        to=Lesson,
        on_delete=models.CASCADE,
        related_name="views"
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="views"
    )
    view_time_seconds = models.PositiveIntegerField()
    status = models.BooleanField(default=False)

    class Meta:
        unique_together = ("lesson", "user")

    def update_status(self):
        progress = (self.view_time_seconds / self.lesson.durations_second) * 100
        if progress > 80:
            self.status = True
            self.save()
