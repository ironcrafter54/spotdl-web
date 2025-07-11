# spotDL Web
(this readme was made by claude take it with a grain of salt,)
A web-based interface for [spotDL](https://github.com/spotDL/spotify-downloader) that allows you to download music from Spotify, YouTube, and other platforms through a clean, real-time web interface. The application also supports automatic playlist integration with Navidrome media servers.

## Features

- 🎵 **Web Interface**: Clean, responsive web UI for easy music downloading
- 📊 **Real-time Progress**: Live download progress updates via WebSockets
- 📱 **Playlist Integration**: Automatically add downloaded songs to Navidrome playlists
- 🔄 **Duplicate Detection**: Skips already downloaded songs
- 📝 **Detailed Logging**: Real-time logs of download progress, failures, and successes
- 🔐 **PIN Authentication**: Secure access with customizable PIN protection
- 🐳 **Docker Support**: Easy deployment with Docker containerization

## Prerequisites

- Python 3.11+
- [spotDL](https://github.com/spotDL/spotify-downloader) installed
- FFmpeg (for audio processing)
- Optional: Navidrome server for playlist integration

## Installation

### Option 1: Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd spotdl-web
```

2. Build and run with Docker:
```bash
docker build -t spotdl-web .
docker run -p 8000:8000 -v ./downloads:/app/downloads spotdl-web
```

### Option 2: Local Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd spotdl-web
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Configuration

### Environment Variables

The application supports the following environment variables:

#### Core Settings
```bash
export PIN="your-secret-pin"                    # PIN for accessing the application (default: 1234)
export SESSION_SECRET="your-session-secret"     # Secret key for session management
export PORT="8000"                              # Port for the web application
```

#### Navidrome Integration
For Navidrome playlist integration, set these environment variables:

```bash
export SECRET_KEY="your-navidrome-url"
export USERNAME="your-navidrome-username"
export PASSWORD="your-navidrome-password"
export PORT="4533"  # Navidrome port
```

### Docker Environment Variables

```bash
docker run -p 8000:8000 \
  -e PIN="your-secret-pin" \
  -e SESSION_SECRET="your-session-secret" \
  -e SECRET_KEY="http://your-navidrome-url" \
  -e USERNAME="your-username" \
  -e PASSWORD="your-password" \
  -e PORT="4533" \
  -v ./downloads:/app/downloads \
  spotdl-web
```

### PIN Authentication Setup

⚠️ **Important Security Notes:**
- The default PIN is `1234` - **change this immediately** for security
- Set a strong, unique session secret for production use
- Sessions are valid for 24 hours after login

#### Setting Your PIN

**Option 1: Environment Variable**
```bash
export PIN="your-secure-pin"
python run.py
```

**Option 2: Docker**
```bash
docker run -p 8000:8000 -e PIN="your-secure-pin" spotdl-web
```

**Option 3: Production Deployment**
```bash
# Create a .env file
echo "PIN=your-secure-pin" >> .env
echo "SESSION_SECRET=your-random-secret-key" >> .env
```

## Usage

1. Open your web browser and navigate to `http://localhost:8000`

2. **First Access - PIN Authentication**:
   - You'll be prompted to enter your PIN
   - Enter the PIN you configured (default: `1234`)
   - Click "Access spotDL" to continue
   - Your session will remain active for 24 hours

3. **Basic Download**:
   - Enter a Spotify URL (playlist, album, or track)
   - Click "Download" to start the process

3. **Download with Playlist Integration**:
   - Format your input as: `spotify-url---playlist-name`
   - Example: `https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M---My Playlist`
   - The app will download songs and automatically add them to the specified Navidrome playlist

4. **Monitor Progress**:
   - Real-time progress updates show current download status
   - View logs for detailed information about each song
   - See which songs were downloaded, skipped, or failed

## Supported URLs

- Spotify playlists, albums, and tracks
- YouTube videos and playlists
- YouTube Music playlists
- SoundCloud tracks and playlists
- Bandcamp albums and tracks
- And more (see [spotDL documentation](https://spotdl.readthedocs.io/en/latest/))

## API Endpoints

- `GET /` - Web interface (requires authentication)
- `GET /login` - PIN authentication page
- `POST /login` - PIN authentication endpoint
- `POST /logout` - Logout endpoint
- `WebSocket /ws` - Real-time communication for downloads and progress updates (requires authentication)

## Project Structure

```
spotdl-web/
├── main.py              # FastAPI application, WebSocket handling, and authentication
├── spotdl_runner.py     # spotDL command execution and output parsing
├── add_to_playlist.py   # Navidrome playlist integration
├── config.py           # Configuration settings and environment variables
├── run.py              # Startup script with configuration validation
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── frontend/
│   └── index.html     # Web interface with authentication
└── downloads/         # Downloaded music files
```

## Development

### Running Tests

```bash
python test_import.py
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export PIN="dev-pin"
export SESSION_SECRET="dev-secret"

# Run in development mode
uvicorn main:app --reload --host 0.0.0.0 --port 8000
# OR use the startup script
python run.py
```

## Troubleshooting

### Common Issues

1. **Can't access the application**: Check that you're using the correct PIN
2. **Session expired**: Re-enter your PIN to get a new 24-hour session
3. **WebSocket connection failed**: Ensure you're logged in with a valid session
4. **spotDL not found**: Ensure spotDL is installed and in your PATH
5. **FFmpeg not found**: Install FFmpeg for audio processing
6. **Permission errors**: Check file permissions in the downloads directory
7. **Navidrome connection failed**: Verify your Navidrome server URL and credentials

### Security Best Practices

- Always change the default PIN (`1234`) before deployment
- Use a strong, random session secret in production
- Consider using HTTPS in production environments
- Regularly rotate your PIN and session secret
- Monitor access logs for suspicious activity

### Logs

Check the console output for detailed error messages and download progress. The web interface also displays real-time logs.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please check the license file for details.

## Acknowledgments

- [spotDL](https://github.com/spotDL/spotify-downloader) - The core music downloading library
- [Navidrome](https://www.navidrome.org/) - Self-hosted music server
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework for building APIs

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.
