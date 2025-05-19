# AutoBrief Backend API

AutoBrief is an AI-powered document generation service that converts audio recordings into structured documents based on customizable templates.

## Features

- Upload audio files (mp3, wav, ogg, m4a)
- Multiple document templates (meeting notes, lecture notes, medical rounds, reports)
- Multiple output formats (DOCX, PDF, TXT)
- RESTful API with JWT authentication
- Asynchronous task processing
- File upload and download handling

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AutoBrief_Back_AI
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   
   # On Windows
   # python -m venv venv
   # .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Copy the `.env.example` to `.env` and update the values as needed:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file with your configuration.

## Running the Application

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Production Mode

For production, you should use a production-grade ASGI server like Uvicorn with Gunicorn:

```bash
pip install gunicorn

gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 app.main:app
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

To run the test suite:

```bash
pytest tests/
```

## Project Structure

```
AutoBrief_Back_AI/
├── app/                      # Main application package
│   ├── __init__.py
│   ├── main.py               # FastAPI application
│   ├── config.py             # Application configuration
│   ├── api/                  # API routes
│   │   ├── __init__.py
│   │   ├── generate_document.py  # Document generation endpoints
│   │   └── download_document.py  # Document download endpoints
│   └── dependencies/         # Application dependencies
│       ├── __init__.py
│       ├── security.py       # Authentication and security
│       └── file_utils.py     # File handling utilities
├── tests/                    # Test files
│   ├── __init__.py
│   ├── conftest.py           # Test fixtures
│   └── test_api.py           # API tests
├── .env                      # Environment variables
├── .gitignore
├── requirements.txt          # Python dependencies
└── README.md
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | `AutoBrief API` |
| `APP_VERSION` | Application version | `1.0.0` |
| `DEBUG` | Debug mode | `False` |
| `SECRET_KEY` | Secret key for JWT | `your-secret-key-here` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `UPLOAD_FOLDER` | Directory for uploaded files | `./uploads` |
| `MAX_CONTENT_LENGTH` | Maximum file size (bytes) | `16777216` (16MB) |
| `ALLOWED_EXTENSIONS` | Allowed file extensions | `mp3,wav,ogg,m4a` |
| `AI_SERVICE_URL` | URL of the AI service | `http://localhost:8001` |

## API Endpoints

### Authentication
- `POST /token` - Get access token (Basic Auth)
- `GET /api/test-auth` - Test authentication (requires auth)

### Document Generation
- `POST /api/generate/` - Generate a document from an audio file
- `GET /api/generate/status/{task_id}` - Check generation status

### Document Download
- `GET /api/download/{task_id}` - Download a generated document

### Health Check
- `GET /health` - Health check endpoint

## Deployment

### Docker

1. Build the Docker image:
   ```bash
   docker build -t autobrief-backend .
   ```

2. Run the container:
   ```bash
   docker run -d -p 8000:8000 --env-file .env autobrief-backend
   ```

### Cloud Deployment

For production deployment, consider using:
- AWS ECS/EKS
- Google Cloud Run
- Azure Container Instances
- Heroku

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- FastAPI for the awesome web framework
- Uvicorn for the ASGI server
- All contributors and team members