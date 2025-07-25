# Setup Guide for PUBG Checker Nuxt.js Project

## Prerequisites

### 1. Install Node.js

You need to install Node.js first. Here are the steps:

#### Option A: Download from Official Website
1. Go to [https://nodejs.org/](https://nodejs.org/)
2. Download the LTS version (recommended)
3. Run the installer and follow the setup wizard
4. Restart your terminal/PowerShell

#### Option B: Using Chocolatey (if you have it)
```powershell
choco install nodejs
```

#### Option C: Using Winget (Windows 10/11)
```powershell
winget install OpenJS.NodeJS
```

### 2. Verify Installation

After installation, restart your terminal and run:
```powershell
node --version
npm --version
```

You should see version numbers like:
```
v18.17.0
9.6.7
```

## Project Setup

### 1. Install Dependencies

Once Node.js is installed, run:
```powershell
npm install
```

### 2. Install Python Dependencies

Make sure you have the Python dependencies installed:
```powershell
pip install cloudscraper curl-cffi
```

### 3. Test Python Script

Test that the Python script works:
```powershell
python pubg_checker_api.py 5204837417
```

You should see output like:
```json
{"status": "success", "userid": "5204837417", "player_name": "Agusbhaji", "openid": "12199295050974504", "valid": true}
```

### 4. Start Development Server

Run the Nuxt.js development server:
```powershell
npm run dev
```

You should see output like:
```
Nuxt 3.x.x ready in xxx ms

  ➜ Local:    http://localhost:3000/
  ➜ Network:  http://192.168.x.x:3000/
```

### 5. Access the Application

Open your browser and go to:
- **Main page**: http://localhost:3000/pubg-checker
- **API endpoint**: http://localhost:3000/api/check-pubg

## Project Structure

```
pubgapiw/
├── app.vue                    # Main app component
├── nuxt.config.ts            # Nuxt.js configuration
├── package.json              # Node.js dependencies
├── pubg_checker.py           # Interactive CLI version
├── pubg_checker_api.py       # API version for Nuxt.js
├── server/
│   └── api/
│       └── check-pubg.post.ts # Nuxt.js API endpoint
├── pages/
│   └── pubg-checker.vue      # Vue frontend page
├── assets/
│   └── css/
│       └── main.css          # Tailwind CSS
├── README.md                 # Project documentation
└── SETUP.md                  # This setup guide
```

## Troubleshooting

### Node.js/npm not found
- Make sure Node.js is installed correctly
- Restart your terminal after installation
- Check if Node.js is in your PATH

### Python dependencies missing
```powershell
pip install cloudscraper curl-cffi
```

### Port 3000 already in use
- Change the port in `nuxt.config.ts`:
```typescript
export default defineNuxtConfig({
  devServer: {
    port: 3001
  }
  // ... rest of config
})
```

### API errors
- Check that Python script works independently
- Verify proxy credentials in `pubg_checker_api.py`
- Check console for error messages

## Development Commands

```powershell
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Generate static site
npm run generate
```

## Next Steps

1. **Customize the UI**: Modify `pages/pubg-checker.vue`
2. **Add more features**: Extend the API in `server/api/check-pubg.post.ts`
3. **Deploy**: Build and deploy to your hosting platform
4. **Add authentication**: Implement user authentication if needed
5. **Rate limiting**: Add rate limiting for production use

## Support

If you encounter issues:
1. Check this setup guide
2. Verify all dependencies are installed
3. Test Python script independently
4. Check Nuxt.js documentation: https://nuxt.com/docs 