# How to Obtain a Gemini API Key
To run GitStory, a Gemini API key will be needed and stored in the .env file, as GitStory communicates with Gemini to generate narrative summaries for users. Here is how to obtain a Gemini API Key:

## Step 1: Create a Google Cloud Console account
Head over to [Google Cloud Console](https://console.cloud.google.com/), and create your account (should be linked to your Gmail account, and if not, create a Google Cloud Console account).

## Step 2: Create a Google Cloud Console Project 
Open "Project Picker" (icon on the left side), and start a new project, naming it `GitStory` (or any name of your choice).

## Step 3: Navigate to your project
Once you enter/select your project (you should have either entered the project already, or select your new project again by going to Project Picker), and navigate to the Navigation Menu. There, you should see "APIs & Services" - click there.

## Step 4: Enable the API
You should be greeted with a screen where you can select which APIs you would like to enable. Click on "Enable APIs and Services," and search for Gemini API. Select the API
named "Gemini API" (make sure to NOT select the others) and enable it (select "Enable").

## Step 5: Create the API key
Head over to "Credentials page" - here, click "Create credentials" creating a new "API key." Give it a name of your choice, and it is up to you to whether you would like to restrict the API key or not (restriction shouldn't matter, as long as you have access). Once you are done, hit "Create." 

## Step 6: Finish API key setup
**Copy** the API key that is generated into your local .env file (located in the project root). However, you will now see a warning to "Configure your OAuth Consent Screen" (as expected). To do this, click on "Configure consent screen" and follow the given prompts (this typically shouldn't take too long, they ask for an "App Name", a support email, etc). When setting your audience for the "Consent screen", make sure to **set your audience as External**, as your API key may not work otherwise.\
\
**Important to Note:** DO NOT PUSH YOUR API KEY! - this will make your specific API keys public to everyone, which is not good practice and can lead to the API key being maliciously used.

# All done!
You can access the API key anytime again by logging back into Google Cloud Console! Please contact the GitStory team for any further clarifications or troubleshooting regarding
obtaining the Gemini API key.
