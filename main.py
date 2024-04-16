#!/usr/bin/env python3

import subprocess
import os

br = "brain.py"

def f_help():
    print("Usage:", br, "[arguments]")
    print("Example:", br, "build")
    print(br, "help")

def get_ini_value(section, key, file_name):
    with open(file_name, 'r') as file:
        for line in file:
            if line.strip() == '[' + section + ']':
                break
        for line in file:
            if line.strip().startswith('['):
                break
            if key in line:
                return line.split('=')[1].strip()

def build_32b(source_dir, build_dir, source_file, ini_file):
    subprocess.run(["clang", "-shared", "-fPIC", "-m32", "-o", os.path.join(build_dir, get_ini_value("Out", "x32", ini_file)), os.path.join(source_dir, source_file)])

def build_64b(source_dir, build_dir, source_file, ini_file):
    subprocess.run(["clang", "-shared", "-fPIC", "-o", os.path.join(build_dir, get_ini_value("Out", "x64", ini_file)), os.path.join(source_dir, source_file)])

def build_ARMv7(source_dir, build_dir, source_file, ini_file):
    subprocess.run(["clang", "-shared", "-fPIC", "-march=armv7-a", "-o", os.path.join(build_dir, get_ini_value("Out", "armv7", ini_file)), os.path.join(source_dir, source_file)])

def build_ARM64(source_dir, build_dir, source_file, ini_file):
    subprocess.run(["clang", "-shared", "-fPIC", "-o", os.path.join(build_dir, get_ini_value("Out", "arm64", ini_file)), os.path.join(source_dir, source_file)])

def if_clang():
    try:
        subprocess.run(["clang", "--version"], check=True)
        print("Clang is already installed.")
    except subprocess.CalledProcessError:
        print("Clang is not installed. Attempting to install...")
        subprocess.run(["apt", "update"])
        subprocess.run(["apt", "install", "clang", "-y"])

def c_ini(ini_file):
    if not os.path.isfile(ini_file):
        with open(ini_file, 'w') as file:
            file.write("[Drs_files]\n")
            file.write("source=src\n")
            file.write("build=build\n")
            file.write("source_file=lib.cpp\n")
            file.write("\n")
            file.write("[build]\n")
            file.write("x32=true\n")
            file.write("x64=true\n")
            file.write("armv7=true\n")
            file.write("arm64=true\n")
            file.write("\n")
            file.write("[Out]\n")
            file.write("x32=my_library_x86.so\n")
            file.write("x64=my_library_x86_64.so\n")
            file.write("armv7=my_library_armv7.so\n")
            file.write("arm64=my_library_arm64.so\n")

def main():
    import sys

    if len(sys.argv) < 2:
        print("No arguments provided.")
        f_help()
        sys.exit(1)

    SOURCE_DIR = "src"
    BUILD_DIR = "build"
    SOURCE_FILE = "lib.cpp"
    INI_FILE = "cfg.ini"

    if sys.argv[1] == "help":
        f_help()
        sys.exit(0)

    print("Run Task", sys.argv[1])

    if sys.argv[1] == "build":
        subprocess.run([br, "install"])
        os.makedirs(BUILD_DIR, exist_ok=True)

        if get_ini_value("build", "x32", INI_FILE) == "true":
            print("build x32")
            build_32b(SOURCE_DIR, BUILD_DIR, SOURCE_FILE, INI_FILE)
        if get_ini_value("build", "x64", INI_FILE) == "true":
            print("build x64")
            build_64b(SOURCE_DIR, BUILD_DIR, SOURCE_FILE, INI_FILE)
        if get_ini_value("build", "armv7", INI_FILE) == "true":
            print("build armv7")
            build_ARMv7(SOURCE_DIR, BUILD_DIR, SOURCE_FILE, INI_FILE)
        if get_ini_value("build", "arm64", INI_FILE) == "true":
            print("build arm64")
            build_ARM64(SOURCE_DIR, BUILD_DIR, SOURCE_FILE, INI_FILE)

        print("Compiler Finish")
        sys.exit(0)

    if sys.argv[1] == "delete":
        subprocess.run(["apt", "remove", "clang", "-y"])
        subprocess.run(["rm", "-r", BUILD_DIR])
        sys.exit(0)

    if sys.argv[1] == "install":
        c_ini(INI_FILE)
        if_clang()
        sys.exit(0)

    print("Invalid Argument")
    sys.exit(1)

if __name__ == "__main__":
    main()
