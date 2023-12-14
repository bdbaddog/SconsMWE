# Create a simple Fortran project structure with multiple files, modules, and programs

# Directory structure:
# src/
# |-- main.f90
# |-- module0.f90
# |-- module1.f90
# |-- module2.f90
# |-- utils/
#     |-- util_module.f90

import os

# Create the src directory and subdirectories
os.makedirs("src/utils", exist_ok=True)

# Define the contents of the Fortran files
main_program = """
program main
    use module0
    use module1
    use module2
    use util_module
    implicit none
    write(*,*) 'Main program using modules.'
    call module0_subroutine()
    call module1_subroutine()
    call module2_subroutine()
    call util_subroutine()
end program main
"""


module0 = """
module module0
    implicit none
contains
    subroutine module0_subroutine()
        write(*,*) 'This is module0 subroutine.'
    end subroutine module0_subroutine
end module module0
"""

module1 = """
module module1
    implicit none
contains
    subroutine module1_subroutine()
        write(*,*) 'This is module1 subroutine.'
    end subroutine module1_subroutine
end module module1
"""

module2 = """
module module2
    use module0
    use module1
    implicit none
contains
    subroutine module2_subroutine()
        write(*,*) 'This is module2 subroutine.'
    end subroutine module2_subroutine
end module module2
"""

util_module = """
module util_module
    implicit none
contains
    subroutine util_subroutine()
        write(*,*) 'This is a utility subroutine.'
    end subroutine util_subroutine
end module util_module
"""

# Write the Fortran files
with open("src/main.f90", "w") as file:
    file.write(main_program)

with open("src/module0.f90", "w") as file:
    file.write(module0)

with open("src/module1.f90", "w") as file:
    file.write(module1)

with open("src/module2.f90", "w") as file:
    file.write(module2)

with open("src/utils/util_module.f90", "w") as file:
    file.write(util_module)
