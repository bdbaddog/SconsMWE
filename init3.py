import os

main_program = """
program main
    use module0
    use module1
    use module2
    use util_module
    implicit none
end program main
"""
module0 = """
module module0
    implicit none
end module module0
"""
module1 = """
module module1
    implicit none
end module module1
"""
module2 = """
module module2
    use module0
    use module1
    implicit none
end module module2
"""
util_module = """
module util_module
    implicit none
end module util_module
"""
with open("main.f90", "w") as file:
    file.write(main_program)
with open("module0.f90", "w") as file:
    file.write(module0)
with open("module1.f90", "w") as file:
    file.write(module1)
with open("module2.f90", "w") as file:
    file.write(module2)
with open("util_module.f90", "w") as file:
    file.write(util_module)
