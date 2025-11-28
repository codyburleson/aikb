# Feature: Content Enhancement

```
Feature: Content Enhancement

  Scenario: User requests metadata enhancement
    Given that Knowledge objects exist with incomplete metadata
    And object content contains extractable information
    When the User requests metadata enhancement
    Then the Agent reads Person entity markdown content
    And the Agent applies NLP to extract entities and facts
    And the Agent identifies missing metadata fields
    And the Agent proposes updates
    And the User approves
    And the Agent updates frontmatter
```

Example:

**Agent Analysis**: "I found these metadata fields in the content:

- jobTitle: Software Engineer (from 'software engineer at Acme Corp')
- worksFor: Acme Corp
- email: [john.smith@acme.com](mailto:john.smith@acme.com)
- telephone: +1-555-0199

Would you like me to add these to the frontmatter?"


```
  Feature: Content Enhancement
  
  Scenario: Suggest Entity Links
    Given that note content mentions entities that exist in vault
    When the User requests link suggestions
    Then the Agent analyzes note content
    And the Agent identifies potential entity references
    And the Agent matches against existing vault entities
    And the Agent proposes link insertions
    And the User approves
    And the Agent updates content
```

