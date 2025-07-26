#!/bin/bash

# PUBG API VPS Deployment Script
echo "🚀 Starting PUBG API VPS Deployment..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and pip
echo "🐍 Installing Python and pip..."
sudo apt install -y python3 python3-pip python3-venv

# Install nginx
echo "🌐 Installing nginx..."
sudo apt install -y nginx

# Create project directory
echo "📁 Creating project directory..."
sudo mkdir -p /var/www/pubgapi
sudo chown $USER:$USER /var/www/pubgapi

# Copy project files (assuming you're in the project directory)
echo "📋 Copying project files..."
cp -r * /var/www/pubgapi/

# Create virtual environment
echo "🔧 Setting up Python virtual environment..."
cd /var/www/pubgapi
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Create systemd service
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/pubgapi.service > /dev/null <<EOF
[Unit]
Description=PUBG API FastAPI Server
After=network.target

[Service]
Type=exec
User=$USER
WorkingDirectory=/var/www/pubgapi
Environment=PATH=/var/www/pubgapi/venv/bin
ExecStart=/var/www/pubgapi/venv/bin/uvicorn pubgapi_server:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Configure nginx
echo "🌐 Configuring nginx..."
sudo tee /etc/nginx/sites-available/pubgapi > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable nginx site
sudo ln -sf /etc/nginx/sites-available/pubgapi /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Start services
echo "🚀 Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable pubgapi
sudo systemctl start pubgapi
sudo systemctl restart nginx

# Check status
echo "✅ Checking service status..."
sudo systemctl status pubgapi --no-pager
sudo systemctl status nginx --no-pager

echo "🎉 Deployment complete!"
echo "📡 Your PUBG API is now running at: http://YOUR_VPS_IP"
echo "🔗 API endpoints:"
echo "   - GET  http://YOUR_VPS_IP/uid/{userid}"
echo "   - POST http://YOUR_VPS_IP/check"
echo "📖 API docs: http://YOUR_VPS_IP/docs" 