from django.db import models

# Create your models here.


class Chat(models.Model):
    content = models.CharField(max_length=1000)
    time_stamp = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey("Group", on_delete=models.CASCADE)


class Group(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
