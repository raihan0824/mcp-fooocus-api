# Installation & Testing Guide

## Quick Installation

### Using uv (Recommended)

```bash
# Install directly from GitHub
uv add git+https://github.com/raihan0824/mcp-fooocus-api.git

# Or install from PyPI (when published)
uv add mcp-fooocus-api

# Run with uvx without installing
uvx --from git+https://github.com/raihan0824/mcp-fooocus-api.git mcp-fooocus-api
```

### Using pip

```bash
# Install from GitHub
pip install git+https://github.com/raihan0824/mcp-fooocus-api.git

# Or install from PyPI (when published)
pip install mcp-fooocus-api

# Or install from local development
pip install -e .
```

## Development Setup

### With uv (Recommended)

1. **Clone and set up with uv:**
```bash
git clone https://github.com/raihan0824/mcp-fooocus-api.git
cd mcp-fooocus-api

# Create virtual environment and install dependencies
uv sync --dev

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Set up environment:**
```bash
cp .env.example .env
# Edit .env with your Fooocus API endpoint
```

3. **Test the installation:**
```bash
# Test module import
uv run python -c "import mcp_fooocus_api; print('✓ Package imports successfully')"

# Test server startup (dry run)
uv run python -m mcp_fooocus_api.server --help
```

### With pip

1. **Clone and install in development mode:**
```bash
git clone https://github.com/raihan0824/mcp-fooocus-api.git
cd mcp-fooocus-api
pip install -e ".[dev]"
```

2. **Set up environment:**
```bash
cp .env.example .env
# Edit .env with your Fooocus API endpoint
```

3. **Test the installation:**
```bash
# Test module import
python -c "import mcp_fooocus_api; print('✓ Package imports successfully')"

# Test server startup (dry run)
python -m mcp_fooocus_api.server --help
```

## Running the Server

### Method 1: As MCP Server (Recommended)

Add to your MCP client configuration:

**For GitHub installation:**
```json
{
  "mcpServers": {
    "fooocus": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/raihan0824/mcp-fooocus-api.git", "mcp-fooocus-api"]
    }
  }
}
```

**For PyPI installation:**
```json
{
  "mcpServers": {
    "fooocus": {
      "command": "uvx",
      "args": ["mcp-fooocus-api"]
    }
  }
}
```

### Method 2: Direct Execution

```bash
# With uv (from GitHub)
uvx --from git+https://github.com/raihan0824/mcp-fooocus-api.git mcp-fooocus-api

# With uv (if installed locally)
uv run mcp-fooocus-api

# With pip/python
python -m mcp_fooocus_api.server
```

### Method 3: Entry Point

```bash
# If installed with uv
uv run mcp-fooocus-api

# If installed with pip
mcp-fooocus-api
```

## Testing the API

Once the server is running, you can test it with tools like:

1. **MCP Inspector** (if available)
2. **Direct tool calls** through your MCP client
3. **Manual testing** with the available tools:
   - `generate_image`
   - `list_available_styles` 
   - `get_server_info`

## Troubleshooting

### Common Issues:

1. **Import Error**: 
   - With uv: Make sure you ran `uv sync` or `uv add`
   - With pip: Make sure you installed with `pip install -e .`

2. **Environment Variables**: Ensure `.env` file exists and `FOOOCUS_API_URL` is set

3. **API Connection**: Verify the Fooocus API endpoint is accessible

4. **Dependencies**: 
   - With uv: Run `uv sync` to install all dependencies
   - With pip: Run `pip install -e ".[dev]"` to install with dev dependencies

### Debug Mode:
```bash
# Enable debug logging with uv
export MCP_DEBUG=1
uv run python -m mcp_fooocus_api.server

# Enable debug logging with pip
export MCP_DEBUG=1
python -m mcp_fooocus_api.server
```

## Package Structure

```
mcp-fooocus-api/
├── src/mcp_fooocus_api/
│   ├── __init__.py          # Package initialization
│   ├── __main__.py          # Module entry point
│   └── server.py            # Main server implementation
├── .env.example             # Environment template
├── pyproject.toml           # Package configuration
├── README.md                # Main documentation
├── LICENSE                  # MIT License
└── uv.lock                  # uv lock file (if using uv)
```

## Publishing (for maintainers)

### With uv:
```bash
# Build the package
uv build

# Upload to PyPI
uv publish
```

### With pip:
```bash
# Build the package
python -m build

# Upload to PyPI
python -m twine upload dist/*
``` 