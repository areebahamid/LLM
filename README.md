# Student LLM Assistant

A real-time, deployable LLM assistant for students using RAG + LangChain + FastAPI + React frontend.

## 🚀 Features

- **Real-time AI Chat**: Powered by Ollama with local LLM inference
- **RAG (Retrieval-Augmented Generation)**: Enhanced responses using FAISS vector database
- **Modern UI/UX**: Beautiful React frontend with responsive design
- **FastAPI Backend**: High-performance API with async support
- **Student-Focused**: Optimized for educational content and academic queries
- **Deployable**: Ready for Vercel deployment

## 🛠️ Tech Stack

### Backend

- **FastAPI**: Modern, fast web framework
- **LangChain**: LLM orchestration and RAG implementation
- **Ollama**: Local LLM inference (supports various models)
- **FAISS**: Vector similarity search for RAG
- **Pydantic**: Data validation and serialization

### Frontend

- **React 18**: Modern React with hooks
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Vite**: Fast build tool and dev server
- **Axios**: HTTP client for API calls

### Deployment

- **Vercel**: Frontend and API deployment
- **Docker**: Containerization (optional)

## 📁 Project Structure

```
student-llm-assistant/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configurations
│   │   ├── models/         # Data models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utility functions
│   ├── data/               # Knowledge base and embeddings
│   ├── requirements.txt    # Python dependencies
│   └── main.py            # FastAPI application entry
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # API services
│   │   ├── types/          # TypeScript types
│   │   └── utils/          # Utility functions
│   ├── package.json        # Node.js dependencies
│   └── vite.config.ts      # Vite configuration
├── docs/                   # Documentation
├── scripts/                # Setup and deployment scripts
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.9+**
2. **Node.js 18+**
3. **Ollama** (for local LLM inference)

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Ollama (install first from https://ollama.ai)
ollama pull llama2:7b

# Run the backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📚 Knowledge Base Setup

The assistant comes with a pre-configured knowledge base focused on academic content. To customize:

1. Add your documents to `backend/data/documents/`
2. Run the embedding generation script:
   ```bash
   python scripts/generate_embeddings.py
   ```

## 🎯 Usage

1. **Start a Chat**: Begin a conversation with the AI assistant
2. **Ask Questions**: The assistant uses RAG to provide accurate, contextual responses
3. **Upload Documents**: Add new knowledge to the system (coming soon)
4. **Customize Responses**: Adjust model parameters for different use cases

## 🔧 Configuration

### Environment Variables

Create `.env` files in both backend and frontend directories:

**Backend (.env)**

```env
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=llama2:7b
FAISS_INDEX_PATH=./data/faiss_index
OPENAI_API_KEY=your_openai_key  # Optional for fallback
```

**Frontend (.env)**

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 🚀 Deployment

### Vercel Deployment

1. **Frontend**: Connect your GitHub repo to Vercel
2. **Backend**: Deploy FastAPI using Vercel's Python runtime
3. **Environment**: Set up environment variables in Vercel dashboard

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for LLM orchestration
- [Ollama](https://ollama.ai/) for local LLM inference
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [React](https://reactjs.org/) for the frontend framework
- [Vercel](https://vercel.com/) for deployment platform

## 📞 Support

For support and questions:

- Create an issue in this repository
- Check the documentation in the `docs/` folder
- Review the API documentation at `/docs` when running the backend
