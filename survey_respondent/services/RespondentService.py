from survey_respondent.models.Respondent import Respondent
from survey_respondent.models.Answers import YesNoAnswer, MatrixAnswer, MultipleChoiceAnswer, RankingAnswer
from survey_studio.models.Questions import MultipleChoiceQuestion, YesNoQuestion, RankingQuestion, MatrixQuestion, BaseQuestion


class RespondentService:

    def __init__(self, user_id, survey_id):
        self.respondent, created = Respondent.objects.get_or_create(user_id=user_id, survey_id=survey_id)


    def submit_answer_go_next(self, answer) -> BaseQuestion:

        if answer:
            self.__submit_answer(self.__get_question_by_order(self.respondent.last_question_order + 1),answer)
        return  self.__get_question_by_order(self.respondent.last_question_order + 1)

    def get_current_question(self) -> BaseQuestion:
        return self.__get_question_by_order(self.respondent.last_question_order + 1)

    def __get_question_by_order(self, order_value) -> BaseQuestion:

        question = (self.respondent.survey.yesnoquestion_questions.filter(order=order_value).first() or
                    self.respondent.survey.multiplechoicequestion_questions.filter(order=order_value).first() or
                    self.respondent.survey.matrixquestion_questions.filter(order=order_value).first() or
                    self.respondent.survey.rankingquestion_questions.filter(order=order_value).first())

        return question

    def __submit_answer(self, question, answer_data):

        if isinstance(question, YesNoQuestion):
            answer = YesNoAnswer.objects.create(respondent=self.respondent, survey=self.respondent.survey, question=question, answer=answer_data)
        elif isinstance(question, MultipleChoiceQuestion):
            answer = MultipleChoiceAnswer.objects.create(respondent=self.respondent, survey=self.respondent.survey, question=question,
                                                         selected_option=answer_data)
        elif isinstance(question, RankingQuestion):
            answer = RankingAnswer.objects.create(respondent=self.respondent, survey=self.respondent.survey, question=question, ranking=answer_data)
        elif isinstance(question, MatrixQuestion):
            answer = MatrixAnswer.objects.create(respondent=self.respondent, survey=self.respondent.survey, question=question,
                                                 answer_matrix=answer_data)
        self.__update_last_question_order(question)

    def __update_last_question_order(self, question: BaseQuestion):
        self.respondent.last_question_order = question.order
        self.respondent.save()