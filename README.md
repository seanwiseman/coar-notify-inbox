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
