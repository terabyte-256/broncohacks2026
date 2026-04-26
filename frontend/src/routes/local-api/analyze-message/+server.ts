// frontend/src/routes/local-api/analyze-message/+server.ts
import { json } from "@sveltejs/kit";
import type { RequestHandler } from "./$types";

type RiskLevel = "Low" | "Medium" | "High";

interface MessageAnalysis {
  verdict: string;
  riskLevel: RiskLevel;
  redFlags: string[];
  explanation: string;
  tips: string[];
}

export const POST: RequestHandler = async ({ request }) => {
  try {
    const body = await request.json();
    const message = String(body?.message ?? "").trim();

    if (!message) {
      return json({ message: "Message is required." }, { status: 400 });
    }

    const text = message.toLowerCase();
    const redFlags: string[] = [];

    if (text.includes("urgent")) redFlags.push("Uses urgency to pressure you.");
    if (text.includes("click")) redFlags.push("Asks you to click a link.");
    if (text.includes("verify")) redFlags.push("Requests account verification.");
    if (text.includes("password")) redFlags.push("Mentions passwords or credentials.");
    if (text.includes("login")) redFlags.push("References login activity.");
    if (text.includes("bank")) redFlags.push("Mentions financial information.");
    if (text.includes("immediately")) redFlags.push("Pushes immediate action.");
    if (text.includes("gift card")) redFlags.push("Requests unusual payment method.");
    if (text.includes("wire transfer")) redFlags.push("Mentions wire transfer.");
    if (text.includes("suspended")) redFlags.push("Threatens account suspension.");

    let riskLevel: RiskLevel = "Low";
    if (redFlags.length >= 4) riskLevel = "High";
    else if (redFlags.length >= 2) riskLevel = "Medium";

    const result: MessageAnalysis = {
      verdict:
        riskLevel === "High"
          ? "Likely suspicious"
          : riskLevel === "Medium"
            ? "Potentially suspicious"
            : "No major warning signs detected",
      riskLevel,
      redFlags,
      explanation:
        redFlags.length > 0
          ? "This message contains patterns commonly seen in phishing or scam attempts."
          : "No obvious phishing indicators were detected, though automated checks cannot guarantee safety.",
      tips: [
        "Do not click unknown links.",
        "Verify the sender through an official site or phone number.",
        "Do not share passwords or one-time codes.",
        "Check the real domain before signing in."
      ]
    };

    return json(result);
  } catch (error) {
    console.error("analyze-message failed:", error);
    return json({ message: "Failed to analyze message." }, { status: 500 });
  }
};