import os
from langchain_openai import OpenAI  # Updated import
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate  # Corrected import
from newsapi import NewsApiClient
from typing import List, Dict

# Load API keys from environment variables for security
openai_api_key = os.getenv('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')  # Use a proper environment variable name
newsapi_key = os.getenv('55c55ec203f2484fa8b0a81caf2e9dcb')  

# Check if API keys are loaded
if not openai_api_key or not newsapi_key:
    raise ValueError("API keys for OpenAI and NewsAPI must be set in environment variables.")

# Initialize OpenAI API
openai = OpenAI(api_key=openai_api_key)

# Initialize NewsAPI
newsapi = NewsApiClient(api_key=newsapi_key)

def create_prompt_template() -> PromptTemplate:
    """Creates a prompt template for summarization."""
    template = """
    You are an AI assistant helping an equity research analyst. Given
    the following query and the provided news article summaries, provide
    an overall summary.
    
    Query: {query}
    Summaries: {summaries}
    """
    return PromptTemplate(template=template, input_variables=['query', 'summaries'])

def get_news_articles(query: str) -> List[Dict]:
    """Fetches relevant news articles using NewsAPI."""
    try:
        response = newsapi.get_everything(q=query, language='en', sort_by='relevancy')
        return response.get('articles', [])
    except Exception as e:
        print(f"Error fetching news articles: {e}")
        return []

def summarize_articles(articles: List[Dict]) -> str:
    """Creates a combined summary from article descriptions."""
    summaries = [article['description'] for article in articles if article.get('description')]
    return ' '.join(summaries) if summaries else "No descriptions available."

def get_summary(query: str) -> str:
    """Retrieves news articles and generates a combined summary."""
    articles = get_news_articles(query)
    if not articles:
        return "No articles found for the given query."
    
    summaries = summarize_articles(articles)
    prompt = create_prompt_template()
    llm_chain = LLMChain(prompt=prompt, llm=openai)
    
    return llm_chain.run({'query': query, 'summaries': summaries})

# Example usage
if __name__ == "__main__":
    query = "latest technology trends"
    summary = get_summary(query)
    print(summary)
