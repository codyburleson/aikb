# Feature: Query for Event Information

```
Feature: Query for Event Information

  Scenario: Query upcoming events
    Given that the Knowledge Vault contains Event entities
    When the User asks for this week's events
    Then the Agent queries Event entities where "startDate" falls within range
    And the Agent sorts by `startDate` and `startTime`
    And the Agent presents formatted calendar view
```
