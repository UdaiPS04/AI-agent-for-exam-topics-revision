
Exam Revision AI Agent - Usage

Files:
- exam_agent.py       : The agent implementation.
- memory.json         : (created after first run) stores the last 3 queries.

How to run:
1. Make sure you have Python 3.8+ installed.
2. (Optional) Install OpenAI package if you want to use the real API:
   pip install openai
   Then set your API key:
   export OPENAI_API_KEY="sk-..."
   The agent will attempt to call OpenAI; otherwise it uses a local fallback generator.

3. Run the demo (fallback mode if no API key):
   python3 exam_agent.py

How to use as a CLI:
- Start the script: python3 exam_agent.py
- Type requests like:
  "Give me 5 questions on DBMS normalization"
  "Give me a summary on OS deadlocks"
  "Generate a quiz on DSA arrays"
- Type 'exit' to quit.

Notes:
- The OpenAI call is optional; when used, change the model name as needed.
- memory.json keeps only the last 3 entries.

Author: Generated for Udai Pratap Singh
