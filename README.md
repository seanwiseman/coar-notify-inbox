# coar-notify-inbox

## Running the app

### Create a Python virtual environment
```bash
python3 -m venv venv
``` 

### Install dependencies
```bash
make install
```

### Run the application
```bash
make start
```

----

## Using the inbox

### Endpoints

#### GET `/docs`
Returns the OpenAPI documentation for the inbox.

#### OPTIONS `/inbox`
Returns the options meta for the inbox.

#### GET `/inbox`
Returns a list of ids for all notification in the inbox.

#### GET `/inbox/{notification_id}`
Returns a single notification from the inbox.

#### POST `/inbox`
Adds a notification to the inbox.


----

## Optional features

There are a few optional features that have been implemented to extend the functionality of the inbox and provide initial 
solutions for common tasks you may want to perform with the inbox.

### On receive new notification webhook

Once you have an inbox up and running, you will want to process new notifications as they arrive. One way to do this is 
to be constantly polling the inbox for new notifications. This can work but is not ideal as it is inefficient and can 
lead to other issues. A better way is to have the inbox notify you when a new notification is added. 

With this in mind, you can configure a webhook to be called when a new notification is added to the inbox.

#### Configure the webhook

To configure the webhook, you will need to provide the target URL as an environment variable when starting the inbox, either 
inline or in a `.env` file.
e.g.
```bash
ON_RECEIVE_NOTIFICATION_WEBHOOK_URL=https://<some-endpoint>
```
This will cause the inbox to send a POST request to the provided URL with the notification as the JSON body.

### Notification state management

WIP


