# Record Contact Information

```
Feature: Record Contact Information

  Scenario: Record contact information
    Given the Knowledge vault contains a Person template
    When the User asks for a contact to be added
    Then the Agent creates a new Person entity with the provided information
    And the entity is saved in the correct vault folder
```