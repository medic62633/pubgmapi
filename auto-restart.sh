#!/bin/bash

# Auto-restart script for PUBG API services
# This script ensures services start on boot and restart on crashes

echo "🚀 Setting up auto-restart for PUBG API services..."

# Create systemd override directory
mkdir -p /etc/systemd/system/pubgapi.service.d

# Create restart configuration
cat > /etc/systemd/system/pubgapi.service.d/restart.conf << 'EOF'
[Service]
Restart=always
RestartSec=10
StartLimitInterval=0
StartLimitBurst=0
EOF

# Enable services to start on boot
systemctl enable pubgapi
systemctl enable nginx

# Reload systemd configuration
systemctl daemon-reload

# Start services if not running
systemctl start pubgapi
systemctl start nginx

# Check status
echo "✅ Services configured for auto-restart:"
systemctl is-enabled pubgapi
systemctl is-enabled nginx
systemctl is-active pubgapi
systemctl is-active nginx

echo "🎉 Auto-restart configuration complete!"
echo "📋 Services will now:"
echo "   - Start automatically on boot"
echo "   - Restart automatically if they crash"
echo "   - Restart after 10 seconds on failure" 