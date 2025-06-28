# 🛍️ Shop Assistant RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot for shop assistance using PostgreSQL, Pinecone, and Google Gemini AI.

## 🌟 Features

- **PostgreSQL Database**: Product catalog stored in PostgreSQL (Neon DB)
- **RAG Architecture**: Vector search with Pinecone + Google Gemini AI
- **FastAPI Backend**: RESTful API with SQLAlchemy ORM
- **Streamlit Frontend**: Beautiful UI with chat interface and product catalog
- **Smart Search**: AI-powered product recommendations and queries

## 🏗️ Architecture

```
├── backend/
│   ├── database/          # PostgreSQL models & configuration
│   ├── routes/           # FastAPI endpoints
│   └── services/         # AI services (Gemini, Pinecone)
├── data/                 # Dataset download & insertion scripts
├── embeddings/           # Pinecone vector store sync
├── frontend/            # Alternative Streamlit UI
```

## 🚀 Setup Instructions

### 1. Environment Variables

Create a `.env` file in the project root:

```env
# PostgreSQL (Neon DB)
DATABASE_URL=postgresql://username:password@host/database

# Google AI
GOOGLE_API_KEY=your_google_ai_api_key

# Pinecone
PINECONE_API_KEY=your_pinecone_api_key
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download & Insert Data

```bash
# Download dataset and populate PostgreSQL
cd data
python data_insertion.py
```

### 4. Sync with Pinecone

```bash
# Create vector embeddings and sync with Pinecone
cd embeddings
python sync_pinecone.py
```

### 5. Initialize Database

```bash
# Ensure database tables are created
python init_database.py
```

### 6. Run the Application

#### Option 1: Using the run script
```bash
python run_server.py
```

#### Option 2: Using uvicorn directly
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Launch Frontend

```bash
streamlit run ui.py
```

## 📱 Usage

### Web Interface
- Open http://localhost:8501 for the Streamlit UI
- Browse products in the main area
- Use the sidebar chat for AI-powered assistance

### API Endpoints
- `GET /` - API status
- `GET /products` - List all products
- `POST /chat` - Chat with AI assistant
- `GET /docs` - API documentation

### Example Chat Queries
- "Show me running shoes"
- "What Nike products do you have?"
- "I need shoes for women under ₹10,000"
- "Tell me about Adidas products"
- "What colors are available for sneakers?"

## 🛠️ Database Schema

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    ProductID VARCHAR UNIQUE,
    ProductName VARCHAR,
    ProductBrand VARCHAR,
    Gender VARCHAR,
    Price FLOAT,
    Description TEXT,
    PrimaryColor VARCHAR
);
```

## 🔧 Configuration

### PostgreSQL Connection
- Update `backend/database/config.py` for database settings
- Ensure PostgreSQL connection string is correct in `.env`

### Vector Store
- Pinecone index: `shop-product-catalog`
- Embedding model: `models/embedding-001` (Google)
- Dimension: 768

### AI Model
- Primary: Google Gemini 1.5 Flash
- Embeddings: Google Generative AI Embeddings

## 🐛 Troubleshooting

### Database Issues
```bash
# Check database connection
python init_database.py

# Re-populate data
cd data && python data_insertion.py
```

### Vector Store Issues
```bash
# Re-sync with Pinecone
cd embeddings && python sync_pinecone.py
```

### API Issues
```bash
# Check API status
curl http://localhost:8000/health

# View API docs
open http://localhost:8000/docs
```

## 📊 Data Source

Dataset: [Shop Product Catalog](https://www.kaggle.com/datasets/supratimnag06/shop-product-catalog) from Kaggle

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Kaggle for the product dataset
- Google AI for Gemini and embedding models
- Pinecone for vector search capabilities
- FastAPI and Streamlit for the web framework
