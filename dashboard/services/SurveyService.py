from typing import Optional
from commons.CommonFunctionResponse import BooleanTypeResponse
from dashboard.models.Survey import Survey


class SurveyService:
    __survey: Optional[Survey] = None

    def set_survey(self, survey_id: Optional[int]) -> Optional[BooleanTypeResponse]:
        if not survey_id:
            return BooleanTypeResponse(is_successful=False, message="Survey ID is required.", status_code=400)

        response = self.__set_survey(survey_id)
        if not response.is_successful:
            return response

    def get_survey(self) -> Survey:
        return self.__survey

    def __set_survey(self, survey_id: int) -> BooleanTypeResponse:

        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            return BooleanTypeResponse(is_successful=False, message="Survey not found.", status_code=404)

        if survey.is_expired():
            return BooleanTypeResponse(is_successful=False, message="Cannot publish an expired survey.", status_code=400)

        self.__survey = survey
        return BooleanTypeResponse(is_successful=True)
