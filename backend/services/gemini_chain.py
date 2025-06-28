import os
import google.generativeai as genai
from dotenv import load_dotenv
from services.vector_store import vectorstore

load_dotenv()

system_message = (
    "You are a helpful shop assistant for our product catalog. Answer only about shop products. "
    "Use a friendly and helpful tone. Always use dollar ($) currency format for prices. "
    "If the question is not product-related, say: "
    "'I can only help with product-related queries about our shop catalog.'"
)

def get_relevant_context(query):
    """Get relevant product context from PostgreSQL via Pinecone vector search"""
    try:
        results = vectorstore.similarity_search(query, k=3)  # Get top 3 matches
        if results:
            context_parts = []
            for result in results:
                metadata = result.metadata
                context_parts.append(
                    f"Product: {metadata.get('ProductName', 'N/A')}\n"
                    f"Brand: {metadata.get('ProductBrand', 'N/A')}\n"
                    f"Price: ${metadata.get('Price', 'N/A')}\n"
                    f"Gender: {metadata.get('Gender', 'N/A')}\n"
                    f"Color: {metadata.get('PrimaryColor', 'N/A')}\n"
                    f"Description: {result.page_content}\n"
                )
            return "\n---\n".join(context_parts)
    except Exception as e:
        print(f"Error getting context: {e}")
    
    return "No relevant products found in our catalog."

def generate_response(query, history):
    """Generate response using Google Gemini with PostgreSQL RAG context"""
    try:
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Add current query to history
        history.append(f"User: {query}")
        
        # Get relevant context from PostgreSQL via vector search
        context = get_relevant_context(query)
        
        # Build prompt with system message, history, and context
        prompt = (
            f"{system_message}\n\n"
            f"Previous conversation:\n{chr(10).join(history[-10:])}\n\n"  # Last 10 messages
            f"Product catalog context:\n{context}\n\n"
            f"Please provide a helpful response based on the product information above:"
        )
        
        response = model.generate_content(prompt).text
        history.append(f"Assistant: {response}")
        
        return response, history
        
    except Exception as e:
        error_msg = f"Sorry, I encountered an error: {str(e)}"
        history.append(f"Assistant: {error_msg}")
        return error_msg, history