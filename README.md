# CS361 Microservice A - Pie Chart Maker



## Running the Program
Before running the program, be sure that there is a JSON config file with the data that is to be displayed in the pie chart. 
To start the program, run the CreatePieMicroservice.py and TestClient.py. 

## Requesting and Receiving Data
### Requesting Data
The CreatePieMicroservice.py opens a server socket that waits for a message from the client using a ZeroMQ communication pipe.
The message should contain the file name of the JSON config file containing the data to be displayed in the pie chart. 
Using the ZeroMQ communication pipe, this is achieved programatically using the following code:

Initialize Server socket and bind to the desired port to connect with the client on.
```
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    print("Pie Chart Microservice started, server is listening for requests...")
```
Receive messages from the client.
```
        while True:
            # Receive JSON message from the client (the filename to read)
            message = socket.recv_json()
            print(f"Received request: {message}")

            # When the client is closed, send a stop message to the server to close the server
            if message.get('command') == 'stop':
                print("Stopping Pie Chart Microservice, closing sockets...")
                break
```
Take the message, parse the JSON file, and create a pie chart by generating the image data to send back to the client to display.
```
            try:
                # Read title and data from the JSON file
                filename = message.get('filename', 'data.json')
                with open(filename, 'r') as file:
                    json_data = json.load(file)
                    metadata = json_data.get('metadata', {})
                    title = metadata.get('title', 'Pie Chart')  # Default title is 'Pie Chart' if not found
                    data = json_data.get('data', {})

                chart_data = create_pie_chart(title, data)  # Creates the pie chart image data
                socket.send(chart_data)  # Send the image buffer data back to the client to display the pie chart
```

### Receiving Data


## Stopping the Microservice
To stop the program from running (and closing the socket connection), close the open pie chart window. This 
will close the client and send a "stop" message to the server. This message will tell the server to close and 
end its process. To re-open the server socket for new messages, the progrm will need to be ran again.

## UML Sequence Diagram

