**Document Title:** Software Requirements Specification (SRS) for Minimalist Django Blog Platform
**Version:** 1.0
**Date:** October 26, 2023
**Author:** Lyra, Senior Full Stack Developer & Technical Architect
**Status:** Draft / Approval Pending

---

## 1. Introduction

### 1.1 Purpose
The purpose of this Software Requirements Specification (SRS) is to define the functional and non-functional requirements for the development of a minimalist, single-author blog platform. This document serves as the primary roadmap for developers and stakeholders, ensuring the final deliverable meets the specific constraints of low operational overhead and a strict technology stack.

### 1.2 Scope
The product is a web-based content management system built using **Python** and **Django**. The application allows a single administrator (the Author) to publish rich-text content, while enabling community interaction through a registration-gated commenting system.

The visual presentation will be handled exclusively via **Tailwind CSS**, ensuring a modern, responsive, and lightweight frontend. Data persistence is managed via **SQLite**, removing the need for complex database server management.

### 1.3 Definitions & Acronyms
*   **CRUD:** Create, Read, Update, Delete.
*   **Slug:** A URL-friendly version of a string (e.g., "My First Post" becomes `my-first-post`).
*   **MPTT:** Modified Preorder Tree Traversal (an algorithm/library used for efficient storage of hierarchical data, such as nested comments).
*   **ORM:** Object-Relational Mapping (Django’s system for interacting with the database).
*   **LTS:** Long Term Support.
*   **CSRF:** Cross-Site Request Forgery.
*   **WYSIWYG:** What You See Is What You Get (Rich Text Editor).

---

## 2. Overall Description

### 2.1 User Roles
The system defines three distinct user levels with escalating privileges:

1.  **Public Reader (Guest):**
    *   Can view the homepage (post list).
    *   Can read individual published posts.
    *   Can read comments.
    *   Can subscribe to the newsletter via email form (without account creation).
2.  **Authenticated User (Subscriber/Reader):**
    *   Inherits all Guest privileges.
    *   Must register and login to perform actions.
    *   Can post comments on articles.
    *   Can reply to existing comments (nested threads).
    *   Can manage their profile subscription status.
3.  **Admin (Author):**
    *   Has full access to the Django Admin Panel.
    *   Can create, edit, delete, and publish posts.
    *   Can moderate/delete comments if necessary (via Admin panel).
    *   Can view the list of subscribers.

### 2.2 Constraints
*   **Backend Framework:** Django 5.x (running on Python 3.x).
*   **Database:** SQLite 3 (File-based database; no PostgreSQL/MySQL allowed to maintain simplicity).
*   **Frontend Styling:** Tailwind CSS (Utility-first framework). No heavy UI libraries (e.g., Bootstrap, Materialize) allowed.
*   **Operational:** The system must run on a minimal environment (e.g., a small VPS or basic PaaS container).

### 2.3 Assumptions
*   The blog will be maintained by a single author; therefore, complex role-based permission systems (RBAC) beyond standard Django groups are unnecessary.
*   Traffic is expected to be low-to-medium; SQLite write-locking limitations will not be a bottleneck.
*   The deployment environment supports persistent storage (for the SQLite file and media uploads).

---

## 3. Functional Requirements (FR)

### FR 3.1 Content Management (Blog Posts)
*   **FR 3.1.1:** The system shall provide a `Post` model containing:
    *   `title` (Char: Max 200).
    *   `slug` (Slug: Unique, Auto-generated from title).
    *   `content` (Rich Text: Must use `django-ckeditor` or similar integration).
    *   `created_at` (DateTime: Auto-now-add).
    *   `updated_at` (DateTime: Auto-now).
    *   `status` (Choice: Draft/Published).
    *   `author` (ForeignKey: User).
*   **FR 3.1.2:** The Author shall be able to create, read, update, and delete posts via the Django Admin interface.
*   **FR 3.1.3:** Only posts with `status='Published'` shall be visible on the public frontend. Drafts are visible only to the Admin.

### FR 3.2 User Authentication
*   **FR 3.2.1:** The system shall utilize Django’s standard `contrib.auth` system.
*   **FR 3.2.2:** Users must be able to register using an Email, Username, and Password.
*   **FR 3.2.3:** Users must be able to log in and log out securely.
*   **FR 3.2.4:** Password resets should be handled via standard Django email workflows (Console backend sufficient for dev; SMTP for prod).

### FR 3.3 Commenting System
*   **FR 3.3.1:** The system shall allow **only Authenticated Users** to submit comments.
*   **FR 3.3.2:** The Comment model must support hierarchy (Nested Replies).
    *   *Architecture Note:* Implementation must utilize `django-mptt` or recursive adjacency lists to manage tree structures efficiently.
*   **FR 3.3.3:** Comments shall be displayed immediately upon submission (No pre-moderation queue required).
*   **FR 3.3.4:** The frontend must visually distinguish between parent comments and nested replies (e.g., via indentation using Tailwind padding classes).

### FR 3.4 Subscription Management
*   **FR 3.4.1 - User Subscription:** Authenticated users shall have a toggle/button in their profile or on the dashboard to "Subscribe" to new post notifications. This updates a boolean flag or relation in the database.
*   **FR 3.4.2 - Guest Subscription:** The system shall provide a standalone form (footer or sidebar) accepting an Email Address.
    *   This data shall be stored in a `NewsletterSubscriber` model.
    *   The form must implement basic validation (Email format check).

### FR 3.5 Frontend Display
*   **FR 3.5.1:** All templates must use **Tailwind CSS** for styling. No custom CSS files should be used unless absolutely necessary for specific overrides.
*   **FR 3.5.2:** **Homepage:** Shall display a paginated list of published posts (Title, Excerpt/First 200 words, Date, Author).
*   **FR 3.5.3:** **Post Detail:** Shall display the full rich-text content, followed by the comment section.
*   **FR 3.5.4:** **responsiveness:** The layout must adapt seamlessly to Mobile, Tablet, and Desktop viewports.

---

## 4. Non-Functional Requirements (NFR)

### NFR 4.1 Security
*   **NFR 4.1.1:** All forms (login, comment, subscription) must utilize Django’s built-in **CSRF protection**.
*   **NFR 4.1.2:** Password storage must use Django’s default hashing algorithms (PBKDF2/Argon2).
*   **NFR 4.1.3:** The application must be configured to prevent XSS attacks by auto-escaping template variables (Django default).
*   **NFR 4.1.4:** `DEBUG` mode must be set to `False` in the production environment.

### NFR 4.2 Performance
*   **NFR 4.2.1:** The database is SQLite; meant for single-writer concurrency. The application code should minimize long-running write transactions.
*   **NFR 4.2.2:** Static assets (CSS/JS) should be collected via `collectstatic` and served efficiently (e.g., via WhiteNoise or Nginx alias).

### NFR 4.3 Maintainability
*   **NFR 4.3.1:** Codebase must adhere to **PEP 8** style guidelines.
*   **NFR 4.3.2:** Project structure must follow Django best practices (App separation: e.g., `core`, `blog`, `users`).
*   **NFR 4.3.3:** Tailwind configuration should be maintained via `tailwind.config.js` to ensure style consistency.

### NFR 4.4 Usability
*   **NFR 4.4.1:** The design must be minimalist. High contrast text, readable typography, and lack of "clutter" are design priorities.
*   **NFR 4.4.2:** The admin interface should be the standard Django Admin, potentially customized slightly (e.g., `list_display` configurations) for easier data scannability.

---

## 5. System Architecture & Data Model (Technical Appendix)

### 5.1 Proposed Database Schema (Simplified)

**1. User (Extension of AbstractUser)**
*   `bio` (Text)
*   `is_subscribed` (Boolean)

**2. Post**
*   `title`, `slug`, `body`, `created_at`, `status`
*   `author` (FK to User)

**3. Comment**
*   `post` (FK to Post)
*   `author` (FK to User)
*   `content` (Text)
*   `parent` (FK to self, null=True - *MPTT handled*)
*   `created_at`

**4. NewsletterSubscriber**
*   `email` (EmailField, Unique)
*   `confirmed` (Boolean, default=True for MVP)
*   `created_at`

### 5.2 Directory Structure
```text
project_root/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── config/             # Project settings
│   ├── settings.py
│   └── urls.py
├── blog/               # App: Posts and Comments
│   ├── models.py
│   ├── views.py
│   └── templates/blog/
├── users/              # App: Auth and Profiles
    └── ...
```

---