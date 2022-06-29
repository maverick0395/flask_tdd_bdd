from app.custom_types import CreateUser, CreatePost


TEST_USERS_DATA: list[CreateUser] = [
    {
        "username": "test_user_1",
        "email": "test_user_1@mail.com",
        "password": "password",
    },
    {
        "username": "test_user_2",
        "email": "test_user_2@mail.com",
        "password": "password",
    },
    {
        "username": "test_user_3",
        "email": "test_user_3@mail.com",
        "password": "password",
    },
    {
        "username": "test_user_4",
        "email": "test_user_4@mail.com",
        "password": "password",
    },
    {
        "username": "test_user_5",
        "email": "test_user_5@mail.com",
        "password": "password",
    },
]

TEST_POSTS_DATA: list[CreatePost] = [
    {
        "title": "test_post1_title",
        "body": "test_post1_body",
        "user_id": 1
    },
    {
        "title": "test_post2_title",
        "body": "test_post2_body",
        "user_id": 1
    },
    {
        "title": "test_post3_title",
        "body": "test_post3_body",
        "user_id": 2
    },
    {
        "title": "test_post4_title",
        "body": "test_post4_body",
        "user_id": 2
    },
    {
        "title": "test_post5_title",
        "body": "test_post5_body",
        "user_id": 3
    },
    {
        "title": "test_post6_title",
        "body": "test_post6_body",
        "user_id": 3
    },
    {
        "title": "test_post7_title",
        "body": "test_post7_body",
        "user_id": 4
    },
    {
        "title": "test_post8_title",
        "body": "test_post8_body",
        "user_id": 4
    },
    {
        "title": "test_post9_title",
        "body": "test_post9_body",
        "user_id": 5
    },
    {
        "title": "test_post10_title",
        "body": "test_post10_body",
        "user_id": 5
    },
]
