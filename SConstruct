import os
import fortdepend as fd
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
  """ use fortdepend to get dependencies """
  fproj = fd.FortranProject(files=source_files, **kwargs)
  source_deps, prog_deps = {}, {}
  for key, val in fproj.depends_by_module.items():
    _key = key.source_file.filename
    _val = [v.source_file.filename for v in val] 
    if key.unit_type=='module':
      source_deps[_key] = _val
    elif key.unit_type=='program':
      prog_deps[_key] = _val
  return source_deps, prog_deps

env = Environment(tools=['default', 'gfortran'], F90='gfortran', LINK='gfortran', LINKFLAGS='', F90FLAGS='')

all_files = find_fortran_files(os.getcwd(), fortran_extensions=fexts, abspath=False)
print('- all files found with fortran ext: ', all_files)

source_deps, prog_deps = generate_fortran_dependencies(all_files, fexts)
source_files = list(source_deps.keys())
prog_files = list(prog_deps.keys())
print('- all source deps (no progs)       ', source_deps)
print('- all program deps found           ', prog_deps)
print('- all source files (no progs)      ', source_files)
print('- all prog files                   ', prog_files)

objects = []
all_deps = {**source_deps, **prog_deps}
for src in all_deps:
    obj_path = os.path.splitext(src)[0] + '.o'
    object = env.Object(obj_path, src)
    print(f'-- tell SCons {obj_path} also depends on {all_deps[src]}')
    env.Depends(target=object, dependency = all_deps[src])
    objects.append(object)
print('- all SCons objects', [str(o) for o in objects])

for prog in prog_deps:
  prog_name = os.path.splitext(os.path.basename(prog))[0]
  print(f'-- tell SCons {prog_name} also depends on {ss2os(prog_deps[prog])}')
  env.Depends(target=prog_name, dependency = ss2os(prog_deps[prog]))

# Filter out .mod files from the objects list
objects_for_linking = [str(o[0]) for o in objects] # get only the first entry which is the object file 
print('- all SCons objects for linking', objects_for_linking)

prog_to_make = 'main'
env.Program(target=prog_to_make, source=objects_for_linking)