cmake_minimum_required(VERSION 3.15)
project(pyorbbecsdk)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_C_STANDARD 11)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fPIC -O3")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC -O3")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -fPIC -g")
set(CMAKE_BUILD_TYPE "Release") 

# Install prefix
set(CMAKE_INSTALL_PREFIX "${CMAKE_CURRENT_SOURCE_DIR}/install")

set(CMAKE_BUILD_RPATH_USE_ORIGIN TRUE) 
set(CMAKE_INSTALL_RPATH "$ORIGIN")
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

option(BUILD_TESTING "Build tests" ON)

if (CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif ()

# Platform-specific library prefix and suffix
if (WIN32)
  set(ORBBEC_LIB_PREFIX "")
  set(ORBBEC_LIB_SUFFIX ".lib")
elseif (APPLE)
  set(ORBBEC_LIB_PREFIX "lib")
  set(ORBBEC_LIB_SUFFIX ".dylib")
elseif (UNIX)
  set(ORBBEC_LIB_PREFIX "lib")
  set(ORBBEC_LIB_SUFFIX ".so")
endif ()

# Determine host platform
include(${CMAKE_CURRENT_SOURCE_DIR}/cmake/DetermineHostPlatform.cmake)

# Orbbec SDK paths
if(APPLE)
  set(ORBBEC_LIBS ${CMAKE_CURRENT_SOURCE_DIR}/sdk/lib/macOS)
else()
  set(ORBBEC_LIBS ${CMAKE_CURRENT_SOURCE_DIR}/sdk/lib/${HOST_PLATFORM})
endif()
set(ORBBEC_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/sdk/include/)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
find_package(pybind11 REQUIRED)

link_directories(${ORBBEC_LIBS})

# Python extension module
pybind11_add_module(${PROJECT_NAME}
  src/pyorbbecsdk/pyorbbecsdk.cpp
  src/pyorbbecsdk/context.cpp
  src/pyorbbecsdk/device.cpp
  src/pyorbbecsdk/error.cpp
  src/pyorbbecsdk/filter.cpp
  src/pyorbbecsdk/frame.cpp
  src/pyorbbecsdk/pipeline.cpp
  src/pyorbbecsdk/properties.cpp
  src/pyorbbecsdk/sensor.cpp
  src/pyorbbecsdk/stream_profile.cpp
  src/pyorbbecsdk/types.cpp
  src/pyorbbecsdk/utils.cpp
  src/pyorbbecsdk/record_playback.cpp
)

set_target_properties(${PROJECT_NAME} PROPERTIES
    SKIP_BUILD_RPATH FALSE
    BUILD_WITH_INSTALL_RPATH FALSE
    INSTALL_RPATH "$ORIGIN"
    BUILD_RPATH "$ORIGIN"
    PREFIX ""
)

if (UNIX AND NOT APPLE)
    target_link_options(${PROJECT_NAME} PRIVATE
        "LINKER:--enable-new-dtags"
    )
endif ()

if (CMAKE_CXX_COMPILER_ID MATCHES "Clang" AND NOT APPLE)
  target_link_libraries(${PROJECT_NAME} PRIVATE atomic)
endif ()

target_include_directories(${PROJECT_NAME} PRIVATE
  ${ORBBEC_INCLUDE_DIR}
  src/pyorbbecsdk/
)

if (UNIX)
  target_link_libraries(${PROJECT_NAME} PRIVATE
    ${ORBBEC_LIBS}/libOrbbecSDK${ORBBEC_LIB_SUFFIX}
  )
elseif (WIN32)
  target_link_libraries(${PROJECT_NAME} PRIVATE
    OrbbecSDK
  )
endif ()

# Fix rpath on macOS after build
if (APPLE)
  add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
    COMMAND install_name_tool -change "@rpath/libOrbbecSDK.2.dylib" "@loader_path/libOrbbecSDK.2.dylib" $<TARGET_FILE:${PROJECT_NAME}>
    COMMENT "Fixing rpath for macOS"
  )
endif ()

# ===============================
# Tests
# ===============================
set(PY_TEST_SRCS
  test/test_context.py
  test/test_device.py
  test/test_pipeline.py
  test/test_sensor_control.py
)

if (BUILD_TESTING)
  enable_testing()
  if (TARGET Python3::Interpreter)
    set(Python3_EXECUTABLE Python3::Interpreter)
  endif()
  set(ENV{PYTHONPATH} "${CMAKE_CURRENT_BINARY_DIR}:$ENV{PYTHONPATH}")
  foreach (PY_TEST_SRC ${PY_TEST_SRCS})
    get_filename_component(PY_TEST_NAME ${PY_TEST_SRC} NAME_WE)
    add_test(NAME ${PY_TEST_NAME}
      COMMAND ${Python3_EXECUTABLE} -v ${CMAKE_CURRENT_SOURCE_DIR}/${PY_TEST_SRC}
    )
  endforeach ()
endif ()

# ===============================
# Installation layout
# ===============================

# Final Python package directory
set(PY_PACKAGE_DIR ${CMAKE_INSTALL_PREFIX}/lib/pyorbbecsdk)

# 1. Install pybind11 extension module (.pyd / .so)
install(TARGETS ${PROJECT_NAME}
  LIBRARY DESTINATION ${PY_PACKAGE_DIR}
  RUNTIME DESTINATION ${PY_PACKAGE_DIR}
)

# 2. Install OrbbecSDK shared libraries
if (APPLE)
  install(DIRECTORY ${ORBBEC_LIBS}/
          DESTINATION ${PY_PACKAGE_DIR}
          FILES_MATCHING 
            PATTERN "*.dylib"
            PATTERN "*.md"
            PATTERN "*.xml")
elseif (UNIX)
  install(DIRECTORY ${ORBBEC_LIBS}/
          DESTINATION ${PY_PACKAGE_DIR}
          FILES_MATCHING
            PATTERN "*.so*"
            PATTERN "*.md"
            PATTERN "*.xml")
elseif (WIN32)
  install(DIRECTORY ${ORBBEC_LIBS}/
          DESTINATION ${PY_PACKAGE_DIR}
          FILES_MATCHING
            PATTERN "*.dll"
            PATTERN "*.lib"
            PATTERN "*.md"
            PATTERN "*.xml")
endif ()

# 3. Examples
if (EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/examples)
  install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/examples
          DESTINATION ${PY_PACKAGE_DIR})
endif ()

# 4. Config files
if (EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/config)
  install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/config
          DESTINATION ${PY_PACKAGE_DIR})
endif ()

# 5. env_setup scripts
if (EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/scripts/env_setup)
  if (WIN32)
    install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/scripts/env_setup/
            DESTINATION ${PY_PACKAGE_DIR}/shared
            FILES_MATCHING
              PATTERN "*.md"
              PATTERN "*.ps1"
              PATTERN "setup_env.py")
  elseif (UNIX)
    install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/scripts/env_setup/
            DESTINATION ${PY_PACKAGE_DIR}/shared
            FILES_MATCHING
              PATTERN "*.rules"
              PATTERN "*.sh"
              PATTERN "setup_env.py")
  endif ()
endif ()

# 6. Extension directory 
if (EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/extension)
  install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/extension
          DESTINATION ${PY_PACKAGE_DIR})
endif ()

if (EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/cmake/UninstallTarget.cmake)
    include(${CMAKE_CURRENT_SOURCE_DIR}/cmake/UninstallTarget.cmake)
endif ()