from starlette import status

from ..routers.admin import get_db, get_current_user
from .utils import *

# Mocking (overrides functions)
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_get_todos(test_todo):
    response = client.get("admin/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'title': 'Test Todos',
                                'description': 'Test Todos description',
                                'priority': 5,
                                'complete' : False,
                                'owner_id' : 1,
                                'id' : 1}]

def test_admin_delete_todo(test_todo):
    response = client.delete("admin/todos/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None
