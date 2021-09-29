import os

python_projects = ['crawler', 'parsed_sup']

os.system(f'pip3 freeze > requirements.txt')

for project in python_projects:
  print(f'./src/{project}')
  os.system(f'cp requirements.txt ./src/{project}')
