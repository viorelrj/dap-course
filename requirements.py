from python_projects import projects
import os

os.system('pip3 freeze > requirements.txt')

for project in projects:
  os.system(f'cp requirements.txt ./src/{project}')
