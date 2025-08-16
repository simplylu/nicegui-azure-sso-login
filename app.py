from msal import ConfidentialClientApplication
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from fastapi import Request
from nicegui import ui, app
import requests
import json
import os

# Load environment variables from a .env file
load_dotenv()


# Define the main page of the application
@ui.page("/")
def index():
    # Check if the user has an access token stored
    if "access_token" in app.storage.user:
        # If the token exists, navigate to the profile page
        ui.navigate.to("/profile")
    else:
        # If no token, display a login button
        ui.button(text="Login with SSO", color="purple", on_click=login)


# Define the login page
@ui.page("/login")
def login():
    # Create a ConfidentialClientApplication instance for authentication
    msal_app = ConfidentialClientApplication(
        client_id=os.getenv("CLIENT_ID"),
        authority=os.getenv("AUTHORITY"),
        client_credential=os.getenv("CLIENT_SECRET")
    )
    # Generate the authorization request URL
    auth_url = msal_app.get_authorization_request_url(scopes=["User.Read"], redirect_uri=os.getenv("REDIRECT_URI"))
    # Redirect the user to the authorization URL
    ui.navigate.to(auth_url)


# Define the logout page
@ui.page("/logout")
def logout():
    # Clear the user's session data
    app.storage.user.clear()

    # Construct the logout URL for Microsoft authentication
    logout_url = f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}/oauth2/v2.0/logout?post_logout_redirect_uri=http://localhost:5000/"
    # Redirect the user to the logout URL
    ui.navigate.to(logout_url)


# Define the token retrieval page
@ui.page("/getToken")
def getToken(request: Request):
    # Get the authorization code from the request query parameters
    code = request.query_params.get("code")
    if not code:
        # Return an error if no code is found
        return "Authorization code not found."

    # Create a ConfidentialClientApplication instance for token acquisition
    msal_app = ConfidentialClientApplication(
        client_id=os.getenv("CLIENT_ID"),
        authority=os.getenv("AUTHORITY"),
        client_credential=os.getenv("CLIENT_SECRET")
    )

    # Acquire the access token using the authorization code
    result = msal_app.acquire_token_by_authorization_code(code, scopes=["User.Read"], redirect_uri=os.getenv("REDIRECT_URI"))

    # Check if the access token was successfully acquired
    if "access_token" in result:
        # Store the access token in the user's session
        app.storage.user["access_token"] = result["access_token"]
        # Redirect the user to the profile page
        ui.navigate.to("/profile")
    else:
        # Return an error if token acquisition fails
        return "Could not acquire token."


# Define the profile page
@ui.page("/profile")
def profile():
    # Check if the user has an access token
    if "access_token" not in app.storage.user:
        # Redirect to the main page if no token is found
        return RedirectResponse("/")

    # Retrieve the access token from the session
    access_token = app.storage.user["access_token"]

    # Set up the headers for the request to the Microsoft Graph API
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Make a request to the Microsoft Graph API to get user information
    user_info_response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)

    # Check if the request was successful
    if user_info_response.status_code == 200:
        user_info = user_info_response.json()  # Parse the JSON response
        # Display the user information in a formatted code block
        ui.code(content=json.dumps(user_info, indent=4), language="json")
        # Add a logout button
        ui.button(icon="logout", text="Logout", color="purple", on_click=logout)
    else:
        # Return an error if user info retrieval fails
        return "Could not retrieve user information."


# Run the application
if __name__ in {"__mp_main__", "__main__"}:
    ui.run(host="0.0.0.0", port=5000, storage_secret=os.urandom(128))
