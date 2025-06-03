## Chat Application

This project is a real-time chat application built with React and TypeScript. It provides a modern UI for sending and receiving messages, and communicates with an backend API.

## Features

- Real-time chat interface
- Message history display
- User input with send button
- Loading indicators for pending responses
- Error handling for failed requests
- Responsive design

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (v16+ recommended)
- [npm](https://www.npmjs.com/) or [yarn](https://yarnpkg.com/)
- Backend API accessible

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/vcse59/frontend-chat.git
    cd frontend-chat
    ```
2. Install dependencies:
    ```sh
    npm install
    ```

### Running the App Locally

Start the development server:
```sh
npm start
```
The app will be available at [http://localhost:5000](http://localhost:5000).

### Configuration

- The MCP backend API endpoint can be configured in `src/api/mcpClient.ts`.
- Environment variables can be set in a `.env` file at the project root.

### Docker Support

A `Dockerfile` is provided for containerized deployment.

#### Build the Docker Image

```sh
docker build -t frontend-chat .
```

#### Run the App in Docker

```sh
docker run --rm -it -p 5000:5000 frontend-chat
```
Access the app at [http://localhost:5000](http://localhost:5000).

## Usage

- Type your message in the input box and press "Send".
- Messages and responses will appear in the chat window.
- Errors and loading states are displayed as appropriate.

## Troubleshooting

- Ensure the backend API is running and accessible.
- Check browser console and terminal logs for errors.
- For Docker, verify port mappings and network connectivity.

## Resources

- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/)
- [Docker Documentation](https://docs.docker.com/)

## License

This project is licensed under the MIT License.
