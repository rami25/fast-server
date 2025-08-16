from pydantic import BaseModel

class Question(BaseModel):
  question: str
  answer: int

class Form(BaseModel):
  questions: list[Question] = []

class FormResponse(Form):
  id: str

class UpdateForm(FormResponse):
  pass

class DeleteForm(BaseModel):
  id: str