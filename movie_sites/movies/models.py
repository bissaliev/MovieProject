from django.db import models


GENDER_CHOICES = [("М", "Мужчина"), ("Ж", "Женщина"), ("U", "Unknown")]


class Actor(models.Model):
    first_name = models.CharField("Имя актера", max_length=100)
    last_name = models.CharField("Фамилия актера", max_length=100)
    birthdate = models.DateField("Дата рождения")
    description = models.TextField("Описание", blank=True, null=True)
    picture = models.ImageField(
        "Фото актера",
        upload_to="actor/images/%Y/%m/%d/",
        blank=True,
        null=True,
    )
    gender = models.CharField(
        "Гендер",
        max_length=1,
        choices=GENDER_CHOICES,
        default="U",
    )

    class Meta:
        verbose_name = "Актер"
        verbose_name_plural = "Актеры"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
