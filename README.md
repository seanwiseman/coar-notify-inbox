# coar-notify-inbox

A basic implementation of an LDN inbox intended for COAR Notify developments purposes written in Python using FastAPI.

There is an instance of this inbox running at https://coar-notify-inbox.fly.dev .

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

When you receive a notification, you may want to keep track of the state of the notification. For example, you may want 
to mark a notification as read once it has been processed. To do this, you can use `notification_states` as a seperate 
state manager for your notifications. This is a simple key-value store that allows you to store a `read` state against a 
notification id. **Note this is completely optional, you can use your own state manager if you wish.**


#### To mark a notification as read
````
PATCH /notification_states/{notification_id}
Content-Type: application/json

{
    "read": true
}
````

#### To mark a notification as unread
````
PATCH /notification_states/{notification_id}
Content-Type: application/json

{
    "read": false
}
````

#### To get your unread notifications ids
```
GET http://127.0.0.1:8000/notification_states?read=false
Accept: application/json
```

#### To get your read notifications ids
```
GET http://127.0.0.1:8000/notification_states?read=true
Accept: application/json
```