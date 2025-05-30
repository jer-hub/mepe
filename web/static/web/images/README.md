# MEPE Cooperative - Images and Icons

This directory contains static images and icons for the MEPE Cooperative web application.

## Directory Structure

```
images/
├── icons/          # UI icons and small graphics
├── logos/          # Cooperative logos and branding
├── backgrounds/    # Background images and patterns
├── illustrations/  # Decorative illustrations
└── favicons/       # Favicon files for different devices
```

## Icon Files

The following icon files should be added to the `icons/` directory:

- **arrow-left.svg** - Back navigation arrow
- **search.svg** - Search icon
- **filter.svg** - Filter icon
- **table.svg** - Table view icon
- **card.svg** - Card view icon
- **close.svg** - Close/clear icon
- **loading.svg** - Loading spinner
- **success.svg** - Success checkmark
- **error.svg** - Error icon
- **warning.svg** - Warning icon
- **info.svg** - Information icon

## Logo Files

Add these logo files to the `logos/` directory:

- **mepe-logo.svg** - Main cooperative logo (vector)
- **mepe-logo.png** - Logo in PNG format (multiple sizes)
- **mepe-logo-white.svg** - White version for dark backgrounds
- **mepe-wordmark.svg** - Text-only logo

## Favicon Files

Add these favicon files to the `favicons/` directory:

- **favicon.ico** - Standard favicon
- **favicon-16x16.png** - 16x16 PNG favicon
- **favicon-32x32.png** - 32x32 PNG favicon
- **apple-touch-icon.png** - Apple touch icon (180x180)
- **android-chrome-192x192.png** - Android Chrome icon
- **android-chrome-512x512.png** - Android Chrome icon (large)

## Usage

To use these images in templates, reference them with:

```html
<!-- Icons -->
<img src="{% static 'web/images/icons/search.svg' %}" alt="Search">

<!-- Logos -->
<img src="{% static 'web/images/logos/mepe-logo.svg' %}" alt="MEPE Cooperative">

<!-- In CSS -->
background-image: url('../images/backgrounds/pattern.svg');
```

## Optimization

All images should be optimized for web:
- SVG files should be minified
- PNG files should be compressed
- Use appropriate file formats (SVG for icons, PNG for photos)
- Consider WebP format for better compression

## Accessibility

- Always include meaningful alt text
- Use SVG with proper title and desc elements
- Ensure sufficient color contrast
- Provide fallbacks for critical icons
