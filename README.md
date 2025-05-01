🧭 Lost & Found Management System
A full-featured web application to report, track, and manage lost or found items within an organization or community. Users can report items they've lost or found, upload item images, view item details, and manage the item's status. This system ensures that only the person who reported an item can mark it as resolved or unresolved, enhancing data integrity and user trust.

📌 Features
🔍 Report Lost or Found Items

🖼️ Upload Item Images for Easy Identification

🧾 View Item Details with Date, Location, Description

🔐 Only Reporter Can Toggle Status (Resolved/Unresolved)

📨 Flash Messages for Success and Errors

📄 Separate Detail Views for Lost and Found Items

🔒 CSRF Protection & User-Based Authorization

🏠 Clean Navigation and User-Friendly Interface

🛠️ Tech Stack
⚙️ Backend
Python 3.x – Core programming language.

Django – Web framework for backend logic and routing.

SQLite3 – Default database used for local development.

🎨 Frontend
HTML5/CSS3 – Page structure and styling.

Bootstrap 5 – Responsive UI components.

JavaScript (minimal use) – For basic UI interactions if needed.

🔐 Security
Django CSRF Protection – To prevent cross-site request forgery.

User Authentication – Only logged-in users can report or update item status.
