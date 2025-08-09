from uuid import UUID
from . import models

# all
def get_user_by_id(user_id: UUID) -> models.UserResponse:
  pass
def change_password(user_id: UUID, password_change: models.PasswrodChange) -> None:
  pass
def get_dash(dash_id: UUID):
  pass
def get_report(report_id: UUID):
  pass
def register_form():
  pass
# manager
def create_user():
  pass
def update_user():
  pass
def delete_user():
  pass