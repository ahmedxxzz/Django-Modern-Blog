# Database Schema Design

**Author:** Lyra, Senior Full Stack Architect  
**Context:** Data persistence layer for the Minimalist Django Blog.  
**Database Engine:** SQLite 3  
**ORM:** Django 5.x

---

## 1. Entity Relationship Overview

The schema is designed to remain normalized while keeping the operational overhead low, suitable for SQLite.

*   **Users (CustomUser):** Central entity. Acts as the **Author** (superuser) or **Subscriber** (authenticated reader).
*   **Posts:** Belong to an Author (User).
*   **Comments:** Belong to a Post and a User. They support a hierarchical structure (Tree) for nested replies.
*   **NewsletterSubscribers:** A standalone entity for public readers who wish to subscribe via email without creating a full account.

### Relationship Map
*   **User (1) $\longleftrightarrow$ (N) Post:** One author can write many posts.
*   **Post (1) $\longleftrightarrow$ (N) Comment:** One post can have many comments.
*   **User (1) $\longleftrightarrow$ (N) Comment:** One user can write many comments.
*   **Comment (1) $\longleftrightarrow$ (N) Comment:** Self-referential relationship for nested replies (Parent/Child).

---

## 2. Detailed Data Models

### 2.1 Custom User Model (`CustomUser`)
*Rationale:* Inherits from `django.contrib.auth.models.AbstractUser`. It encapsulates both the Author and Authenticated Readers. It includes a flag for subscription management as per **FR 3.4.1**.

| Field Name | Data Type (Django ORM) | Constraints / Notes | Purpose |
| :--- | :--- | :--- | :--- |
| `id` | `BigAutoField` | Primary Key, Auto-increment. | Unique Record ID. |
| `username` | `CharField` | Max Length: 150, Unique, Required. | Standard login identifier. |
| `email` | `EmailField` | Unique, Required. | Used for password resets and notifications. |
| `password` | `CharField` | Max Length: 128. | Stores the hashed password string. |
| `is_subscribed` | `BooleanField` | Default: `False`. | **FR 3.4.1**: Tracks if the auth user wants email updates. |
| `bio` | `TextField` | Nullable, Blank: `True`. | Optional profile bio for the Author or Users. |
| `is_staff` | `BooleanField` | Default: `False`. | Determines access to Django Admin (Author role). |
| `is_active` | `BooleanField` | Default: `True`. | Soft deletion flag. |
| `date_joined` | `DateTimeField` | Auto Now Add: `True`. | Audit timestamp. |

### 2.2 Blog Post (`Post`)
*Rationale:* Stores the core content. Implementation must utilize a Rich Text field (e.g., `django-ckeditor`) for the body as per **FR 3.1**.

| Field Name | Data Type (Django ORM) | Constraints / Notes | Purpose |
| :--- | :--- | :--- | :--- |
| `id` | `BigAutoField` | Primary Key, Auto-increment. | Unique Record ID. |
| `title` | `CharField` | Max Length: 200, Unique. | Headline of the article. |
| `slug` | `SlugField` | Max Length: 200, Unique, DB Index. | **FR 3.1**: SEO-friendly URL generated from Title. |
| `author` | `ForeignKey` | Relation: `CustomUser`, On Delete: `CASCADE`. | Links post to the creator. |
| `content` | `RichTextField` | Blank: `False`. (Third-party field). | **FR 3.1**: The HTML body of the post. |
| `status` | `IntegerField` | Choices: `(0, 'Draft'), (1, 'Published')`. Default: `0`. | **FR 3.1**: Controls visibility on the frontend. |
| `created_at` | `DateTimeField` | Auto Now Add: `True`. | Publication timestamp. |
| `updated_at` | `DateTimeField` | Auto Now: `True`. | Modification timestamp. |

### 2.3 Comment (`Comment`)
*Rationale:* Handles user interaction. Utilizes `django-mptt` (or similar tree structure logic) to manage nested replies efficiently without expensive recursive queries in Python.

| Field Name | Data Type (Django ORM) | Constraints / Notes | Purpose |
| :--- | :--- | :--- | :--- |
| `id` | `BigAutoField` | Primary Key, Auto-increment. | Unique Record ID. |
| `post` | `ForeignKey` | Relation: `Post`, On Delete: `CASCADE`, Related Name: `comments`. | Links comment to the specific article. |
| `author` | `ForeignKey` | Relation: `CustomUser`, On Delete: `CASCADE`. | **FR 3.3**: Only auth users can comment. |
| `content` | `TextField` | Max Length: 2000 (Suggested). | The comment text. |
| `parent` | `TreeForeignKey` | Relation: `Self`, Nullable, On Delete: `CASCADE`, Related Name: `children`. | **FR 3.3**: Links a reply to a parent comment. |
| `created_at` | `DateTimeField` | Auto Now Add: `True`. | Sort order for display. |
| `lft` | `IntegerField` | *Managed automatically by MPTT*. | Tree traversal index (Left). |
| `rght` | `IntegerField` | *Managed automatically by MPTT*. | Tree traversal index (Right). |
| `tree_id` | `IntegerField` | *Managed automatically by MPTT*. | Identifies the specific comment tree. |
| `level` | `IntegerField` | *Managed automatically by MPTT*. | Depth level (used for indentation styling). |

### 2.4 Newsletter Subscriber (`NewsletterSubscriber`)
*Rationale:* Fulfills **FR 3.4.2**. Allows public readers (guests) to subscribe without creating a user account. Separating this from `CustomUser` keeps the authentication table clean.

| Field Name | Data Type (Django ORM) | Constraints / Notes | Purpose |
| :--- | :--- | :--- | :--- |
| `id` | `BigAutoField` | Primary Key, Auto-increment. | Unique Record ID. |
| `email` | `EmailField` | Unique, Error Message: "Already subscribed". | **FR 3.4.2**: Contact info for guests. |
| `created_at` | `DateTimeField` | Auto Now Add: `True`. | Tracking when subscription started. |
| `is_active` | `BooleanField` | Default: `True`. | Allows "Unsubscribe" without deleting data (optional). |