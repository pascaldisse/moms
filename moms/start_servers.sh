#!/bin/bash

# Kill any existing servers
echo "Stopping existing servers..."
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:8002 | xargs kill -9 2>/dev/null
pkill -f "server.py" 2>/dev/null
pkill -f "simple-bik-server.py" 2>/dev/null

sleep 1

# Start main server
echo "Starting main server on port 8000..."
python3 server.py > server.log 2>&1 &
MAIN_PID=$!
echo "Main server PID: $MAIN_PID"

# Start BIK proxy server
echo "Starting BIK proxy server on port 8002..."
python3 simple-bik-server.py > simple-bik-server.log 2>&1 &
BIK_PID=$!
echo "BIK server PID: $BIK_PID"

sleep 2

# Check if servers are running
if lsof -i:8000 > /dev/null 2>&1; then
    echo "✅ Main server is running on http://localhost:8000"
else
    echo "❌ Main server failed to start"
fi

if lsof -i:8002 > /dev/null 2>&1; then
    echo "✅ BIK proxy server is running on http://localhost:8002"
else
    echo "❌ BIK proxy server failed to start"
fi

echo ""
echo "To stop servers, run:"
echo "  kill $MAIN_PID $BIK_PID"
echo "  or: pkill -f server.py && pkill -f simple-bik-server.py"