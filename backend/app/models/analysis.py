from dataclasses import dataclass


@dataclass
class AnalysisResult:
    verdict: str
    riskLevel: str
    redFlags: list[str]
    explanation: str
    tips: list[str]

    def to_dict(self):
        return {
            "verdict": self.verdict,
            "riskLevel": self.riskLevel,
            "redFlags": self.redFlags,
            "explanation": self.explanation,
            "tips": self.tips,
        }
