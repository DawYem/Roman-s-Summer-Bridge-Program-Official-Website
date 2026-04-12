# Roman’s Summer Bridge Program Web App

A full-stack web application built to manage volunteer activity, user accounts, and administrative operations for the Roman’s Summer Bridge Program.

## Live Demo
[Insert Deployed Link Here]

## Screenshots
<img width="1905" height="966" alt="image" src="https://github.com/user-attachments/assets/5e6a3ec5-e721-4b29-9bbf-7350b5302544" />
<img width="1912" height="968" alt="image" src="https://github.com/user-attachments/assets/d57c9e61-fc08-45e4-9abb-49062d64d134" />
<img width="1912" height="976" alt="image" src="https://github.com/user-attachments/assets/d7f6f244-7f25-4a27-96a6-0a2aa367a574" />
<img width="1907" height="978" alt="image" src="https://github.com/user-attachments/assets/df1e2432-3d3b-4bd9-aee7-aa5e2c328b92" />
<img width="1906" height="977" alt="image" src="https://github.com/user-attachments/assets/82e33e5e-0f8f-4b93-9824-06289187e3b6" />

## Features
- Secure user authentication (signup/login)
- Volunteer dashboard for tracking hours and activity
- Record submission with date, time, and image proof
- Admin dashboard for managing users and roles
- Responsive UI for accessibility across devices

## Tech Stack
- **Frontend:** React  
- **Backend:** Flask (Python)  
- **Database:** SQLite  
- **Styling:** CSS / Bootstrap  
- **Architecture:** RESTful API design  

## Key Highlights
- Built a full-stack system integrating a React frontend with a Flask backend via REST APIs  
- Designed role-based functionality for both volunteers and administrators  
- Implemented file upload handling for proof-based submissions  
- Structured backend logic for scalable data tracking and user management  

## Overview
This platform streamlines operations for the Roman’s Summer Bridge Program by allowing volunteers to log and verify their hours while enabling administrators to monitor participation and manage users efficiently.

## Deploy: Render Backend + Netlify Frontend

### 1) Deploy Backend on Render
1. Push this repo to GitHub.
2. In Render, create a new Web Service from your repo.
3. Render will detect `render.yaml` automatically.
4. Set environment variable `FRONTEND_ORIGIN` to your Netlify site URL (example: `https://your-site.netlify.app`).
5. Deploy and copy your backend URL (example: `https://your-backend.onrender.com`).
6. Verify health endpoint at `/health`.

### 2) Deploy Frontend on Netlify
1. Create a Netlify site from your frontend code.
2. Add an environment variable in Netlify:
	- `VITE_API_BASE_URL` or `REACT_APP_API_BASE_URL` or your frontend equivalent
	- Value: your Render backend URL (example: `https://your-backend.onrender.com`)
3. Update frontend API calls to use that environment variable.
4. Redeploy frontend.

### Important Notes
- This project currently uses SQLite (`users.db`), which is not persistent for production multi-instance scaling.
- For real production use, move to PostgreSQL.
- If you keep cookie-based auth across domains, your frontend requests must include credentials and the backend `FRONTEND_ORIGIN` must exactly match the Netlify domain.

## Future Improvements
- Migrate to PostgreSQL for production-level scalability  
- Integrate cloud storage (AWS S3) for image uploads  
- Add real-time analytics for admin insights  
- Improve UI/UX with modern component libraries  

## Author
Dawit Yemane
