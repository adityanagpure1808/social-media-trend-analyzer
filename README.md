# Social Media Trend Analyzer - Project Documentation

---

## Project Overview

The Social Media Trend Analyzer is a web application that enables users to select social media platforms (Facebook, LinkedIn, Instagram) and generate comprehensive trend reports using Tavily Research API. The application analyzes trending topics and sentiment from selected platforms, then provides an interactive RAG-based chat interface where users can query the generated reports. If questions cannot be answered from the report, the system automatically uses Tavily API to research the internet and provide answers.

### Target Users
- Social media managers
- Marketing professionals
- Content creators
- Researchers studying social trends
- Business analysts tracking brand mentions

### Core Value Proposition
Provides AI-powered trend analysis from major social media platforms through Tavily Research API, generating comprehensive reports on trending topics and sentiment. Users can interactively explore these reports through a RAG-based chat interface, with intelligent fallback to internet research when needed, enabling data-driven decision making based on social media conversations.

---

## Technology Stack

### Frontend
- **React 19** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router DOM** - Client-side routing
- **Firebase SDK** - Authentication

### Backend
- **Python 3.12+** - Programming language
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **LangChain** - AI integration and RAG
- **ChromaDB or FAISS** - Vector database for embeddings

### Database
- **SQLite** - Application data storage (NOT for authentication)
- **Vector Database** - ChromaDB or FAISS for report embeddings

### Authentication
- **Firebase Authentication** - Email/password authentication (handled entirely in frontend)

### AI/ML Services
- **Tavily Research API** - Trend research, report generation, and internet search
- **Google Gemini LLM** - Used only for RAG-based chat (via LangChain)
- **LangChain** - RAG chains, embeddings, vector store integration

### Development Tools
- **UV** - Python package manager
- **npm** - Node package manager
- **Git** - Version control

---

## Issue Flow Overview

This project is broken down into 19 issues, organized into logical phases:

### Foundation Phase (Issues 1-8)
**Issues #01-08** establish the project foundation:
- **Issue #01**: Project Setup (README format)
- **Issue #02**: Landing Page UI (static)
- **Issue #03**: Signup Page UI (static form)
- **Issue #04**: Login Page UI (static form)
- **Issue #05**: Firebase Auth Setup (configuration)
- **Issue #06**: Integrate Signup with Firebase
- **Issue #07**: Integrate Login with Firebase
- **Issue #08**: Dashboard UI (protected route)

### Core Features Phase (Issues 9-15)
**Issues #09-15** implement the main application features:
- **Issue #09**: Platform Selection (combined frontend + backend)
- **Issue #10**: Tavily API Integration (backend setup)
- **Issue #11**: Report Generation (combined frontend + backend, Tavily API)
- **Issue #12**: Report Display (combined frontend + backend)
- **Issue #13**: Vector Database Setup (backend)
- **Issue #14**: RAG Implementation (backend)
- **Issue #15**: Chat Interface (combined frontend + backend, LLM used here)

### Advanced Features Phase (Issues 16-18)
**Issues #16-18** add advanced functionality:
- **Issue #16**: Tavily Fallback (backend logic)
- **Issue #17**: Report Export (combined frontend + backend)
- **Issue #18**: Dashboard Integration (combined frontend + backend)

### Final Phase (Issue 19)
**Issue #19** ensures everything works together:
- **Issue #19**: Final Testing and Application Flow Verification

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────┐
│   React Frontend │
│  (React 19)     │
│                 │
│  - Landing      │
│  - Auth Pages   │
│  - Dashboard    │
│  - Reports      │
│  - Chat UI      │
└────────┬────────┘
         │
         │ HTTP/REST API
         │
┌────────▼────────┐
│  FastAPI Backend│
│                 │
│  - Auth Routes  │
│  - Report APIs  │
│  - Chat APIs    │
│  - RAG Service │
└────────┬────────┘
         │
    ┌────┴────┬──────────────┬─────────────┐
    │         │              │             │
┌───▼───┐ ┌──▼────┐   ┌─────▼─────┐  ┌───▼────┐
│SQLite │ │Vector │   │  Tavily   │  │ Gemini │
│       │ │  DB   │   │    API    │  │  LLM   │
│       │ │       │   │           │  │        │
│Reports│ │Embed- │   │  Trend    │  │  RAG   │
│Chat   │ │dings  │   │  Research │  │  Chat  │
│Platform│ │       │   │           │  │        │
└───────┘ └───────┘   └───────────┘  └────────┘
```

### Data Flow

**Report Generation Flow:**
```
User selects platform → Frontend → Backend API → Tavily API → 
Complete report generated → Stored in SQLite → Embeddings generated → 
Stored in Vector DB → User notified
```

**Chat Flow:**
```
User asks question → Frontend → Backend API → RAG Chain → 
Vector DB search → Retrieve relevant context → LLM generates answer → 
If RAG fails → Tavily API research → Response returned → 
Stored in SQLite → Displayed in UI
```

---

## API Endpoints Reference

### Authentication Endpoints
**Note:** Authentication is handled entirely by Firebase SDK in the frontend. No backend auth endpoints are needed.

### Platform Selection Endpoints

| Method | Endpoint | Protected | Purpose | Request Body | Response |
|--------|----------|-----------|---------|--------------|----------|
| POST | `/api/platform/select` | Yes | Select social media platform | `{platform, userId}` | `{id, platform, status}` |
| GET | `/api/platform/current` | Yes | Get current selected platform | - | `{platform, selectedAt}` |

### Report Generation Endpoints

| Method | Endpoint | Protected | Purpose | Request Body | Response |
|--------|----------|-----------|---------|--------------|----------|
| POST | `/api/reports/generate` | Yes | Generate trend report using Tavily | `{platform}` | `{reportId, status, jobId}` |
| GET | `/api/reports/status/:jobId` | Yes | Get report generation status | - | `{status, progress, reportId}` |

### Report Management Endpoints

| Method | Endpoint | Protected | Purpose | Request Body | Response |
|--------|----------|-----------|---------|--------------|----------|
| GET | `/api/reports` | Yes | Get all user reports | `?platform=...` | `[{id, platform, createdAt, title}]` |
| GET | `/api/reports/:id` | Yes | Get specific report details | - | `{id, platform, content, sentiment, trends}` |
| DELETE | `/api/reports/:id` | Yes | Delete report | - | `{success, message}` |
| GET | `/api/reports/:id/export` | Yes | Export report | `?format=markdown` | Report file or data |

### Chat Endpoints

| Method | Endpoint | Protected | Purpose | LLM Integration | Request Body | Response |
|--------|----------|-----------|---------|-----------------|--------------|----------|
| POST | `/api/chat` | Yes | Send chat message (RAG or Tavily fallback) | Yes | `{message, reportId}` | `{response, source, confidence}` |
| GET | `/api/chat/history` | Yes | Get chat history | No | `?reportId=...` | `[{id, message, response, timestamp, source}]` |
| DELETE | `/api/chat/history/:id` | Yes | Delete chat message | No | - | `{success, message}` |

### Embeddings Endpoint

| Method | Endpoint | Protected | Purpose | Request Body | Response |
|--------|----------|-----------|---------|--------------|----------|
| POST | `/api/reports/:id/embeddings` | Yes | Generate embeddings for report | - | `{status, embeddingsCount}` |

### Dashboard Endpoint

| Method | Endpoint | Protected | Purpose | Request Body | Response |
|--------|----------|-----------|---------|--------------|----------|
| GET | `/api/dashboard/stats` | Yes | Get dashboard statistics | - | `{totalReports, recentReports, platforms}` |

---

## Frontend Pages and Routes

| Page Name | Route | Protected | Purpose | Main Components |
|-----------|-------|-----------|---------|-----------------|
| Landing | `/` | No | Welcome page with app info | Navbar, Hero, Features, Footer |
| Signup | `/signup` | No | User registration | SignupForm |
| Login | `/login` | No | User authentication | LoginForm |
| Dashboard | `/dashboard` | Yes | Platform selection and overview | Navbar, PlatformSelector, StatsCards, RecentReports |
| Reports | `/reports` | Yes | View and manage reports | Navbar, ReportList, ReportCard, GenerateReportButton |
| Report Detail | `/reports/:id` | Yes | View report and chat interface | Navbar, ReportViewer, ChatInterface, ChatHistory |
| Chat | `/chat/:reportId` | Yes | Chat with report (RAG) | Navbar, ChatInterface, ChatHistory, MessageInput |
| Profile | `/profile` | Yes | User profile settings | ProfileForm, SettingsPanel |

---

## Frontend Components

| Component Name | Used On Pages | Purpose |
|----------------|---------------|---------|
| Navbar | All pages | Navigation header |
| Hero | Landing | Hero section with CTA |
| Features | Landing | Feature showcase |
| Footer | All pages | Footer with links |
| SignupForm | Signup | Registration form |
| LoginForm | Login | Login form |
| PlatformSelector | Dashboard | Select social media platform |
| PlatformCard | Dashboard | Single platform selection card |
| StatsCards | Dashboard | Display statistics |
| RecentReports | Dashboard | Display recent reports |
| ReportList | Reports | Display all reports |
| ReportCard | Reports | Single report card |
| GenerateReportButton | Reports, Dashboard | Trigger report generation |
| ReportViewer | Report Detail | Display report content |
| ChatInterface | Report Detail, Chat | Chat UI with messages |
| ChatHistory | Report Detail, Chat | Display chat messages |
| MessageInput | Report Detail, Chat | Input field for chat |
| MessageBubble | Report Detail, Chat | Single chat message |
| LoadingSpinner | Multiple | Loading indicator |
| ErrorMessage | Multiple | Error display |
| ReportStatus | Reports, Dashboard | Show report generation status |
| ExportButton | Report Detail | Export report |

---

## Database Schema (High-Level)

### Tables Needed

**platform_selections**
- Purpose: Store user's selected social media platform
- Essential fields: identifier, user reference, platform name, selected timestamp

**reports**
- Purpose: Store generated trend reports
- Essential fields: identifier, user reference, platform, report content (JSON), sentiment data, created timestamp

**chat_history**
- Purpose: Store chat conversations with reports
- Essential fields: identifier, user reference, report reference, message, response, source (RAG/Tavily), timestamp

**report_embeddings**
- Purpose: Metadata for vector database embeddings (actual embeddings in vector DB)
- Essential fields: identifier, report reference, embedding count, status

**report_generation_jobs**
- Purpose: Track report generation job status
- Essential fields: identifier, user reference, platform, status, progress, report reference

**Note:** Specific field names and data types are decided by developers. This is conceptual guidance only.

---

## User Journey

1. **First Visit**: User lands on Landing page, sees features, clicks "Sign Up"
2. **Registration**: User fills signup form, Firebase creates account, redirects to login
3. **Login**: User enters credentials, Firebase authenticates, redirects to Dashboard
4. **Platform Selection**: User selects social media platform (Facebook, LinkedIn, or Instagram)
5. **Report Generation**: User clicks "Generate Report", backend calls Tavily API, report is generated and stored
6. **Report Viewing**: User navigates to Reports page, views list, clicks on report to see details
7. **Chat with Report**: User opens chat interface, asks questions, RAG system answers based on report content
8. **Fallback Research**: If RAG cannot answer, system uses Tavily API to research internet
9. **Report Management**: User exports reports, deletes old reports, manages chat history

---

## Key Features

### Platform Selection
- Users can select from Facebook, LinkedIn, or Instagram
- Selection is saved and persists across sessions
- Selected platform is used for report generation

### Report Generation
- Uses Tavily Research API to generate comprehensive trend reports
- Tavily API generates complete reports including trending topics and sentiment analysis
- Reports are stored in SQLite database
- Report generation status can be tracked

### Vector Database & RAG
- Report content is embedded and stored in vector database
- RAG chain retrieves relevant report sections based on user questions
- LLM generates contextually relevant answers using retrieved content

### Chat Interface
- Interactive chat interface for querying reports
- Uses RAG to answer questions based on report content
- Falls back to Tavily API when RAG cannot answer
- Chat history is stored and can be viewed

### Report Export
- Reports can be exported as Markdown files
- Exported reports include all trends and sentiment data
- Files are properly formatted and downloadable

---

## Important Notes

### Tavily API Usage
- **Report Generation**: Tavily Research API generates complete reports including sentiment analysis
- **No LLM for Reports**: LLM is NOT used for report generation - Tavily handles everything
- **LLM Only for Chat**: LLM (via LangChain) is used ONLY for RAG-based chat interface
- **Fallback**: Tavily API is also used as fallback when RAG cannot answer questions

### Authentication
- Firebase Authentication handles ALL authentication
- No backend auth endpoints needed
- Firebase SDK is used entirely in frontend
- SQLite is NOT used for authentication

### Database
- SQLite stores application data (reports, chat history, platform selections)
- Vector database (ChromaDB/FAISS) stores report embeddings
- Students design their own database schemas

### RAG Implementation
- LangChain is used for RAG chains
- Vector database stores report embeddings
- RAG retrieves relevant context and passes to LLM
- Fallback to Tavily API when RAG cannot answer

---

## Development Setup

### Prerequisites
- Python 3.12+
- UV package manager
- Node.js 18+
- Google API Key (for Gemini LLM)
- Tavily API Key (for trend research)
- Firebase project (for authentication)

### Backend Setup
1. Navigate to Backend directory
2. Create virtual environment: `uv venv`
3. Activate virtual environment
4. Install dependencies: `uv add -r requirements.txt`
5. Create `.env` file with API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```
6. Run server: `uvicorn main:app --reload`

### Frontend Setup
1. Navigate to Frontend directory
2. Install dependencies: `npm install`
3. Create `.env` file with Firebase config
4. Run dev server: `npm run dev`

---

## Testing

See **Issue #19: Final Testing and Application Flow Verification** for complete testing documentation and flow verification.

---

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Firebase Authentication](https://firebase.google.com/docs/auth)
- [LangChain Documentation](https://python.langchain.com/)
- [Tavily Research API](https://docs.tavily.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)

---

## License

This is a template project for educational purposes.
