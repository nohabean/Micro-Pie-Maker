import matplotlib.pyplot as plt
from io import BytesIO
import zmq


def main():
    # Initialize client socket and connect to the server port
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    # Specify the name of the JSON file to send in the message to the server
    filename = 'data.json'

    try:
        # Send request to the server containing the filename
        message = {'filename': filename}
        socket.send_json(message)

        # Receive the image buffer from the server
        chart_data = socket.recv()

        # Display the pie chart
        display_pie_chart(chart_data)

    finally:
        # On pie chart close, send a "stop" command to the server before closing the socket
        socket.send_json({'command': 'stop'})
        socket.close()


def display_pie_chart(data):
    # Display the pie chart image data as a plot
    image_data = BytesIO(data)
    plt.figure(figsize=(8, 6))  # Adjust figure size as needed
    plt.imshow(plt.imread(image_data))
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    main()