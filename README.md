# MCP Fooocus API

A Model Context Protocol (MCP) server that provides text-to-image generation capabilities through the Fooocus Stable Diffusion API.

## Features

- **Text-to-Image Generation**: Generate high-quality images from text prompts
- **Intelligent Style Selection**: Automatically selects 1-3 appropriate styles based on your prompt
- **Custom Style Override**: Manually specify styles from 300+ available options
- **Multiple Performance Modes**: Choose between Speed, Quality, and Extreme Speed
- **Configurable Aspect Ratios**: Support for various image dimensions
- **Environment-based Configuration**: Easy API endpoint configuration via `.env` file

## Installation

### Using uv (Recommended)

Install directly from GitHub:
```bash
uv add git+https://github.com/raihan0824/mcp-fooocus-api.git
```

Or install from PyPI (when published):
```bash
uv add mcp-fooocus-api
```

Run with uvx:
```bash
uvx --from git+https://github.com/raihan0824/mcp-fooocus-api.git mcp-fooocus-api
```

### Using pip

```bash
pip install git+https://github.com/raihan0824/mcp-fooocus-api.git
```

Or from PyPI (when published):
```bash
pip install mcp-fooocus-api
```

### Development Installation

```bash
# Clone the repository
git clone https://github.com/raihan0824/mcp-fooocus-api.git
cd mcp-fooocus-api

# Install with uv
uv sync --dev

# Or install with pip
pip install -e ".[dev]"
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit the `.env` file to configure your Fooocus API endpoint:
```bash
FOOOCUS_API_URL=http://103.125.100.56:8888/v1/generation/text-to-image
```

## Usage

### Available Tools

The MCP server provides three main tools:

#### 1. `generate_image`
Generate an image using the Fooocus API.

**Parameters:**
- `prompt` (required): Text description of the image to generate
- `performance` (optional): Performance setting - "Speed" (default), "Quality", or "Extreme Speed"
- `custom_styles` (optional): Comma-separated list of custom styles
- `aspect_ratio` (optional): Image dimensions (default: "1024*1024")

**Example:**
```json
{
  "prompt": "A serene landscape with mountains and a lake at sunset",
  "performance": "Quality",
  "aspect_ratio": "1024*1024"
}
```

#### 2. `list_available_styles`
Lists all available styles organized by category.

**Returns:**
- Total number of available styles
- Styles organized by categories (Fooocus, SAI, MRE, Art Styles, etc.)
- Available performance options

#### 3. `get_server_info`
Get information about the server configuration and capabilities.

**Returns:**
- Server version and name
- Configured API endpoint
- Available features
- Performance options

### Style Categories

The server includes 300+ styles organized into categories:

- **Fooocus Styles**: Native Fooocus styles (V2, Enhance, Sharp, etc.)
- **SAI Styles**: Stability AI styles (Photographic, Digital Art, Anime, etc.)
- **Art Styles**: Classical art movements (Renaissance, Impressionist, Cubist, etc.)
- **Photography**: Various photography styles (Film Noir, HDR, Macro, etc.)
- **Game Styles**: Video game-inspired styles (Minecraft, Pokemon, Retro, etc.)
- **Futuristic**: Sci-fi and cyberpunk styles
- **And many more...**

### Intelligent Style Selection

When you don't specify custom styles, the server automatically selects appropriate styles based on your prompt:

- **"renaissance portrait"** → Selects "Artstyle Renaissance"
- **"cyberpunk city"** → Selects "Futuristic Cyberpunk Cityscape"
- **"anime character"** → Selects "SAI Anime"
- **"realistic photo"** → Selects "SAI Photographic"
- **"watercolor painting"** → Selects "Artstyle Watercolor"

## Running the Server

### As an MCP Server

Add to your MCP client configuration:

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

Or if installed from PyPI:
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

### Standalone Server

You can also run the server directly:

```bash
# With uv
uvx --from git+https://github.com/raihan0824/mcp-fooocus-api.git mcp-fooocus-api --port 3000 --host localhost

# Or if installed locally
python -m mcp_fooocus_api.server --port 3000 --host localhost
```

## API Response Format

Successful generation returns:

```json
{
  "success": true,
  "prompt": "Your prompt here",
  "selected_styles": ["Style1", "Style2"],
  "performance": "Speed",
  "aspect_ratio": "1024*1024",
  "result": {
    // Fooocus API response data
  }
}
```

Error responses include:

```json
{
  "success": false,
  "error": "Error description",
  "prompt": "Your prompt here",
  "selected_styles": ["Style1", "Style2"]
}
```

## Requirements

- Python 3.8+
- Access to a Fooocus API endpoint
- Internet connection for API requests

## Dependencies

- `mcp` >= 1.0.0
- `httpx` >= 0.27
- `python-dotenv` >= 1.0.0
- `pydantic` >= 2.7.2, < 3.0.0

## Development

To set up for development:

1. Clone the repository
2. Install dependencies: `pip install -e .`
3. Configure your `.env` file
4. Run the server: `python -m mcp_fooocus_api.server`

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please visit the [GitHub repository](https://github.com/raihan0824/mcp-fooocus-api).
