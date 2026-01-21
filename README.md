# Contract Management Platform (CMP)

**Live Demo:** [https://contractmanagementplatform.onrender.com](https://contractmanagementplatform.onrender.com)

A production-ready full-stack Contract Management Platform that enables organizations to create reusable contract blueprints, manage contract lifecycles, and track status via a dashboard.

## 🚀 Features

*   **Blueprint Creation**: Visual drag-and-drop interface to design contract templates with text, date, signature, and checkbox fields.
*   **Contract Generation**: Innovative instantiation of contracts from blueprints.
*   **Lifecycle Management**: Strict enforcement of contract states: Created → Approved → Sent → Signed → Locked (or Revoked).
*   **Dashboard**: Real-time overview of all contracts with status filtering.
*   **Audit Trail**: Tracks status changes and users involved.

## 🛠 Technology Stack

*   **Frontend**: HTML5, Vanilla JavaScript, Tailwind CSS (via CDN).
*   **Backend**: Python, FastAPI (API Layer), Django (ORM, Admin, Auth).
*   **Database**: MySQL (Compatible with 5.5+ via custom patching).

## 📂 Project Structure

```
/
    /api              # FastAPI routers (Business Logic)
    /cmp_project      # Django settings & configuration
    /core             # Django models & migrations
    /static           # Frontend HTML/JS/CSS Assets
    main.py           # FastAPI entry point
    manage.py         # Django management script
    init_db_compat.py # Database initialization script
    reset_db.py       # Database reset script
```

## ⚙️ Setup Instructions

### 1. Prerequisites
*   Python 3.8+
*   MySQL Server

### 2. Quick Start

1.  **Clone the Repository** (if applicable)

2.  **Configure Environment Variables**:
    *   Create a `.env` file in the root directory.
    *   Add the following environment variables:
        ```bash
        DB_NAME=your_db_name
        DB_USER=your_db_user
        DB_PASSWORD=your_db_password
        DB_HOST=localhost
        DB_PORT=3306
        SECRET_KEY=your_secret_key
        DEBUG=True
        ALLOWED_HOSTS=localhost,127.0.0.1
        ```

3.  **Install Dependencies**:
    ```bash
    python -m venv venv
    # Activate virtual environment:
    # Windows: .\venv\Scripts\activate
    # Linux/Mac: source venv/bin/activate
    pip install -r requirements.txt
    ```

4.  **Initialize Database**:
    ```bash
    python init_db_compat.py
    python manage.py migrate --fake-initial
    ```

5.  **Run the Application**:
    ```bash
    uvicorn main:app --reload
    ```

6.  **Access the Dashboard**:
    Open `http://localhost:8000` in your web browser.

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
