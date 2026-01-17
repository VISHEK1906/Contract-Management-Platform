# Contract Management Platform (CMP)

A production-ready full-stack application for creating, managing, lifecycle tracking, and signing contracts.

## 🌟 Key Features

*   **Blueprint Management**: Create reusable contract templates (Blueprints) with a rich layout editor.
    *   **A4 Canvas**: Design contracts on a standard A4 visual interface.
    *   **Smart Positioning**: Place input fields (Text, Signatures, Dates, Checkboxes) using semantic positioning (Top-Left, Bottom-Right, etc.).
    *   **Body Context**: Define the static legal text of the agreement.
*   **Contract Lifecycle**:
    *   **Instantiation**: Generate contracts from blueprints.
    *   **Visual Editing**: Fill in contract details directly on the digital paper.
    *   **Workflow Integration**: Strict status transitions: `CREATED` → `APPROVED` → `SENT` → `SIGNED` → `LOCKED`.
    *   **Security**: Contracts are locked and read-only once signed/finalized.
*   **Unified Architecture**:
    *   **Frontend**: Vanilla JS/HTML served via FastAPI (No separate node server needed).
    *   **Backend**: Hybrid FastAPI (High-performance API) + Django (ORM & Admin) architecture.
    *   **Database**: Robust MySQL storage.

## 🚀 Quick Start

### Prerequisites
*   Python 3.8+
*   MySQL Server running locally or remotely.

### 1. Configuration
Ensure your `.env` or `settings.py` is configured for your MySQL instance.
*   *Note*: The project includes a helper `backend/reset_db.py` to initialize the schema for development.

### 2. Run the Application
We provide a unified PowerShell script to manage the environment and start the server.

```powershell
.\run_app.ps1
```

*   **Port**: `8001`
*   **URL**: [http://127.0.0.1:8001/](http://127.0.0.1:8001/)
*   **API Documentation**: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

## 🗄️ Database Migrations

If you modify the models (`backend/core/models.py`), you must update the database schema.

**1. Activate the Virtual Environment**
```powershell
. venv\Scripts\Activate.ps1
```

**2. Generate Migrations**
Detects changes in your models and creates migration files.
```bash
python backend/manage.py makemigrations
```

**3. Apply Migrations**
Applies the changes to your MySQL database.
```bash
python backend/manage.py migrate
```

> [!IMPORTANT]
> **MySQL 5.x Compatibility**: If you encounter errors creating the `django_migrations` table on older MySQL versions, run our compatibility script:
> ```bash
> python backend/init_db_compat.py
> ```

## 📖 Usage Guide

### Step 1: Create a Blueprint
1.  Navigate to **"Create Blueprint"**.
2.  **Title**: Name your template (e.g., "NDA Agreement").
3.  **Contract Body**: Paste the full legal text. It will render on the A4 page.
4.  **Add Fields**:
    *   Select Type: *Signature*, *Text*, *Date*, or *Checkbox*.
    *   Select Position: *Top-Left*, *Top-Right*, *Bottom-Left*, *Bottom-Right*.
    *   Click **Add**.
5.  **Save**.

### Step 2: Issue a Contract
1.  On the Dashboard, click **"Create Contract"**.
2.  Choose the Blueprint you just created.
3.  Assign to a User (Mock ID used for MVP).
4.  Launch.

### Step 3: Manage & Sign
1.  Open the contract from the dashboard.
2.  **Fill Data**: Type into the fields overlaid on the contract.
3.  **Save Changes**: Persist your inputs.
4.  **Approve/Send**: Use the lifecycle buttons top-right to progress the contract.
5.  **Sign & Lock**: Once marked `SIGNED`, sending it to `LOCKED` makes it immutable.

## 🛠️ Technology Stack

*   **Backend Framework**: FastAPI (Validation, Async I/O) & Django (ORM).
*   **Database**: MySQL.
*   **Frontend**: HTML5, TailwindCSS, Vanilla JavaScript.
*   **Server**: Uvicorn (ASGI).

## 📂 Project Structure

```
├── backend/
│   ├── api/            # API Endpoints (Blueprints, Contracts)
│   ├── core/           # Database Models
│   ├── static/         # Frontend Assets (HTML/JS)
│   ├── main.py         # App Entry Point
│   └── manage.py       # Django Utilities
├── run_app.ps1         # Unified Start Script
└── README_CMP.md       # This file
```
