Feature: CRUD operations with posts

    Scenario: I want to get all posts
        Given I am logged in as "test_user_1"
        When I request all posts
        Then I should see all posts

    Scenario: I want to get only my posts
        Given I am logged in as "test_user_1"
        When I request my posts
        Then I should see only my posts

    Scenario: I want to get specific post by ID
        Given I am logged in as "test_user_1"
        When I request post with ID "4"
        Then I should see post with ID "4"
        
    Scenario: I want to create new post
        Given I am logged in as "test_user_1"
        When I fill post creation form and press create
            | field | value             |
            | title | Unique post title |
            | body  | Unique post body  |
        Then I should see newly created post in post list

    Scenario: I want to update my post
        Given I am logged in as "test_user_1"
        When I fill post update form and press update
            | field | value             |
            | title | Updated post title |
            | body  | Updated post body  |
        Then I should see updated post info in post list

    Scenario: I want to delete my post
        Given I am logged in as "test_user_1"
        When I press delete button for post with ID "1"
        Then Post with ID "1" should be deleted from database
