# DocEx Frontend

React frontend for the DocEx document extraction application.

## Tech Stack

- React 19
- Vite 7
- ESLint

## Setup

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Configuration

Copy `.env.example` to `.env` and configure:

| Variable       | Description                          | Default |
| -------------- | ------------------------------------ | ------- |
| `VITE_API_URL` | Backend API URL (empty for dev proxy)| -       |

For local development, leave `VITE_API_URL` empty to use the Vite proxy.

For production, set it to your backend URL:
```
VITE_API_URL=https://your-backend.onrender.com
```

## Project Structure

```
src/
├── components/
│   ├── FileUpload.jsx    # Document upload component
│   ├── ResultView.jsx    # Extraction results display
│   └── Toast.jsx         # Notification component
├── services/
│   └── api.js            # Backend API client
├── App.jsx               # Main application
└── main.jsx              # Entry point
```

## Deployment (Render)

1. Create a new Static Site on Render
2. Set build command: `npm install && npm run build`
3. Set publish directory: `dist`
4. Add environment variable: `VITE_API_URL=https://your-backend.onrender.com`
