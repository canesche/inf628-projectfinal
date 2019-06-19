cmake_minimum_required(VERSION 2.8)

project(genetic-algorithm)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS_RELEASE "-O3")

if (NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif ()

include_directories("${CMAKE_PREFIX_PATH}/include" "${CMAKE_SOURCE_DIR}/include")

file(GLOB CPP_SRCS *.cpp)
file(GLOB H_SRCS *.h)

add_executable(genetic_algorithm ${CPP_SRCS} ${H_SRCS})
