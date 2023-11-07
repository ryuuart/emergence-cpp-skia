cmake_minimum_required(VERSION 3.5)

project(SkiaTest
	VERSION 0.0.0
	LANGUAGES CXX
)

add_executable(SkiaTestApp ${CMAKE_SOURCE_DIR}/src/main.cpp)

set(SKIA_SOURCE_DIR ${CMAKE_SOURCE_DIR}/externals/skia/source/skia)
set(SKIA_HEADERS 
	${SKIA_SOURCE_DIR}
)
include_directories(${SKIA_HEADERS})

set(SKIA_LIB_DIR "${SKIA_SOURCE_DIR}/out/StaticAppleSilicon")

find_package(OpenGL REQUIRED)

if (APPLE)
    target_link_libraries(SkiaTestApp PRIVATE "-framework Cocoa")
endif()

target_link_libraries(SkiaTestApp 
	PRIVATE 
		${SKIA_LIB_DIR}/libskia.a
)

target_compile_features(SkiaTestApp PRIVATE cxx_std_17)