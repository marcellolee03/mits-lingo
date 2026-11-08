from pydantic import BaseModel


class QuestionSchema(BaseModel):
    text: str
    answers: list[str]

    model_config = {
        'json_schema_extra': {
            'example': {
                'text': 'Olá! Tudo bem?',
                'answers': ['Hallo! Wie geht`s?'],
            }
        }
    }


class UserAnswerSchema(BaseModel):
    answer: str

    model_config = {
        'json_schema_extra': {
            'example': {
                'answer': 'Hallo! Wie geht`s?'
            }
        }
    }