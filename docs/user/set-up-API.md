# How to Obtain a Gemini API Key
To run GitStory, a Gemini API key will be needed, as GitStory communicates with Gemini to generate narrative summaries for users. Here is how to obtain one of your own, in case you were not able to reach one of the GitStory members (or if you just would like to have one of your own!).

You will need to have cloned this repository, as you will be adding the API key you generate into your local .env copy:
```
git clone https://github.com/vinamra57/gitstory.git
```

## Step 1: Create a Google AI Studio account
Head over to Google AI Studio (https://aistudio.google.com/), and create your account (should be linked to your Gmail account or you may be prompted to sign in using a Gmail account, if not, create your account).
\
\
**Note: for any UW students wanting to use GitStory, you will need to create this API key using a personal Gmail account, as Google AI Studio isn't included in UW Google accounts.**

## Step 2: Create a Gemini API Key 
Click on "Get API Key" (on the lower-left corner), where you will be navigated to create an API key. 
\
\
Click on the "Create API Key" in the top-right corner, where you will be prompted to name the API key (such as "GitStory Gemini API Key" or any name of your choice) and select its designated project. Here, you will want to select the "Create Project" option, where you can create + name your Google Studio project (that will be associated with this API key). 
\
\
Hit "Create" once done, and you will see the new API key pop up on your dashboard. Here's how this should look like (ignore the two API keys in the screenshot below, you should see at least one, the one that you just created).

<img width="3420" height="1644" alt="image" src="https://github.com/user-attachments/assets/9efc1337-1165-4b49-9aaa-fbb732482431" />

## Step 3: Copy Gemini API Key into GitStory
Copy the generated API key from Google AI Studio by clicking on the API key you created (and copying the long string, typically starting with "Alza..."), and paste it in while running GitStory's `key` command, which loads your generated API key into the GitStory project. 
\
\
You may not be able to run this until you head back [here](user-guide.md) and complete uv installation + other requirements, but once you have completed all those steps, you should load your key in using the following command:

```
uv run python3.13 src/gitstory/__main__.py key --key="<YOUR_API_KEY>"
```
**IMPORTANT: YOU MUST RUN THE KEY COMMAND BEFORE RUNNING ANY OTHER COMMANDS IN GITSTORY, otherwise you will recieve many errors.**

# ALL DONE!
You can access the API key anytime again by logging back into Google AI Studio! Please contact the GitStory team for any further clarifications or troubleshooting regarding
obtaining the Gemini API key (or errors occurring when adding your key into GitStory).
