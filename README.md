# Shadow-Messenger
Encoded Device to Device chat

This program is a simple TCP messaging program that allows a user to send and receive messages to/from a target IP address using TCP sockets.

The program starts by importing the required modules - socket, threading, ipaddress, and os. It then prints a welcome message to the console.

The first function defined in the program is send_tcp_message, which takes two arguments - the target IP address and the message to be sent. This function sends the message to the target IP address using TCP sockets. It retries sending the message up to three times in case of any errors. The message is first converted to a hexadecimal representation, then to a binary representation, and finally to a Latin-1 encoded string before being sent over the socket.

The second function defined in the program is listen_tcp, which listens on port 13377 for incoming connections. When a connection is received, the function reads the incoming data and decodes it back into the original message format. The message is then printed to the console and saved in a file called "received_messages.txt". This function runs on a separate thread to allow for concurrent sending and receiving of messages.

The program then starts the listen_tcp function on a separate thread using the threading.Thread class.

The program then prompts the user to enter their username and the IP address of the target machine. If the program finds a saved IP address in the file "ip.txt" that matches the entered username, it uses that IP address instead of prompting the user to enter a new one. The user input is validated to ensure that a valid IP address is entered. If a valid IP address is entered, it is saved in the "ip.txt" file.

Finally, the program enters an infinite loop, prompting the user to enter a message to send to the target machine. The message is sent to the target machine using the send_tcp_message function on a separate thread to allow for concurrent sending and receiving of messages. The program waits for the user to press the Enter key before prompting the user for another message.
