# StudyBuddy AI

StudyBuddy AI is a Flask web application for the CS4680 AI Assistant Project. A student enters a subject, topic, difficulty, available time, and learning preference. The application sends a structured prompt to a generative AI model and returns a study schedule, explanation, practice questions, answer key, and recommendations.

## Prompt-engineering techniques

1. **Persona pattern:** The system prompt tells the model to act as an experienced college tutor and academic study planner. This creates a consistent, supportive, and appropriately detailed response.
2. **Few-shot prompting:** The user prompt includes an example showing how the schedule should be formatted. This guides the model toward readable, predictable output.
3. **Iterative refinement:** The prompt tells the model to review its draft for realistic timing, appropriate difficulty, organization, and complete answers before returning it.

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   # macOS/Linux
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Copy `.env.example` to `.env`.
6. Put your API key in `.env`.
7. Start the application:

   ```bash
   python app.py
   ```

8. Open `http://127.0.0.1:5000` in a browser.

