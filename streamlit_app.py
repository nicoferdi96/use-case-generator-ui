import os
import time
import json
import requests
import streamlit as st
import hmac

# Set page configuration
st.set_page_config(page_title="CrewAI Use Case Generator", page_icon="🤖", layout="wide")

# Authentication function
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["username"], st.secrets["auth"]["username"]) and \
           hmac.compare_digest(st.session_state["password"], st.secrets["auth"]["password"]):
            st.session_state["password_correct"] = True
            # Delete password from session state
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False
            st.error("😕 Username or password incorrect")

    # Return True if the password is validated
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password
    st.title("CrewAI Use Case Generator Login")
    
    # Display login form
    with st.form("login_form"):
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        st.form_submit_button("Login", on_click=password_entered)
    
    return False

# Check if the user is authenticated
if not check_password():
    st.stop()  # Stop execution if authentication failed

# If we get here, the user is authenticated
API_URL = st.secrets["CRW_API_URL"]
API_TOKEN = st.secrets["CRW_API_TOKEN"]

# Main app title
st.title("CrewAI Use Case Generator")

# Function to make authenticated API requests
def api_request(endpoint, method="GET", data=None):
    """Make an authenticated request to the CrewAI API"""
    url = f"{API_URL}/{endpoint}".rstrip("/")
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {str(e)}")
        return None

# Check API health
def check_api_health():
    """Check if the CrewAI API is healthy using the status endpoint"""
    try:
        # First try checking status endpoint
        url = f"{API_URL}/status".rstrip("/")
        response = requests.get(url, headers={"Authorization": f"Bearer {API_TOKEN}"})
        
        # If status endpoint returns any response (even error), API is likely running
        if response.status_code < 500:
            return True
            
        # If status fails, try root endpoint as fallback
        root_response = requests.get(API_URL, headers={"Authorization": f"Bearer {API_TOKEN}"})
        return root_response.status_code < 500
    except:
        # If connection completely fails, API is not available
        return False

# Sidebar content
with st.sidebar:
    st.subheader("API Status")
    
    if check_api_health():
        st.success("✅ API is connected and healthy")
    else:
        st.error("❌ API is not available")
        st.info("Please check your API configuration")
    
    st.divider()
    st.subheader("About")
    st.markdown(":rainbow[This UI allows you to kickoff your Crew!]")
    
    # Add logout button
    st.divider()
    if st.button("Logout"):
        # Reset authentication status
        st.session_state["password_correct"] = False
        st.experimental_rerun()

# Input form
st.subheader("Crew Inputs")

company_name = st.text_input("Company Name", placeholder="e.g., Acme Corporation")
company_website = st.text_input("Company Website", placeholder="e.g., https://acme.com")

# Kickoff button
if st.button("Kickoff Crew", type="primary", disabled=not (company_name and company_website)):
    with st.spinner("Kicking off crew..."):
        # Prepare input data
        input_data = {
            "inputs": {
                "company_name": company_name,
                "company_website": company_website
            }
        }
        
        # Make kickoff request
        kickoff_response = api_request("kickoff", method="POST", data=input_data)
        
        if kickoff_response and "kickoff_id" in kickoff_response:
            kickoff_id = kickoff_response["kickoff_id"]
            st.success(f"Crew kicked off successfully! Kickoff ID: {kickoff_id}")
            
            # Create a placeholder for status updates
            status_container = st.empty()
            result_container = st.empty()
            
            # Poll for status until complete
            complete = False
            attempts = 0
            max_attempts = 120  # Limit polling to prevent infinite loops
            
            while not complete and attempts < max_attempts:
                status_data = api_request(f"status/{kickoff_id}")
                
                if status_data:
                    status_container.info(f"State: {status_data.get('state', 'null')}")
                    
                    # Check if execution is complete
                    if status_data.get('state') == "SUCCESS":
                        complete = True
                        result_container.success("Execution complete!")
                        
                        # Display the response directly as markdown
                        st.subheader("Crew Response")
                        
                        # Get the result as string
                        result_str = status_data.get('result', '')
                        
                        # Display the result directly as markdown
                        response_container = st.container()
                        response_container.markdown(result_str)
                        
                        break
                    
                    # If still running, wait and try again
                    time.sleep(10)
                else:
                    status_container.error("Failed to retrieve status")
                    break
                
                attempts += 1
            
            # Handle execution timeout
            if attempts >= max_attempts and not complete:
                status_container.warning("Execution is taking longer than expected.")
                st.info(f"You can manually check the status using ID: {kickoff_id}")
        else:
            st.error("Failed to kickoff crew")

# Instructions
st.divider()
st.subheader("Instructions")
st.markdown("""
1. Enter the required inputs (Company Name and Website)
2. Click "Kickoff Crew" to start the execution
3. The system will automatically poll for updates until completion
4. Once complete, results will be displayed below
""")
