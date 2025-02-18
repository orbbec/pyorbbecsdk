# Set the target system's environment
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR x86_64)

# Set the path to the sysroot
set(CMAKE_SYSROOT ${CMAKE_CURRENT_SOURCE_DIR}/cc-env/sysroot/ubuntu-16.04)

# Set the cross-compilation compiler paths
set(CMAKE_C_COMPILER ${CMAKE_CURRENT_SOURCE_DIR}/cc-env/sysroot/ubuntu-16.04/usr/bin/gcc)
set(CMAKE_CXX_COMPILER ${CMAKE_CURRENT_SOURCE_DIR}/cc-env/sysroot/ubuntu-16.04/usr/bin/g++)

# Add the sysroot paths for includes and libraries
set(CMAKE_INCLUDE_PATH ${CMAKE_SYSROOT}/usr/include)
set(CMAKE_LIBRARY_PATH ${CMAKE_SYSROOT}/usr/lib)

# Set appropriate C++ ABI flags for older glibc versions
set(CMAKE_CXX_FLAGS "-D_GLIBCXX_USE_CXX11_ABI=0 -fPIC -O3")

# Specify the path for dynamic linker
set(CMAKE_EXE_LINKER_FLAGS "-L${CMAKE_SYSROOT}/usr/lib")
