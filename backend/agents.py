# agents.py
import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

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

def bmat_router(user_query):
    faq_response = faq_agent(user_query)
    if faq_response:
        return {"agent": "FAQ Agent", "response": faq_response}
    else:
        return {"agent": "Escalation Agent", "response": escalation_agent(user_query)}
