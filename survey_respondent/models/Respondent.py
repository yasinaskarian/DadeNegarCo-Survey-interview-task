from django.db import models
from dashboard.models.Survey import Survey



class Respondent(models.Model):
    user_id = models.PositiveBigIntegerField()
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    last_question_order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'Respondent {self.user_id} for Survey {self.survey}'

    class Meta:
        unique_together = ('survey', 'user_id')