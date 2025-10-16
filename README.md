# 🎯 Priyam AI - Professional Talent Scout Assistant

## 🌟 Overview

**Priyam AI** (प्रियम - meaning "beloved" in Sanskrit) is an intelligent, professional hiring assistant powered by advanced AI technology. Built for the modern recruitment landscape, Priyam AI provides enterprise-grade candidate screening and interview assistance with a beautiful, professional interface.

## ✨ Key Features

- **🤖 AI-Powered Conversations**: Intelligent interview flows using Groq's llama-3.1-8b-instant model
- **🎨 Professional UI**: Enterprise-grade Streamlit interface with Inter font and modern design
- **📊 Comprehensive Analytics**: Detailed candidate assessment and conversation tracking
- **🔒 Secure**: PostgreSQL database with session management and data persistence
- **⚡ Fast & Scalable**: Docker containerized for easy deployment and scaling
- **🧪 Extensive Testing**: Comprehensive testing framework with Jupyter notebooks

## Technology Stack

### Frontend
- Streamlit - Web application framework
- HTML/CSS/JavaScript - Enhanced UI components
- Responsive design for desktop, tablet, and mobile

### Backend
- FastAPI - High-performance Python web framework
- TinyLlama-1.1B-Chat-v1.0-GGUF - Open-source LLM via CTransformers
- PostgreSQL - Relational database
- SQLAlchemy - ORM for database operations

### Infrastructure
- Docker & Docker Compose - Containerization
- Python 3.12+ - Runtime environment

## Prerequisites

- Python 3.12 or higher
- Docker and Docker Compose
- Git

## Installation

### Option 1: Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd assist
```

2. Start the application:
```bash
docker-compose up --build
```

3. Access the application:
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Option 2: Local Development

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up PostgreSQL database (or use Docker):
```bash
docker run --name postgres-db -e POSTGRES_DB=talentscout -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=sans -p 5432:5432 -d postgres:15
```

3. Run the backend API:
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

4. Run the frontend (in another terminal):
```bash
streamlit run app.py
```

## Usage

### For Candidates
1. Visit the Streamlit interface at http://localhost:8501
2. Start a conversation with the AI assistant
3. Answer questions about your:
   - Full name
   - Years of professional experience
   - Desired position/role
   - Technical skills and technologies

### For Recruiters
- Monitor candidate progress in real-time
- Access conversation history via the API
- Review collected candidate information
- Export data for further processing

## API Documentation

The backend provides a comprehensive REST API:

### Endpoints

- `GET /` - API information and status
- `POST /chat` - Send messages to the AI assistant
- `GET /sessions/{session_id}` - Retrieve conversation history
- `GET /docs` - Interactive API documentation with testing interface

### Example API Usage

```python
import requests

# Start a conversation
response = requests.post("http://localhost:8000/chat", json={
    "user_input": "Hello, I'm interested in a software engineering position"
})

print(response.json())
```

## Database Schema

The application uses PostgreSQL with the following tables:

- `chat_sessions` - Stores session information and collected candidate data
- `messages` - Stores conversation history (user and AI messages)

## Configuration

### Environment Variables
- `DATABASE_URL` - PostgreSQL connection string (default: postgresql://postgres:sans@db:5432/talentscout)

### Model Configuration
- Model: TinyLlama-1.1B-Chat-v1.0-GGUF
- Max tokens: 256
- Temperature: 0.7
- Repetition penalty: 1.2

## Development

### Project Structure
```
assist/
├── api.py              # FastAPI backend application
├── app.py              # Streamlit frontend application
├── models.py           # Database models and configuration
├── api_docs.html       # Interactive API documentation
├── requirements.txt    # Python dependencies
├── pyproject.toml      # Project configuration
├── Dockerfile          # Container configuration
├── docker-compose.yml  # Multi-container setup
└── README.md          # This file
```

### Adding New Features
1. Backend changes: Modify `api.py` and update API documentation
2. Frontend changes: Modify `app.py` and update UI components
3. Database changes: Update `models.py` and create migrations

## Testing

### API Testing
Visit http://localhost:8000/docs for interactive API testing with built-in Swagger UI.

### Manual Testing
1. Start the application with Docker Compose
2. Open the Streamlit interface
3. Test various conversation flows
4. Verify data persistence in the database

## Deployment

### Production Deployment
1. Update environment variables for production database
2. Configure proper SSL/TLS certificates
3. Set up monitoring and logging
4. Configure backup strategies for the database

### Scaling Considerations
- The TinyLlama model requires GPU acceleration for better performance
- Consider using a more powerful LLM for production use
- Implement rate limiting and authentication for API endpoints

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Ensure PostgreSQL container is running
   - Check DATABASE_URL configuration
   - Verify database credentials

2. **Model Loading Issues**
   - Ensure sufficient RAM (model requires ~2GB)
   - Check model file path and permissions
   - Verify CTransformers installation

3. **Port Conflicts**
   - Ensure ports 5432, 8000, and 8501 are available
   - Stop other applications using these ports

### Logs
- View application logs: `docker-compose logs`
- View specific service logs: `docker-compose logs api` or `docker-compose logs app`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Check the API documentation at http://localhost:8000/docs
- Review the troubleshooting section above
- Create an issue in the repository

## Future Enhancements

- Integration with more powerful LLM models
- Multi-language support
- Advanced candidate analytics
- Integration with ATS (Applicant Tracking Systems)
- Voice-based interviews
- Real-time collaboration features

The app will start at `http://localhost:8501`.

## Usage

- Open the URL in your browser.
- Start chatting with the TalentScout AI.
- The chatbot will guide you through the hiring process.

## Development

- Edit `main.py` for code changes.
- Add dependencies with `uv add <package>`.
- Run tests or additional scripts as needed.

## License

This project is open-source.
