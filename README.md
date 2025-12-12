# 🏙️ SoundCity Living

A data visualization platform for Münster's environmental livability, combining air quality and noise pollution data to help residents make informed housing decisions.

## 🌟 Features

- Interactive map of Münster neighborhoods
- Real-time air quality and noise pollution scores
- Customizable weighting system
- Detailed neighborhood profiles
- Responsive design for desktop and mobile

## 🚀 Live Demo

**Frontend:** https://soundcity-living.vercel.app
**API Docs:** https://your-api.railway.app/docs

## 🛠️ Technology Stack

### Backend
- FastAPI
- Python 3.11
- Uvicorn
- Pydantic

### Frontend
- Vue.js 3
- Vite
- Tailwind CSS
- Leaflet.js
- Pinia

## 📦 Installation

### Prerequisites
- Anaconda
- Node.js 18+
- Git

### Backend Setup
```bash
# Create conda environment
conda create -n soundcity python=3.11
conda activate soundcity

# Install dependencies
cd backend
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
# Install dependencies
cd frontend
npm install

# Run development server
npm run dev
```

## 📊 Data Sources

- **Air Quality:** OpenAQ, European Environment Agency
- **Noise Pollution:** EU Environmental Noise Directive, OSM data

## 👥 Team

Developed by [Your Team Name] for [Course Name]

## 📄 License

MIT License

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.