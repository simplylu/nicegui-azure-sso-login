# nicegui-azure-sso-login
Small sample on how to authenticate with an Azure application for a nicegui web application

## Create application in Azure
- Create an Azure account if you don't have one
- Click on App Registrations or click [here](https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade)
Click on `+ New registration`
- Give your new app a name
- Select the preferred account types. I used "Accounts in this organizational directory only (Default Directory only - Single tenant)"
- Enter the redirect URL you've defined in your `app.py` and `.env` file
- Click on `Register`

## Configure environment variables
- Open your newly registered app
- The following variables need to be present in your `.env` file:
    - CLIENT_ID: `Application (client) ID`, can be found in the overview of your app
    - CLIENT_SECRET: Create a new secret under `Manage > Certificates & Secrets` by clicking on  `+ New client secret` and following the required steps. Copy the value of the secret.
    - TENANT_ID: `Directory (tenant) ID`, can be found in the overview of yoru app
    - AUTHORITY: URL + Tenant ID (https://login.microsoftonline.com/\<tenant id\>)
    - REDIRECT_URI: The token endpoint defined in your code (http://localhost:5000/getToken)

## Install requirements
The following libraries are required: fastapi, msal, nicegui, python-dotenv and requests. You can install them by running: `pip3 install -r requirements.txt`

## Run the server
To run the application, simply start it via `python3 app.py`. You can authenticate by clicking on `Login`
