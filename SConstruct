from copy import deepcopy
import os
import fortdepend as fdep
from  SCons.Environment import Environment

fexts = ['.f', '.for', '.f90', '.f95', '.f03', '.f08']

def find_fortran_files(root_dir, fortran_extensions, abspath=False):
  """Find all Fortran source files in src directory and its subdirectories"""
  source_files = []
  for dir, _, files in os.walk(root_dir):
    for file in files:
      if any(file.endswith(ext) for ext in fortran_extensions):
        source_files.append( os.path.join(dir, file) if abspath else os.path.join(dir.replace(root_dir, '.'), file))
  return source_files

def fortran_source_to_object(source, fortran_extensions):
  """replace the fortran ext with .o"""
  for ext in fortran_extensions:
    if source.endswith(ext):
      return source.replace(ext, '.o')
s2o = lambda src: fortran_source_to_object(str(src), fexts)
ss2os = lambda srcs: [fortran_source_to_object(str(src), fexts) for src in srcs]

def generate_fortran_dependencies(source_files, fortran_extensions, **kwargs):
  """ use fortdepend to get dependencies"""
  fproj = fdep.FortranProject(files=source_files, **kwargs)
  source_deps, prog_deps = {}, {}
  for key, val in fproj.depends_by_module.items():
    _key = key.source_file.filename
    _val = [v.source_file.filename for v in val] 
    if key.unit_type=='module':
      source_deps[_key] = _val
    elif key.unit_type=='program':
      prog_deps[_key] = _val
  return source_deps, prog_deps

# Set up the environment with Fortran compiler and linker options
env = Environment(tools=['default', 'gfortran'], F90='gfortran', LINK='gfortran', LINKFLAGS='', F90FLAGS='')

# get source files
all_files = find_fortran_files(os.getcwd(), fortran_extensions=fexts, abspath=False)
print('- all files with fortran ext found: ', all_files)

# get deps
source_deps, prog_deps = generate_fortran_dependencies(all_files, fexts)
source_files = list(source_deps.keys())
prog_files = list(prog_deps.keys())
print('- all source deps (no progs)       ', source_deps)
print('- all program deps found           ', prog_deps)
print('- all source files (no progs)      ', source_files)
print('- all prog files                   ', prog_files)

objects = []
for prog in source_deps:
    obj_path = os.path.splitext(prog)[0] + '.o'
    _object = env.Object(obj_path, prog)
    print(f'-- tell SCons {obj_path} also depends on {source_deps[prog]}')
    env.Depends(target=_object, dependency = source_deps[prog])
    objects.append(_object)
print('- all SCons objects', [str(o) for o in objects])
print('- all SCons objects', [o for o in objects])
print('- remark: SCons handles Fortran objects as tuples of module and object files')

for prog in prog_deps:
  prog_name = os.path.splitext(os.path.basename(prog))[0]
  print(prog_name)
  print(f'-- tell SCons {prog_name} also depends on {ss2os(prog_deps[prog])}')
  env.Depends(target=prog_name, dependency = prog_deps[prog])

# Filter out .mod files from the objects list
objects_for_linking = [str(o[0]) for o in objects]
print('objects_for_linking', objects_for_linking)
env.Program(target='main', source=objects_for_linking)