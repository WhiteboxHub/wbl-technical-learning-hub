"""Security Guardrails: PII redaction and Prompt Injection detection."""
import re
from typing import Tuple, List

# Common PII Regex Patterns
SSN_REGEX = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
PHONE_REGEX = re.compile(r'\b(?:\+?1[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}\b')
EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')

# Hostile injection signatures
INJECTION_KEYWORDS = [
    "ignore previous instructions",
    "override safety protocol",
    "bypass authorization",
    "system: grant full approval",
    "pretend you are an administrator"
]

class GuardrailsManager:
    """Multi-layer security guardrail ensuring HIPAA compliance and prompt isolation."""
    
    @staticmethod
    def sanitize_pii(text: str) -> Tuple[str, List[str]]:
        """Detects and redacts SSN, phone numbers, and emails."""
        redactions = []
        
        if SSN_REGEX.search(text):
            text = SSN_REGEX.sub("[REDACTED-SSN]", text)
            redactions.append("SSN")
        if PHONE_REGEX.search(text):
            text = PHONE_REGEX.sub("[REDACTED-PHONE]", text)
            redactions.append("PHONE")
        if EMAIL_REGEX.search(text):
            text = EMAIL_REGEX.sub("[REDACTED-EMAIL]", text)
            redactions.append("EMAIL")
            
        return text, redactions

    @staticmethod
    def detect_prompt_injection(text: str) -> Tuple[bool, str]:
        """Detects hostile instruction injection attempts."""
        lower_text = text.lower()
        for kw in INJECTION_KEYWORDS:
            if kw in lower_text:
                return True, f"Prompt injection detected: contains forbidden sequence '{kw}'"
        return False, ""
