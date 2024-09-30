from django.db import models
from dashboard.models.Survey import Survey
from django.core.exceptions import ValidationError

class BaseQuestion(models.Model):
    survey = models.ForeignKey(Survey, related_name='%(class)s_questions', on_delete=models.CASCADE)
    text = models.TextField()
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        abstract = True

class MatrixQuestion(BaseQuestion):
    rows = models.JSONField()
    columns = models.JSONField()

    class Meta:
        unique_together = ('survey', 'order', 'text')

    def clean(self):
        super().clean()

        if isinstance(self.rows, list) and len(self.rows) != len(set(self.rows)):
            raise ValidationError('Rows must be unique.')

        if isinstance(self.columns, list) and len(self.columns) != len(set(self.columns)):
            raise ValidationError('Columns must be unique.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class MultipleChoiceQuestion(BaseQuestion):
    options = models.JSONField()

    class Meta:
        unique_together = ('survey', 'order', 'text')

    def clean(self):
        super().clean()

        if isinstance(self.options, list) and len(self.options) != len(set(self.options)):
            raise ValidationError('options must be unique.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class RankingQuestion(BaseQuestion):
    options = models.JSONField()

    class Meta:
        unique_together = ('survey', 'order', 'text')

    def clean(self):
        super().clean()

        if isinstance(self.options, list) and len(self.options) != len(set(self.options)):
            raise ValidationError('options must be unique.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class YesNoQuestion(BaseQuestion):
    pass

    class Meta:
        unique_together = ('survey', 'order', 'text')
