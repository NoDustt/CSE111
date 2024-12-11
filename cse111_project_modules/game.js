// Connect to the WebSocket server
const socket = new WebSocket("ws://localhost:5000");

// Listen for messages from the server
socket.onmessage = (event) => {
    console.log("Message from server:", event.data);
};

// Send a message to the server
socket.onopen = () => {
    console.log("WebSocket connection established!");
    socket.send("Hello, server!");
};

// Handle errors
socket.onerror = (error) => {
    console.error("WebSocket error:", error);
};

// Handle connection closure
socket.onclose = () => {
    console.log("WebSocket connection closed.");
};
