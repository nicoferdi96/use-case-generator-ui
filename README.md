# CrewAI Use Case Generator

A Streamlit interface for interacting with the CrewAI Enterprise API with authentication.

## Features

- Secure login using username/password authentication
- Kickoff CrewAI executions with custom inputs
- Monitor execution status in real-time
- View results when execution completes

## Setup

1. Clone this repository
2. Configure Streamlit secrets in `.streamlit/secrets.toml`:

   ```toml
   # API Configuration
   CRW_API_URL = "https://your-crew-url.crewai.com"
   CRW_API_TOKEN = "your_token_here"
   
   # Authentication credentials
   [auth]
   username = "your_username"
   password = "your_password"
   ```
   
   For Streamlit Cloud deployment, add these same secrets in the Streamlit Cloud dashboard.

3. Install dependencies using `uv`:
   ```bash
   uv venv
   uv pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```
2. Open your browser and navigate to the URL provided by Streamlit (typically http://localhost:8501)
3. Log in using the configured username and password
4. Fill in the required company information
5. Click "Kickoff Crew" to start the execution
6. The UI will automatically poll for updates until completion

## API Interaction

This app uses the CrewAI Enterprise API to:
- Check API health
- Kickoff new crew executions
- Poll for execution status
- Retrieve results when complete

The required crew inputs are:
- `company_name`: The name of the company
- `company_website`: The URL of the company website

## Deployment

### Local Development
Update the `.streamlit/secrets.toml` file with your credentials.

### Streamlit Cloud
For Streamlit Cloud deployment:
1. Push your code to GitHub
2. Create a new app on Streamlit Cloud pointing to your repo
3. In the app settings, add the following secrets:
   - `CRW_API_URL`: Your CrewAI API URL
   - `CRW_API_TOKEN`: Your CrewAI API token
   - `auth.username`: Login username
   - `auth.password`: Login password
