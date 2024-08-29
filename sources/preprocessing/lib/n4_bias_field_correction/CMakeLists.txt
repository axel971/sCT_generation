CMAKE_MINIMUM_REQUIRED(VERSION 2.8.8)

SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")

PROJECT(n4_bias_field_correction)


find_package(ITK REQUIRED)
include(${ITK_USE_FILE})

add_executable(${PROJECT_NAME} ./source/n4_bias_field_correction.cpp)
target_link_libraries(${PROJECT_NAME} ${ITK_LIBRARIES})


