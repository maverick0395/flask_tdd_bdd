@one_tag
Feature: Account registration, login and logout with that account

    @test_tag
    Scenario: I want to visit the main page as unregistered user
        Given User is not logged in
        When I go to app's main page
        Then I should be redirected to "auth.login" endpoint

    Scenario: I want to register new account in this app
        Given User is not logged in
        When I fill registration form and press Submit
            | field                | value         |
            | username             | test_username |
            | email                | test@mail.com |
            | password             | 123456        |
            | password_confirmation| 123456        |
        Then I should be redirected to main page and see "Registration successful. You are logged in." message
        And New User object should be created in database

    Scenario: I want to login into my account
        Given User is not logged in
        When I fill log-in form with username "test_user_1", password "password" and press Login
        Then I should be redirected to the main page of the app and see message "Login successful."

    Scenario: I want to logout from my account
        Given User is logged in as "test_user_1"
        When I press "Log Out"
        Then I should be redirected to login page and see message "You were logged out."
