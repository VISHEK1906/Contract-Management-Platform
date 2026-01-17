# Check for virtual environment and activate if present
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..."
    . .\venv\Scripts\Activate.ps1
}
else {
    Write-Warning "Virtual environment not found in 'venv'. Assuming dependencies are installed globally or in another environment."
}

# Navigate to backend directory
if (Test-Path "backend") {
    Set-Location "backend"
}
else {
    Write-Error "Backend directory not found!"
    exit 1
}

# Run the FastAPI application
Write-Host "Starting Contract Management Platform..."
uvicorn main:app --port 8001 --reload
