from django.db import models

from common.models import TimeStampMixin


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
