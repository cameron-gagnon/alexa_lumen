#!/bin/sh

echo "Killing any previous alexa_lumen/{lumen_callback.py|ngrok} processes"

ps aux | grep ngrok | tee /dev/tty | sudo kill $(awk '{print $2}')
ps aux | grep lumen | tee /dev/tty | sudo kill $(awk '{print $2}')

echo "\n"

echo "Starting alexa_lumen/ngrok..."
nohup ./ngrok http 5000 &
sleep 2

echo "ngrok host is: "
curl "http://localhost:4040/api/tunnels" 2>/dev/null | python3 -c "import sys, json; print(json.load(sys.stdin)['tunnels'][1]['public_url'])"

echo "Starting alexa_lumen/lumen_callback.py..."
nohup ./lumen_callback.py &
sleep 0.5

echo "\n"
