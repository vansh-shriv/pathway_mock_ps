import re

class EntityExtractor:
    def __init__(self):
        # No spaCy needed - using pure regex
        self.name_patterns = [
            r"(?:my name is|i'm|i am|this is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
            r"^([A-Z][a-z]+\s+[A-Z][a-z]+)",  # First and last name at start
        ]
    
    def extract_entities(self, text):
        """Extract personal information from text using regex"""
        entities = {
            'name': None,
            'email': None,
            'phone': None,
            'financial_info': []
        }
        
        # Email extraction
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            entities['email'] = emails[0]
        
        # Phone extraction (various formats)
        phone_patterns = [
            r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b',
            r'\b([0-9]{10})\b'  # Simple 10-digit
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                if isinstance(phones[0], tuple):
                    entities['phone'] = ''.join(phones[0])
                else:
                    entities['phone'] = phones[0]
                break
        
        # Name extraction using patterns
        for pattern in self.name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                entities['name'] = match.group(1)
                break
        
        # Money amount extraction
        money_pattern = r'\$?\s?(\d+(?:,\d{3})*(?:\.\d{2})?)\s?(?:dollars|USD|\$)?'
        money_matches = re.findall(money_pattern, text)
        for money in money_matches:
            entities['financial_info'].append({
                'type': 'money',
                'value': money
            })
        
        # Financial keywords detection
        financial_keywords = {
            'loan': ['loan', 'borrow', 'mortgage', 'emi'],
            'investment': ['invest', 'stock', 'mutual fund', 'bond', 'shares'],
            'savings': ['save', 'savings', 'deposit', 'fixed deposit'],
            'credit': ['credit card', 'credit score', 'credit limit']
        }
        
        text_lower = text.lower()
        detected_categories = set()
        
        for category, keywords in financial_keywords.items():
            for keyword in keywords:
                if keyword in text_lower and category not in detected_categories:
                    entities['financial_info'].append({
                        'type': 'interest',
                        'category': category,
                        'keyword': keyword
                    })
                    detected_categories.add(category)
                    break
        
        return entities
