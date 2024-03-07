# Part of a Github action chain: 
    # dynamic_logEntry.yml (in target_repo) https://github.com/RuDeeVelops/RuDeeVelops/blob/main/.github/workflows/dynamic_logEntry.yml
    # convert_md_to_html.py (in target_repo) https://github.com/RuDeeVelops/RuDeeVelops/blob/main/.github/workflows/convert_md_to_html.py
    # dispatch_log_updated_event.yml (in source repo) https://github.com/RuDeeVelops/creativedev-log/blob/main/.github/workflows/dispatch_log_updated_event.yml

# This action is triggered by the dispatch_log_updated_event.yml in the source repository.
# This action reads the README.md file from the source repository, extracts the latest log entry, and converts it to HTML.
# It expects the README.md file to have a specific structure, and it will not work with other structures.
# The structure it expects can be seen in the README.md file in the source repository (https://github.com/rudeevelops/creativedev-log)

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
latest_entry = re.search(r'- #### (\d{2}-\w{3}.*?)(?=- #### \d{2}-\w{3}|<details close>)', md_text, re.DOTALL).group(1)

# Find date
date = latest_entry.split(' || ')[0]

# Convert the latest log entry to HTML
html = markdown.markdown(latest_entry)

# Parse HTML
soup = BeautifulSoup(html, 'html.parser')

# Create first two rows
rows = [
    f'<tr><td align="center" valign="middle" colspan="2"><p><strong>{date} {year}</strong></p><code>updates automagically from <a href="https://github.com/rudeevelops/creativedev-log">creativedev-log</a></code><br/><br/></td></tr>'
]

# Define the left part of the table
left_parts = [
    '🎓 <strong>Learning</strong>',
    '🛠️ <strong>Building</strong>',
    '🎨 <strong>Daily Design</strong>',
    '💡 <strong>Big Challenge</strong>',
    '🏆 <strong>Big Solution</strong>',
    '🌟 <strong>One Cool Find</strong>',
    '💭 <strong>Idea Cloud</strong>',
    '📝 <strong>Blog Entry</strong>',
    '🎥 <strong>YouTube Entry</strong>'
]

# Convert list items to table rows
for i, li in enumerate(soup.find_all('li')):
    contents = ''.join(str(item) for item in li.contents)
    right_part = contents.split('||</strong> ', 1)[1] if '||</strong> ' in contents else contents  # Split the string at '||</strong> ' and assign the second part to right_part if it exists, otherwise assign the whole string
    rows.append(f'<tr><td>{left_parts[i]}</td><td>{right_part}</td></tr>')

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