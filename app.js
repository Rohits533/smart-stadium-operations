// Import the Google Gen AI SDK from a light CDN (no heavy npm packages needed!)
import { GoogleGenAI } from "https://esm.run/@google/genai";

// ⚠️ In a production app, you'd secure this API key behind a backend.
// For a fast hackathon prototype, we can use a temporary key or a user prompt.
const GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"; 

const ai = new GoogleGenAI({ apiKey: GEMINI_API_KEY });

// System instructions to prime the AI with live stadium knowledge
const systemInstruction = `
You are the "StadiumPulse AI" Co-Pilot for a smart sports stadium and tournament. 
Your role is to assist venue operators and tournament directors. 

Current Stadium Telemetry context:
- Venue Capacity: 50,000 seats
- Gate A: Highly Congested (92% flow)
- Gate B & C: Low Congestion (20% flow)
- Concession Queue: Average 14-minute wait time (Stand #4 is backlogged)
- Weather: 82°F (28°C), clear skies, slight breeze.

When the user asks you a command or question, act as an operational expert. Provide concise, highly-actionable strategies (e.g., routing traffic to Gate B, suggesting concession discounts to clear lines, drafting public announcement templates). Always keep answers professional, brief, and structured.
`;

export async function askStadiumAI(userPrompt) {
    try {
        const response = await ai.models.generateContent({
            model: 'gemini-2.5-flash', // Light, fast, and incredibly smart model
            contents: userPrompt,
            config: {
                systemInstruction: systemInstruction,
                temperature: 0.7,
            }
        });

        return response.text;
    } catch (error) {
        console.error("Gemini API Error:", error);
        return "⚠️ Failed to connect to Stadium Intelligence. Please verify your Gemini API key in app.js.";
    }
}
