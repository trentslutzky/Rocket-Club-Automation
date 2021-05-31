import os
import secret
import pgTool
# Use the package we installed
from slack_bolt import App

# Initializes your app with your bot token and signing secret
app = App(
    token=secret.app_token,
    signing_secret=secret.signing_secret
)

@app.event("app_mention")
def test(event,say):
    message_text = event['text']
    message = ''
    if 'hello' in message_text:
        message = message + 'Hello! '
    if 'rclcode' in message_text:
        code = pgTool.get_rcl_code_today()
        message = (message + 
                "Today's Rocket Club Live code is `"+
                code+
                "`. ")
    say(message)

@app.event("app_home_opened")
def update_home_tab(client, event, logger):
  try:
    # views.publish is the method that your app uses to push a view to the Home tab
    client.views_publish(
      # the user that opened your app's app home
      user_id=event["user"],
      # the view object that appears in the app home
      view={
        "type": "home",
        "callback_id": "home_view",

        # body of the view
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*_RocketBot Home Page_*"
            }
          },
          {
            "type": "divider"
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "Under construction..."
            }
          }
        ]
      }
    )
  
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
