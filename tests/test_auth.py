from .utils import register, login, logout


def test_register(client):
    response = client.post(
        "/register",
        data=dict(
            username="sam",
            email="sam@test.com",
            password="password",
            password_confirmation="password",
        ),
        follow_redirects=True,
    )
    assert b"Registration successful. You are logged in" in response.data


def test_login_and_logout(client):
    # Access to logout view before login should fail.
    response = logout(client)
    assert b"Please log in to access this page." in response.data
    register("sam")
    response = login(client, "sam")
    assert b"Login successful." in response.data
    # Should successfully logout the currently logged in user.
    response = logout(client)
    assert b"You were logged out." in response.data
    # Incorrect login credentials should fail.
    response = login(client, "sam", "wrongpassword")
    assert b"Wrong user ID or password." in response.data
    # Correct credentials should login
    response = login(client, "sam")
    assert b"Login successful." in response.data
