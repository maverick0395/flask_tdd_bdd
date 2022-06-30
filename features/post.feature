Feature: CRUD operations with posts

    @post
    Scenario: I want to get all posts
        Given I logged in as a user "test_user_1"
        When I request all posts
        Then I should see all posts