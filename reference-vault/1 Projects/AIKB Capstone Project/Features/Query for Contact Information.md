# Query for Contact Information

```
Feature: Query for Contact Information

  Scenario: Retrieve contact email address
    Given that the Knowledge Vault contains Person entities
    When the User requests a person's email address
    Then the Agent returns the value of the person's email property
    
  Scenario: Query contact by professional affiliation
    Given that the Knowledge Vault contains Person entities
    When the User asks a question like "Who do I know at Tesla?"
    Then the Agent searches Person entities where `worksFor` contains "Tesla"
    And the Agent responds with the correct list of Persons
```

