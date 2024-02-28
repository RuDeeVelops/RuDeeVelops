import os
import re
import markdown
from bs4 import BeautifulSoup

# Read the README.md file from the source repository
with open('source_repo/README.md', 'r') as file:
    md_text = file.read()

# Extract the year
year = re.search(r'## 📅 (\d{4})', md_text).group(1)

# Extract the latest log entry
latest_entry = re.search(r'- #### (\d{2}-\w{3} \|\| Day \d{2}.*?)(?=- #### \d{2}-\w{3} \|\| Day \d{2}|<details close>)', md_text, re.DOTALL).group(1)

# Find date
date = latest_entry.split(' || ')[0]

# Convert the latest log entry to HTML
md = markdown.Markdown(extras=["link-patterns", "code-friendly"])
html = md.convert(latest_entry)

# Parse HTML
soup = BeautifulSoup(html, 'html.parser')

# Create first two rows
rows = [
    f'<tr><td align="center" valign="middle" colspan="2"><p><strong>{date} {year}</strong></p><code>updates automagically from <a href="https://github.com/rudeevelops/creativedev-log">creativedev-log</a></code><br/><br/></td></tr>'
]

# Convert list items to table rows
for li in soup.find_all('li'):
    key, value = li.text.split(' || ')
    rows.append(f'<tr><td><strong>{key}</strong></td><td>{value}</td></tr>')

# Combine rows into a table
table = '<table>' + ''.join(rows) + '</table>'

# Read the README.md file from the target repository
with open('target_repo/README.md', 'r') as file:
    readme = file.read()

# Replace the content between "<!-- START LOG -->" and "<!-- END LOG -->" with the table
new_readme = re.sub(r'<!-- START LOG -->.*<!-- END LOG -->', '<!-- START LOG -->\n' + table + '\n<!-- END LOG -->', readme, flags=re.DOTALL)

# Write the updated README.md file to the target repository
with open('target_repo/README.md', 'w') as file:
    file.write(new_readme)