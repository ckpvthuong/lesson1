from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from module.survey.models import Question


@receiver(pre_save, sender=Question)
def pre_save_callback(sender, **kwargs):
    print("pre_save!")


@receiver(post_save, sender=Question)
def post_save_callback(sender, **kwargs):
    print("post_save!")
