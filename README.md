# Metadata Studio — Academy-inspired theme

A Streamlit prototype for BDM → PDM metadata management with a minimal warm-white, black, and grey interface inspired by the OpenAI Academy Agents and Workflows course page.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Includes model search, domain/status filters, editable model metadata and attributes, visual BDM/PDM preview, and a simulated conversion log. Data is stored in Streamlit session state and is not persisted. Agent-based conversion requires backend integration.
