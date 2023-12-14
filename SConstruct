# SCons script to compile and link a Fortran project with .o files in './.obj' and .mod files in './.mod'

import os, subprocess



# Function to run fortdepend and generate dependency file
def generate_fortran_dependencies(source_files, dep_file):
    command = ['fortdepend', '-w', '-o', dep_file, '-f', *source_files]
    print(command)
    subprocess.run(command)

def parse_fortdepend_dependencies(dep_file):
  dependencies = {}
  target = None
  with open(dep_file, 'r') as file:
      for line in file:
        if not line.startswith('#') and not line.strip()=='':
          # print('line', line)
          if ':' in line:
              # store old target and deps
              if target:
                dependencies[target] = deps
              target = line.split(':')[0].strip()
              deps = []
              # print('new target', target)
          else:
            _dep = line.replace('/', '').replace('/t', ' ').replace('/n', ' ').replace('\\', ' ').strip()
            deps.append(_dep)
  print(dependencies)
  return dependencies


# Set up the environment with Fortran compiler and linker options
env = Environment(tools=['default', 'gfortran'], F90='gfortran', LINK='gfortran', LINKFLAGS='', F90FLAGS='')

# Source directory
src_dir = 'src'

# Object and module directories
obj_dir = './.obj'
mod_dir = './.mod'
dep_file = "deps.txt"

# Create object and module directories if they do not exist
if not os.path.exists(obj_dir):
    os.makedirs(obj_dir)
if not os.path.exists(mod_dir):
    os.makedirs(mod_dir)

# Fortran file extensions
fortran_extensions = ['.f', '.for', '.f90', '.f95', '.f03', '.f08']

# Find all Fortran source files in src directory and its subdirectories
source_files = []
for root, dirs, files in os.walk(src_dir):
    for file in files:
        if any(file.endswith(ext) for ext in fortran_extensions):
            full_path = os.path.join(root, file)
            source_files.append(full_path)

print('source_files', source_files)
generate_fortran_dependencies(source_files, dep_file)
dependencies = parse_fortdepend_dependencies(dep_file)


... ändere parse_fortdepend_dependencies so , dass die paths beibehalten werden! ...

# Compile each source file into an object file
objects = []
for src in source_files:
    obj_path = os.path.join(obj_dir, os.path.splitext(os.path.basename(src))[0] + '.o')
    objects.extend(env.Object(target=obj_path, source=src))

print('objects', objects)
for target in dependencies:
    print(' - target', target)

    deps = dependencies[target]
    obj_path = os.path.join(obj_dir, os.path.splitext(os.path.basename(target))[0] + '.o')
    source_files = [os.path.join(src_dir, dep) for dep in deps]
    print('target=',obj_path, 'source=', source_files)
    _object = env.Object(target=obj_path, sources=source_files)
    objects.extend(_object)



# Specify where to place the object and module files
env.Replace(OBJSUFFIX='.o', FORTRANMODDIR=mod_dir, FORTRANMODPREFIX='')


# Link the object files into an executable
# Filter out .mod files from the objects list
objects_for_linking = [obj for obj in objects if str(obj).endswith('.o')]
env.Program(target='main', source=objects_for_linking)