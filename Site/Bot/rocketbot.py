import os
import secret
# Use the package we installed
from slack_bolt import App

# Initializes your app with your bot token and signing secret
app = App(
    token=secret.app_token,
    signing_secret=secret.signing_secret
)

# Add functionality here
# @app.event("app_home_opened") etc
@app.event("")


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
