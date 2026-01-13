#!/bin/bash
cd /opt/smindeck-bot
pkill -f 'python.*bot.py' 2>/dev/null
sleep 2
nohup python3 bot.py > bot_output.log 2>&1 &
echo "✅ Bot reiniciado"
sleep 1
tail -n 20 bot_output.log
