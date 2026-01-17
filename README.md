# Contract Management Platform (CMP)

A production-ready full-stack Contract Management Platform that enables organizations to create reusable contract blueprints, manage contract lifecycles, and track status via a dashboard.

## 🚀 Features

*   **Blueprint Creation**: Visual drag-and-drop interface to design contract templates with text, date, signature, and checkbox fields.
*   **Contract Generation**: innovative instantiation of contracts from blueprints.
*   **Lifecycle Management**: Strict enforcement of contract states: Created → Approved → Sent → Signed → Locked (or Revoked).
*   **Dashboard**: Real-time overview of all contracts with status filtering.
*   **Audit Trail**: Tracks status changes and users involved.

## 🛠 Technology Stack

*   **Frontend**: HTML5, Vanilla JavaScript, Tailwind CSS (via CDN).
*   **Backend**: Python, FastAPI (API Layer), Django (ORM, Admin, Auth).
*   **Database**: MySQL (Compatible with 5.5+ via custom patching).

## 📂 Project Structure

```
/backend
    /cmp_project      # Django settings & configuration
    /core             # Django models & migrations
    /api              # FastAPI routers (Business Logic)
    main.py           # FastAPI entry point
    manage.py         # Django management script

/frontend
    index.html             # Dashboard
    create_blueprint.html  # Visual Template Editor
    create_contract.html   # Contract generation
    contract_detail.html   # Contract viewing & lifecycle actions
```


## ⚙️ Setup Instructions

### 1. Prerequisites
*   Python 3.8+
*   MySQL Server

### 2. Quick Start
1.  **Configure Database**:
    *   Navigate to `backend`.
    *   Rename `.env.example` to `.env`.
    *   Update `DB_USER` and `DB_PASSWORD` with your MySQL credentials.
    *   Initialize Database (if not already done):
        ```bash
        cd backend
        python init_db_compat.py
        python manage.py migrate --fake-initial
        cd ..
        ```

2.  **Run the Application**:
    Simply execute the run script from the root directory:
    ```powershell
    .\run_app.ps1
    ```
    *Tip: If you see a security error, try running this instead:*
    ```powershell
    powershell -ExecutionPolicy Bypass -File .\run_app.ps1
    ```
    The application will automatically activate the virtual environment (if present in `venv`) and start the server.

3.  **Access the Dashboard**:
    Open `http://localhost:8000` in your web browser. 
    (Note: The frontend is now served directly by the backend).

## 🏗 Architecture Decisions

### Django + FastAPI Hybrid
We leverage **Django** for what it does best: solid ORM, schema migration management, and a battle-tested Admin interface. **FastAPI** is layered on top to provide high-performance, async-capable REST APIs for the frontend. This hybrid approach ensures robustness and speed.

### MySQL Compatibility
Includes a custom compatibility layer to support older MySQL versions (5.5) by selectively disabling unsupported features (microsecond precision) while maintaining data integrity.

### Frontend Simplicity
Built with Vanilla JS and Tailwind integration to ensure zero build-step complexity while delivering a premium, modern UI.

## 📝 Assumptions & Limitations

*   **Authentication**: The UI simulates a logged-in user (ID: 1) for the MVP scope. Real-world deployment would require a login screen integrating with Django Auth.
*   **Field Positioning**: Visual placement saves coordinates; PDF generation is not included (contracts are viewed as HTML web views).
