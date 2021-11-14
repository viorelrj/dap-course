import os

python_projects = ['crawler', 'parsed_sup', 'service']

os.system('pip3 freeze > requirements.txt')

for project in python_projects:
  os.system(f'cp requirements.txt ./src/{project}')
