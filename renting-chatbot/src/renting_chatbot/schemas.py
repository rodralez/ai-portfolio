from typing_extensions import TypedDict

class WelcomeAgentResponse(TypedDict):
    message: str
    onboarding_complete: bool
    client_type: str