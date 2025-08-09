#!/bin/bash

# Service monitoring script for PUBG API
# Run this script periodically to ensure services are running

LOG_FILE="/var/log/pubgapi-monitor.log"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOG_FILE
}

log "🔍 Checking PUBG API services..."

# Check if services are running
if ! systemctl is-active --quiet pubgapi; then
    log "❌ PUBG API service is down, restarting..."
    systemctl restart pubgapi
    sleep 5
    if systemctl is-active --quiet pubgapi; then
        log "✅ PUBG API service restarted successfully"
    else
        log "❌ Failed to restart PUBG API service"
    fi
else
    log "✅ PUBG API service is running"
fi

if ! systemctl is-active --quiet nginx; then
    log "❌ Nginx service is down, restarting..."
    systemctl restart nginx
    sleep 5
    if systemctl is-active --quiet nginx; then
        log "✅ Nginx service restarted successfully"
    else
        log "❌ Failed to restart nginx service"
    fi
else
    log "✅ Nginx service is running"
fi

# Check if ports are listening
if ! ss -tlnp | grep -q ":8000 "; then
    log "⚠️  Port 8000 not listening, restarting PUBG API..."
    systemctl restart pubgapi
fi

if ! ss -tlnp | grep -q ":80 "; then
    log "⚠️  Port 80 not listening, restarting nginx..."
    systemctl restart nginx
fi

log "📊 Service check completed" 