cmake_minimum_required(VERSION 3.5)

project(SkiaTest
	VERSION 0.0.0
	LANGUAGES CXX
)

add_executable(SkiaTestApp ${CMAKE_SOURCE_DIR}/src/main.cpp)

set(SKIA_SOURCE_DIR ${CMAKE_SOURCE_DIR}/externals/skia/source/skia)
set(SKIA_HEADERS 
	${SKIA_SOURCE_DIR}
	${SKIA_SOURCE_DIR}/include
	${SKIA_SOURCE_DIR}/include/android
	${SKIA_SOURCE_DIR}/include/codec
	${SKIA_SOURCE_DIR}/include/config
	${SKIA_SOURCE_DIR}/include/core
	${SKIA_SOURCE_DIR}/include/docs
	${SKIA_SOURCE_DIR}/include/effects
	${SKIA_SOURCE_DIR}/include/encode
	${SKIA_SOURCE_DIR}/include/gpu
	${SKIA_SOURCE_DIR}/include/pathops
	${SKIA_SOURCE_DIR}/include/ports
	${SKIA_SOURCE_DIR}/include/private
	${SKIA_SOURCE_DIR}/include/sksl
	${SKIA_SOURCE_DIR}/include/svg
	${SKIA_SOURCE_DIR}/include/third_party
	${SKIA_SOURCE_DIR}/include/utils
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