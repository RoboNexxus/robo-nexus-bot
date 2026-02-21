#!/bin/bash
# Test deployment readiness

echo "================================"
echo "DEPLOYMENT READINESS TEST"
echo "================================"

# Check Python version
echo -e "\n1. Checking Python version..."
python3 --version

# Check if all required files exist
echo -e "\n2. Checking required files..."
files=("main.py" "bot.py" "requirements.txt" ".replit" "replit.nix" "pyproject.toml")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file MISSING"
    fi
done

# Check Python syntax
echo -e "\n3. Checking Python syntax..."
python3 -m py_compile main.py && echo "✅ main.py syntax OK" || echo "❌ main.py syntax ERROR"
python3 -m py_compile bot.py && echo "✅ bot.py syntax OK" || echo "❌ bot.py syntax ERROR"

# Check if requirements can be parsed
echo -e "\n4. Checking requirements.txt..."
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt found"
    echo "Dependencies:"
    cat requirements.txt
else
    echo "❌ requirements.txt missing"
fi

# Try importing main modules
echo -e "\n5. Testing imports..."
python3 -c "import discord; print('✅ discord.py installed')" 2>/dev/null || echo "❌ discord.py not installed"
python3 -c "import flask; print('✅ flask installed')" 2>/dev/null || echo "❌ flask not installed"
python3 -c "import requests; print('✅ requests installed')" 2>/dev/null || echo "❌ requests not installed"

# Check environment variables (without showing values)
echo -e "\n6. Checking environment variables..."
if [ -n "$DISCORD_TOKEN" ]; then
    echo "✅ DISCORD_TOKEN is set"
else
    echo "⚠️  DISCORD_TOKEN not set (required for deployment)"
fi

if [ -n "$SUPABASE_URL" ]; then
    echo "✅ SUPABASE_URL is set"
else
    echo "⚠️  SUPABASE_URL not set"
fi

if [ -n "$SUPABASE_SERVICE_KEY" ]; then
    echo "✅ SUPABASE_SERVICE_KEY is set"
else
    echo "⚠️  SUPABASE_SERVICE_KEY not set"
fi

echo -e "\n================================"
echo "TEST COMPLETE"
echo "================================"
