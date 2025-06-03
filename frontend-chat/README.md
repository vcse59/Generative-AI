## Chat application

This application allows users to send messages to an MCP client and displays the responses in a real-time chat interface. The app leverages React Native for the UI and communicates with the MCP backend over HTTP.

## Running the App with Docker

A `Dockerfile` is provided to run the React Native Metro bundler in a containerized environment.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed.
- React Native development environment set up (Android/iOS emulator, etc.).
- MCP client accessible (locally or remotely).

### Build the Docker Image

From the project root, build the Docker image:

```sh
docker build -t chat-app .
```

### Start the Metro Bundler

Run the Metro bundler in a container, mounting your project directory:

```sh
docker run --rm -it -p 5000:5000 chat-app
```

### Connect Your App

- **Web:** Access the app at [http://localhost:5000](http://localhost:5000) in your browser.


### Troubleshooting

- Check the [React Native Troubleshooting Guide](https://reactnative.dev/docs/troubleshooting).
- Review Docker logs for errors.
- Ensure MCP client is reachable and responding.

### Resources

- [React Native Docs](https://reactnative.dev/)
- [Docker Documentation](https://docs.docker.com/)
- [Metro Bundler](https://facebook.github.io/metro/)
