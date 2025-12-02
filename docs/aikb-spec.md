# Agent-Interoperable Knowledge Base (AIKB)

- **Version:** 0.4 (DRAFT)
- **Status:** Draft Specification
- **Date:** 2025-12-01
- **Editors:** AIKB Working Group

---

## Abstract

Agent-Interoperable Knowledge Base (AIKB) defines a set of rules and conventions for enabling AI agents to better understand, organize, and enhance knowledge stored in markdown-based personal knowledge management systems (PKMs).

## Status of This Document

This is a draft specification under active development for the [Capstone Project](https://www.kaggle.com/competitions/agents-intensive-capstone-project) of the [5-Day AI Agents Intensive Course with Google](https://www.kaggle.com/learn-guide/5-day-agents). It is subject to significant change and should not be considered stable for production use.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Conformance](#2-conformance)
3. [Core Concepts](#3-core-concepts)
4. [File System Structure](#4-file-system-structure)
5. [Document Format Standards](#5-document-format-standards)
6. [Templates and Schemas](#6-templates-and-schemas)
7. [Metadata Vocabulary](#7-metadata-vocabulary)
8. [Linking and References](#8-linking-and-references)
9. [Use Cases](#9-use-cases)
10. [Agent Interaction Protocol](#10-agent-interaction-protocol)
11. [Security and Privacy](#11-security-and-privacy)

---

## 1. Introduction

### 1.1 Purpose and Scope

Artificial Intelligence (AI) is reshaping the way we work, communicate, and interact with the world. As AI agents become more advanced and ubiquitous, they are increasingly being used to assist in personal knowledge management (PKM). However, current PKM tools and formats are not optimized for AI agent interaction, leading to suboptimal knowledge organization and retrieval. This specification addresses this gap by defining a set of rules and conventions for enabling AI agents to better understand, organize, and enhance knowledge stored in markdown-based personal knowledge management systems (PKMs).

This specification focuses on metadata schemas, file organization, and document templates that facilitate agent interoperability while maintaining human readability and editability.

### 1.2 Target Audience

This specification is intended for:

#### Power Users

For power users using markdown notebook tools like Obsidian, Logseq, or even just plain markdown files with simple text editors, this specification provides guidelines for structuring and organizing knowledge in a way that is both human-readable and machine-interpretable. Students, academics, writers, project managers, software developers, and anyone else who uses personal knowledge management tools can benefit from this specification because it provides proven principles, patterns, and practices for PKM. Whether you intend to use AI agents to enhance your PKM or simply want to level-up your PKM skills, this specification is for you. It answers the central question: "How can I structure my knowledge in a way that makes it easier to manage and retrieve the information in my digital notebook?"

Given the right formula of related information and technology, we envision that it could even guide you toward the achievement your personal and professional goals. "What is the greatest use of my time right now? Who can I contact to help with this? What mental model should I be using? How am I doing and what could I do better? Am I living in accordance with my core values? What are my next steps?"

#### Notebook Application Developers

Given a community of power users following a common set of Patterns for PKM, we can then provide features that support these patterns to improve the user experience of our applications. This specification formalizes a pattern language for PKM, providing a common vocabulary for notebook applications to support and communicate features and functions in a non-prescriptive way, honoring each user's unique needs, preferences, and desires for innovation and creativity.

#### Agent Developers

Agent developers can use this specification to build autonomous agents and tools that integrate digital services and interact with personal knowledge bases. These agents can leverage the user's knowledge base as a rich source of context to help provide personalized and contextually relevant assistance with user goals. They can interact with foundation models, online services, and the user's knowledge base to provide personalized and contextually relevant assistance with user goals. For agent developers, this specification attempts to answer the question: "How can I build an agent that can understand the user as a person, not just the context of a particular session, while respecting the user's privacy and ensuring the security of their data?"

### 1.3 Design Principles

1. **Human-First**: All formats remain human-readable and editable
2. **Locally-Sourced**: While knowledge resources may be shared or published, they are sourced (stored) locally, enabling offline access and portability
3. **Standards-Based**: Built upon existing standards (Markdown, RDF, YAML, [Schema.org](https://schema.org/), ISO 8601)
4. **Extensible**: Allow custom extensions while maintaining core interoperability
5. **Simple**: Minimize complexity; prefer convention over configuration
6. **Vendor Neutral**: Avoid lock-in to proprietary models, tools or platforms
7. **Privacy and Security**: The user should be in control of their data and have the ability to choose what data is shared with AI agents and services.

---

## 2. Conformance

### 2.1 Conformance Requirements

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

### 2.2 Conformance Classes

**Minimal Conformance**: A knowledge base MUST:

- Use UTF-8 encoded `.md` files
- Include valid YAML frontmatter with required metadata
- Implement at least one core entity type template

**Standard Conformance**: A knowledge base MUST additionally:

- Implement all __core__ entity type templates
- Use standard linking conventions

**Extended Conformance**: A knowledge base MAY additionally:

- Implement custom document templates
- Add extended metadata vocabularies
- Integrate with external systems

---

## 3. Core Concepts

- Abstract Syntax Tree (AST): A tree representation of the structure of a document, used to represent the structure of a knowledge document.

### 3.1 Knowledge Vault

A **Knowledge Vault** is a directory containing AIKB-compliant markdown documents, structured and organized according to this specification. A vault:

- MUST reside in a single root directory
- MUST contain subdirectories for organization
- SHOULD contain a `.aikb` metadata directory
- MAY be version-controlled (e.g., Git repository), synced to cloud storage, shared with others, etc.

_Synonyms: Knowledge Base, Knowledge Library, Knowledge Repository, Vault_

### 3.2 Knowledge Document (Entity / Instance)

A **Knowledge Document** is a single markdown file representing an entity, note, or artifact. Each knowledge document:

- MUST have a `.md` file extension
- MUST contain YAML frontmatter
- SHOULD declare a document type
- MAY reference other knowledge documents

Synonyms: Instance, Knowledge Object, Note

### 3.3 Templates (Entity Type Definitions)

A **Template** is a markdown file that represents an entity type (a class of real-world things having common properties). Templates are used to create instances of the entity type. A Person Template, for example, is used to create John Doe.md, a knowledge document representing the person, John Doe. A Template MUST, at minimum, define the properties that are necessary and sufficient to logically classify a thing as a member of the type, and it MAY define additional properties. Properties need not be required to be populated by users, but SHOULD be useful to agents, and populated by agents to improve usefulness to themselves and the user.

_Synonyms: Type, Class_

Each template:

- MUST have a `.md` file extension
- MUST contain YAML frontmatter
- MUST declare a document type as a link to itself, which creates a self-referential back-link in all instances created from the template
- MUST define the minimum required metadata properties that are necessary and sufficient to represent the entity type in a knowledge document
- MUST use empty values for metadata properties (not placeholders like `{date}` or `{title}`)
- SHOULD have an associated JSON Schema available to agents for validation and proper population of instances
- MAY define additional metadata properties that are optional
- MAY include boilerplate content structure

**Important**: Template metadata fields should contain empty values (e.g., `created:` or `name:`) rather than placeholder strings. This ensures YAML 1.2 compliance and compatibility with tools like Obsidian. Agents use the corresponding JSON Schema to determine field types and populate values when creating instances.

#### Core Entity Types

The following entity types are defined as core entity types and available in the Reference Vault. Where the entity type is defined in Schema.org, the properties available to the entity type should be assumed to be available in the AIKB specification. A later section will define those exceptions, and which properties are considered to be necessary and sufficient for the type.

##### CreativeWork:

The most generic kind of creative work, including books, movies, photographs, software programs, etc.

- More specific Types of CreativeWork MAY be defined as templates
- More specific Types of CreativeWork MUST be tagged with `type/CreativeWork/<SpecificTypeName>` in templates
- More specific Types of CreativeWork MAY be tagged with `type/CreativeWork/<SpecificTypeName>` in instances

For more specific Types of CreativeWork, see [Schema.org](https://schema.org/CreativeWork).

##### DailyNote:

A document created on a given day for recording general notes and observations about the day or throughout the day (e.g. a journal entry, a working scratchpad for meeting notes, to-do lists, etc.).

##### Event:

An event happening at a certain time.

Instances of an Event could also specify a location and used in a calendar to remind the user where and when the need to attend a concert, lecture, or festival, for example. But events may also just indicate important moments in time－useful, for example, to render a historical timeline.

##### Organization:

An organization (e.g. a company, institution, group, or team)

Instances of an Organization can represent any kind of group that is organized for some purpose. It can link to its members (Person instances), and projects (Project instances), for example.

##### Person:

A person (alive, dead, undead, or fictional)

Instances of a Person can be useful for personal notes about a person, for recording contact information, and relating persons to other entities in the knowledge base.

##### Place:

Entities that have a somewhat fixed, physical location (e.g. a drawer, a bookshelf, a room, a building, a city, a country, a planet, a star, a galaxy, etc.)

Instances of a Place can be useful, for example, for relating notes and back-linking to all things related to the place, such as events, people, organizations, and other places.

##### Project:

An enterprise (potentially individual but typically collaborative), planned to achieve a particular aim.

Instances of a Project can be useful for conveying the start and end dates, objectives, and associated action plans for a given project, for example.

##### Task:

An action item or to-do.

Instances of a Task can be useful for a to-do list or the action items in a project plan, for example. Tasks as a type are different from the traditional markdown task (e.g. `- [ ] To do item 1, - [x] To do item 2`, etc.). We recommend using markdown tasks only for sub-tasks of a Task instance because they are not as useful as documents for tracking progress, setting deadlines, adding notes, relationships, etc.

### 3.4 Properties

**Properties** are metadata fields that define the structure and required metadata for document types. Properties:

- MUST be defined in a frontmatter YAML block when used in a template
- SHOULD be defined in a frontmatter YAML block when used in a knowledge document

---

## 4. File System Structure

### 4.1 Directory Organization

A AIKB vault MAY implement the Reference Vault directory structure as a starting point for organization:

```
/my-vault/
 .aikb/                  # AIKB metadata (RECOMMENDED)
    config.yaml          # Vault configuration
    schemas/             # Custom schema definitions
 1 Projects/             # (OPTIONAL)
 2 Areas/                # (OPTIONAL)
 3 Resources/            # (RECOMMENDED)
    Creative Works/      # Instances of CreativeWork
    Daily Notes/         # Instances of DailyNote
    Events/              # Instances of Event
    Organizations/       # Instances of Organization
    Persons/             # Instances of Person
    Places/              # Instances of Place
    Projects/            # Instances of Project
    Tasks/               # Instances of Task
    Templates/           # Entity type templates (RECOMMENDED)
 4 Archive/              # (OPTIONAL)
```

### 4.2 File Naming Conventions

- File names SHOULD be human-readable and descriptive
- File names MAY include spaces
- File names SHOULD match the common name for the primary entity (e.g., "John Doe" for a person)
- Templates SHOULD be named `[EntityType] Template.md`

### 4.3 Reserved Names

The following directory and file names are reserved:

- `.aikb/` - AIKB metadata directory
- `Templates/` - Entity type templates

---

## 5. Document Format Standards

### 5.1 Markdown Syntax

Knowledge Documents MUST use CommonMark-compliant markdown with the following clarifications:

- UTF-8 encoding REQUIRED
- Line endings: LF (`\n`) RECOMMENDED, CRLF (`\r\n`) ALLOWED
- Frontmatter MUST appear at the beginning of the file

### 5.2 YAML Frontmatter

All knowledge objects MUST include YAML frontmatter delimited by `---`:

```yaml
---
# Metadata here
---

Document content begins here.
```

#### 5.2.1 Frontmatter Requirements

- MUST use valid YAML 1.2 syntax ([YAML 1.2 Specification](https://yaml.org/spec/1.2/))
- MUST be enclosed by `---` delimiters
- MUST appear before any markdown content
- MUST use empty values for unpopulated fields (not placeholder strings)
- SHOULD include entity type indicator

**Note**: Empty values in YAML can be represented as `key:` (with no value after the colon) or `key: ""` (empty string). Do not use placeholder strings like `{date}` or `{title}` as these are not valid YAML values and break compatibility with tools that parse frontmatter.

---

## 6. Templates and Schemas

### 6.1 Overview

Templates are markdown documents with pre-populated frontmatter and content that are copied to create Instances of a given Entity Type. Templates typically contain a minimal set of frontmatter properties acting as placeholders; some may be pre-populated with values and others may be empty and intended to be populated by the user when the Instance is created.

Schemas are JSON documents providing a formal descriptions of the structure of Entity Types. To improve interoperability with agents and tools, a JSON schema file SHOULD exist that corresponds to an Entity Type Template. That is to say, for each Template, a corresponding JSON Schema SHOULD exist. While a Template may only contain minimal properties, a Schema defines a comprehensive set of properties that may be used in Templates and Instances of the given type.

An Entity Type can be thought of as the combination of a Template and its corresponding Schema.

### 6.2 Core Entity Types

The following core Entity Types exist in the Reference Vault and available for use in AIKB-compliant knowledge vaults.

#### CreativeWork

Books, articles, media, software

- Reference Template: [3 Resources/Templates/CreativeWork.md](https://raw.githubusercontent.com/codyburleson/aikb/refs/heads/main/reference-vault/3%20Resources/Templates/CreativeWork.md)
- Schema: [.aikb/CreativeWork.json](https://raw.githubusercontent.com/codyburleson/aikb/refs/heads/main/reference-vault/.aikb/schemas/CreativeWork.json)
- Example Use Cases: Library management, inventory tracking, study notes, technical notes, bookmarks

#### DailyNote

Notes taken on a specific date

- Reference Template: [3 Resources/Templates/DailyNote.md](https://raw.githubusercontent.com/codyburleson/aikb/refs/heads/main/reference-vault/3%20Resources/Templates/DailyNote.md)
- Schema: [.aikb/DailyNote.json](https://raw.githubusercontent.com/codyburleson/aikb/refs/heads/main/reference-vault/.aikb/schemas/DailyNote.json)
- Example Use Cases: Daily note taking, journaling, meeting minutes

#### Event

Represents an event happening at a certain time and location.

- Reference Template: [3 Resources/Templates/Event.md](https://raw.githubusercontent.com/codyburleson/aikb/refs/heads/main/reference-vault/3%20Resources/Templates/Event.md)
- Schema: [.aikb/Event.json](https://raw.githubusercontent.com/codyburleson/aikb/refs/heads/main/reference-vault/.aikb/schemas/Event.json)
- Example Use Cases: Calendar management, meeting tracking, historical timeline construction

#### Organization

Companies, institutions, groups

- Reference Template: [3 Resources/Templates/Organization.md](https://raw.githubusercontent.com/codyburleson/aikb/refs/heads/main/reference-vault/3%20Resources/Templates/Organization.md)
- Schema: [.aikb/Organization.json](https://raw.githubusercontent.com/codyburleson/aikb/refs/heads/main/reference-vault/.aikb/schemas/Organization.json)
- Example Use Cases: Contact management, relating affiliations, aggregating lists, graphs

#### Person

Represents an individual person (alive, dead, undead, or fictional).

- Reference Template: [3 Resources/Templates/Person.md](https://raw.githubusercontent.com/codyburleson/aikb/refs/heads/main/reference-vault/3%20Resources/Templates/Person.md)
- Schema: [.aikb/Person.json](https://raw.githubusercontent.com/codyburleson/aikb/refs/heads/main/reference-vault/.aikb/schemas/Person.json)
- Example Use Cases: Contact management, relationship tracking, biographical information

#### Place

Locations with physical presence

- Reference Template: [3 Resources/Templates/Place.md](https://raw.githubusercontent.com/codyburleson/aikb/refs/heads/main/reference-vault/3%20Resources/Templates/Place.md)
- Schema: [.aikb/Place.json](https://raw.githubusercontent.com/codyburleson/aikb/refs/heads/main/reference-vault/.aikb/schemas/Place.json)
- Example Use Cases: Travel planning/logging, inventory management, historical research

#### Project

Represents an enterprise or initiative planned to achieve a particular aim.

- Reference Template: [3 Resources/Templates/Project.md](https://raw.githubusercontent.com/codyburleson/aikb/refs/heads/main/reference-vault/3%20Resources/Templates/Project.md)
- Schema: [.aikb/Project.json](https://raw.githubusercontent.com/codyburleson/aikb/refs/heads/main/reference-vault/.aikb/schemas/Project.json)
- Example Use Cases: Project management, progress tracking, resource planning

#### Task

Action items and to-dos

- Reference Template: [3 Resources/Templates/Task.md](https://raw.githubusercontent.com/codyburleson/aikb/refs/heads/main/reference-vault/3%20Resources/Templates/Task.md)
- Schema: [.aikb/Task.json](https://raw.githubusercontent.com/codyburleson/aikb/refs/heads/main/reference-vault/.aikb/schemas/Task.json)
- Example Use Cases: Project management, to-do lists, productivity systems, issue tracking

### 6.3 Template Validation

#### 6.3.1 JSON Schema Files

Each core entity type template SHOULD have a corresponding JSON Schema file located in `.aikb/schemas/[EntityType].json`. JSON Schemas:

- MUST follow JSON Schema Draft 07 or later specification
- SHOULD define all properties available for the entity type
- MUST specify which properties are required
- SHOULD include property descriptions and data type formats
- MAY define enumerations for fields with fixed value sets

#### 6.3.2 Validation Requirements

Agent and tool implementations SHOULD validate document Instances against their declared templates using JSON Schema validation. When creating instances from templates:

1. Read the template file to understand structure
2. Read the corresponding JSON Schema to understand field types and validation rules
3. Populate empty fields with appropriate values (e.g., current timestamp for `created`, user-provided input for `name`)
4. Validate the populated instance against the JSON Schema before writing

**Example**: When creating a Project instance, the agent reads `Project.md` template, reads `Project.json` schema, populates the `name` field with user input, populates `created` with the current ISO 8601 timestamp, and validates the complete frontmatter against the schema.

### 6.4 Custom Templates

Users MAY define custom entity types by:

1. Creating a Template file for a given Entity Type
2. Defining a JSON Schema for the Entity Type in the Vault root under `/.aikb/schemas/`

---

## 7. Metadata Vocabulary

### 7.1 Naming Conventions

All metadata property names MUST:

- Use camelCase formatting (e.g., `givenName`, `startDate`)
- Avoid spaces or special characters
- Be descriptive and unambiguous
- Prefer established vocabularies (eg. [Schema.org](https://schema.org/), [Dublin Core™ Metadata Element Set](https://www.dublincore.org/specifications/dublin-core/dces/))

### 7.2 Common Metadata Properties

The following properties are applicable across Entity Types and SHOULD be included in frontmatter of all templates in the order of appearance:

| Property | Type | Description | Format |
|----------|------|-------------|--------|
| `name` | string | The name of the item | string |
| `type` | string | Template reference | `[[Template Name]]` |
| `tags` | array | Classification tags | Array of strings |
| `created` | string | Creation timestamp | ISO 8601 date-time |
| `updated` | string | Modification timestamp | ISO 8601 date-time |

### 7.3 Date and Time Formats

All dates and times MUST use ISO 8601 format:

- **Date**: `YYYY-MM-DD` (e.g., `2025-11-17`)
- **DateTime**: `YYYY-MM-DDTHH:MM:SS` or with timezone (e.g., `2025-11-17T14:30:00Z`)
- **Time**: `HH:MM` in 24-hour format (e.g., `14:30`)

---

## 8. Linking and References

### 8.1 Internal Links

Knowledge objects MUST reference each other using either Obsidian-style wiki links or markdown-style links:

```markdown
[[Target Document Name]]
[[Target Document Name|Display Text]]
```

```markdown
[Target Document Name](Target Document Name)
[Display Text](Target Document Name)
```

### 8.2 Backlinks

Agents SHOULD maintain bidirectional awareness of relationships between knowledge objects.

### 8.3 Metadata References

Template and entity references in frontmatter use the same wiki link syntax:

```yaml
type: "[[Person Template]]"
worksFor: "[[Tesla]]"
attendees:
  - "[[John Doe]]"
  - "[[Jane Smith]]"
```

---

## 9. Use Cases (Informative)

This section provides high-level use cases that demonstrate the intended application of AIKB-compliant knowledge bases. Detailed scenarios, example interactions, and requirements traceability are documented in the companion [AIKB Use Cases and Requirements](./aikb-use-cases.md) document.

### 9.1 Contact Information Retrieval

Agents retrieve contact details for individuals stored in the knowledge base.

**Example Query**: "Give me John Smith's email address"

**Agent Actions**:
1. Search vault for Person entities matching "John Smith"
2. Parse YAML frontmatter to extract `email` property
3. Return contact information to user

**Related Templates**: Person Template (§6.2.1)

### 9.2 Calendar and Event Management

Agents query scheduled events, create calendar views, and manage recurring appointments.

**Example Queries**:
- "What events do I have this week?"
- "Show me all events related to the ACME project"
- "When is my next meeting with Sarah?"

**Agent Actions**:
1. Query Event entities by date range or filters
2. Parse temporal metadata (`startDate`, `startTime`, recurrence patterns)
3. Resolve entity references (attendees, related projects)
4. Present aggregated calendar view

**Related Templates**: Event Template (§6.2.2)

### 9.3 Project Status and Progress Tracking

Agents aggregate project information, track progress, and identify next actions across multiple initiatives.

**Example Queries**:
- "What's the status of the AIKB project?"
- "Show me all high-priority projects"
- "What are my next actions across all active projects?"

**Agent Actions**:
1. Query Project entities by status, priority, or other filters
2. Extract progress metrics, milestones, and action items
3. Resolve relationships (sub-projects, team members, stakeholders)
4. Generate status reports or dashboards

**Related Templates**: Project Template (§6.2.3)

### 9.4 Knowledge Graph Construction

Agents analyze entity relationships to build queryable knowledge graphs.

**Example Use**:
- Visualize connections between people, projects, and events
- Discover implicit relationships through backlinks
- Identify knowledge clusters and themes

**Agent Actions**:
1. Traverse all knowledge objects in vault
2. Parse entity references in frontmatter and content
3. Build graph with entities as nodes and references as edges
4. Enable graph-based queries and visualizations

**Related Sections**: Linking and References (§8)

### 9.5 Automated Metadata Enhancement

Agents enrich existing knowledge objects with additional metadata based on content analysis.

**Example Actions**:
- Extract structured information from unstructured notes
- Auto-populate missing metadata fields
- Suggest entity relationships and tags
- Generate summaries and descriptions

**Agent Actions**:
1. Read knowledge object content
2. Apply NLP/LLM analysis to extract entities and information
3. Validate against entity template schemas
4. Propose metadata updates for user approval

**Related Sections**: Template Validation (§6.3)

### 9.6 Cross-Vault Collaboration

Multiple users with separate vaults share and synchronize knowledge objects through agent mediation.

**Example Scenarios**:
- Team members share project updates
- Collaborative event planning
- Distributed contact management

**Agent Considerations**:
- Conflict resolution for concurrent edits
- Privacy and access control
- Merge strategies for divergent versions

**Related Sections**: Security and Privacy (§11)

---

**Note**: These use cases are informative and non-normative. Implementations MAY support additional use cases beyond those listed here. For detailed scenarios with example data and agent interactions, see the [AIKB Use Cases and Requirements](./aikb-use-cases.md) document.

---

## 10. Agent Interaction Protocol

(To be developed)

Topics to cover:
- Vault discovery and validation
- Read/write operations
- Conflict resolution
- Change notifications
- Query interfaces

---

## 11. Security and Privacy

(To be developed)

Topics to cover:
- Access control considerations
- Personal data handling
- Agent authentication
- Local-first principles
- Data portability

---

## 12. Core Reference Agents

(To be developed)

Topics to cover: TBD

---

## Appendix A: Complete JSON Schemas

The core JSON schemas are maintained in: [AIKB Reference Vault / .aikb/schemas](https://github.com/codyburleson/aikb/tree/main/reference-vault/.aikb/schemas).

---

## Appendix B: Core Document Templates

The core document templates are maintained in: [AIKB Reference Vault / 3 Resources/Templates](https://github.com/codyburleson/aikb/tree/main/reference-vault/3%20Resources/Templates).

---

## Appendix C: Change Log

### Version 0.1 (2025-11-22)

- Initial draft specification

---

## References

- [CommonMark Specification](https://spec.commonmark.org/)
- [YAML 1.2 Specification](https://yaml.org/spec/1.2/)
- [vCard Format (RFC 6350)](https://datatracker.ietf.org/doc/html/rfc6350)
- [Schema.org](https://schema.org/)
- [ISO 8601 Date and Time Format](https://www.iso.org/iso-8601-date-and-time-format.html)
- [JSON Schema](https://json-schema.org/)

---

**License:** [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) Attribution-ShareAlike 4.0 International
