# Policy Pundit

An AI-powered policy analysis system that uses advanced NLP and machine learning to analyze legal documents, contracts, and policies. The system provides intelligent querying capabilities with explainable AI responses.

## Features

- **Document Upload**: Support for PDF and DOCX files
- **Intelligent Querying**: Natural language questions about policy content
- **Explainable AI**: Detailed reasoning and evidence citations
- **Semantic Search**: Advanced embedding-based retrieval
- **Real-time Analysis**: Fast processing with confidence scores

## Architecture

### Frontend (React + TypeScript)
- Modern UI with shadcn/ui components
- Real-time document processing
- Interactive query interface
- Detailed results display with evidence

### Backend (FastAPI + Python)
- Document parsing and chunking
- Semantic embedding and retrieval
- AI-powered analysis and reasoning
- RESTful API with CORS support

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the backend server:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## API Endpoints

### Document Upload
- **POST** `/api/v1/upload/`
- Upload PDF or DOCX files for analysis
- Returns success message on completion

### Query Analysis
- **POST** `/api/v1/ask/`
- Send natural language questions about uploaded documents
- Returns detailed analysis with evidence and reasoning

### Health Check
- **GET** `/health`
- Check server status

### API Documentation
- **GET** `/docs`
- Interactive API documentation (Swagger UI)

## Usage

1. **Upload Document**: Use the document upload interface to upload a PDF or DOCX file
2. **Ask Questions**: Type natural language questions about the document content
3. **Review Results**: View detailed analysis with supporting evidence and conditions
4. **Understand Reasoning**: Examine the AI's decision rationale and confidence scores

## Example Queries

- "Does this policy cover knee surgery, and what are the conditions?"
- "What is the waiting period for pre-existing conditions?"
- "Are mental health services covered under this plan?"
- "What are the exclusions for dental procedures?"
- "Is emergency room treatment covered out-of-network?"

## Development

### Backend Structure
```
backend/
├── app/
│   ├── routers/          # API route handlers
│   ├── services/         # Core business logic
│   └── utils/           # Helper functions
├── data/                # Document storage
└── requirements.txt     # Python dependencies
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/      # React components
│   ├── pages/          # Page components
│   └── hooks/          # Custom React hooks
├── public/             # Static assets
└── package.json        # Node.js dependencies
```

## Testing

### Backend Testing
```bash
cd backend
python test_server.py
```

### Frontend Testing
```bash
cd frontend
npm run test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
