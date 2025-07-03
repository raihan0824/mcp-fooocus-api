#!/usr/bin/env python3
"""
MCP server for Fooocus Stable Diffusion API.

This server provides text-to-image generation capabilities through the Fooocus API.
"""

import os
import asyncio
from typing import Any, List, Optional
from dotenv import load_dotenv
import httpx
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Configuration
FOOOCUS_API_URL = os.getenv("FOOOCUS_API_URL", "http://127.0.0.1:8888/v1/generation/text-to-image")

# Performance options
PERFORMANCE_OPTIONS = ["Speed", "Quality", "Extreme Speed"]

# Available styles
AVAILABLE_STYLES = [
    "Fooocus V2",
    "Random Style",
    "Fooocus Enhance",
    "Fooocus Semi Realistic",
    "Fooocus Sharp",
    "Fooocus Masterpiece",
    "Fooocus Photograph",
    "Fooocus Negative",
    "Fooocus Cinematic",
    "Fooocus Pony",
    "SAI 3D Model",
    "SAI Analog Film",
    "SAI Anime",
    "SAI Cinematic",
    "SAI Comic Book",
    "SAI Craft Clay",
    "SAI Digital Art",
    "SAI Enhance",
    "SAI Fantasy Art",
    "SAI Isometric",
    "SAI Line Art",
    "SAI Lowpoly",
    "SAI Neonpunk",
    "SAI Origami",
    "SAI Photographic",
    "SAI Pixel Art",
    "SAI Texture",
    "MRE Cinematic Dynamic",
    "MRE Spontaneous Picture",
    "MRE Artistic Vision",
    "MRE Dark Dream",
    "MRE Gloomy Art",
    "MRE Bad Dream",
    "MRE Underground",
    "MRE Surreal Painting",
    "MRE Dynamic Illustration",
    "MRE Undead Art",
    "MRE Elemental Art",
    "MRE Space Art",
    "MRE Ancient Illustration",
    "MRE Brave Art",
    "MRE Heroic Fantasy",
    "MRE Dark Cyberpunk",
    "MRE Lyrical Geometry",
    "MRE Sumi E Symbolic",
    "MRE Sumi E Detailed",
    "MRE Manga",
    "MRE Anime",
    "MRE Comic",
    "Ads Advertising",
    "Ads Automotive",
    "Ads Corporate",
    "Ads Fashion Editorial",
    "Ads Food Photography",
    "Ads Gourmet Food Photography",
    "Ads Luxury",
    "Ads Real Estate",
    "Ads Retail",
    "Artstyle Abstract",
    "Artstyle Abstract Expressionism",
    "Artstyle Art Deco",
    "Artstyle Art Nouveau",
    "Artstyle Constructivist",
    "Artstyle Cubist",
    "Artstyle Expressionist",
    "Artstyle Graffiti",
    "Artstyle Hyperrealism",
    "Artstyle Impressionist",
    "Artstyle Pointillism",
    "Artstyle Pop Art",
    "Artstyle Psychedelic",
    "Artstyle Renaissance",
    "Artstyle Steampunk",
    "Artstyle Surrealist",
    "Artstyle Typography",
    "Artstyle Watercolor",
    "Futuristic Biomechanical",
    "Futuristic Biomechanical Cyberpunk",
    "Futuristic Cybernetic",
    "Futuristic Cybernetic Robot",
    "Futuristic Cyberpunk Cityscape",
    "Futuristic Futuristic",
    "Futuristic Retro Cyberpunk",
    "Futuristic Retro Futurism",
    "Futuristic Sci Fi",
    "Futuristic Vaporwave",
    "Game Bubble Bobble",
    "Game Cyberpunk Game",
    "Game Fighting Game",
    "Game Gta",
    "Game Mario",
    "Game Minecraft",
    "Game Pokemon",
    "Game Retro Arcade",
    "Game Retro Game",
    "Game Rpg Fantasy Game",
    "Game Strategy Game",
    "Game Streetfighter",
    "Game Zelda",
    "Misc Architectural",
    "Misc Disco",
    "Misc Dreamscape",
    "Misc Dystopian",
    "Misc Fairy Tale",
    "Misc Gothic",
    "Misc Grunge",
    "Misc Horror",
    "Misc Kawaii",
    "Misc Lovecraftian",
    "Misc Macabre",
    "Misc Manga",
    "Misc Metropolis",
    "Misc Minimalist",
    "Misc Monochrome",
    "Misc Nautical",
    "Misc Space",
    "Misc Stained Glass",
    "Misc Techwear Fashion",
    "Misc Tribal",
    "Misc Zentangle",
    "Papercraft Collage",
    "Papercraft Flat Papercut",
    "Papercraft Kirigami",
    "Papercraft Paper Mache",
    "Papercraft Paper Quilling",
    "Papercraft Papercut Collage",
    "Papercraft Papercut Shadow Box",
    "Papercraft Stacked Papercut",
    "Papercraft Thick Layered Papercut",
    "Photo Alien",
    "Photo Film Noir",
    "Photo Glamour",
    "Photo Hdr",
    "Photo Iphone Photographic",
    "Photo Long Exposure",
    "Photo Neon Noir",
    "Photo Silhouette",
    "Photo Tilt Shift",
    "Cinematic Diva",
    "Abstract Expressionism",
    "Academia",
    "Action Figure",
    "Adorable 3D Character",
    "Adorable Kawaii",
    "Art Deco",
    "Art Nouveau",
    "Astral Aura",
    "Avant Garde",
    "Baroque",
    "Bauhaus Style Poster",
    "Blueprint Schematic Drawing",
    "Caricature",
    "Cel Shaded Art",
    "Character Design Sheet",
    "Classicism Art",
    "Color Field Painting",
    "Colored Pencil Art",
    "Conceptual Art",
    "Constructivism",
    "Cubism",
    "Dadaism",
    "Dark Fantasy",
    "Dark Moody Atmosphere",
    "Dmt Art Style",
    "Doodle Art",
    "Double Exposure",
    "Dripping Paint Splatter Art",
    "Expressionism",
    "Faded Polaroid Photo",
    "Fauvism",
    "Flat 2d Art",
    "Fortnite Art Style",
    "Futurism",
    "Glitchcore",
    "Glo Fi",
    "Googie Art Style",
    "Graffiti Art",
    "Harlem Renaissance Art",
    "High Fashion",
    "Idyllic",
    "Impressionism",
    "Infographic Drawing",
    "Ink Dripping Drawing",
    "Japanese Ink Drawing",
    "Knolling Photography",
    "Light Cheery Atmosphere",
    "Logo Design",
    "Luxurious Elegance",
    "Macro Photography",
    "Mandola Art",
    "Marker Drawing",
    "Medievalism",
    "Minimalism",
    "Neo Baroque",
    "Neo Byzantine",
    "Neo Futurism",
    "Neo Impressionism",
    "Neo Rococo",
    "Neoclassicism",
    "Op Art",
    "Ornate And Intricate",
    "Pencil Sketch Drawing",
    "Pop Art 2",
    "Rococo",
    "Silhouette Art",
    "Simple Vector Art",
    "Sketchup",
    "Steampunk 2",
    "Surrealism",
    "Suprematism",
    "Terragen",
    "Tranquil Relaxing Atmosphere",
    "Sticker Designs",
    "Vibrant Rim Light",
    "Volumetric Lighting",
    "Watercolor 2",
    "Whimsical And Playful",
    "Mk Chromolithography",
    "Mk Cross Processing Print",
    "Mk Dufaycolor Photograph",
    "Mk Herbarium",
    "Mk Punk Collage",
    "Mk Mosaic",
    "Mk Van Gogh",
    "Mk Coloring Book",
    "Mk Singer Sargent",
    "Mk Pollock",
    "Mk Basquiat",
    "Mk Andy Warhol",
    "Mk Halftone Print",
    "Mk Gond Painting",
    "Mk Albumen Print",
    "Mk Aquatint Print",
    "Mk Anthotype Print",
    "Mk Inuit Carving",
    "Mk Bromoil Print",
    "Mk Calotype Print",
    "Mk Color Sketchnote",
    "Mk Cibulak Porcelain",
    "Mk Alcohol Ink Art",
    "Mk One Line Art",
    "Mk Blacklight Paint",
    "Mk Carnival Glass",
    "Mk Cyanotype Print",
    "Mk Cross Stitching",
    "Mk Encaustic Paint",
    "Mk Embroidery",
    "Mk Gyotaku",
    "Mk Luminogram",
    "Mk Lite Brite Art",
    "Mk Mokume Gane",
    "Pebble Art",
    "Mk Palekh",
    "Mk Suminagashi",
    "Mk Scrimshaw",
    "Mk Shibori",
    "Mk Vitreous Enamel",
    "Mk Ukiyo E",
    "Mk Vintage Airline Poster",
    "Mk Vintage Travel Poster",
    "Mk Bauhaus Style",
    "Mk Afrofuturism",
    "Mk Atompunk",
    "Mk Constructivism",
    "Mk Chicano Art",
    "Mk De Stijl",
    "Mk Dayak Art",
    "Mk Fayum Portrait",
    "Mk Illuminated Manuscript",
    "Mk Kalighat Painting",
    "Mk Madhubani Painting",
    "Mk Pictorialism",
    "Mk Pichwai Painting",
    "Mk Patachitra Painting",
    "Mk Samoan Art Inspired",
    "Mk Tlingit Art",
    "Mk Adnate Style",
    "Mk Ron English Style",
    "Mk Shepard Fairey Style"
]

# Create the MCP server
mcp = FastMCP("Fooocus API")


def select_styles_for_prompt(prompt: str) -> List[str]:
    """
    Intelligently select 1-3 styles based on the prompt content.
    
    Args:
        prompt: The user's text prompt for image generation
        
    Returns:
        List of selected style names (1-3 styles)
    """
    prompt_lower = prompt.lower()
    selected_styles = []
    
    # Art movement keywords
    if any(word in prompt_lower for word in ["abstract", "modern art"]):
        selected_styles.append("Artstyle Abstract")
    elif any(word in prompt_lower for word in ["renaissance", "classical"]):
        selected_styles.append("Artstyle Renaissance")
    elif any(word in prompt_lower for word in ["impressionist", "monet", "renoir"]):
        selected_styles.append("Artstyle Impressionist")
    elif any(word in prompt_lower for word in ["cubist", "picasso"]):
        selected_styles.append("Artstyle Cubist")
    elif any(word in prompt_lower for word in ["pop art", "warhol"]):
        selected_styles.append("Artstyle Pop Art")
    elif any(word in prompt_lower for word in ["watercolor", "painting"]):
        selected_styles.append("Artstyle Watercolor")
    
    # Photography styles
    if any(word in prompt_lower for word in ["photo", "photograph", "realistic", "portrait"]):
        selected_styles.append("SAI Photographic")
    elif any(word in prompt_lower for word in ["noir", "black and white", "dramatic"]):
        selected_styles.append("Photo Film Noir")
    elif any(word in prompt_lower for word in ["hdr", "high dynamic range"]):
        selected_styles.append("Photo Hdr")
    elif any(word in prompt_lower for word in ["long exposure", "motion blur"]):
        selected_styles.append("Photo Long Exposure")
    elif any(word in prompt_lower for word in ["macro", "close up"]):
        selected_styles.append("Macro Photography")
    
    # Digital art styles
    if any(word in prompt_lower for word in ["digital art", "digital", "cg"]):
        selected_styles.append("SAI Digital Art")
    elif any(word in prompt_lower for word in ["pixel art", "8bit", "16bit"]):
        selected_styles.append("SAI Pixel Art")
    elif any(word in prompt_lower for word in ["3d model", "3d render"]):
        selected_styles.append("SAI 3D Model")
    elif any(word in prompt_lower for word in ["line art", "sketch"]):
        selected_styles.append("SAI Line Art")
    elif any(word in prompt_lower for word in ["lowpoly", "low poly"]):
        selected_styles.append("SAI Lowpoly")
    
    # Anime/Manga styles
    if any(word in prompt_lower for word in ["anime", "manga", "japanese"]):
        if "manga" in prompt_lower:
            selected_styles.append("MRE Manga")
        else:
            selected_styles.append("SAI Anime")
    
    # Cinematic styles
    if any(word in prompt_lower for word in ["cinematic", "movie", "film"]):
        selected_styles.append("SAI Cinematic")
    elif any(word in prompt_lower for word in ["dramatic", "epic"]):
        selected_styles.append("MRE Cinematic Dynamic")
    
    # Fantasy/Sci-fi styles
    if any(word in prompt_lower for word in ["fantasy", "magical", "wizard", "dragon"]):
        selected_styles.append("SAI Fantasy Art")
    elif any(word in prompt_lower for word in ["cyberpunk", "futuristic", "neon"]):
        selected_styles.append("Futuristic Cyberpunk Cityscape")
    elif any(word in prompt_lower for word in ["space", "alien", "galaxy"]):
        selected_styles.append("MRE Space Art")
    elif any(word in prompt_lower for word in ["steampunk", "victorian", "gears"]):
        selected_styles.append("Artstyle Steampunk")
    
    # Horror/Dark themes
    if any(word in prompt_lower for word in ["horror", "scary", "dark", "nightmare"]):
        selected_styles.append("MRE Dark Dream")
    elif any(word in prompt_lower for word in ["gothic", "cathedral"]):
        selected_styles.append("Misc Gothic")
    
    # Game styles
    if any(word in prompt_lower for word in ["game", "gaming", "video game"]):
        if "minecraft" in prompt_lower:
            selected_styles.append("Game Minecraft")
        elif "pokemon" in prompt_lower:
            selected_styles.append("Game Pokemon")
        elif "retro" in prompt_lower:
            selected_styles.append("Game Retro Game")
        else:
            selected_styles.append("Game Rpg Fantasy Game")
    
    # Advertising/Commercial
    if any(word in prompt_lower for word in ["advertisement", "commercial", "product"]):
        if "food" in prompt_lower:
            selected_styles.append("Ads Food Photography")
        elif "luxury" in prompt_lower:
            selected_styles.append("Ads Luxury")
        elif "automotive" in prompt_lower or "car" in prompt_lower:
            selected_styles.append("Ads Automotive")
        else:
            selected_styles.append("Ads Advertising")
    
    # Papercraft
    if any(word in prompt_lower for word in ["paper", "origami", "papercraft"]):
        if "origami" in prompt_lower:
            selected_styles.append("SAI Origami")
        else:
            selected_styles.append("Papercraft Collage")
    
    # Minimalist/Clean
    if any(word in prompt_lower for word in ["minimal", "simple", "clean"]):
        selected_styles.append("Misc Minimalist")
    
    # If no specific styles were selected, use default enhance style
    if not selected_styles:
        selected_styles.append("Fooocus Enhance")
    
    # Limit to maximum 3 styles and remove duplicates
    selected_styles = list(dict.fromkeys(selected_styles))[:3]
    
    return selected_styles


@mcp.tool()
async def generate_image(
    prompt: str,
    performance: str = "Speed",
    custom_styles: Optional[str] = None,
    aspect_ratio: str = "1024*1024"
) -> dict[str, Any]:
    """
    Generate an image using Fooocus Stable Diffusion API.
    
    Args:
        prompt: Text description of the image to generate
        performance: Performance setting (Speed, Quality, Extreme Speed)
        custom_styles: Comma-separated list of custom styles (optional, will auto-select if not provided)
        aspect_ratio: Image aspect ratio (default: 1024*1024)
    
    Returns:
        Dictionary containing generation result with image URLs
    """
    # Validate performance setting
    if performance not in PERFORMANCE_OPTIONS:
        performance = "Speed"
    
    # Select styles
    if custom_styles:
        # Parse custom styles from comma-separated string
        styles = [style.strip() for style in custom_styles.split(",")]
        # Validate that all styles are in the available list
        valid_styles = [style for style in styles if style in AVAILABLE_STYLES]
        if not valid_styles:
            styles = select_styles_for_prompt(prompt)
        else:
            styles = valid_styles[:3]  # Limit to 3 styles
    else:
        styles = select_styles_for_prompt(prompt)
    
    # Prepare API request
    params = {
        "prompt": prompt,
        "performance_selection": performance,
        "style_selections": styles,
        "async_process": False,
        "require_base64": False,
        "aspect_ratios_selection": aspect_ratio
    }
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(FOOOCUS_API_URL, json=params)
            response.raise_for_status()
            
            result = response.json()
            
            return {
                "success": True,
                "prompt": prompt,
                "selected_styles": styles,
                "performance": performance,
                "aspect_ratio": aspect_ratio,
                "result": result
            }
            
    except httpx.TimeoutException:
        return {
            "success": False,
            "error": "Request timed out. Image generation took too long.",
            "prompt": prompt,
            "selected_styles": styles
        }
    except httpx.HTTPStatusError as e:
        return {
            "success": False,
            "error": f"HTTP error {e.response.status_code}: {e.response.text}",
            "prompt": prompt,
            "selected_styles": styles
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "prompt": prompt,
            "selected_styles": styles
        }


@mcp.tool()
def list_available_styles() -> dict[str, Any]:
    """
    List all available styles for image generation.
    
    Returns:
        Dictionary containing all available styles organized by category
    """
    # Organize styles by category
    categories = {
        "Fooocus Styles": [s for s in AVAILABLE_STYLES if s.startswith("Fooocus")],
        "SAI Styles": [s for s in AVAILABLE_STYLES if s.startswith("SAI")],
        "MRE Styles": [s for s in AVAILABLE_STYLES if s.startswith("MRE")],
        "Art Styles": [s for s in AVAILABLE_STYLES if s.startswith("Artstyle")],
        "Advertising": [s for s in AVAILABLE_STYLES if s.startswith("Ads")],
        "Futuristic": [s for s in AVAILABLE_STYLES if s.startswith("Futuristic")],
        "Game Styles": [s for s in AVAILABLE_STYLES if s.startswith("Game")],
        "Miscellaneous": [s for s in AVAILABLE_STYLES if s.startswith("Misc")],
        "Papercraft": [s for s in AVAILABLE_STYLES if s.startswith("Papercraft")],
        "Photography": [s for s in AVAILABLE_STYLES if s.startswith("Photo")],
        "Cinematic": [s for s in AVAILABLE_STYLES if "Cinematic" in s],
        "Art Movements": [s for s in AVAILABLE_STYLES if s.startswith("Mk")],
        "Other": [s for s in AVAILABLE_STYLES if not any(s.startswith(prefix) for prefix in 
                 ["Fooocus", "SAI", "MRE", "Artstyle", "Ads", "Futuristic", "Game", 
                  "Misc", "Papercraft", "Photo", "Mk"]) and "Cinematic" not in s]
    }
    
    # Remove empty categories
    categories = {k: v for k, v in categories.items() if v}
    
    return {
        "total_styles": len(AVAILABLE_STYLES),
        "categories": categories,
        "performance_options": PERFORMANCE_OPTIONS
    }


@mcp.tool()
def get_server_info() -> dict[str, Any]:
    """
    Get information about the Fooocus MCP server configuration.
    
    Returns:
        Dictionary containing server configuration information
    """
    return {
        "server_name": "Fooocus MCP Server",
        "version": "0.1.0",
        "fooocus_api_url": FOOOCUS_API_URL,
        "available_performance_options": PERFORMANCE_OPTIONS,
        "total_available_styles": len(AVAILABLE_STYLES),
        "default_aspect_ratio": "1024*1024",
        "features": [
            "Text-to-image generation",
            "Intelligent style selection",
            "Custom style override",
            "Multiple performance modes",
            "Configurable aspect ratios"
        ]
    }


def main():
    """Main entry point for the server."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Fooocus MCP Server")
    parser.add_argument("--port", type=int, default=3000, help="Port to run the server on")
    parser.add_argument("--host", default="localhost", help="Host to run the server on")
    args = parser.parse_args()
    
    # Run the MCP server
    # Note: MCP servers typically run over stdio, not HTTP
    # The host and port arguments are kept for compatibility but not used
    mcp.run()


if __name__ == "__main__":
    main() 