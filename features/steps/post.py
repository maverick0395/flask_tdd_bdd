from behave import given, when, then

from app.services import PostService, UserService


@given('I am logged in as "{username}"')
def step_given1(context, username):
    context.username = username
    response = context.client.post(
        "/login",
        data=dict(user_id=username, password="password"),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Login successful." in response.data


@when("I request all posts")
def step_when(context):
    context.response = context.client.get("posts/all", follow_redirects=True)


@then("I should see all posts")
def step_then(context):
    assert context.response.status_code == 200
    post_service: PostService = PostService()
    posts = post_service.get_all()
    first_post = posts[0]
    last_post = posts[-1]
    assert str.encode(first_post.title) in context.response.data
    assert str.encode(last_post.title) in context.response.data


@when("I request my posts")
def step_when2(context):
    context.response = context.client.get("posts/my_posts", follow_redirects=True)


@then("I should see only my posts")
def step_then2(context):
    assert context.response.status_code == 200
    user_service: UserService = UserService()
    user = user_service.get(username=context.username)
    post_service: PostService = PostService()
    posts = post_service.get_all_by_filter_query(user_id=user.id)
    first_post = posts[0]
    other_user_posts = post_service.get_all_by_filter_query(user_id=3)
    other_user_post = other_user_posts[0]
    assert str.encode(first_post.title) in context.response.data
    assert str.encode(other_user_post.title) not in context.response.data


@when('I request post with ID "{post_id}"')
def step_when3(context, post_id):
    context.response = context.client.get(f"posts/{post_id}", follow_redirects=True)


@then('I should see post with ID "{post_id}"')
def step_then3(context, post_id):
    assert context.response.status_code == 200
    post_service: PostService = PostService()
    post = post_service.get(id=post_id)
    assert str.encode(post.title) in context.response.data
    assert str.encode(post.body) in context.response.data


@when("I fill post creation form and press create")
def step_when4(context):
    context.post_data: dict = {}
    for row in context.table:
        context.post_data[row["field"]] = row["value"]
    user_service: UserService = UserService()
    user = user_service.get(username=context.username)
    context.post_data["user_id"] = user.id
    context.response = context.client.post(
        "posts/create", data=context.post_data, follow_redirects=True
    )


@then("I should see newly created post in post list")
def step_then4(context):
    assert context.response.status_code == 200
    assert str.encode(context.post_data["title"]) in context.response.data
    assert str.encode(context.post_data["body"]) in context.response.data


@when("I fill post update form and press update")
def step_when5(context):
    context.update_data: dict = {}
    for row in context.table:
        context.update_data[row["field"]] = row["value"]
    context.response = context.client.post(
        "posts/1/update", data=context.update_data, follow_redirects=True
    )


@then("I should see updated post info in post list")
def step_then5(context):
    assert context.response.status_code == 200
    assert str.encode(context.update_data["title"]) in context.response.data
    assert str.encode(context.update_data["body"]) in context.response.data


@when('I press delete button for post with ID "{post_id}"')
def step_when6(context, post_id):
    context.response = context.client.delete(
        f"posts/{post_id}/delete", follow_redirects=True
    )


@then('Post with ID "{post_id}" should be deleted from database')
def step_then6(context, post_id):
    assert context.response.status_code == 200
    post_service: PostService = PostService()
    post = post_service.get(id=post_id)
    assert post is None
