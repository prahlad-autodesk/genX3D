# genx3D

A next-generation 3D CAD assistant platform combining browser-based parametric modeling (Cascade Studio) with an AI-powered backend for chat, model generation, and analysis.

## Features
- Web-based 3D CAD modeling (Cascade Studio)
- AI chat assistant (LLM-powered)
- Model generation, analysis, and help agents
- FastAPI backend with LangGraph orchestration
- Production-ready Docker deployment

## Project Structure
```
backend/    # FastAPI, LangGraph, LLM, CAD endpoints
frontend/   # Cascade Studio static files
static/     # Exported models (STEP, STL)
Dockerfile  # Production build
```

## Quick Start
1. **Clone the repo:**
   ```bash
   git clone https://github.com/yourusername/genx3D.git
   cd genx3D
   ```
2. **Set up environment:**
   - Add your `OPENROUTER_API_KEY` to a `.env` file.
3. **Build and run with Docker:**
   ```bash
   docker build -t genx3d .
   docker run -d --env-file .env -p 8000:8000 genx3d
   ```
4. **Access the app:**
   - Open [http://localhost:8000/app/](http://localhost:8000/app/) in your browser.

## Development
- Backend: Python 3.11+, FastAPI, LangChain, LangGraph, CadQuery
- Frontend: Static JS/HTML (Cascade Studio)

## License
MIT (see LICENSE)

## Contact
For questions or contributions, open an issue or contact the maintainer. 