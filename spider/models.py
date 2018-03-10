from django.db import models


class AddUrlsInTable(models.Model):
    inn = models.CharField(max_length=1000)
    out = models.CharField(max_length=1000)

    class Meta:
        verbose_name = "Таблица "
        verbose_name_plural = "Таблица для расчета"

    def __str__(self):
        return "Объект номер {}".format(self.id)


class AddMainUrls(models.Model):
    url = models.CharField(max_length=1000)

    class Meta:
        verbose_name = "ссылка"
        verbose_name_plural = "ссылки"

    def __str__(self):
        # return "Объект номер {}".format(self.id)
        return self.url


class MainTable(models.Model):
    url = models.CharField(max_length=1000)
    in_count = models.IntegerField()
    out_count = models.IntegerField()
    rank = models.FloatField()