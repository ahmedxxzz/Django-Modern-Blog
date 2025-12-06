# Phase 2: User Interaction & Engagement

**Project:** Minimalist Django Blog Platform
**Version:** 2.0 (Interaction Phase)
**Architect:** Lyra
**Date:** December 03, 2025

---

## 1. Overview

Phase 2 focuses on transforming the static read-only blog into an interactive community. This involves implementing user authentication, a commenting system with nested replies, and a newsletter subscription mechanism.

---

## 2. Authentication System Logic

### 2.1 Registration & Login

- **Objective:** Allow readers to create accounts to comment.
- **Logic:**
  1.  Use Django's built-in `UserCreationForm` (extended for `CustomUser`).
  2.  Views: `LoginView`, `LogoutView`, and a custom `RegisterView`.
  3.  **Templates:** `users/login.html`, `users/register.html`.
  4.  **Redirects:** After login/logout, redirect to `home` or the previous page.

### 2.2 User Profile (Basic)

- **Objective:** Allow users to see their status.
- **Logic:**
  1.  Simple profile page displaying username, email, and "Member since" date.
  2.  (Optional for this phase) Edit profile capability.

---

## 3. Commenting Engine Algorithms

### 3.1 Data Model (Recap)

- **Model:** `Comment` (already implemented in Phase 1).
- **Key Fields:** `post`, `author`, `content`, `parent` (MPTT).

### 3.2 Displaying Comments (Tree Structure)

- **Objective:** Show comments in a nested hierarchy (Parent -> Child -> Grandchild).
- **Algorithm:**
  1.  **Query:** `Comment.objects.filter(post=current_post)`.
  2.  **Ordering:** MPTT handles ordering via `tree_id` and `lft`.
  3.  **Template Recursion:** Use `{% recursetree comments %}` from `mptt_tags` to render the tree efficiently in HTML.

### 3.3 Submitting Comments

- **Objective:** Authenticated users can post a comment or reply.
- **Logic:**
  1.  **Form:** `CommentForm` (ModelForm) with `content` field.
  2.  **View Logic (Post Detail):**
      - Handle POST requests on the `PostDetailView`.
      - Validate form.
      - Set `comment.author = request.user`.
      - Set `comment.post = current_post`.
      - **Reply Logic:** If `parent_id` is present in POST data, set `comment.parent`.
  3.  **Security:** `@login_required` for the submission action.

---

## 4. Subscription Logic

### 4.1 Newsletter (Guest)

- **Objective:** Capture emails from non-logged-in visitors.
- **Logic:**
  1.  **Model:** `NewsletterSubscriber` (already implemented).
  2.  **Form:** Simple form with `email` field.
  3.  **Placement:** Footer or Sidebar on all pages.
  4.  **Handling:** AJAX or standard POST. Check uniqueness (ignore if already subscribed).

### 4.2 User Subscription (Toggle)

- **Objective:** Allow registered users to opt-in/out.
- **Logic:**
  1.  Toggle `request.user.is_subscribed` field.
  2.  Expose this via a button on the User Profile page.

---

## 5. URL Routing Updates

| URL Pattern             | View Logic             | Name          |
| :---------------------- | :--------------------- | :------------ |
| `/register/`            | `RegisterView`         | `register`    |
| `/login/`               | `LoginView`            | `login`       |
| `/logout/`              | `LogoutView`           | `logout`      |
| `/profile/`             | `ProfileView`          | `profile`     |
| `/post/<slug>/comment/` | `add_comment`          | `add_comment` |
| `/subscribe/`           | `subscribe_newsletter` | `subscribe`   |
