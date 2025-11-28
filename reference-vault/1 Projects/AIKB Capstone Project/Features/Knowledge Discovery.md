# Feature: Knowledge Discovery

```
Feature: Knowledge Discovery

  Scenario: Explore entity connections
    Given that the Knowledge Vault contains entities that reference each other via metadata or content links
    When the User asks a question like "Show me everything related to Andrej Karpathy"
    Then the Agent presents an organized view of entities related to Andrej Karpathy

```

