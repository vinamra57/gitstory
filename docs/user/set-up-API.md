# How to Obtain a Gemini API Key
To run GitStory, a Gemini API key will be needed, as GitStory communicates with Gemini to generate narrative summaries for users. Here is how to obtain one of your own, in case
you were not able to reach one of the GitStory members (or if you just would like to have one of your own!).

You will need to have cloned this repository, as you will be adding the API key you generate into your local .env copy:
```
git clone https://github.com/vinamra57/gitstory.git
```

## Step 1: Create a Google Cloud Console account
Head over to Google Cloud Console (https://console.cloud.google.com/), and create your account (should be linked to your Gmail account, if not, create your account).

## Step 2: Create a Google Cloud Console Project 
Open "Project Picker" (icon on the left side), and start a new project, naming it GitStory (or any name of your choice).

## Step 3: Navigate to your project
Once you enter/select your project (you should have either entered the project already, or select your new project again by going to Project Picker), and navigate to the Navigation Menu.
There, you should see "APIs & Services" - click there.

## Step 4: Enable the API
You should be greeted with a screen where you can select which APIs you would like to enable. Click on "Enable APIs and Services," and search for Gemini API. Select the API
named "Gemini API" (the others are NOT what we use) and enable it (select enable).

## Step 5: Create the API key
Head over to "Credentials page" - here, click "Create credentials" creating a new "API key." Give it a name of your choice, and it is up to you to whether you would like to restrict
the API key or not (restriction shouldn't matter, as long as you have access). Once you are done, hit "Create." 

## Step 6: Finish API key setup
Once you are done, you will (or might) now see a warning to "Configure your OAuth Consent Screen" (as expected). To do this, click on "Configure consent screen" and follow the given prompts (this typically shouldn't take too long, they ask for an "App Name", a support email, etc). 
\
\
**IMPORTANT: MAKE SURE TO SET YOUR AUDIENCE AS EXTERNAL (when setting your consent screen).**

## Step 7: Add API Key to GitStory
Copy the generated API key from Google Cloud Console, and paste it in while running GitStory's `key` command, which loads your generated API key into the GitStory project. You may not be able to run this until you head back [here](setup-guide.md) and complete uv installation + other requirements, but once you have completed all those steps, you should load your key in using the following command:
\
\
**IMPORTANT: YOU MUST RUN THIS COMMAND BEFORE RUNNING ANY OTHER COMMANDS IN GITSTORY, otherwise you will recieve many errors.**

```
uv run python3.13 src/gitstory/__main__.py key key="<YOUR_API_KEY>"
```

# ALL DONE!
You can access the API key anytime again by logging back into Google Cloud Console! Please contact the GitStory team for any further clarifications or troubleshooting regarding
obtaining the Gemini API key (or errors occurring when adding your key into GitStory).
