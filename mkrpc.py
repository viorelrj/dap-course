import os
import glob
from python_projects import projects
from shutil import copy

protos_path = './src/proto'
build_path = './src/proto_build'

if (not glob.glob(build_path)):
  os.mkdir(build_path)

protos_full_paths = glob.glob(f'{protos_path}/*.proto')
protos_names = list(map(lambda s: s.split('.')[0], [
                    os.path.basename(x) for x in protos_full_paths]))

for generated in glob.glob(f'{build_path}/*_pb2*'):
  if (generated.split('_pb2')[0] not in protos_names):
    os.remove(generated)

for proto in protos_full_paths:
  os.system(
      f'python -m  grpc_tools.protoc --proto_path={protos_path} --python_out={build_path} --grpc_python_out={build_path} {proto}')


proto_builds = glob.glob(f'{build_path}/*.py')
project_paths = list(map(lambda n: f'./src/{n}/app/', projects))
for project in project_paths:
  if (not os.path.exists(project)):
    os.mkdir(project)

for build in proto_builds:
  for project in project_paths:
    copy(build, project)
