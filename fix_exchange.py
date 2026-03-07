import re

with open('templates/exchange_connections.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the broken fetch statement - it has method and headers mixed up
# Pattern to find the broken fetch
old_pattern = r"fetch\('/add-exchange', \{\s*'POST',\s*headers\s*method:\s*:\s*\{ 'Content-Type': 'application/json' \},"
new_pattern = "fetch('/add-exchange', {\n                method: 'POST',\n                headers: { 'Content-Type': 'application/json' },"

content = content.replace("fetch('/add-exchange', {\nPOST',\n                headers    method: ': { 'Content-Type': 'application/json' },", 
                          "fetch('/add-exchange', {\n                method: 'POST',\n                headers: { 'Content-Type': 'application/json' },")

# Also check for the second broken pattern
content = content.replace("fetch('/add-exchange', {\n                method:\n                body:", 
                          "fetch('/add-exchange', {\n                method: 'POST',\n                headers: { 'Content-Type': 'application/json' },\n                body:")

with open('templates/exchange_connections.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed exchange_connections.html!")

