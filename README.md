# Inbox Action Agent
### AI-Powered Email Intelligence, Task Extraction & Response Management System


 An intelligent email management system that uses Large Language Models (LLMs), rule-based classification, persistent memory and automated information extraction to transform a traditional inbox into an actionable workspace.

Inbox Action Agent analyzes incoming emails, identifies their importance, extracts tasks and deadlines, maintains conversation context, and generates context-aware response drafts. It keeps the user in control by requiring explicit approval before any email response can be sent.

---

## 1. Project Overview

Managing an email inbox involves more than reading messages. Important information is often buried in long conversations, deadlines are missed, follow-ups are forgotten, and drafting appropriate responses takes time.

**Inbox Action Agent** addresses these challenges through an AI-driven email intelligence pipeline.

The system is designed to:

- Retrieve and synchronize emails through the Gmail API.
- Understand email content using AI and rule-based processing.
- Classify emails into meaningful categories.
- Identify urgency and assign priority levels.
- Generate concise email summaries.
- Extract actionable tasks, deadlines and follow-up requirements.
- Maintain persistent memory using SQLite.
- Determine whether an email requires a response.
- Identify appropriate response types, including thank-you messages, acknowledgements, confirmations and follow-ups.
- Generate contextual response drafts.
- Maintain human approval as a mandatory safety requirement.

### Core Philosophy

**AI handles email intelligence. Persistent memory maintains context. Humans retain control over communication.**

---

## 2. Key Features

| Feature | Description |
|---|---|
| Gmail Integration | Retrieves emails through Gmail API using OAuth 2.0 |
| Email Classification | Categorizes emails using rule-based classification |
| Priority Detection | Identifies critical, high, medium and low-priority messages |
| Email Analysis | Understands email content and recommends actions |
| Email Summarization | Generates concise summaries |
| Task Extraction | Identifies actionable items and deadlines |
| Persistent Memory | Stores email history, tasks, reminders and follow-ups in SQLite |
| Response Intelligence | Determines whether a response is required |
| Response Type Detection | Identifies thank-you, acknowledge, confirm, answer and other response types |
| AI Response Drafting | Generates contextual email response drafts |
| Draft Management | Supports retrieving and editing generated drafts |
| Human Approval | Requires explicit approval before communication is sent |

---

# 3. System Architecture

The Inbox Action Agent follows a modular, layered architecture. Each layer has a specific responsibility, allowing individual components to be developed, tested and maintained independently.

## 3.1 High-Level Architecture

The system is organized into seven logical levels.

```text
┌──────────────────────────────────────────────────────┐
│                 LEVEL 1: INPUT LAYER                 │
│                                                      │
│             Gmail API / Incoming Emails              │
│                 OAuth 2.0 Authentication             │
└──────────────────────────┬───────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────┐
│              LEVEL 2: INTEGRATION LAYER              │
│                                                      │
│         Gmail Service  |  Gmail Sync Service         │
│          Email Retrieval | Duplicate Detection       │
└──────────────────────────┬───────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────┐
│             LEVEL 3: INTELLIGENCE LAYER               │
│                                                      │
│  ┌──────────────┐  ┌──────────────┐                   │
│  │ Classifier   │  │ Inbox Agent  │                   │
│  └──────────────┘  └──────────────┘                   │
│  ┌──────────────┐  ┌──────────────┐                   │
│  │ Summarizer   │  │ Response     │                   │
│  │              │  │ Intelligence │                   │
│  └──────────────┘  └──────────────┘                   │
│                                                      │
│             Groq LLM / Rule-Based Logic              │
└──────────────────────────┬───────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────┐
│             LEVEL 4: MEMORY & DATA LAYER              │
│                                                      │
│                  SQLite Database                     │
│                                                      │
│    Emails | Tasks | Reminders | Follow-ups           │
│          Response Drafts | Action History            │
└──────────────────────────┬───────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────┐
│               LEVEL 5: API LAYER                      │
│                                                      │
│          FastAPI REST API Endpoints                  │
│                                                      │
│       Email API | Memory API | Response API          │
└──────────────────────────┬───────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────┐
│           LEVEL 6: HUMAN CONTROL LAYER               │
│                                                      │
│     Review → Edit → Approve / Reject                 │
│                                                      │
│            Explicit User Authorization               │
└──────────────────────────┬───────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────┐
│              LEVEL 7: OUTPUT LAYER                   │
│                                                      │
│       Email Insights | Tasks | Drafts | History      │
│                                                      │
│          Approved Communication Workflow            │
└──────────────────────────────────────────────────────┘
```

### Explanation of Architecture Levels

**Level 1: Input Layer**

Responsible for receiving email data from the Gmail account.

Components:
- Gmail account.
- Gmail API.
- OAuth 2.0 authentication.
- Incoming email messages and metadata.

Purpose: Provide secure access to the user's email data.

**Level 2: Integration Layer**

Responsible for communicating with Gmail and preparing email information for processing.

Components:
- `gmail_service.py`
- `gmail_sync_service.py`
- `inbox_service.py`

Responsibilities:
- Authenticate Gmail API requests.
- Retrieve email messages.
- Extract sender, recipient, subject, body and timestamps.
- Synchronize messages with the local application.
- Detect duplicate emails using Gmail message IDs.

**Level 3: Intelligence Layer**

This is the core AI processing layer.

Components:

1. **Classifier Agent**
   - Categorizes incoming emails.
   - Identifies security alerts, important messages, newsletters, promotions and account notifications.
   - Assigns priority levels.

2. **Inbox Agent**
   - Analyzes email information.
   - Recommends suitable actions.
   - Applies safety checks to sensitive operations.

3. **Summarizer**
   - Produces concise summaries of email content.
   - Helps users understand lengthy messages quickly.

4. **Response Intelligence Agent**
   - Determines whether a reply is required.
   - Identifies the appropriate response type.
   - Generates contextual response drafts.
   - Avoids unsupported facts and commitments.

5. **LLM Service**
   - Connects the application to the Groq inference API.
   - Processes prompts and returns model-generated responses.

**Level 4: Memory and Data Layer**

Responsible for persistent storage and retrieval of application information.

Technology: SQLite and SQLAlchemy.

Main data entities:

| Entity | Purpose |
|---|---|
| Emails | Stores imported email information |
| Tasks | Stores extracted actionable items |
| Reminders | Stores reminder information |
| Follow-ups | Stores pending follow-up records |
| Response Drafts | Stores generated response drafts and approval status |
| Agent Actions | Maintains a record of agent operations |

The memory layer allows the application to retain structured information across sessions rather than depending entirely on temporary conversational context.

**Level 5: API Layer**

Provides communication between application services and external clients.

Technology: FastAPI.

Main API modules:
- Email API
- Memory API
- Response API

Responsibilities:
- Accept incoming requests.
- Validate request data.
- Invoke application services.
- Return structured JSON responses.
- Handle errors and API responses.

**Level 6: Human Control Layer**

This layer establishes user authority over email communication.

Workflow:

1. AI generates a response draft.
2. The draft is stored with `PENDING_APPROVAL` status.
3. The user reviews the content.
4. The user can edit the draft.
5. The user can approve or reject it.
6. The action is recorded.

Approval currently updates the draft status; it does not send the email. Gmail sending functionality is not yet implemented.

**Level 7: Output Layer**

Provides the results of email processing.

Expected outputs:
- Classified emails.
- Priority information.
- Email summaries.
- Extracted tasks and deadlines.
- Follow-up records.
- Response drafts.
- Action history.

---

## 3.2 Detailed Email Processing Workflow

```text
             START
               │
               ▼
       Connect Gmail Account
               │
               ▼
        Authenticate via OAuth
               │
               ▼
        Retrieve Email Messages
               │
               ▼
       Synchronize with SQLite
               │
               ▼
        Check Duplicate Emails
               │
               ▼
        Analyze Email Content
               │
               ▼
       Classify Email Category
               │
               ▼
        Determine Priority
               │
               ▼
        Generate Email Summary
               │
               ▼
       Extract Tasks and Dates
               │
               ▼
       Store Structured Memory
               │
               ▼
       Is Response Required?
           /         \
         No           Yes
         │             │
         ▼             ▼
    Record Action   Identify Response Type
         │             │
         │             ▼
         │       Generate AI Draft
         │             │
         │             ▼
         │       Store Pending Draft
         │             │
         │             ▼
         │       User Reviews Draft
         │             │
         │          /     \
         │       Reject   Approve
         │          │       │
         │          ▼       ▼
         │       Record   Record Approval
         │       Rejection   │
         │                   ▼
         └─────────────► Update Action History
                             │
                             ▼
                            END
```

---

# 4. Response Intelligence System

One of the major components of Inbox Action Agent is its response intelligence engine.

Instead of generating a generic reply for every incoming email, the agent first determines whether a response is actually necessary.

### Supported Response Categories

| Response Type | Purpose |
|---|---|
| `NO_REPLY` | No response is necessary |
| `THANK` | Express gratitude |
| `ACKNOWLEDGE` | Acknowledge receipt of information |
| `ANSWER` | Answer a question |
| `CONFIRM` | Confirm an arrangement or request |
| `ACCEPT` | Accept an invitation or proposal |
| `DECLINE` | Politely decline a request |
| `REQUEST_INFORMATION` | Ask for additional information |
| `FOLLOW_UP` | Follow up on an earlier communication |
| `SCHEDULE` | Coordinate a meeting or appointment |
| `CUSTOM` | Handle other response situations |

### Response Generation Workflow

```text
Incoming Email
      │
      ▼
Analyze Context
      │
      ▼
Determine Response Requirement
      │
      ▼
Identify Response Category
      │
      ▼
Generate Structured AI Output
      │
      ▼
Validate Response
      │
      ▼
Save Draft in SQLite
      │
      ▼
User Review and Editing
      │
      ▼
Approve or Reject
```

The response engine is designed to:
- Avoid unnecessary replies.
- Distinguish gratitude from simple acknowledgement.
- Avoid inventing facts, dates or commitments.
- Preserve the context of the original email.
- Require human review before any communication is sent.

---

# 5. Persistent Memory Architecture

Traditional email assistants often focus on processing individual messages. Inbox Action Agent is designed to maintain structured information beyond a single interaction.

### Memory Components

**1. Email Memory**

Stores:
- Sender and recipient.
- Subject and body.
- Gmail message ID.
- Thread ID.
- Received timestamp.
- Read status and labels.

**2. Task Memory**

Stores:
- Task title.
- Description.
- Priority.
- Due date.
- Task status.
- Source email reference.

**3. Reminder Memory**

Stores:
- Reminder title.
- Associated task.
- Reminder timestamp.
- Reminder status.

**4. Follow-up Memory**

Stores:
- Related email.
- Follow-up subject.
- Description.
- Follow-up date.
- Follow-up status.

**5. Response Memory**

Stores:
- Original email reference.
- Response type.
- Generated draft.
- Confidence score.
- Approval status.

**6. Action History**

Records operations performed by the agent, including response draft creation and approval or rejection actions.

### Memory Design

```text
                 SQLite Database
                        │
       ┌────────────────┼────────────────┐
       │                │                │
       ▼                ▼                ▼
    Emails            Tasks          Reminders
       │                │                │
       ▼                ▼                │
 Follow-ups        Response Drafts       │
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
                 Agent Actions
```

This structured storage provides the foundation for future memory retrieval features, such as:
- What tasks are pending?
- Which emails require follow-up?
- What did a particular sender communicate?
- Which response drafts are awaiting approval?
- What actions has the agent performed?

---

# 6. Technology Stack

| Technology | Application |
|---|---|
| Python 3.11 | Core backend development |
| FastAPI | REST API framework |
| Groq API | Large Language Model inference |
| OpenAI GPT-OSS 120B | Configured language model |
| Gmail API | Email integration |
| OAuth 2.0 | Gmail authentication |
| SQLite | Persistent application storage |
| SQLAlchemy | ORM and database operations |
| Pydantic | Request and response validation |
| Uvicorn | ASGI application server |
| Python-dotenv | Environment variable management |
| Pytest / Python unittest | Testing support |

---

# 7. Project Directory Structure

```text
inbox-action-agent/
│
├── .gitignore
│
├── backend/
│   │
│   ├── app/
│   │   ├── agents/
│   │   │   ├── classifier.py
│   │   │   ├── inbox_agent.py
│   │   │   ├── response_agent.py
│   │   │   └── summarizer.py
│   │   │
│   │   ├── api/
│   │   │   ├── emails.py
│   │   │   ├── memory.py
│   │   │   └── responses.py
│   │   │
│   │   ├── core/
│   │   │
│   │   ├── models/
│   │   │   ├── db_models.py
│   │   │   └── email.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── email.py
│   │   │   ├── memory.py
│   │   │   └── response.py
│   │   │
│   │   ├── services/
│   │   │   ├── gmail_service.py
│   │   │   ├── gmail_sync_service.py
│   │   │   ├── inbox_service.py
│   │   │   ├── llm_service.py
│   │   │   └── memory_service.py
│   │   │
│   │   ├── tools/
│   │   │   └── email_actions.py
│   │   │
│   │   ├── utils/
│   │   │
│   │   ├── database.py
│   │   ├── init_db.py
│   │   ├── migrate_db.py
│   │   └── main.py
│   │
│   ├── tests/
│   │   └── test_memory.py
│   │
│   ├── requirements.txt
│   ├── test_gmail.py
│   ├── test_groq.py
│   ├── test_gemini.py
│   └── test_response_agent.py
│
└── README.md
```

---

# 8. Installation and Setup

### Prerequisites

- Python 3.11 or later.
- Git.
- Gmail account for testing.
- Google Cloud project with Gmail API enabled.
- Google OAuth Desktop application credentials.
- Groq API key.

### Step 1: Clone the Repository

```bash
git clone https://github.com/adityaghodke275/inbox-action-agent.git
cd inbox-action-agent
```

### Step 2: Create a Virtual Environment

```bash
cd backend

python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
python -m pip install --upgrade pip

pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file inside the backend directory.

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

Never commit this file or share your actual API key.

### Step 5: Configure Gmail API

1. Open Google Cloud Console.
2. Create or select a Google Cloud project.
3. Enable the Gmail API.
4. Configure the OAuth consent screen.
5. Create OAuth 2.0 Desktop credentials.
6. Download the credentials JSON file.
7. Place it inside the backend directory as:

```text
backend/credentials.json
```

Use a dedicated test Gmail account rather than your primary personal account.

The current integration uses the Gmail read-only scope. Gmail sending permissions are not yet configured.

### Step 6: Start the Backend

From the `backend` directory:

```bash
python -m uvicorn app.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

### Step 7: Open API Documentation

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Alternative ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

---

# 9. API Documentation

The backend exposes REST API endpoints organized into three main groups.

### Email API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/emails/` | Retrieve stored emails |
| POST | `/emails/sync-gmail` | Synchronize emails from Gmail |

### Memory API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/tasks` | Retrieve stored tasks |
| GET | `/reminders` | Retrieve reminders |
| GET | `/follow-ups` | Retrieve follow-up records |
| GET | `/history` | Retrieve agent action history |

### Response API

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/responses/emails/{email_id}/generate` | Generate a response draft |
| GET | `/responses/drafts` | Retrieve response drafts |
| GET | `/responses/drafts/{draft_id}` | Retrieve a specific draft |
| PATCH | `/responses/drafts/{draft_id}` | Edit a pending draft |
| POST | `/responses/drafts/{draft_id}/approve` | Approve a draft |
| POST | `/responses/drafts/{draft_id}/reject` | Reject a draft |

For request parameters, response schemas and examples, refer to the interactive Swagger documentation.

---

# 10. Safety and Security

Email communication is sensitive. The system is designed with human authorization and credential protection in mind.

### Human-in-the-Loop Approval

- AI-generated responses are not automatically sent.
- Drafts are stored with a pending approval status.
- Users can edit drafts before approval.
- Approval and rejection are recorded.
- Approval currently changes the database status only. It does not trigger Gmail sending.

### Credential Protection

Sensitive files are excluded from Git:

- `.env`
- `credentials.json`
- `token.json`
- Local SQLite database files
- Python virtual environments

API keys and OAuth credentials should always be stored locally or in a secure secrets manager.

### Data Protection

Use a dedicated Gmail test account and review the permissions granted through OAuth. Do not expose personal email content or authentication tokens in public repositories.

---

# 11. Current Implementation Status

| Component | Status |
|---|---|
| FastAPI backend | Implemented |
| Gmail OAuth authentication | Implemented |
| Gmail email retrieval | Implemented |
| Gmail synchronization | Implemented |
| Duplicate email detection | Implemented |
| Rule-based classification | Implemented |
| Priority detection | Implemented |
| Inbox agent | Implemented |
| Email summarization | Basic implementation |
| SQLite persistent storage | Implemented |
| Task and reminder storage | Implemented |
| Follow-up storage | Implemented |
| Response intelligence | Implemented |
| AI response generation | Implemented |
| Draft editing | Implemented |
| Approval and rejection workflow | Implemented |
| Gmail email sending | Not implemented |
| Frontend dashboard | Planned |
| Advanced conversational memory retrieval | Planned |

---

# 12. Future Enhancements

The project can be extended with the following capabilities:

1. **Interactive Dashboard:** React-based interface for inbox analytics, email classification and task management.
2. **Advanced Conversational Memory:** Natural-language retrieval across historical emails, tasks and previous actions.
3. **Semantic Search:** Vector database integration for retrieving relevant email context.
4. **Deadline Intelligence:** Automatic deadline extraction and reminder scheduling.
5. **Follow-up Monitoring:** Identify unanswered emails and pending conversations.
6. **Email Thread Understanding:** Analyze complete conversation threads instead of isolated messages.
7. **Gmail Sending Integration:** Add secure sending functionality with explicit user approval, confirmation and audit logging.
8. **Background Processing:** Schedule synchronization and analysis jobs.
9. **Analytics:** Track email volume, priority distribution, response workload and task completion.

---

# 13. Project Objective

The long-term objective of Inbox Action Agent is to evolve from a conventional email assistant into a persistent AI-powered personal communication and productivity system.

Rather than simply answering questions about emails, the agent aims to understand communication, preserve useful context, identify responsibilities and help users take informed actions.

**The goal is not to automate communication blindly. It is to make communication more intelligent, organized and manageable while keeping the user in control.**

---

## Author

**Aditya Ghodke**

GitHub: https://github.com/adityaghodke275

Project Repository: https://github.com/adityaghodke275/inbox-action-agent

---

*Built with Python, FastAPI, Groq, Gmail API and SQLite.*
