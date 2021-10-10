import os

python_projects = ['crawler', 'parsed_sup', 'service']

for project in python_projects:
  os.system(f'cp requirements.txt ./src/{project}')
