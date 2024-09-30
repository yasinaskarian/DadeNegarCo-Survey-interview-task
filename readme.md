# SurveyApp

SurveyApp contains 3 main apps:

1. **dashboard**: This contains the ability to create surveys and retrieve reports.
2. **survey_studio**: This contains the studio feature for creating all types of questions and designing the survey.
3. **survey_respondent**: This contains the user/consumer API that allows respondents to walk through the questions and answer them based on priority (question order


### Create Survey Endpoint

- **URL**: `/api/dashboard/survey/create/`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
      "title": "FirstSurvey",
      "description": "My First Survey"
    }
    ```
### Update Survey Questions Endpoint

- **URL**: `/api/studio/survey/update/questions/`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
      "survey_id": 1,
      "questions": [
        {
          "RankingQuestion": {
            "text": "Rank these fruits",
            "order": 1,
            "options": ["Apple", "Banana", "Cherry"]
          }
        },
        {
          "YesNoQuestion": {
            "text": "Do you like pizza?",
            "order": 2
          }
        },
        {
          "YesNoQuestion": {
            "text": "Do you like burgers?",
            "order": 3
          }
        },
        {
          "MultipleChoiceQuestion": {
            "text": "Select your favorite color",
            "order": 4,
            "options": ["Red", "Blue", "Green"]
          }
        },
        {
          "MatrixQuestion": {
            "text": "What are your preferences?",
            "order": 5,
            "rows": ["Row 1", "Row 2"],
            "columns": ["Column 1", "Column 2"]
          }
        }
      ]
    }
    ```

- **Description**: This is a single API that can update all types of questions, making it helpful for the frontend. A single endpoint allows for dynamic changes to the JSON structure, simplifying frontend integration.

### Get Survey Questions Endpoint

- **URL**: `/api/studio/survey/get/questions/`
- **Method**: `GET`
- **Query Parameters**: 
  - `survey_id` (required)

- **Response**:
    ```json
    {
      "id": 1,
      "title": "Test Survey",
      "questions": [
        {
          "MultipleChoiceQuestion": {
            "text": "What is your favorite color?",
            "order": 1,
            "options": ["Red", "Blue"]
          }
        },
        {
          "YesNoQuestion": {
            "text": "Do you like pizza?",
            "order": 2
          }
        },
        {
          "MatrixQuestion": {
            "text": "Rate these items",
            "order": 3,
            "rows": ["Item 1", "Item 2"],
            "columns": ["Bad", "Good"]
          }
        },
        {
          "RankingQuestion": {
            "text": "Rank these",
            "order": 4,
            "options": ["Option 1", "Option 2"]
          }
        }
      ]
    }
    ```

- **Description**: This endpoint retrieves all the questions in a given survey by using the `survey_id` as a query parameter. The response includes various question types such as `MultipleChoiceQuestion`, `YesNoQuestion`, `MatrixQuestion`, and `RankingQuestion`.

### Walk Through The Survey Endpoint

- **URL**: `/api/respondent/go/next/`
- **Method**: `POST`

- **Request Body**:
    ```json
    {
      "survey_id": 3,
      "user_id": 6,
      "answer": {"Row 1": "Bad", "Row 2": "Good"} // For starting, this value should not be passed.
    }
    ```

- **Response**:
    ```json
    {
      "text": "Rate these items",
      "order": 1,
      "rows": [
        "Row 1",
        "Row 2"
      ],
      "columns": [
        "Good",
        "Bad"
      ],
      "question_type": "matrix"
    }
    ```

- **Description**: This API is used for respondents to walk through a survey. When the survey is first started, no answers are passed in the body. The response will provide the next question based on the survey's order. The response includes the question text, order, rows, columns, and the type of question (in this case, `matrix`).

### Get Current Question Endpoint

- **URL**: `/api/respondent/get/current/`
- **Method**: `GET`
- **Query Parameters**:
  - `user_id=1` (required)
  - `survey_id=3` (required)

- **Response**:
    ```json
    {
      "text": "Rate these items",
      "order": 1,
      "rows": [
        "Row 1",
        "Row 2"
      ],
      "columns": [
        "Good",
        "Bad"
      ],
      "question_type": "matrix"
    }
    ```

- **Description**: This endpoint retrieves the current question for a respondent based on the `user_id` and `survey_id`. The response contains the question text, order, rows, columns, and the type of question (e.g., `matrix`).

### Get Raw Answers Based on Survey and Question Order

- **URL**: `/api/dashboard/survey/raw/answers/`
- **Method**: `GET`
- **Query Parameters**:
  - `order_value=1` (required)
  - `survey_id=3` (required)

- **Response**:
    ```json
    {
      "matrix_answers": [
        {
          "user_id": 1,
          "question_text": "Rate these items",
          "rows": ["Row 1", "Row 2"],
          "columns": ["Good", "Bad"],
          "answer_matrix": [
            {"Row 1": "Good"},
            {"Row 2": "Good"}
          ],
          "created_at": "2024-09-30T05:53:44.092118Z"
        },
        {
          "user_id": 2,
          "question_text": "Rate these items",
          "rows": ["Row 1", "Row 2"],
          "columns": ["Good", "Bad"],
          "answer_matrix": [
            {"Row 1": "Good"},
            {"Row 2": "Good"}
          ],
          "created_at": "2024-09-30T05:54:15.674603Z"
        },
        {
          "user_id": 3,
          "question_text": "Rate these items",
          "rows": ["Row 1", "Row 2"],
          "columns": ["Good", "Bad"],
          "answer_matrix": [
            {"Row 1": "Good"},
            {"Row 2": "Good"}
          ],
          "created_at": "2024-09-30T05:54:26.711121Z"
        },
        {
          "user_id": 4,
          "question_text": "Rate these items",
          "rows": ["Row 1", "Row 2"],
          "columns": ["Good", "Bad"],
          "answer_matrix": {
            "Row 1": "Good",
            "Row 2": "Good"
          },
          "created_at": "2024-09-30T06:02:12.942802Z"
        },
        {
          "user_id": 5,
          "question_text": "Rate these items",
          "rows": ["Row 1", "Row 2"],
          "columns": ["Good", "Bad"],
          "answer_matrix": {
            "Row 1": "Good",
            "Row 2": "Good"
          },
          "created_at": "2024-09-30T06:02:35.584424Z"
        }
      ]
    }
    ```

- **Description**: This endpoint retrieves raw answers for a specific question in a survey, based on the `order_value` (question order) and `survey_id`. The response includes multiple respondents' answers for matrix-type questions,


## What Should I Do Next:

1. **Add Versioning to Published Surveys**:
   - Implement a versioning system for each published survey.
   - This will allow users to modify the survey during its published state without losing previous responses.
   - Each modification will create a new version of the survey, ensuring that past answers remain linked to the correct version.

2. **Add a Second Database for Archived Surveys**:
   - Create a second database called `Archived_db` to store expired surveys.
   - All expired surveys, along with their related data (questions, answers, etc.), will be moved to this archive.
   - This separation ensures that active surveys are not cluttered with historical data, improving performance and manageability.
