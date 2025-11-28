# Retrieve Contact Information

```
Feature: Retrieve Contact Information

  Scenario: Retrieve contact email address
    Given the Knowledge vault contains Person entities
    When the User requests a person's email address
    Then the Agent returns the email address
```
