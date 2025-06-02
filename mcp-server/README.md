# MCP Server

MCP Server with a list of tools (e.g., arithmetic operations in this repo) to perform tasks.

## List of Tools

- **addition**: Addition of two numbers.
- **subtraction**: Subtraction of two numbers.
- **multiplication**: Multiplication of two numbers.
- **division**: Division of two numbers.

## Usage

### Locally

**Pre-requisite**

- Ensure Python 3.12 is installed

1. Navigate to the project directory:

    ```bash
    cd mcp-server
    ```

2. Create a Python virtual environment:

    ```bash
    python -m venv .venv
    ```

3. Install Poetry in the virtual environment:

    ```bash
    pip install poetry
    ```

4. Install dependencies defined in `pyproject.toml`:

    ```bash
    poetry install
    ```

5. Run the MCP server on port 8080:

    ```bash
    poetry run mcp-server
    ```

### Docker

**Pre-requisite**

- Ensure Docker is installed and running

1. Navigate to the project directory:

    ```bash
    cd $(git rev-parse --show-toplevel)/mcp-server
    ```

2. Build the Docker image:

    ```bash
    docker build -t mcp_server .
    ```

3. Run the Docker image:

    ```bash
    docker run --rm -it -p 8080:8080 mcp_server
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Security

Please report any security vulnerabilities or concerns by opening an issue or contacting the maintainers directly. We encourage responsible disclosure and will address issues promptly.