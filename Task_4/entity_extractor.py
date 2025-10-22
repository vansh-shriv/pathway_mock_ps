import re
import spacy

class EntityExtractor:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            print("Downloading spaCy model...")
            import os
            os.system("python3 -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
    
    def extract_entities(self, text):
        """Extract personal information from text"""
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
        phone_pattern = r'\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b'
        phones = re.findall(phone_pattern, text)
        if phones:
            entities['phone'] = ''.join(phones[0])
        
        # Name extraction using spaCy
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON" and not entities['name']:
                entities['name'] = ent.text
            elif ent.label_ == "MONEY":
                entities['financial_info'].append({
                    'type': 'money',
                    'value': ent.text
                })
        
        # Financial keywords
        financial_keywords = {
            'loan': ['loan', 'borrow', 'mortgage'],
            'investment': ['invest', 'stock', 'mutual fund', 'bond'],
            'savings': ['save', 'savings', 'deposit'],
            'credit': ['credit card', 'credit score']
        }
        
        text_lower = text.lower()
        for category, keywords in financial_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    entities['financial_info'].append({
                        'type': 'interest',
                        'category': category,
                        'keyword': keyword
                    })
                    break
        
        return entities
