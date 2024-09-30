from django.db import models
from survey_respondent.models.Respondent import Respondent
from survey_studio.models.Questions import MultipleChoiceQuestion, YesNoQuestion, RankingQuestion, MatrixQuestion
from dashboard.models.Survey import Survey
from django.core.exceptions import ValidationError


class BaseAnswer(models.Model):
    respondent = models.ForeignKey(Respondent, related_name='%(class)s_answers', on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, related_name='%(class)s_survey_answers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class YesNoAnswer(BaseAnswer):
    question = models.ForeignKey(YesNoQuestion, related_name='yes_no_answers',
                                 on_delete=models.CASCADE)
    answer = models.BooleanField()

    class Meta:
        unique_together = ('respondent', 'question')


class MultipleChoiceAnswer(BaseAnswer):
    question = models.ForeignKey(MultipleChoiceQuestion, related_name='multiple_choice_answers',
                                 on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=255)

    class Meta:
        unique_together = ('respondent', 'question')

    def clean(self):
        super().clean()

        if self.selected_option not in self.question.options:
            raise ValidationError('Selected option is not a valid choice.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class RankingAnswer(BaseAnswer):
    question = models.ForeignKey(RankingQuestion, related_name='ranking_answers',
                                 on_delete=models.CASCADE)
    ranking = models.JSONField()

    class Meta:
        unique_together = ('respondent', 'question')

    def clean(self):
        super().clean()

        if set(self.ranking) != set(self.question.options):
            raise ValidationError('Ranking must include all options from the question.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class MatrixAnswer(BaseAnswer):
    question = models.ForeignKey(MatrixQuestion, related_name='matrix_answers',
                                 on_delete=models.CASCADE)
    answer_matrix = models.JSONField()

    class Meta:
        unique_together = ('respondent', 'question')

    def clean(self):
        super().clean()


        if set(self.answer_matrix.keys()) != set(self.question.rows):
            raise ValidationError('Answer matrix rows must match the question rows.')

        for row, cols in self.answer_matrix.items():

            if cols not in self.question.columns:
                raise ValidationError(f'Answer matrix columns in row "{row}" must match the question columns.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)