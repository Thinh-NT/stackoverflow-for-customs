from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync


class NotificationConsumer(WebsocketConsumer):
    http_user = True

    # Function to connect to the websocket
    def connect(self, **kwargs):
        self.user = self.scope['user']
        # Checking if the User is logged in
        if self.user.is_anonymous:
            # Reject the connection
            self.close()
        else:
            # Can access logged in user details by using self.scope.user, Can only be used if AuthMiddlewareStack is used in the routing.py
            # Setting the group name as the pk of the user primary key as it is unique to each user. The group name is used to communicate with the user.
            self.group_name = str(self.user.pk)
            async_to_sync(self.channel_layer.group_add)(
                self.group_name, self.channel_name)
            self.accept()

    def disconnect(self, close_code):
        self.close()

    # Custom Notify Function which can be called from Views or api to send message to the frontend
    def notify(self, event):
        self.send(text_data=json.dumps(event["text"]))
