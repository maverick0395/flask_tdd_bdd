Feature: Account registration, login and logout with that Account

    Scenario: I want to visit the main page as unregistered user
        Given User is not logged in
        When I go to app's main page
        Then I should be redirected to "auth.login" endpoint

    @test_tag
    Scenario: I want to register new Account
        Given User is not logged in
        When I fill registration form and press Submit
            | field                 | value         |
            | username              | test_username |
            | email                 | test@mail.com |
            | password              | 123456        |
            | password_confirmation | 123456        |
        Then I should be redirected to main page and see "Registration successful. You are logged in." message
        And New User object should be created in database
