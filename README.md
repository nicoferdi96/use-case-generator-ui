# CrewAI Kickoff UI

A simple Streamlit interface for interacting with the CrewAI Enterprise API.

## Features

- Kickoff CrewAI executions with custom inputs
- Monitor execution status in real-time
- View results when execution completes

## Setup

1. Clone this repository
2. Configure your `.env` file with your CrewAI API credentials:
   ```
   CREWAI_API_URL=https://your-crew-url.crewai.com
   CREWAI_API_TOKEN=your_token_here
   ```
3. Install dependencies using `uv`:
   ```bash
   uv venv
   uv pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run main.py
   ```
2. Open your browser and navigate to the URL provided by Streamlit (typically http://localhost:8501)
3. Fill in the required company information
4. Click "Kickoff Crew" to start the execution
5. The UI will automatically poll for updates until completion

## API Interaction

This app uses the CrewAI Enterprise API to:
- Check API health
- Kickoff new crew executions
- Poll for execution status
- Retrieve results when complete

The required crew inputs are:
- `company_name`: The name of the company
- `company_website`: The URL of the company website
