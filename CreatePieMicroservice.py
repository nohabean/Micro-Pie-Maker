import json
import matplotlib.pyplot as plt
import zmq
from io import BytesIO


def create_pie_chart(title, data):
    # The labels and data to be displayed
    labels = list(data.keys())
    sizes = [int(value) for value in data.values()]

    # Create the pie chart
    plt.figure(figsize=(8, 6))  # Can adjust the sizes if needed
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title(title)    # Title is given in the metadata of the JSON

    # Save the plot as a PNG image in memory
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()

    buffer.seek(0)
    return buffer.getvalue()    # return the image data as bytes to be displayed in the client

def main():
    # Initialize Server socket and bind to the desired port
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    print("Pie Chart Microservice started, server is listening for requests...")

    try:
        while True:
            # Receive JSON message from the client (the filename to read)
            message = socket.recv_json()
            print(f"Received request: {message}")

            # When the client is closed, send a stop message to the server to close the server
            if message.get('command') == 'stop':
                print("Stopping Pie Chart Microservice, closing sockets...")
                break

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

            except Exception as e:
                response = {"status": "error", "message": str(e)}
                socket.send_json(response)
    finally:
        socket.close()


if __name__ == "__main__":
    main()
