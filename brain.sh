#!/bin/bash

br="brain.sh"

f_help() {
    echo "Usage: $br [arguments]"
    echo "Example: $br build"
    echo "$br help"
}

if [ $# -eq 0 ]; then
    echo "No arguments provided."
    f_help
    exit 1
fi

get_ini_value() {
    local value=$(awk -F '=' '/^\['$1'\]/{f=1} f==1&&$1~/'$2'/{print $2; f=0}' "$3")
    echo "$value"
}

SOURCE_DIR="src"
BUILD_DIR="build"
SOURCE_FILE="lib.cpp"
INI_FILE="cfg.ini"

build_32b() {
    clang -shared -fPIC -m32 -o "$BUILD_DIR/$(get_ini_value "Out" "x32" "$INI_FILE")" "$SOURCE_DIR/$SOURCE_FILE"
}

build_64b() {
    clang -shared -fPIC -o "$BUILD_DIR/$(get_ini_value "Out" "x64" "$INI_FILE")" "$SOURCE_DIR/$SOURCE_FILE"
}

build_ARMv7() {
    clang -shared -fPIC -march=armv7-a -o "$BUILD_DIR/$(get_ini_value "Out" "armv7" "$INI_FILE")" "$SOURCE_DIR/$SOURCE_FILE"
}

build_ARM64() {
    clang -shared -fPIC -o "$BUILD_DIR/$(get_ini_value "Out" "arm64" "$INI_FILE")" "$SOURCE_DIR/$SOURCE_FILE"
}

if_clang() {
    if ! command -v clang &> /dev/null; then
        echo "Clang is not installed. Attempting to install..."
        apt update
        apt install clang -y

        if [ $? -eq 0 ]; then
            echo "Clang has been successfully installed."
        else
            echo "Failed to install Clang. Exiting."
            exit 1
        fi
    else
        echo "Clang is already installed."
    fi
}

if [ "$1" == "help" ]; then
    f_help
    exit 0
fi

echo "Run Task $1"
try="true"

if [ "$1" == "build" ]; then
    bash "$br" "install"

    mkdir -p "$BUILD_DIR"

    if [ "$(get_ini_value "build" "x32" "$INI_FILE")" == "$try" ]; then
        echo "build x32"
        build_32b
    fi
    if [ "$(get_ini_value "build" "x64" "$INI_FILE")" == "$try" ]; then
        echo "build x64"
        build_64b
    fi
    if [ "$(get_ini_value "build" "armv7" "$INI_FILE")" == "$try" ]; then
        echo "build armv7"
        build_ARMv7
    fi
    if [ "$(get_ini_value "build" "arm64" "$INI_FILE")" == "$try" ]; then
        echo "build arm64"
        build_ARM64
    fi
    echo "Compiler Finish"
    exit 0
fi

if [ "$1" == "delete" ]; then
    apt remove clang -y
    rm -r "$BUILD_DIR"
    exit 0
fi

c_ini() {
    if [ ! -f "$INI_FILE" ]; then
        echo "[Drs_files]" >> "$INI_FILE"
        echo "source=src" >> "$INI_FILE"
        echo "build=build" >> "$INI_FILE"
        echo "source_file=lib.cpp" >> "$INI_FILE"

        echo "[build]" >> "$INI_FILE"
        echo "x32=true" >> "$INI_FILE"
        echo "x64=true" >> "$INI_FILE"
        echo "armv7=true" >> "$INI_FILE"
        echo "arm64=true" >> "$INI_FILE"

        echo "[Out]" >> "$INI_FILE"
        echo "x32=my_library_x86.so" >> "$INI_FILE"
        echo "x64=my_library_x86_64.so" >> "$INI_FILE"
        echo "armv7=my_library_armv7.so" >> "$INI_FILE"
        echo "arm64=my_library_arm64.so" >> "$INI_FILE"
    fi
}

if [ "$1" == "install" ]; then
    c_ini
    if_clang
    exit 0
fi

echo "Invalid Argument"
exit 1
