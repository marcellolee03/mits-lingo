from fastapi import APIRouter, HTTPException, Path
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from dependecies.db_dependency import db_dependency
from entities.question.model import Question
from entities.question.schema import QuestionSchema, UserAnswerSchema

router = APIRouter(
    prefix='/questions',
    tags=['questions']
)

id_type = Path(gt=0)

@router.get('/', status_code=HTTP_200_OK)
async def get_questions(
    db: db_dependency
):

    return db.query(Question).all()


@router.post('/', status_code=HTTP_201_CREATED)
async def create_question(
    db: db_dependency,
    request: QuestionSchema
):
    new_question = Question(**request.model_dump())

    db.add(new_question)
    db.commit()

    return new_question


@router.get('/{id}', status_code=HTTP_200_OK)
async def get_question_by_id(
    db: db_dependency,
    id: int = id_type,
):
    question = db.query(Question).filter(Question.id == id).first()
    
    if not question:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Question not found.')
        
    return question


@router.put('/{id}', status_code=HTTP_200_OK)
async def update_question_by_id(
    db: db_dependency,
    request: QuestionSchema,
    id: int = id_type,
):
    new_question = Question(**request.model_dump())
    question = db.query(Question).filter(Question.id == id).first()
    
    if not question:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Question not found.')

    question.text = new_question.text
    question.answers = new_question.answers

    db.add(question)
    db.commit()

    return question


@router.delete('/{id}', status_code=HTTP_200_OK)
async def delete_question_by_id(
    db: db_dependency,
    id: int = id_type,
):
    question = db.query(Question).filter(Question.id == id).first()
    
    if not question:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Question not found.')

    db.delete(question)
    db.commit()
    

@router.post('/{id}/check_answer', status_code=HTTP_200_OK)
async def check_answer(
    db: db_dependency,
    request: UserAnswerSchema,
    id: int = id_type
):
    question = db.query(Question).filter(Question.id == id).first()
    user_answer = request.answer

    if not question:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Question not found.')
        
    for answer in question.answers:
        if user_answer == answer:
            return True

    return False