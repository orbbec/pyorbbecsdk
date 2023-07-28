cmake_minimum_required(VERSION 3.15)
project(pyorbbecsdk)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fPIC -O3")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG}  -fPIC -g")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC -O3")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -fPIC -g")
set(CMAKE_BUILD_TYPE "Release")
set(CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_SOURCE_DIR}/install)
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")
set(BUILD_TESTING ON CACHE BOOL "Build tests" FORCE)

if (CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif ()

if (WIN32)
  set(ORBBEC_LIB_PREFIX "")
  set(ORBBEC_LIB_SUFFIX ".lib")
elseif (UNIX)
  set(ORBBEC_LIB_PREFIX "lib")
  set(ORBBEC_LIB_SUFFIX ".so")
endif ()
# Determine host platform
include(${CMAKE_CURRENT_SOURCE_DIR}/cmake/DetermineHostPlatform.cmake)

set(ORBBEC_LIBS ${CMAKE_CURRENT_SOURCE_DIR}/sdk/lib/${HOST_PLATFORM})
set(ORBBEC_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/sdk/include/)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
find_package(pybind11 REQUIRED)
link_directories(${ORBBEC_LIBS})

pybind11_add_module(${PROJECT_NAME} SHARED
  src/pyorbbecsdk/pyorbbecsdk.cpp
  src/pyorbbecsdk/context.cpp
  src/pyorbbecsdk/device.cpp
  src/pyorbbecsdk/error.cpp
  src/pyorbbecsdk/filter.cpp
  src/pyorbbecsdk/frame.cpp
  src/pyorbbecsdk/pipeline.cpp
  src/pyorbbecsdk/properties.cpp
  src/pyorbbecsdk/record_playback.cpp
  src/pyorbbecsdk/sensor.cpp
  src/pyorbbecsdk/stream_profile.cpp
  src/pyorbbecsdk/types.cpp
  src/pyorbbecsdk/utils.cpp
  )

if (CMAKE_C_COMPILER_ID MATCHES "Clang" AND NOT APPLE)
  target_link_libraries(${PROJECT_NAME} PRIVATE atomic)
endif ()

target_include_directories(${PROJECT_NAME} PRIVATE
  ${ORBBEC_INCLUDE_DIR}
  src/pyorbbecsdk/
  )

if (UNIX)
  target_link_libraries(${PROJECT_NAME} PRIVATE
    -lOrbbecSDK
    -L${ORBBEC_LIBS}
    )
elseif (WIN32)
  target_link_libraries(${PROJECT_NAME} PRIVATE
    OrbbecSDK
    )
endif ()

set(PY_TEST_SRCS
  test/test_context.py
  test/test_device.py
  test/test_pipeline.py
  test/test_sensor_control.py
  )

if (BUILD_TESTING)
  enable_testing()
  set(Python3_EXECUTABLE Python3::Interpreter)
  set(ENV{PYTHONPATH} "${CMAKE_CURRENT_BINARY_DIR}:$ENV{PYTHONPATH}")
  foreach (PY_TEST_SRC ${PY_TEST_SRCS})
    get_filename_component(PY_TEST_NAME ${PY_TEST_SRC} NAME_WE)
    add_test(NAME ${PY_TEST_NAME}
      COMMAND ${Python3_EXECUTABLE} -v ${CMAKE_CURRENT_SOURCE_DIR}/${PY_TEST_SRC}
      )
  endforeach ()
endif ()

install(TARGETS ${PROJECT_NAME}
  LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX}/lib
  RUNTIME DESTINATION ${CMAKE_INSTALL_PREFIX}/lib)

if (UNIX)
  install(DIRECTORY ${ORBBEC_LIBS}/
    DESTINATION ${CMAKE_INSTALL_PREFIX}/lib
    FILES_MATCHING PATTERN "*.so"
    PATTERN "*.so.*"
    )
elseif (WIN32)
  install(DIRECTORY ${ORBBEC_LIBS}/
    DESTINATION ${CMAKE_INSTALL_PREFIX}/lib
    FILES_MATCHING PATTERN "*.lib"
    PATTERN "*.dll"
    )
endif ()
include(${CMAKE_CURRENT_SOURCE_DIR}/cmake/UninstallTarget.cmake)
