# AIKB Use Cases and Requirements

- **Version:** 0.1 (DRAFT)
- **Status:** Draft Document
- **Date:** 2025-11-17
- **Related:** [AIKB Specification v0.1](./aikb-0.1.md)

---

## Abstract

This document provides detailed use cases and requirements for the Agent-Interoperable Knowledge Base (AIKB) specification. Each use case includes concrete examples, user interactions, agent behavior, and traceability to specification requirements.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Use Case Template](#2-use-case-template)
3. [Contact Management Use Cases](#3-contact-management-use-cases)
4. [Event and Calendar Use Cases](#4-event-and-calendar-use-cases)
5. [Project Management Use Cases](#5-project-management-use-cases)
6. [Knowledge Discovery Use Cases](#6-knowledge-discovery-use-cases)
7. [Content Enhancement Use Cases](#7-content-enhancement-use-cases)
8. [Requirements Summary](#8-requirements-summary)

---

## 1. Introduction

### 1.1 Purpose

This document demonstrates how AIKB-compliant agents should interact with personal knowledge bases through detailed, testable scenarios. Each use case:

- Describes a specific user goal
- Provides example user queries/commands
- Details expected agent behavior
- Shows concrete data examples from the reference vault
- Maps to specification requirements

### 1.2 Audience

- **Agent Developers**: Use these scenarios for implementation and testing
- **Users**: Understand what's possible with AIKB-compliant systems
- **Specification Authors**: Ensure requirements align with real-world needs

### 1.3 Document Conventions

- **UC-XXX**: Use Case identifier
- **REQ-XXX**: Requirement identifier (maps to specification)
- Code blocks show actual file content from reference vault
- User queries appear in quotation marks

---

## 2. Use Case Template

Each use case follows this structure:

**UC-XXX: [Use Case Title]**

- **Category**: Contact Management | Events | Projects | Discovery | Enhancement
- **Priority**: High | Medium | Low
- **Actors**: User, Agent, Knowledge Vault
- **Preconditions**: Required vault state
- **Trigger**: User action or query
- **Main Flow**: Step-by-step interaction
- **Postconditions**: Expected outcome
- **Alternative Flows**: Variations or error cases
- **Example Data**: Actual markdown files
- **Requirements**: Related specification requirements

---

## 3. Contact Management Use Cases

### UC-001: Retrieve Contact Email Address

**Category**: Contact Management
**Priority**: High
**Actors**: User, AIKB Agent

**Preconditions**:
- Knowledge vault contains Person entities
- At least one Person entity has an `email` property

**Trigger**: User asks for someone's email address

**Main Flow**:

1. **User**: "Give me John Smith's email address"
2. **Agent**: Searches vault for Person entities
3. **Agent**: Parses files matching name "John Smith"
4. **Agent**: Extracts `email` from YAML frontmatter
5. **Agent**: "John Smith's email is john.smith@example.com"

**Postconditions**:
- User receives accurate contact information
- No files are modified

**Alternative Flows**:

**A1: Multiple Matches**
- Agent finds multiple people named "John Smith"
- Agent: "I found 2 people named John Smith. Which one did you mean?"
  - "John Smith (Software Engineer at Acme Corp)"
  - "John Smith (Marketing Director)"

**A2: No Email Available**
- Person entity exists but has no email property
- Agent: "I found John Smith, but no email address is listed."

**A3: Person Not Found**
- No Person entity matches the query
- Agent: "I couldn't find anyone named John Smith in your vault."

**Example Data**:

File: `3 Resources/Persons/J - L/John Smith/John Smith.md`

```yaml
---
template: "[[Person Template]]"
tags:
  - type/person
givenName: John
familyName: Smith
email: john.smith@example.com
telephone: "+1-555-0123"
jobTitle: Software Engineer
worksFor: "[[Acme Corp]]"
created: 2024-03-15
updated: 2025-11-10
---

John is a senior software engineer specializing in distributed systems.
```

**Requirements**:
- REQ-SPEC-6.2.1: Person Template schema
- REQ-SPEC-7.1: Metadata naming conventions
- REQ-AGENT-001: Entity search and retrieval

---

### UC-002: Query Contact by Professional Affiliation

**Category**: Contact Management
**Priority**: Medium
**Actors**: User, AIKB Agent

**Preconditions**:
- Vault contains multiple Person entities
- Person entities have `worksFor` or `affiliation` properties

**Trigger**: User searches for contacts by organization

**Main Flow**:

1. **User**: "Who do I know at Tesla?"
2. **Agent**: Searches Person entities where `worksFor` contains "Tesla"
3. **Agent**: Aggregates results
4. **Agent**: "You have 2 contacts at Tesla:"
   - "Andrej Karpathy (Director of AI)"
   - "Elon Musk (CEO)"

**Example Data**:

File: `3 Resources/Persons/A - C/Andrej Karpathy/Andrej Karpathy.md`

```yaml
---
template: "[[Person Template]]"
tags:
  - type/person
givenName: Andrej
familyName: Karpathy
birthday: 1986-10-23
jobTitle: Director of AI
worksFor: Tesla
url: https://karpathy.ai
created: 2024-08-29
updated: 2025-05-08T20:32
---

Andrej Karpathy is a Slovak-Canadian computer scientist specializing in deep learning and computer vision.
```

**Requirements**:
- REQ-SPEC-6.2.1: Person Template with `worksFor` property
- REQ-AGENT-002: Metadata property queries
- REQ-AGENT-003: Result aggregation

---

### UC-003: Export Contact as vCard

**Category**: Contact Management
**Priority**: Low
**Actors**: User, AIKB Agent

**Preconditions**:
- Person entity exists with contact information

**Trigger**: User requests export to vCard format

**Main Flow**:

1. **User**: "Export Andrej Karpathy's contact info as a vCard"
2. **Agent**: Locates Person entity
3. **Agent**: Maps AIKB metadata to vCard properties
4. **Agent**: Generates vCard file
5. **Agent**: "Created andrej-karpathy.vcf"

**Example Output**:

```vcard
BEGIN:VCARD
VERSION:4.0
FN:Andrej Karpathy
N:Karpathy;Andrej;;;
BDAY:19861023
TITLE:Director of AI
ORG:Tesla
URL:https://karpathy.ai
REV:20250508T203200Z
END:VCARD
```

**Requirements**:
- REQ-SPEC-1.4: vCard compatibility
- REQ-AGENT-004: Format conversion
- REQ-SPEC-7.3: ISO 8601 date formats

---

## 4. Event and Calendar Use Cases

### UC-101: Query Upcoming Events

**Category**: Events
**Priority**: High
**Actors**: User, AIKB Agent

**Preconditions**:
- Vault contains Event entities with `startDate` properties

**Trigger**: User asks about upcoming events

**Main Flow**:

1. **User**: "What events do I have this week?"
2. **Agent**: Determines current date and week range
3. **Agent**: Queries Event entities where `startDate` falls within range
4. **Agent**: Sorts by `startDate` and `startTime`
5. **Agent**: Presents formatted calendar view

**Example Response**:

```
Your events this week (Nov 17-23, 2025):

Tuesday, Nov 18
  • 10:00 - Meeting with Sponsor

Thursday, Nov 20
  • 06:00 - Thursday Morning Training Run
  • 16:00 - Physical Therapy

Friday, Nov 21
  • 14:00 - Team Standup
```

**Example Data**:

File: `3 Resources/Events/Recurring Events/Weekly/Meeting with Sponsor.md`

```yaml
---
template: "[[Event Template]]"
tags:
  - type/event
eventName: Meeting with Sponsor
startTime: "10:00"
endTime: "11:00"
weeklyRecurDay: Tuesday
location: Zoom
created: 2024-01-15
updated: 2025-11-01
---

Weekly check-in with program sponsor to discuss progress and roadblocks.
```

**Requirements**:
- REQ-SPEC-6.2.2: Event Template schema
- REQ-SPEC-7.3: Date/time formats
- REQ-AGENT-010: Date range queries
- REQ-AGENT-011: Recurrence expansion

---

### UC-102: Find Events Related to Project

**Category**: Events
**Priority**: Medium
**Actors**: User, AIKB Agent

**Preconditions**:
- Event entities reference Project entities via `relatedTo`

**Trigger**: User queries events by project

**Main Flow**:

1. **User**: "Show me all events related to the ACME project"
2. **Agent**: Finds Project entity matching "ACME"
3. **Agent**: Searches Event entities where `relatedTo` contains project reference
4. **Agent**: Returns chronologically sorted events

**Example Data**:

File: `3 Resources/Events/Current and Future Events/ACME Kickoff Meeting.md`

```yaml
---
template: "[[Event Template]]"
tags:
  - type/event
eventName: ACME Project Kickoff
startDate: 2025-12-01
startTime: "09:00"
endTime: "10:30"
location: Conference Room A
attendees:
  - "[[John Smith]]"
  - "[[Jane Doe]]"
organizer: "[[Sarah Johnson]]"
relatedTo:
  - "[[ACME Redesign Project]]"
eventStatus: scheduled
---

Initial kickoff meeting to align stakeholders on project goals and timeline.
```

**Requirements**:
- REQ-SPEC-8.3: Metadata references
- REQ-AGENT-012: Entity relationship queries
- REQ-AGENT-013: Reference resolution

---

### UC-103: Create Weekly Calendar View

**Category**: Events
**Priority**: Medium
**Actors**: User, AIKB Agent

**Preconditions**:
- Vault contains both one-time and recurring events

**Trigger**: User requests weekly calendar

**Main Flow**:

1. **User**: "Show me my calendar for next week"
2. **Agent**: Determines target week (Nov 24-30, 2025)
3. **Agent**: Expands recurring events for that week
4. **Agent**: Merges one-time events
5. **Agent**: Generates day-by-day view with time slots

**Expected Behavior**:
- Agent must interpret `weeklyRecurDay`, `monthlyRecurDay`, `yearlyRecurMonth` patterns
- Agent sorts events by date/time within each day
- Agent handles all-day events (no `startTime`)

**Requirements**:
- REQ-SPEC-6.2.2: Event recurrence metadata
- REQ-AGENT-011: Recurrence rule processing
- REQ-AGENT-014: Calendar view generation

---

## 5. Project Management Use Cases

### UC-201: Get Project Status

**Category**: Projects
**Priority**: High
**Actors**: User, AIKB Agent

**Preconditions**:
- Vault contains Project entities with status and progress metadata

**Trigger**: User asks about specific project

**Main Flow**:

1. **User**: "What's the status of the AIKB project?"
2. **Agent**: Locates Project entity matching "AIKB"
3. **Agent**: Extracts key metadata
4. **Agent**: Formats status report

**Example Response**:

```
AIKB Specification Development

Status: Active (35% complete)
Priority: High
Owner: Cody Burleson
Timeline: Nov 10 - Nov 14, 2025 (Due: Nov 14)

Next Actions:
  • Complete Person, Event, and Project templates
  • Draft Agent Interaction Protocol section
  • Create reference vault examples

Last Updated: Nov 17, 2025
```

**Example Data**:

File: `3 Resources/Projects/AIKB Specification Development.md`

```yaml
---
template: "[[Project Template]]"
tags:
  - type/project
projectName: AIKB Specification Development
projectStatus: active
priority: high
startDate: 2025-11-10
dueDate: 2025-11-14
owner: "[[Cody Burleson]]"
progress: 35
category: AI Agents
nextActions:
  - Complete Person, Event, and Project templates
  - Draft Agent Interaction Protocol section
  - Create reference vault examples
created: 2025-11-10
updated: 2025-11-17
---

Develop the Agent-Interoperable Knowledge Base specification as a capstone project.
```

**Requirements**:
- REQ-SPEC-6.2.3: Project Template schema
- REQ-AGENT-020: Project status queries
- REQ-AGENT-021: Formatted reporting

---

### UC-202: List All Next Actions

**Category**: Projects
**Priority**: High
**Actors**: User, AIKB Agent

**Preconditions**:
- Multiple Project entities exist with `nextActions` arrays

**Trigger**: User wants consolidated action list

**Main Flow**:

1. **User**: "What are my next actions across all active projects?"
2. **Agent**: Queries all Project entities where `projectStatus` = "active"
3. **Agent**: Extracts `nextActions` arrays from each
4. **Agent**: Aggregates and presents grouped by project

**Example Response**:

```
Your Next Actions (3 active projects):

AIKB Specification Development:
  • Complete Person, Event, and Project templates
  • Draft Agent Interaction Protocol section
  • Create reference vault examples

Website Redesign:
  • Review wireframes with design team
  • Update content inventory
  • Schedule user testing sessions

Q4 Marketing Campaign:
  • Finalize campaign messaging
  • Approve creative assets
  • Set up tracking analytics
```

**Requirements**:
- REQ-SPEC-6.2.3: `nextActions` metadata property
- REQ-AGENT-022: Multi-entity aggregation
- REQ-AGENT-023: Status filtering

---

### UC-203: Track Project Dependencies

**Category**: Projects
**Priority**: Medium
**Actors**: User, AIKB Agent

**Preconditions**:
- Projects have `parentProject`, `subProjects`, or `relatedProjects` references

**Trigger**: User explores project relationships

**Main Flow**:

1. **User**: "Show me all sub-projects of the Digital Transformation initiative"
2. **Agent**: Locates Project entity
3. **Agent**: Follows `subProjects` references
4. **Agent**: Retrieves each referenced project
5. **Agent**: Presents hierarchical view with status

**Example Response**:

```
Digital Transformation Initiative (Planning)
├── Website Redesign (Active, 60%)
├── CRM Migration (Active, 25%)
└── Data Warehouse Modernization (On Hold)
```

**Requirements**:
- REQ-SPEC-6.2.3: Project relationship metadata
- REQ-SPEC-8.3: Entity references
- REQ-AGENT-024: Graph traversal
- REQ-AGENT-025: Hierarchical presentation

---

## 6. Knowledge Discovery Use Cases

### UC-301: Find Related Entities

**Category**: Knowledge Discovery
**Priority**: Medium
**Actors**: User, AIKB Agent

**Preconditions**:
- Entities reference each other via metadata or content links

**Trigger**: User explores entity connections

**Main Flow**:

1. **User**: "Show me everything related to Andrej Karpathy"
2. **Agent**: Locates Person entity for Andrej Karpathy
3. **Agent**: Searches all entities that reference this person
4. **Agent**: Groups by entity type
5. **Agent**: Presents organized view

**Example Response**:

```
Entities related to Andrej Karpathy:

Projects (1):
  • Tesla Autopilot Research (referenced as team member)

Events (2):
  • AI Conference 2025 (listed as attendee)
  • Weekly AI Reading Group (organizer)

Notes (5):
  • Neural Networks Course Notes
  • Deep Learning Best Practices
  • Computer Vision Resources
  • Tesla AI Day Summary
  • OpenAI History Timeline
```

**Requirements**:
- REQ-SPEC-8: Linking and references
- REQ-AGENT-030: Backlink discovery
- REQ-AGENT-031: Cross-entity search

---

### UC-302: Build Knowledge Graph

**Category**: Knowledge Discovery
**Priority**: Low
**Actors**: User, AIKB Agent

**Preconditions**:
- Vault contains multiple interconnected entities

**Trigger**: User requests visualization or graph analysis

**Main Flow**:

1. **User**: "Show me a knowledge graph of my professional network"
2. **Agent**: Traverses all Person entities
3. **Agent**: Identifies connections via:
   - Shared `worksFor` organizations
   - Co-attendance at events (`attendees`)
   - Collaboration on projects (`team`, `stakeholders`)
4. **Agent**: Generates graph data structure
5. **Agent**: Exports to visualization format (GraphML, DOT, JSON)

**Requirements**:
- REQ-AGENT-032: Graph construction
- REQ-AGENT-033: Multi-relation analysis
- REQ-AGENT-034: Export formats

---

## 7. Content Enhancement Use Cases

### UC-401: Auto-populate Missing Metadata

**Category**: Content Enhancement
**Priority**: Medium
**Actors**: User, AIKB Agent

**Preconditions**:
- Knowledge object exists with incomplete metadata
- Object content contains extractable information

**Trigger**: User requests metadata enhancement

**Main Flow**:

1. **User**: "Enhance metadata for John Smith's contact card"
2. **Agent**: Reads Person entity markdown content
3. **Agent**: Applies NLP to extract entities and facts
4. **Agent**: Identifies missing metadata fields
5. **Agent**: Proposes updates
6. **User**: Reviews and approves
7. **Agent**: Updates frontmatter

**Example Scenario**:

**Before** (`John Smith.md`):
```yaml
---
template: "[[Person Template]]"
tags:
  - type/person
givenName: John
familyName: Smith
---

John Smith is a software engineer at Acme Corp specializing in distributed systems.
He can be reached at john.smith@acme.com or +1-555-0199.
```

**Agent Analysis**:
"I found these metadata fields in the content:
- jobTitle: Software Engineer (from 'software engineer at Acme Corp')
- worksFor: Acme Corp
- email: john.smith@acme.com
- telephone: +1-555-0199

Would you like me to add these to the frontmatter?"

**After** (user approves):
```yaml
---
template: "[[Person Template]]"
tags:
  - type/person
givenName: John
familyName: Smith
jobTitle: Software Engineer
worksFor: "[[Acme Corp]]"
email: john.smith@acme.com
telephone: "+1-555-0199"
updated: 2025-11-17T14:30:00
---

John Smith is a software engineer at Acme Corp specializing in distributed systems.
He can be reached at john.smith@acme.com or +1-555-0199.
```

**Requirements**:
- REQ-AGENT-040: Content analysis
- REQ-AGENT-041: Metadata extraction
- REQ-AGENT-042: User approval workflow
- REQ-SPEC-6.3: Template validation

---

### UC-402: Suggest Entity Links

**Category**: Content Enhancement
**Priority**: Medium
**Actors**: User, AIKB Agent

**Preconditions**:
- Note content mentions entities that exist in vault

**Trigger**: User requests link suggestions

**Main Flow**:

1. **User**: "Suggest links for this note"
2. **Agent**: Analyzes note content
3. **Agent**: Identifies potential entity references
4. **Agent**: Matches against existing vault entities
5. **Agent**: Proposes wiki link insertions

**Example**:

**Original Note**:
```markdown
---
created: 2025-11-15
---

Met with Sarah Johnson today to discuss the ACME redesign project.
She suggested we bring in John Smith as a technical consultant.
Need to schedule a kickoff meeting for next Tuesday at 9am.
```

**Agent Suggestions**:
"I found these potential links:
1. 'Sarah Johnson' → [[Sarah Johnson]] (Person)
2. 'ACME redesign project' → [[ACME Redesign Project]] (Project)
3. 'John Smith' → [[John Smith]] (Person)

I can also create:
4. A new Event for 'kickoff meeting next Tuesday at 9am'

Apply suggestions?"

**Requirements**:
- REQ-AGENT-043: Entity recognition in text
- REQ-AGENT-044: Fuzzy matching
- REQ-AGENT-045: Link insertion
- REQ-AGENT-046: New entity suggestion

---

### UC-403: Validate Metadata Compliance

**Category**: Content Enhancement
**Priority**: High
**Actors**: User, AIKB Agent

**Preconditions**:
- Vault contains knowledge objects
- JSON Schemas defined for templates

**Trigger**: User runs validation check

**Main Flow**:

1. **User**: "Validate my vault against AIKB standards"
2. **Agent**: Scans all `.md` files
3. **Agent**: Identifies template declaration in frontmatter
4. **Agent**: Validates against corresponding JSON Schema
5. **Agent**: Reports violations and warnings

**Example Report**:

```
Vault Validation Report

✓ 47 files validated successfully

⚠ 3 warnings:
  • Blake and Sydney's Wedding.md
    - Missing recommended field 'location'
    - Missing recommended field 'eventStatus'

  • Old Project.md
    - Using deprecated field 'state' (use 'projectStatus')

✗ 2 errors:
  • Incomplete Contact.md
    - Missing required field 'template'

  • Bad Event.md
    - Invalid date format in 'startDate': '2025/11/17' (must be YYYY-MM-DD)
    - Field 'priority' not defined in Event Template schema
```

**Requirements**:
- REQ-SPEC-6.3: Template validation
- REQ-SPEC-5.2: YAML frontmatter requirements
- REQ-AGENT-047: JSON Schema validation
- REQ-AGENT-048: Validation reporting

---

## 8. Requirements Summary

This section maps use cases to specification requirements and identifies new agent-level requirements.

### 8.1 Specification Requirements (from AIKB Spec v0.1)

| Requirement ID | Description | Related Use Cases |
|----------------|-------------|-------------------|
| REQ-SPEC-5.2 | YAML frontmatter format | All |
| REQ-SPEC-6.2.1 | Person Template schema | UC-001, UC-002, UC-003 |
| REQ-SPEC-6.2.2 | Event Template schema | UC-101, UC-102, UC-103 |
| REQ-SPEC-6.2.3 | Project Template schema | UC-201, UC-202, UC-203 |
| REQ-SPEC-6.3 | Template validation | UC-403 |
| REQ-SPEC-7.1 | Metadata naming conventions | All |
| REQ-SPEC-7.3 | ISO 8601 date/time formats | UC-101, UC-103, UC-403 |
| REQ-SPEC-8 | Linking and references | UC-203, UC-301, UC-402 |
| REQ-SPEC-8.3 | Metadata references | UC-102, UC-203 |

### 8.2 Agent Requirements (Implied by Use Cases)

These requirements should be considered for inclusion in future specification sections (e.g., §10 Agent Interaction Protocol):

#### Search and Retrieval

- **REQ-AGENT-001**: Agents MUST support entity search by name and fuzzy matching
- **REQ-AGENT-002**: Agents MUST support queries by metadata property values
- **REQ-AGENT-003**: Agents MUST aggregate and present multiple search results
- **REQ-AGENT-004**: Agents SHOULD support export to standard formats (vCard, iCal)

#### Date and Time Handling

- **REQ-AGENT-010**: Agents MUST support date range queries
- **REQ-AGENT-011**: Agents MUST expand recurring events based on recurrence metadata
- **REQ-AGENT-012**: Agents SHOULD handle timezone-aware timestamps
- **REQ-AGENT-013**: Agents MUST resolve entity references in metadata
- **REQ-AGENT-014**: Agents SHOULD generate formatted calendar views

#### Project Management

- **REQ-AGENT-020**: Agents MUST support project status queries
- **REQ-AGENT-021**: Agents SHOULD generate formatted project reports
- **REQ-AGENT-022**: Agents MUST aggregate data across multiple entities
- **REQ-AGENT-023**: Agents MUST support filtering by entity status
- **REQ-AGENT-024**: Agents SHOULD traverse entity relationship graphs
- **REQ-AGENT-025**: Agents SHOULD present hierarchical data structures

#### Knowledge Discovery

- **REQ-AGENT-030**: Agents MUST discover backlinks between entities
- **REQ-AGENT-031**: Agents MUST support cross-entity search
- **REQ-AGENT-032**: Agents SHOULD construct knowledge graphs
- **REQ-AGENT-033**: Agents SHOULD analyze multi-relation connections
- **REQ-AGENT-034**: Agents MAY export graph data in standard formats

#### Content Enhancement

- **REQ-AGENT-040**: Agents SHOULD analyze content for extractable metadata
- **REQ-AGENT-041**: Agents SHOULD extract structured data from unstructured text
- **REQ-AGENT-042**: Agents MUST require user approval before modifying content
- **REQ-AGENT-043**: Agents SHOULD recognize entity references in text
- **REQ-AGENT-044**: Agents SHOULD support fuzzy entity matching
- **REQ-AGENT-045**: Agents MAY insert wiki links into content
- **REQ-AGENT-046**: Agents MAY suggest creation of new entities
- **REQ-AGENT-047**: Agents MUST validate knowledge objects against JSON Schemas
- **REQ-AGENT-048**: Agents MUST provide clear validation error reports

---

## Appendix A: Reference Vault Examples

All example data in this document is drawn from or inspired by the [AIKB Reference Vault](https://github.com/codyburleson/aikb/tree/main/reference-vault).

---

## Appendix B: User Query Patterns

Common query patterns agents should recognize:

### Contact Queries
- "Give me [name]'s [property]"
- "Who do I know at [organization]?"
- "Find contacts in [location]"
- "Show me all [job title]s"

### Event Queries
- "What events [time period]?"
- "When is [event name]?"
- "Show me events related to [project]"
- "What's on my calendar [date/week]?"

### Project Queries
- "What's the status of [project]?"
- "Show me [status] projects"
- "What are my next actions?"
- "List projects by [priority/category]"

### Discovery Queries
- "Show me everything related to [entity]"
- "How are [entity1] and [entity2] connected?"
- "What have I written about [topic]?"

---

## Appendix C: Test Data Sets

For agent developers, recommended test data sets should include:

1. **Minimal Test Set**: 5 persons, 3 events, 2 projects
2. **Standard Test Set**: 25 persons, 15 events, 10 projects with interconnections
3. **Edge Cases**: Missing metadata, malformed dates, circular references, special characters

---

## Change Log

### Version 0.1 (2025-11-17)

- Initial draft use cases document
- Contact management use cases (UC-001 to UC-003)
- Event and calendar use cases (UC-101 to UC-103)
- Project management use cases (UC-201 to UC-203)
- Knowledge discovery use cases (UC-301 to UC-302)
- Content enhancement use cases (UC-401 to UC-403)
- Agent requirements derived from use cases

---

**License:** [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) Attribution-ShareAlike 4.0 International
