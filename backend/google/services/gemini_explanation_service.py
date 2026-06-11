from google.providers.google_providers import GoogleGeminiProvider
from google.schemas.provider_dtos import ExplanationDTO

class GeminiExplanationService:
    def __init__(self):
        self.provider = GoogleGeminiProvider()

    def get_recommendation_explanation(self, recommendation: dict, reasoning: dict, audit: dict) -> ExplanationDTO:
        return self.provider.generate_explanation(recommendation, reasoning, audit)

    def get_travel_narrative(self, route_data: dict, recommendation: dict) -> ExplanationDTO:
        return self.provider.generate_travel_narrative(route_data, recommendation)
