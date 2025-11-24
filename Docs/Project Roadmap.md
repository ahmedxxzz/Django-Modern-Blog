# Project Roadmap: Minimalist Django Blog Platform

**Project:** Minimalist Django Blog
**Version:** 1.0
**Manager/Architect:** Lyra
**Date:** November 22, 2025

---

## 1. Defining the Minimum Viable Product (MVP)

The primary objective of the MVP is to validate the **Content Delivery** pipeline. We need to get the platform online so the Author can start publishing immediately, even if community features are not yet active.

**MVP Core Feature Set:**
1.  **Infrastructure Setup:**
    *   Initialize Django Project with SQLite.
    *   Configure Tailwind CSS pipeline (Standalone CLI).
    *   Set up `CustomUser` model (Critical: Must be done *before* the first migration to avoid database conflicts later, even if public registration is disabled initially).
2.  **Content Management (Backend):**
    *   **Post Model:** Title, Slug (auto-generated), Body (Rich Text/CKEditor), Status (Draft/Published), Date.
    *   **Admin Interface:** Fully functional Django Admin for the Author to create, edit, and delete posts.
3.  **Presentation Layer (Frontend):**
    *   **Homepage:** Displays a list of "Published" posts (paginated).
    *   **Post Detail:** Displays the full article content styled with Tailwind typography.
    *   **Responsiveness:** Layout adapts to mobile and desktop.

---

## 2. Project Phases and Scope

To ensure a stable rollout and manageable code complexity, the project is divided into three distinct phases.

### Phase 1: MVP - Core Launch (Low Effort)
**Goal:** Establish the foundation and go live with read-only content.

*   **System Configuration:** Setup Django environment, Git repository, and static file handling.
*   **Database:** Implement `CustomUser` and `Post` models.
*   **Admin Panel:** Integrate `django-ckeditor` (or similar) for writing posts.
*   **Frontend:** Build the `base.html` layout using Tailwind. Create `PostListView` and `PostDetailView`.
*   **Deployment:** Configure Nginx and Gunicorn on a single VPS. Deploy the MVP to production.
*   **Constraint Check:** No public user accounts or comments in this phase.

### Phase 2: User Interaction & Engagement (Medium Effort)
**Goal:** Transform the static site into a community platform.

*   **Authentication System:**
    *   Implement Registration, Login, and Logout views using standard Django forms.
    *   Create a basic "User Profile" page.
*   **Commenting Engine:**
    *   Implement the `Comment` model using `django-mptt` for nested hierarchies.
    *   Create the comment submission form (Authenticated users only).
    *   Render the recursive comment tree on the Post Detail page.
*   **Subscription:**
    *   Add a "Subscribe" toggle for authenticated users.
    *   Build the `NewsletterSubscriber` model and form for guest visitors (email only).

### Phase 3: Refinement & Growth (Medium Effort)
**Goal:** Improve discoverability and performance.

*   **Search & Discovery:**
    *   Implement a basic search bar using Django `Q` lookups (filtering by Title and Body).
    *   Add **Tags/Categories** to the Post model to allow filtering by topic.
*   **Performance Optimization:**
    *   Implement **Fragment Caching** or **Per-View Caching** for the Homepage and Post Details to reduce database hits on SQLite.
*   **SEO & Polish:**
    *   Add dynamic meta tags (OpenGraph/Twitter Cards) for social sharing.
    *   Add an RSS Feed (Django's built-in Syndication Framework).

---

## 3. Project Roadmap Summary

| Phase | Phase Name | Key Deliverables (User Stories) | Technical Focus | Estimated Duration |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **MVP - Core Launch** | • As an **Author**, I can log in to Admin and write rich-text posts.<br>• As a **Reader**, I can view the latest posts on the home page.<br>• As a **Reader**, I can read a full article on a mobile device. | • Django Setup<br>• Tailwind Integration<br>• SQLite Schema (Post/User)<br>• Deployment (Nginx/Gunicorn) | **1 Week** |
| **2** | **Interaction & Engagement** | • As a **Reader**, I can register for an account.<br>• As a **Subscriber**, I can comment on a post.<br>• As a **Subscriber**, I can reply to another comment.<br>• As a **Guest**, I can submit my email for the newsletter. | • `django.contrib.auth`<br>• `django-mptt` (Trees)<br>• Form Validation<br>• Session Management | **1.5 Weeks** |
| **3** | **Refinement & Growth** | • As a **Reader**, I can search for specific keywords.<br>• As a **Reader**, I can click a tag to see related posts.<br>• As an **Admin**, I want the site to load instantly (Caching). | • Django `Q` Objects<br>• Many-to-Many Relations (Tags)<br>• Django Caching Framework<br>• SEO/Meta Tags | **1 Week** |