# Fantasy Football Roster Viewer (CMS Project)

## 📋 Project Overview

This project is a **Content Management System (CMS)**-driven fantasy football web application that allows users to view league rosters, leave comments on them, and explore detailed player data. Built using **Flask (Python)** on the backend and **HTML/CSS/JavaScript** on the frontend, it supports multiple user roles, authentication, session management, and responsive design.

## 💡 Motivation

Fantasy football is a huge hobby for many sports fans, but most league apps lack personalized, customizable, and clean roster displays. This project aims to enhance the user experience for viewing and commenting on rosters using real-time data from the **Sleeper API**. The goal was to create an engaging interface where users could explore team performance, view player data, and leave comments — all managed in a secure and organized way.

## ⚙️ Features

- 🔐 **User Authentication** with session-based login (username input stored with PHP or Flask sessions)
- 👥 **Two User Roles**: View-only users and commenters
- 📊 **Live Roster Viewing**: Starters, bench, and taxi squad grouped and styled cleanly
- 💬 **Commenting System**: Users can leave comments on rosters, signed with their session username
- 🌙 **Dark Mode Support** with toggle and persistence via `localStorage`
- 📱 **Responsive Layout** for mobile, tablet, and desktop
- 🔄 **Dynamic Data Integration** with the [Sleeper Fantasy Football API](https://docs.sleeper.com/)
- 🧠 **State Management** using Flask sessions
- 🔧 **CRUD Operations** (comment submission/deletion by role)
- 📁 **CMS-Driven Backend** with custom data management (SQLite, `comments.db`)

## 🛠️ Technologies Used

- **Backend**: Python (Flask), Gunicorn, SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite for comment and player data
- **API**: Sleeper Fantasy Football API
- **Hosting**: Render (Free tier for deployment)

## 🚀 Deployment (on Render)

1. Push your project to GitHub.
2. Create a new Web Service on [https://render.com](https://render.com).
3. Set your **Build Command** to:
   ```bash
   pip install -r requirements.txt
   ```
