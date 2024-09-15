import spacy
import re

def load_model():
    """
    Load the spaCy NER model.
    """
    return spacy.load("en_core_web_sm")

def redact_text(text, nlp, custom_marker='*', additional_patterns=None):
    """
    Redact sensitive information from the given text using NER and custom patterns.
    
    :param text: The input text to be redacted
    :param nlp: The spaCy NLP model
    :param custom_marker: The character used for redaction (default is '*')
    :param additional_patterns: A dict of additional regex patterns to redact
    :return: The redacted text
    """
    doc = nlp(text)
    redacted_text = text
    
    # Redact named entities
    for ent in reversed(doc.ents):
        if ent.label_ in ["PERSON", "ORG", "GPE", "LOC", "MONEY"]:
            redacted_text = redacted_text[:ent.start_char] + custom_marker * len(ent.text) + redacted_text[ent.end_char:]
    
    # Redact additional patterns
    if additional_patterns:
        for pattern_name, pattern in additional_patterns.items():
            regex = re.compile(pattern)
            redacted_text = regex.sub(lambda m: custom_marker * len(m.group()), redacted_text)
    
    return redacted_text

# Example usage
if __name__ == "__main__":
    # Load the NER model
    nlp = load_model()
    
    sample_text = """
    Hello, my name is John Smith and I work for Acme Corporation.
    My email is john.smith@acme.com and my phone number is (123) 456-7890.
    I live in New York City and my credit card number is 1234-5678-9012-3456.
    My social security number is 123-45-6789 and my passport number is AB1234567.
    """
    
    # Additional patterns to redact
    additional_patterns = {
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "phone": r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        "credit_card": r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
        "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
        "passport": r'\b[A-Z]{1,2}\d{6,9}\b'
    }
    
    redacted_text = redact_text(sample_text, nlp, additional_patterns=additional_patterns)
    
    print("Original text:")
    print(sample_text)
    print("\nRedacted text:")
    print(redacted_text)

# Note: You need to install spaCy and download the English model:
# pip install spacy
# python -m spacy download en_core_web_sm