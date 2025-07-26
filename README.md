# PUBG Mobile User ID Checker API

A high-performance PUBG Mobile user ID checker with Cloudflare bypass using proxy and cloudscraper.

## Features

* ✅ **Real PUBG API Integration** - Uses actual PUBG Mobile API
* ✅ **Cloudflare Bypass** - Successfully bypasses Cloudflare protection
* ✅ **Proxy Support** - Uses working proxy for reliable access
* ✅ **FastAPI Server** - High-performance REST API
* ✅ **Rate Limiting** - 30 requests per minute per IP
* ✅ **Session Reuse** - Optimized for speed with persistent sessions
* ✅ **Parallel Processing** - Can handle multiple requests simultaneously

## Project Structure

```
pubgapiw/
├── pubgapi.py              # Core PUBG checker with optimized logic
├── pubgapi_server.py       # FastAPI server with endpoints
├── requirements.txt        # Python dependencies
├── deploy.sh              # VPS deployment script
├── app.vue                # Nuxt.js main app
├── pages/
│   └── pubg-checker.vue   # Web interface
├── assets/
│   └── css/
│       └── main.css       # Styles
└── README.md              # This file
```

## API Endpoints

### 1. GET `/uid/{userid}` - Check user ID via URL path
```bash
curl "http://localhost:8000/uid/123456789"
```

### 2. POST `/check` - Check user ID via JSON body
```bash
curl -X POST "http://localhost:8000/check" \
     -H "Content-Type: application/json" \
     -d '{"userid": "123456789"}'
```

## Response Format

### Success Response
```json
{
  "status": "success",
  "userid": "123456789",
  "player_name": "PlayerName",
  "openid": "openid_value",
  "valid": true
}
```

### Invalid User ID
```json
{
  "status": "invalid",
  "userid": "123456789",
  "error": "User ID not found or invalid"
}
```

### Error Response
```json
{
  "status": "error",
  "userid": "123456789",
  "error": "error_message"
}
```

## Local Development

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Server
```bash
uvicorn pubgapi_server:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Test the API
- Visit: `http://localhost:8000/docs` for interactive API docs
- Test endpoint: `http://localhost:8000/uid/123456789`

## VPS Deployment

### Quick Deployment
```bash
# Make deployment script executable
chmod +x deploy.sh

# Run deployment script
./deploy.sh
```

### Manual Deployment Steps

1. **Connect to your VPS via SSH**
2. **Clone or upload your project files**
3. **Run the deployment script:**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

### Post-Deployment

After deployment, your API will be available at:
- **API Base URL:** `http://YOUR_VPS_IP`
- **API Documentation:** `http://YOUR_VPS_IP/docs`
- **Example Usage:** `http://YOUR_VPS_IP/uid/123456789`

## Performance

* **Single Check:** ~1-3 seconds
* **Session Reuse:** Faster subsequent requests
* **Rate Limit:** 30 requests/minute per IP
* **Parallel Processing:** Up to 10 concurrent requests

## Rate Limiting

- **30 requests per minute per IP address**
- Returns HTTP 429 when exceeded
- Automatic retry after rate limit period

## Troubleshooting

### Common Issues

1. **Proxy Connection Failed**
   - Check proxy credentials in `pubgapi.py`
   - Verify proxy service is active

2. **Cloudflare Blocking**
   - The script handles this automatically
   - If issues persist, check proxy configuration

3. **Service Not Starting**
   - Check logs: `sudo journalctl -u pubgapi -f`
   - Verify Python dependencies are installed

### Service Management

```bash
# Check service status
sudo systemctl status pubgapi

# Restart service
sudo systemctl restart pubgapi

# View logs
sudo journalctl -u pubgapi -f

# Stop service
sudo systemctl stop pubgapi
```

## Security Notes

* Keep proxy credentials secure
* Monitor API usage to avoid abuse
* Consider implementing additional authentication for production
* The proxy credentials are for demonstration purposes

## License

This project is for educational purposes. Please respect PUBG Mobile's terms of service.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Test the API locally first
4. Check service logs for errors 