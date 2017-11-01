# Mixmax Slash commands

This test project enables Mixmax users to add support for a new Mixmax Slash command called `flight` that returns the
basic data of an upcoming flight, given by its flight code (e.g. `AA123`), using data from FlightAware API.

## How to use it

### On production
1. Open up the Mixmax Developer Dashboard and click `Add Slash Command`.
2. Enter the following inputs:
  - Name: `Get basic data and track a given flight`
  - Command: `flight`
  - Parameter placeholder: `[Flight code (e.g. AA123)]`
  - Command Parameter Suggestions API URL: `https://HEROKU/v1/commands/flight/suggestions/`
  - Command Parameter Resolver API URL: `https://HEROKU/v1/commands/flight/resolver/`
3. Refresh Gmail with Mixmax installed. Click `Compose` and type `/flight` to use this new command

### Locally
1. Git clone `https://github.com/jcpmmx/REPO`
2. Make sure this Django project is set up and then run the development server: `python manage.py runsslserver`
3. Restart Chrome in a special temporary mode so the self-signed HTTPS urls can be loaded. See [here](https://developer.mixmax.com/docs/integration-api-appendix#local-development-error-neterr_insecure_response).
4. Verify it works by visiting `https://localhost:8000/v1/commands/flight/suggestions/?text=sia1` and `https://localhost:8000/v1/commands/flight/resolver/?text=sia1` in your browser. Both should return results.
5. Open up the Mixmax Developer Dashboard and click `Add Slash Command`.
6. Enter the following inputs:
  - Name: `Get basic data and track a given flight`
  - Command: `testflight`
  - Parameter placeholder: `[Flight code (e.g. AA123)]`
  - Command Parameter Suggestions API URL: `https://localhost:8000/v1/commands/flight/suggestions/`
  - Command Parameter Resolver API URL: `https://localhost:8000/v1/commands/flight/resolver/`
7. Refresh Gmail with Mixmax installed. Click `Compose` and type `/testflight` to use this new command

## Notes on implementation
- FlightAware API free tier is limited thus I can't show more useful data like airline name or airport terminal/gate

---

# Feedback
- The resolver of a Slash command should be able to receive an ID from the selected suggestion
- When trying to create a new slash command with empty data, the message prompts says 'Command parameter hints
required': it should say whether 'Command parameter suggestion API URL' or 'Command parameter resolver API URL' (note
the casing I suggest). It's not clear whether all parameters are required or not.)
- The Developer settings should allow user-created slash commands to be editable, or at least to see its parameters for
reference
- API docs related to Slash commands don't explicitly say requests will be done using GET
- For consistency, you should refer to 'suggestions' rather than 'typeahead' when mentioning the Slash commands API
reference (e.g. like the `Tutorial` part of the Slash command API docs or the placeholder when adding a new command)
