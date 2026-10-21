import os

from flask import Flask, jsonify, render_template, request
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

SYSTEM_PROMPT = """
You are StudyBuddy, an experienced college tutor and academic study planner.
Your job is to create realistic, personalized study material for a student.

Use a supportive but academically accurate tone. Do not invent required
textbook facts. If a topic is ambiguous, state a reasonable assumption.
Organize every answer using the exact sections requested by the user.
Before returning the answer, check that the time allocations add up to the
student's available study time and that every practice question has an answer.
""".strip()


def build_prompt(data):
    return f"""
Create a personalized study session using these student details:

- Subject: {data['subject']}
- Topic: {data['topic']}
- Difficulty: {data['difficulty']}
- Available study time: {data['study_time']}
- Learning preference: {data['learning_style']}

Return the response with these exact headings:

## Personalized Study Schedule
Create a schedule that fits within the available study time.

## Topic Explanation
Explain the topic at the selected difficulty level.

## Important Concepts
List the concepts, formulas, or vocabulary the student should know.

## Practice Questions
Create five questions that increase gradually in difficulty.

## Answer Key With Explanations
Answer all five questions and briefly explain the reasoning.

## Final Study Recommendations
Give three practical recommendations for reviewing this topic.

Use the following example format for the first section:

Example:
- 0-20 minutes: Review the core definitions
- 20-50 minutes: Study the main concepts
- 50-90 minutes: Complete practice questions

Use the Persona pattern by acting as an experienced college tutor.
Use the Few-Shot pattern by following the example format above.
Use iterative refinement internally: review the draft for realistic timing,
appropriate difficulty, clear organization, and complete answers before
returning the final response.
""".strip()


DEMO_RESPONSE = """## Personalized Study Schedule
- 0-20 minutes: Review effective stress, allowable stress, and factor of safety.
- 20-50 minutes: Study the bearing-capacity equation and the meaning of each term.
- 50-85 minutes: Work through two calculation examples.
- 85-100 minutes: Complete the practice questions below.
- 100-120 minutes: Review mistakes and summarize the process in your own words.

## Topic Explanation
Bearing capacity analysis estimates the maximum pressure that soil can support before excessive shear failure occurs. The analysis considers the soil strength, foundation dimensions, embedment depth, unit weight, and groundwater conditions. The calculated ultimate bearing capacity must be reduced using a factor of safety or resistance factor to obtain a safe design value.

## Important Concepts
- Ultimate bearing capacity: The theoretical pressure at failure.
- Allowable bearing pressure: The design pressure after applying a factor of safety.
- Cohesion, c: A measure of apparent soil bonding.
- Friction angle, phi: A measure of frictional resistance in soil.
- Factor of safety: The ratio between ultimate capacity and allowable pressure.

## Practice Questions
1. What is the difference between ultimate and allowable bearing capacity?
2. Why does the friction angle matter for sandy soil?
3. If ultimate capacity is 2400 psf and the factor of safety is 3, what is the allowable pressure?
4. Name two conditions that can reduce bearing capacity.
5. Explain why groundwater may affect a bearing-capacity calculation.

## Answer Key With Explanations
1. Ultimate capacity represents failure pressure, while allowable pressure is reduced for safe design.
2. The friction angle controls the shear resistance produced by particle interlocking and friction.
3. Allowable pressure = 2400/3 = 800 psf.
4. Weak soil and a high groundwater table can reduce capacity; shallow embedment and eccentric loading may also matter.
5. Groundwater changes effective stress and can reduce the soil's effective unit weight, lowering shear resistance.

## Final Study Recommendations
1. Practice identifying the soil parameters before selecting an equation.
2. Keep units consistent between psf, tsf, feet, and inches.
3. Check whether the problem asks for ultimate, allowable, or factored capacity.
"""


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/generate")
def generate():
    data = request.get_json(silent=True) or {}
    required = ["subject", "topic", "difficulty", "study_time", "learning_style"]
    missing = [field for field in required if not str(data.get(field, "")).strip()]

    if missing:
        return jsonify({"error": f"Please complete: {', '.join(missing)}."}), 400

    # This mode makes rehearsals possible without consuming API credits.
    if os.getenv("DEMO_MODE", "false").lower() == "true" or not os.getenv("OPENAI_API_KEY"):
        return jsonify({"answer": DEMO_RESPONSE, "demo_mode": True})

    try:
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            instructions=SYSTEM_PROMPT,
            input=build_prompt(data),
        )
        return jsonify({"answer": response.output_text, "demo_mode": False})
    except Exception as exc:
        app.logger.exception("AI request failed")
        return jsonify({"error": f"The AI request failed: {exc}"}), 502


if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("PORT", "5000")))
