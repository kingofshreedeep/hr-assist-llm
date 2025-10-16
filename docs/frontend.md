# Frontend

The frontend provides a modern, professional chat interface for the HR Assistant LLM application. It consists of a standalone HTML UI that can be served directly from the API or embedded within the Streamlit application.

## Overview

The frontend is implemented as a single HTML file (`professional_ui.html`) with embedded CSS and JavaScript. It provides a clean, responsive chat interface with the following features:

- **Real-time messaging** with the AI assistant
- **Theme support** (light/dark mode) synchronized with the parent Streamlit app
- **Responsive design** that works on desktop and mobile devices
- **Professional styling** with smooth animations and transitions
- **Error handling** with user-friendly error messages
- **Typing indicators** to show when the AI is processing

## Architecture

### File Structure
```
frontend/
├── professional_ui.html    # Main chat interface (also in root directory)
├── app.py                  # Streamlit app entry point
├── app_main.py            # Alternative app entry point
├── features.py            # UI feature management
└── __init__.py
```

### Integration Methods

The frontend can be accessed in two ways:

1. **Direct Access**: Served directly by the FastAPI backend at `/ui` endpoint
2. **Embedded in Streamlit**: Loaded via iframe within the Streamlit application

## Key Features

### Chat Interface
- **Message Input**: Multi-line textarea that auto-resizes
- **Send Button**: Disabled when input is empty or when AI is typing
- **Keyboard Shortcuts**:
  - `Enter`: Send message
  - `Shift+Enter`: Insert new line
- **Message History**: Scrollable message list with timestamps
- **Message Types**: User messages (right-aligned, blue) and AI responses (left-aligned, gray)

### Theme Support
- **Light Theme**: Default professional appearance
- **Dark Theme**: Automatically switches based on Streamlit theme
- **Dynamic Switching**: Themes change instantly via postMessage API

### Responsive Design
- **Desktop**: Full-width layout with optimal message widths
- **Mobile**: Adapted padding and message sizing
- **Touch-friendly**: Large touch targets for mobile devices

### Error Handling
- **Network Errors**: Displays user-friendly error messages
- **API Failures**: Graceful degradation with retry capability
- **Connection Status**: Visual indicator showing online/offline status

## API Integration

### Chat Endpoint
The frontend communicates with the backend via the `/chat` endpoint:

```javascript
POST /chat
Content-Type: application/json

{
  "user_input": "Hello, how can you help with HR tasks?",
  "session_id": "optional-session-identifier"
}
```

**Response Format**:
```json
{
  "response": "I can help you with various HR tasks including...",
  "session_id": "generated-or-existing-session-id"
}
```

### Theme Synchronization
The parent Streamlit application can control the theme:

```javascript
// Send theme change message to iframe
iframe.contentWindow.postMessage({
  type: 'set-theme',
  theme: 'dark' // or 'light'
}, '*');
```

## Technical Implementation

### CSS Architecture
- **CSS Variables**: Comprehensive design token system
- **Component-based**: Modular styling for each UI component
- **Responsive**: Mobile-first approach with media queries
- **Animations**: Smooth transitions and micro-interactions

### JavaScript Classes
- **ChatInterface**: Main controller class managing all functionality
- **Event-driven**: Clean separation of concerns
- **Async/Await**: Modern JavaScript with proper error handling
- **DOM Manipulation**: Efficient updates without framework dependencies

### Browser Compatibility
- **Modern Browsers**: Chrome, Firefox, Safari, Edge
- **Mobile Browsers**: iOS Safari, Chrome Mobile
- **Progressive Enhancement**: Graceful fallbacks for older browsers

## Usage Examples

### Direct Access
```bash
# Start the FastAPI server
python api.py

# Access the UI at
http://localhost:8000/ui
```

### Streamlit Integration
```python
# The Streamlit app automatically embeds the UI
streamlit run app.py
```

### Custom Integration
```html
<iframe
  src="http://localhost:8000/ui"
  style="width:100%; height:600px; border:0;"
  onload="setupThemeSync(this)">
</iframe>

<script>
function setupThemeSync(iframe) {
  // Sync theme with your application
  iframe.contentWindow.postMessage({
    type: 'set-theme',
    theme: 'light'
  }, '*');
}
</script>
```

## Screenshots

### Light Theme
![Light Theme](images/frontend_light.png)

### Dark Theme
![Dark Theme](images/frontend_dark.png)

### Mobile View
![Mobile View](images/frontend_mobile.png)

## Development

### Local Development
1. Start the backend API server
2. Open `professional_ui.html` directly in a browser
3. Or run the Streamlit app for full integration

### Customization
The UI can be customized by modifying:
- **CSS Variables**: Change colors, spacing, and typography
- **JavaScript**: Add new features or modify behavior
- **HTML Structure**: Adjust layout and components

### Testing
- **Manual Testing**: Interact with the UI in different browsers
- **API Testing**: Use browser dev tools to monitor network requests
- **Theme Testing**: Verify theme switching works correctly

## Troubleshooting

### Common Issues

**UI not loading in iframe**
- Check that the backend server is running
- Verify the API_BASE URL is correctly set
- Check browser console for CORS errors

**Theme not switching**
- Ensure postMessage is sent with correct format
- Check that iframe origin allows message passing
- Verify theme values are 'light' or 'dark'

**Messages not sending**
- Check network tab for failed requests
- Verify API endpoint is accessible
- Check browser console for JavaScript errors

**Styling issues**
- Clear browser cache
- Check for CSS conflicts with parent page
- Verify all CSS variables are defined

### Debug Mode
Enable debug logging by opening browser dev tools and monitoring:
- Network tab for API requests
- Console tab for JavaScript errors
- Application tab for local storage/session data

## Contributing

When contributing to the frontend:

1. **Follow the existing code style**
2. **Test in multiple browsers**
3. **Ensure responsive design works**
4. **Update documentation** for any new features
5. **Add screenshots** for visual changes

## Future Enhancements

Potential improvements for the frontend:

- **File upload support** for document analysis
- **Voice input/output** capabilities
- **Message reactions** and feedback
- **Chat history export**
- **Multi-language support**
- **Accessibility improvements** (ARIA labels, keyboard navigation)
- **Progressive Web App** features

