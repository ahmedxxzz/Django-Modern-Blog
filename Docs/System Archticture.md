# System Architecture Design

**Project:** Minimalist Django Blog Platform
**Version:** 1.0
**Architect:** Lyra
**Date:** November 22, 2025

---

## 1. High-Level 3-Tier Architecture

The system follows the classical **Three-Tier Architecture** pattern. However, given the "Minimalist" constraint and the use of SQLite, the Data Tier is physically co-located with the Application Tier, simplifying the infrastructure significantly.

### 1.1 The Tiers

1.  **Presentation Tier (Client-Side):**
    *   **Technology:** HTML5, Tailwind CSS (via compiled CSS), JavaScript (minimal).
    *   **Responsibility:** Renders the User Interface (UI) in the user's browser. It handles display logic for posts, comment threads, and forms. It communicates with the backend via standard HTTP/HTTPS requests.
    *   **State:** Stateless. Relies on Cookies (Session ID/CSRF Tokens) for state management.

2.  **Application Tier (Server-Side Logic):**
    *   **Technology:** Python 3.x, Django 5.x (WSGI), Gunicorn.
    *   **Responsibility:** Contains the business logic, routing, authentication, and data processing. It receives HTTP requests from the Presentation Tier, processes them using Django Views, queries the Data Tier via the ORM, and returns rendered HTML templates.

3.  **Data Tier (Persistence):**
    *   **Technology:** SQLite 3.
    *   **Responsibility:** Stores persistent data (Users, Posts, Comments, Subscriptions) in a single file (`db.sqlite3`) located on the server's file system.
    *   **Constraint:** Due to SQLite's file-locking mechanism, this tier is tightly coupled to the Application Tier instance.

### 1.2 Data Flow Diagram (Conceptual)

```mermaid
[User Browser] <--> (HTTPS) <--> [Nginx Reverse Proxy] <--> (Unix Socket) <--> [Gunicorn/Django] <--> (File I/O) <--> [SQLite File]
                                          |
                                          v
                                    [Static Files]
                                  (CSS/Images/JS)
```

---

## 2. Logical Architecture (Django Component Breakdown)

This section details how the Django Framework's Model-View-Template (MVT) pattern implements the Functional Requirements defined in the SRS.

### 2.1 Models (Data Layer)
The Models define the structure of the data and business rules surrounding data integrity.
*   **Core Entities:** `Post`, `Comment` (using `django-mptt` for tree traversal), `NewsletterSubscriber`.
*   **Authentication:** `CustomUser` extends the standard AbstractUser.
*   **Abstraction:** All database interactions occur via the **Django ORM**, preventing SQL injection and abstracting the raw SQLite commands.

### 2.2 Views (Business Logic Layer)
Views act as the traffic controller, enforcing authentication and permissions.
*   **Public Views:** `ListView` (Home), `DetailView` (Post reading). These are Read-Only and accessible to all.
*   **Protected Views:** `CreateView` (Comments), `UpdateView` (User Profile). These utilize `LoginRequiredMixin` to strictly enforce **FR 3.2**.
*   **Admin Views:** Built-in Django Admin logic handles the heavy lifting for Post CRUD (**FR 3.1**).
*   **Logic Flow:**
    1.  Receive Request.
    2.  Check Permissions (Is user author? Is user subscriber?).
    3.  Validate Input (Forms).
    4.  Trigger Model save.
    5.  Return Response (Redirect or Render).

### 2.3 Templates & Frontend Strategy (Presentation Layer)
*   **Template Engine:** Django Template Language (DTL). Logic in templates is restricted to display loops (e.g., iterating through comments) and conditionals (e.g., `{% if user.is_authenticated %}`).
*   **Styling Architecture (Tailwind CSS):**
    *   **Development:** A Tailwind build process (using the Standalone CLI or Node) scans HTML templates for classes.
    *   **Production:** A single, minified `styles.css` file is generated.
    *   **Constraint:** No dynamic JavaScript frameworks (React/Vue) are used. The UI is Server-Side Rendered (SSR).

### 2.4 URL Routing
*   **Scheme:** RESTful-style semantic URLs.
    *   `/` - Home
    *   `/post/<slug:slug>/` - Post Detail
    *   `/accounts/login/` - Auth
    *   `/subscribe/` - Newsletter logic

---

## 3. Technology & Deployment Architecture

### 3.1 Technology Stack Justification
*   **Python/Django:** Provides "Batteries Included" (Auth, Admin, ORM, Security) out of the box, reducing development time and code volume.
*   **SQLite:** Removes the need for a separate database process (like PostgreSQL). Zero configuration, single-file backup, sufficient performance for single-author blogs (capable of handling ~10-50 concurrent req/sec comfortably).
*   **Tailwind CSS:** Allows for rapid UI development without writing custom CSS files, keeping the maintainability high.

### 3.2 Deployment Strategy: Single-Server Model
**Constraint Enforcement:** Because SQLite handles concurrency via file locking, the architecture **cannot** be horizontally scaled (load balanced across multiple servers) without replacing the database engine.

**Production Stack Configuration:**
1.  **Host:** Small Virtual Private Server (VPS) - e.g., AWS Lightsail, DigitalOcean Droplet, or Linode.
2.  **Reverse Proxy (Nginx):**
    *   Handles SSL/TLS termination (HTTPS).
    *   Serves **Static Files** (CSS, Images) and **Media Files** directly (High Performance).
    *   Forwards application requests to the Application Server.
3.  **Application Server (Gunicorn):**
    *   Runs the Django Python code.
    *   Communicates with Nginx via a Unix Socket.
    *   Worker Class: `sync` (Standard for Django) or `gthread`.
4.  **Process Manager (Systemd):**
    *   Ensures Gunicorn starts on boot and restarts on failure.

**Maintenance:**
*   **Backups:** Extremely simple. A cron job copies the `db.sqlite3` file and the `media/` directory to an external storage (e.g., S3 bucket) nightly.

---

## 4. Security Architecture

This architecture relies heavily on Django's mature security middleware to satisfy **NFR 4.1**.

### 4.1 Input Validation & Sanitization
*   **Forms:** All user inputs (Comments, Logins) are processed via Django Forms, which validate data types server-side.
*   **SQL Injection:** The Django ORM parameterizes all queries by default, neutralizing SQL injection risks from user input.
*   **XSS (Cross-Site Scripting):** Django Templates auto-escape all variable output by default.
    *   *Exception:* The Post Body (Rich Text) uses `django-ckeditor`. This must be configured to sanitize HTML input (stripping script tags) before rendering with the `|safe` filter.

### 4.2 Authentication & Session Management
*   **Passwords:** Hashed using PBKDF2 (Django Default) or Argon2. Passwords are never stored in plain text.
*   **Session Security:**
    *   `SESSION_COOKIE_SECURE = True` (HTTPS only).
    *   `SESSION_COOKIE_HTTPONLY = True` (Prevents JS access to cookies).
    *   `CSRF_COOKIE_SECURE = True`.

### 4.3 Network Security
*   **CSRF Protection:** Django's `CsrfViewMiddleware` is mandatory for all POST requests.
*   **Allowed Hosts:** The application is hardcoded to only respond to specific domain names (preventing Host Header attacks).

---

## 5. Frontend Asset Pipeline (Architect's Choice)

1.  **Development:** Developer uses Tailwind CLI to watch template files and regenerate CSS in real-time.
2.  **Build:** Before deployment, a CI/CD step (or manual script) runs the Tailwind CLI with `--minify`.
3.  **Artifact:** The resulting `styles.css` is committed or moved to the Django `static/` directory.
4.  **Production:** Django's `collectstatic` command moves this file to the Nginx-served directory.
    *   *Result:* Production server needs only Python installed; no Node/NPM required.