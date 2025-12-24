# Sherlock Web Application

A full-stack web application that wraps the [Sherlock](https://github.com/sherlock-project/sherlock) tool to search for usernames across 400+ social media platforms. The backend is built with FastAPI and Python, while the frontend is built with Next.js and TypeScript.

## Project Structure

```
kkkash/
├── sherlock/          # Sherlock repository and FastAPI backend
│   ├── api.py         # FastAPI application
│   ├── venv/          # Python virtual environment
│   └── sherlock_project/  # Sherlock source code
└── frontend/          # Next.js frontend application
    └── app/
        ├── page.tsx   # Main page
        └── components/
            ├── SearchForm.tsx
            └── SearchResults.tsx
```

## Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- npm or yarn
- Git (for cloning the repository)

## Setup Instructions

### Windows Setup

#### 1. Backend Setup (FastAPI) - Windows

1. Open PowerShell or Command Prompt and navigate to the project directory:
```powershell
cd sherlock
```

2. Create a virtual environment (if not already created):
```powershell
python -m venv venv
```

3. Activate the virtual environment:
   - **PowerShell:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   - **Command Prompt (CMD):**
   ```cmd
   venv\Scripts\activate.bat
   ```

4. Install dependencies:
```powershell
pip install -e .
pip install fastapi uvicorn python-multipart
```

5. Start the FastAPI server:
```powershell
python api.py
```

The API will be available at `http://localhost:8000`

**Alternative: Use uvicorn directly:**
```powershell
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

#### 2. Frontend Setup (Next.js) - Windows

1. Open a new PowerShell or Command Prompt window and navigate to the frontend directory:
```powershell
cd frontend
```

2. Install dependencies:
```powershell
npm install
```

3. Start the development server:
```powershell
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Linux/Mac Setup

#### 1. Backend Setup (FastAPI)

1. Navigate to the sherlock directory:
```bash
cd sherlock
```

2. Create and activate the virtual environment (if not already created):
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -e .
pip install fastapi uvicorn python-multipart
```

4. Start the FastAPI server:
```bash
python api.py
```

The API will be available at `http://localhost:8000`

**Alternative: Use uvicorn directly:**
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

**Alternative: Use the startup script:**
```bash
# From the project root
./start-backend.sh
```

#### 2. Frontend Setup (Next.js)

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

The frontend will be available at `http://localhost:3000`

**Alternative: Use the startup script:**
```bash
# From the project root
./start-frontend.sh
```

## Usage

1. Make sure both the backend (FastAPI) and frontend (Next.js) servers are running.

2. Open your browser and navigate to `http://localhost:3000`

3. Enter a username in the search form and click "Search"

4. The results will display all social media platforms where the username was found, along with direct links to the profiles.

## API Endpoints

### POST `/search`

Search for a username across social media platforms.

**Request Body:**
```json
{
  "username": "string",
  "sites": ["string"],  // Optional: specific sites to search
  "timeout": 60,        // Optional: request timeout in seconds
  "nsfw": false         // Optional: include NSFW sites
}
```

**Response:**
```json
{
  "username": "string",
  "total_sites": 0,
  "found_count": 0,
  "results": [
    {
      "site_name": "string",
      "url_main": "string",
      "url_user": "string",
      "status": "Claimed|Available|Unknown|Illegal|WAF",
      "query_time": 0.0,
      "context": "string"
    }
  ]
}
```

### GET `/health`

Health check endpoint.

### GET `/`

API information endpoint.

## Features

- Search usernames across 400+ social media platforms
- Filter results by status (Found, Not Found, All)
- Direct links to found profiles
- Real-time search progress
- Responsive design with dark mode support
- Optional site filtering
- Configurable timeout settings

## Notes

- The search may take some time depending on the number of sites being checked
- Some sites may block automated requests (WAF status)
- The API includes CORS middleware configured for `http://localhost:3000`

## Troubleshooting

### Backend Issues

- Ensure the virtual environment is activated
- Check that all dependencies are installed
- Verify Python version is 3.9+

### Frontend Issues

- Ensure the backend is running on port 8000
- Check browser console for CORS errors
- Verify Node.js version is 18+

### Connection Issues

- Make sure both servers are running
- Check firewall settings
- Verify the API URL in the frontend code matches your backend URL

## License

This project uses the Sherlock tool which is licensed under MIT License.

