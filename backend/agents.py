# agents.py
import openai

openai.api_key = "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"  # Replace with your API key

def faq_agent(user_query):
    faqs = {
        "what is bmat": "BMAT is a universal AI agent framework for building, managing, and automating multi-agent workflows.",
        "how do i install bmat": "You can install BMAT via pip using: pip install bmat",
    }
    query_lower = user_query.lower()
    for question, answer in faqs.items():
        if question in query_lower:
            return answer
    return None

def escalation_agent(user_query):
    return f"Ticket created for: '{user_query}'. Our support team will get back to you soon."

def openai_agent(user_query):
    """Call OpenAI API for real-time AI response."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are BMAT Helpdesk AI assistant."},
                {"role": "user", "content": user_query}
            ],
            max_tokens=200
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Error with AI service: {e}"

def bmat_router(user_query):
    faq_response = faq_agent(user_query)
    if faq_response:
        return {"agent": "FAQ Agent", "response": faq_response}
    
    # If no FAQ match, use OpenAI agent
    ai_response = openai_agent(user_query)
    if ai_response:
        return {"agent": "AI Agent", "response": ai_response}
    
    return {"agent": "Escalation Agent", "response": escalation_agent(user_query)}
