set(HOST_PLATFORM "linux_x64")

if(APPLE)
  set(HOST_PLATFORM "macOS")
elseif (UNIX)
  execute_process(COMMAND uname -m OUTPUT_VARIABLE MACHINES OUTPUT_STRIP_TRAILING_WHITESPACE)
  execute_process(COMMAND getconf LONG_BIT OUTPUT_VARIABLE MACHINES_BIT OUTPUT_STRIP_TRAILING_WHITESPACE)

  if ((${MACHINES} MATCHES "x86_64") AND (${MACHINES_BIT} MATCHES "64"))
    set(HOST_PLATFORM "linux_x64")
  elseif (${MACHINES} MATCHES "arm")
    set(HOST_PLATFORM "arm32")
  elseif ((${MACHINES} MATCHES "aarch64") AND (${MACHINES_BIT} MATCHES "64"))
    set(HOST_PLATFORM "arm64")
  elseif ((${MACHINES} MATCHES "aarch64") AND (${MACHINES_BIT} MATCHES "32"))
    set(HOST_PLATFORM "arm32")
  endif ()
elseif (WIN32)
  if (CMAKE_SIZEOF_VOID_P EQUAL 8)
    set(HOST_PLATFORM "win_x64")
  elseif (CMAKE_SIZEOF_VOID_P EQUAL 4)
    set(HOST_PLATFORM "win_x86")
  endif ()
endif ()
message(STATUS "Host platform set to: ${HOST_PLATFORM}")
