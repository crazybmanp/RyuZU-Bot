# RyuZU-Bot
A discord bot built on modularity with cogs.

## Configuration
In order to run, RyuZU needs a settings.json file to be created inside of its directory. Your file should look something like this...
```json
{
  "key": "",
  "startup_extensions": [],
  "owner_username": [],
  "command_string": ""
}
```
You may wish to have more in this file depending on what cogs you are using.

### Key Definitions
* *key*: Your Discord App Bot User Token. This is **required** for the bot to run.
* *startup_extensions*: An array of what cogs you want to use. The strings should match the **exact** way they are in the project.
* *description*: The bot's description. This should be an empty string if you want to leave it blank.
* *owner_usernames*: An array of usernames for the server owner(s). These names should include the discriminator (the # with numbers after it)
* *command_string*: A string that contains what character the bot uses for commands. This is **required** for the bot to do anything.
* *dev_mode*: Optional. Signifies that the bot is in development mode.

Even if you don't plan on using the *owner_usernames* or any extensions, you should include an empty array for those values.
