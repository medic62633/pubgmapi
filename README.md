# PUBG Mobile User ID Checker for Nuxt.js

A complete solution for checking PUBG Mobile user IDs with Cloudflare bypass using proxy and cloudscraper.

## Features

- ✅ **Real PUBG API Integration** - Uses actual PUBG Mobile API
- ✅ **Cloudflare Bypass** - Successfully bypasses Cloudflare protection
- ✅ **Proxy Support** - Uses DataImpulse proxy for reliable access
- ✅ **Nuxt.js Integration** - Full-stack solution with Vue frontend
- ✅ **Fast Performance** - Optimized for speed with session reuse
- ✅ **Beautiful UI** - Modern, responsive interface

## Files Structure

```
pubgapiw/
├── pubg_checker.py              # Interactive CLI version
├── pubg_checker_api.py          # API version for Nuxt.js
├── server/
│   └── api/
│       └── check-pubg.post.ts   # Nuxt.js API endpoint
├── pages/
│   └── pubg-checker.vue         # Vue frontend page
└── README.md                    # This file
```

## Setup

### 1. Install Python Dependencies

```bash
pip install cloudscraper curl-cffi
```

### 2. Configure Proxy (Optional)

The script uses a working proxy by default. If you want to use your own:

Edit `pubg_checker_api.py` and update the proxy credentials:

```python
proxy_host = "your-proxy-host.com"
proxy_port = "your-port"
proxy_username = "your-username"
proxy_password = "your-password"
```

### 3. Test the Python Script

```bash
# Test single user ID
python pubg_checker_api.py 5204837417

# Expected output:
# {"status": "success", "userid": "5204837417", "player_name": "Agusbhaji", "openid": "12199295050974504", "valid": true}
```

### 4. Nuxt.js Integration

The project includes:

- **API Endpoint**: `/server/api/check-pubg.post.ts`
- **Frontend Page**: `/pages/pubg-checker.vue`

#### API Usage

```javascript
// POST /api/check-pubg
const response = await $fetch('/api/check-pubg', {
  method: 'POST',
  body: {
    userid: '5204837417'
  }
})

// Response format:
{
  "status": "success",
  "userid": "5204837417",
  "player_name": "Agusbhaji",
  "openid": "12199295050974504",
  "valid": true
}
```

#### Frontend Usage

Visit `/pubg-checker` in your Nuxt.js app to use the web interface.

## How It Works

1. **Cloudflare Bypass**: Uses `cloudscraper` library to bypass Cloudflare protection
2. **Proxy Integration**: Routes requests through DataImpulse proxy for reliable access
3. **Session Management**: Establishes session once and reuses it for faster requests
4. **Real API**: Connects to actual PUBG Mobile API at `https://api.elitedias.com/checkid`

## Response Types

### Success Response
```json
{
  "status": "success",
  "userid": "5204837417",
  "player_name": "Agusbhaji",
  "openid": "12199295050974504",
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
  "userid": "5204837417",
  "error": "API request failed: HTTP 403"
}
```

## Performance

- **Single Check**: ~2-3 seconds
- **Session Reuse**: Faster subsequent requests
- **Parallel Processing**: Can handle multiple requests simultaneously

## Troubleshooting

### Common Issues

1. **Python not found**: Ensure Python is installed and in PATH
2. **Module not found**: Install required packages with pip
3. **Proxy errors**: Check proxy credentials and connectivity
4. **Cloudflare blocking**: The script should handle this automatically

### Debug Mode

To see detailed output, modify the Python script to add debug prints:

```python
print(f"Debug: Checking user ID {userid}", file=sys.stderr)
```

## Security Notes

- Keep proxy credentials secure
- Consider rate limiting for production use
- Monitor API usage to avoid abuse
- The proxy credentials in this repo are for demonstration

## License

This project is for educational purposes. Please respect PUBG Mobile's terms of service.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify Python dependencies are installed
3. Test the Python script directly first
4. Check proxy connectivity 