# Image Assets

This folder contains image assets for the Deck of Cards Lab 03 project.

## Image Paths

### Project Images
- `image/card_back.png` - Default card back image
- `image/deck_icon.png` - Deck icon for UI
- `image/logo.png` - Project logo

### Usage in Streamlit

To reference images in your Streamlit app:

```python
import streamlit as st

# Display image from image folder
st.image('image/logo.png', width=200)

# Or use relative path
st.image('./image/card_back.png')
```

### Supported Formats
- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- SVG (.svg)

## Notes
- Place all project images in this folder
- Use descriptive filenames
- Keep image sizes optimized for web
- Reference paths relative to project root
