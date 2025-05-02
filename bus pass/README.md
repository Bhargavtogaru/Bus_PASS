# Bus_PASS

A comprehensive Bus Pass Management System with e-pass generation and admin dashboard capabilities.

## Features

- User Authentication and Authorization
- E-Pass Generation
- Admin Dashboard
- Pass Status Tracking
- User Management

## Tech Stack

### Backend
- Flask (Python Web Framework)
- SQLAlchemy (ORM)
- MySQL Database

### Frontend
- React.js
- Express.js
- Node.js

## Setup Instructions

1. Clone the repository
```bash
git clone https://github.com/Bhargavtogaru/Bus_PASS.git
```

2. Install Python dependencies
```bash
pip install -r requirements.txt
```

3. Install Node.js dependencies
```bash
npm install
```

4. Set up environment variables in `.env` file
```env
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
```

5. Run the application
```bash
# Start Flask backend
python app.py

# Start Node.js server
npm start

# Start full development environment
npm run dev:full
```

## Project Structure

- `/client` - Frontend React application
- `/templates` - Flask HTML templates
- `/static` - Static assets (CSS, JS)
- `/routes` - API routes
- `/config` - Configuration files

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.