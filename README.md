# 🐍 404 Project Not Found — Backend (Django & DRF)

> "Push boundaries. Build with style. Ensure components don’t break under pressure." 🚀
This is the robust, secure, and production-ready backend engine for the 404 Project. Engineered using **Python**, **Django ORM**, and **Django REST Framework (DRF)**, this core manages database persistent states, JWT authentication lifecycles, structured Kanban task matrix manipulation, and binary multi-image annotation processing.

---

## 🌋 The Chronology of Difficulties: Villains Defeated

Building a highly adaptive API ledger using Django means running into performance walls and data format conflicts. Here is how we conquered the villains threatening our server stability:

### 1. The Missing Identity Mapping (The Missing Profile Path)
* **The Villain:** The frontend application initiated profile lookup requests to dynamically load usernames and avatars, resulting in `404 Request Failed` errors due to a missing identity view in our application router[cite: 18].
* **How We Overcame It:** We extended our custom user system by establishing a dedicated `UserProfileView(APIView)` protected by SimpleJWT's strict `IsAuthenticated` permission class. We designed it to read properties directly from our `CustomUser(AbstractUser)` model[cite: 10]. To ensure seamless loading across external frontends, we leveraged `request.build_absolute_uri()` to automatically bind the full local media proxy URLs to the profile picture fields.

### 2. The Absolute Media Path Enigma
* **The Villain:** Uploaded annotation images and user avatars were saving correctly to the database, but when queried via REST endpoints, they returned relative paths (`/media/profiles/...`). This caused the Next.js Image components to fail rendering due to broken image links.
* **How We Overcame It:** By utilizing the **Django REST Framework Documentation**, we customized our serializers and API view responses. We intercepted the query stream and wrapped image fields with Django’s URI builder, ensuring the API always serves fully absolute asset paths (`http://127.0.0.1:8000/media/...`) regardless of the client's deployment host.

### 3. The Date Mismatch Validation Wall
* **The Villain:** Whenever frontend client nodes omitted a calendar date selection, incoming JSON payloads transmitted blank date strings (`""`), causing the backend SQLite layer to throw fatal schema validation errors.
* **How We Overcame It:** We adjusted our custom `CustomUser` and `Task` model schemas, mapping explicit `blank=True, null=True` configurations across non-mandatory text, date, and image properties[cite: 10]. We also configured DRF validators to gracefully handle empty inputs, turning potential server crashes into clean, safe database entries.

---

## ⚙️ Tech Stack & Technical Specifications

* **Runtime Environment:** Python 3.11.x or higher
* **Framework:** Django Web Framework & Django REST Framework (DRF)
* **Authentication:** SimpleJWT (JSON Web Tokens)[cite: 18]
* **Database Engine:** SQLite (Relational Storage Engine using Django ORM)
* **Image Processing:** Pillow (Python Imaging Library)

---

## 🚀 Step-by-Step Installation & Boot Guide

Follow these steps to spin up the Django API backend:

1. **Initialize a Isolated Python Virtual Environment:**
   ```bash
   python -m venv venv

    **Activate the Virtual Environment:**
    * **Windows (CMD/Bash):** venv\Scripts\activate or source venv/Scripts/activate
    * **macOS/Linux:** source venv/bin/activate

2. **Install Core System Dependencies:**
    ```bash
    pip install django djangorestframework django-cors-headers djangorestframework-simplejwt pillow

3. **Synchronize Database Schemas & Run Migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate

4. **Create an Admin Superuser (For Dashboard Management):**
    ```bash
    python manage.py createsuperuser

5. **Ignite the Local Development Server Engine:**
    ```bash
    python manage.py runserver
### The server will successfully bind to: http://127.0.0.1:8000/