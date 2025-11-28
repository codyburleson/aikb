# Create Contact (Person)

```
Feature: Create Contact (Person)

  Scenario: Create new contact with email
    Given that the Knowledge Vault contains a Person template
    When the User asks for a contact to be added with a specified email
    Then the Agent creates a new Person entity with the provided email address
    And the contact is saved as a Person type in the correct vault folder
    And the email address is saved with the "email" metadata property
```