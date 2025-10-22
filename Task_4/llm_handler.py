import ollama

class LLMHandler:
    def __init__(self, model_name="llama3.1:8b"):
        self.model_name = model_name
        self.system_prompt = """You are FinanceBot, an expert AI financial advisor assistant. 
Your role is to help users with financial queries including:
- Banking and savings accounts
- Investment advice (stocks, mutual funds, bonds)
- Loan information (personal, home, car loans)
- Credit cards and credit scores
- Budgeting and financial planning
- Tax basics

Always be helpful, clear, and provide accurate financial information. 
If you're unsure, admit it and suggest consulting a certified financial advisor.
Keep responses concise but informative."""
        
        self.conversation_history = []
    
    def chat(self, user_message):
        """Send message to LLM and get response"""
        try:
            # Add user message to history
            self.conversation_history.append({
                'role': 'user',
                'content': user_message
            })
            
            # Prepare messages with system prompt
            messages = [
                {'role': 'system', 'content': self.system_prompt}
            ] + self.conversation_history
            
            # Get response from Ollama
            response = ollama.chat(
                model=self.model_name,
                messages=messages
            )
            
            assistant_message = response['message']['content']
            
            # Add assistant response to history
            self.conversation_history.append({
                'role': 'assistant',
                'content': assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            return f"Error connecting to LLM: {str(e)}"
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
