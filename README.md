# Prerequisites

- Git
- Python 3.10+
- Docker & Docker Compose

# Installation & Setup

1. **Clone the repository:**
   git clone https://github.com/your-username/europe-air-quality.git
   cd europe-air-quality

2. **Set up virtual environment & install dependencies:**
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt

3. **Create environment file from template:**
   cp .env.example .env
   # Windows: copy .env.example .env

4. **Start the database:**
   docker compose up -d

# TODO: Finish README.md later.
