from tkinter.messagebox import NO
from behave import given, when, then

from app.services.user import UserService


@given("User is not logged in")
def step_given1(context):
    response = context.client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page" in response.data


@when("I go to app's main page")
def step_when1(context):
    context.response = context.client.get("/", follow_redirects=True)


@then('I should be redirected to "auth.login" endpoint')
def step_then1(context):
    assert context.response.status_code == 200
    assert b"Please log in to access this page" in context.response.data


@when("I fill registration form and press Submit")
def step_when2(context):
    context.registration_data: dict = {}
    for row in context.table:
        context.registration_data[row["field"]] = row["value"]
    context.response = context.client.post(
        "/register", data=context.registration_data, follow_redirects=True
    )


@then('I should be redirected to main page and see "{message}" message')
def step_then2(context, message):
    assert context.response.status_code == 200
    assert str.encode(message) in context.response.data


@then("New User object should be created in database")
def step_then22(context):
    user_service: UserService = UserService()
    user = user_service.get(username=context.registration_data["username"])
    assert user is not None