from behave import given, when , then

from app.services.post import PostService


@given('I logged in as a user "{username}"')
def step_given1(context, username):
    context.username = username
    response = context.client.post(
        '/login',
        data=dict(user_id=username, password="password"),
        follow_redirects=True
    )
    
@when('I request all posts')
def step_when2(context):
    context.response = context.client.get(
        'posts/all',
        follow_redirects=True
    )
    
@then('I should see all posts')
def step_then2(context):
    assert context.response.status_code == 200
    post_service: PostService = PostService()
    posts = post_service.get_all()
    first_post = posts[0]
    last_post = posts[-1]
    assert str.encode(first_post.title) in context.response.data
    assert str.encode(last_post.title) in context.response.data
    