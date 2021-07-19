from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class TimeStampMixin(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return ""


class CustomUserManager(UserManager):

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser, TimeStampMixin):
    objects = CustomUserManager()

    @property
    def full_name(self):
        return self.get_full_name()

    class Meta:
        db_table = 'tbl_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username


# Create your models here.
class Survey(TimeStampMixin):
    name = models.CharField(max_length=255, null=True, blank=True, help_text='Hãy điền tên khảo sát ở đây!',
                            verbose_name='Câu khảo sát!')

    class Meta:
        db_table = 'tbl_survey'
        verbose_name = 'Survey'
        verbose_name_plural = 'Danh sách khảo sát'

    def __str__(self):
        return self.name


class Question(TimeStampMixin):
    name = models.CharField(max_length=255, null=True, blank=True, help_text='Hãy điền câu hỏi ở đây!',
                            verbose_name='Câu hỏi')
    survey = models.ForeignKey(Survey, null=True, blank=True, help_text='Chọn khảo sát', on_delete=models.DO_NOTHING,
                               related_name='questions')

    image = models.ForeignKey("Image", null=True, blank=True, on_delete=models.DO_NOTHING,
                              related_name='question_images')
    is_deleted = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        db_table = 'tbl_question'
        verbose_name = 'Câu hỏi'
        verbose_name_plural = 'Câu hỏi'

    def __str__(self):
        return self.name


class Answer(TimeStampMixin):
    name = models.CharField(max_length=255, null=True, blank=True, help_text='Hãy điền câu trả lời ở đây!',
                            verbose_name='Câu trả lời')
    question = models.ForeignKey(Question, null=True, blank=True, help_text='Chọn khảo sát',
                                 on_delete=models.DO_NOTHING,
                                 related_name='answer')
    is_deleted = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        db_table = 'tbl_answer'
        verbose_name = 'Câu trả lời'
        verbose_name_plural = 'Câu trả lời'

    def __str__(self):
        return self.name


class Image(TimeStampMixin):
    image = models.ImageField(null=True, blank=True, upload_to='upload/images/%Y/%m/%d')
    h = models.FloatField(null=True, blank=True, default=0)
    w = models.FloatField(null=True, blank=True, default=0)

    class Meta:
        db_table = 'tbl_image'

    @staticmethod
    def get_entity_name():
        return 'Image'
