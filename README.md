# Counterfactual Ramayana Narrative Engine (CRNE)

An autonomous narrative–ethical intelligence that explains Rama’s behavior by narrating situations and demonstrating the dharmic necessity of his actions.

## Logic
The engine follows a strict 6-stage loop for each situation:
1. **Situation Emergence**: Observable facts only.
2. **Ethical Pause**: Explicit pause.
3. **Possible Action Space**: Listing realistic alternatives.
4. **Actual Action**: Rama's decision.
5. **Counterfactual Simulation**: What would happen if he chose otherwise.
6. **Dharma Resolution**: Why the action preserves order.

## Setup

1. **Install Dependencies**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **API Key**:
   - Create a `.env` file in the root directory:
     ```
     GROQ_API_KEY=your_api_key_here
     ```
   - OR enter the key in the Streamlit Sidebar.

3. **Run the Interface**:
   ```bash
   venv\Scripts\streamlit run app.py
   ```

## Structure
- `src/engine.py`: Manages the state machine.
- `src/prompts.py`: strict Prompt templates.
- `src/llm_client.py`: Groq API wrapper.
