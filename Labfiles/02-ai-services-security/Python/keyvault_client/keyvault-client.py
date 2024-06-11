from dotenv import load_dotenv
import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential


def main():
    global ai_endpoint
    global cog_key

    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('https://mvti.cognitiveservices.azure.com/')
        key_vault_name = os.getenv('mvti-boveda')
        app_tenant = os.getenv('d1cfbf10-1770-4f47-a9ba-ddafcd908643')
        app_id = os.getenv('d2aa8234-777c-4696-a88a-f9f13686ba38')
        app_password = os.getenv('WdM8Q~TeaAxtvP1UdfLBMVU8d8pigjoEypsbSb-D')

        # Get Azure AI services key from keyvault using the service principal credentials
        key_vault_uri = f"https://{key_vault_name}.vault.azure.net/"
        credential = ClientSecretCredential(app_tenant, app_id, app_password)
        keyvault_client = SecretClient(key_vault_uri, credential)
        secret_key = keyvault_client.get_secret("AI-Services-Key")
        cog_key = secret_key.value

        # Get user input (until they enter "quit")
        userText =''
        while userText.lower() != 'quit':
            userText = input('\nEnter some text ("quit" to stop)\n')
            if userText.lower() != 'quit':
                language = GetLanguage(userText)
                print('Language:', language)

    except Exception as ex:
        print(ex)

def GetLanguage(text):

    # Create client using endpoint and key
    credential = AzureKeyCredential(cog_key)
    client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

    # Call the service to get the detected language
    detectedLanguage = client.detect_language(documents = [text])[0]
    return detectedLanguage.primary_language.name


if __name__ == "__main__":
    main()
