cmake_minimum_required(VERSION 3.12)

include(CheckIPOSupported)
check_ipo_supported(RESULT _IsIPOSupported)

if(_IsIPOSupported)
	message(STATUS "Enabled IPO optimization")
	set(CMAKE_INTERPROCEDURAL_OPTIMIZATION TRUE)
endif()

find_program(CCACHE_FOUND ccache)

if(CCACHE_FOUND)
	message(STATUS "Enabled ccache: ${CCACHE_FOUND}")
	set_property(GLOBAL PROPERTY RULE_LAUNCH_COMPILE ${CCACHE_FOUND})
	set_property(GLOBAL PROPERTY RULE_LAUNCH_LINK ${CCACHE_FOUND}) # Less useful to do it for linking, see edit2
endif()

project(WebUI-Impl)

add_subdirectory(webui)

add_executable(DeepSeek src/deepseek.c)
target_link_libraries(DeepSeek webui)

if(WIN32 AND EXISTS icons/deepseek.rc)
	# linux cmake cant recognize .rc file
	# NOTE: Use MSVC CMake instead of mingw version if build failed here
	target_sources(DeepSeek PRIVATE icons/deepseek.rc)
endif()

if(NOT CMAKE_BUILD_TYPE MATCHES "Deb")
	if(MSVC)
		target_link_options(DeepSeek PRIVATE /SUBSYSTEM:WINDOWS /ENTRY:mainCRTStartup)
	else()
		target_link_options(DeepSeek PRIVATE -mwindows) # -mconsole
	endif()
endif()

add_executable(Qwen src/qwen.c)
target_link_libraries(Qwen webui)

if(WIN32 AND EXISTS icons/qwen.rc)
	# linux cmake cant recognize .rc file
	# NOTE: Use MSVC CMake instead of mingw version if build failed here
	target_sources(Qwen PRIVATE icons/qwen.rc)
endif()

if(NOT CMAKE_BUILD_TYPE MATCHES "Deb")
	if(MSVC)
		target_link_options(Qwen PRIVATE /SUBSYSTEM:WINDOWS /ENTRY:mainCRTStartup)
	else()
		target_link_options(Qwen PRIVATE -mwindows) # -mconsole
	endif()
endif()

add_executable(Desmos src/desmos.c)
target_link_libraries(Desmos webui)

if(WIN32 AND EXISTS icons/desmos.rc)
	# linux cmake cant recognize .rc file
	# NOTE: Use MSVC CMake instead of mingw version if build failed here
	target_sources(Desmos PRIVATE icons/desmos.rc)
endif()

if(NOT CMAKE_BUILD_TYPE MATCHES "Deb")
	if(MSVC)
		target_link_options(Desmos PRIVATE /SUBSYSTEM:WINDOWS /ENTRY:mainCRTStartup)
	else()
		target_link_options(Desmos PRIVATE -mwindows) # -mconsole
	endif()
endif()

add_executable(Kimi src/kimi.c)
target_link_libraries(Kimi webui)

if(WIN32 AND EXISTS icons/kimi.rc)
	# linux cmake cant recognize .rc file
	# NOTE: Use MSVC CMake instead of mingw version if build failed here
	target_sources(Kimi PRIVATE icons/kimi.rc)
endif()

if(NOT CMAKE_BUILD_TYPE MATCHES "Deb")
	if(MSVC)
		target_link_options(Kimi PRIVATE /SUBSYSTEM:WINDOWS /ENTRY:mainCRTStartup)
	else()
		target_link_options(Kimi PRIVATE -mwindows) # -mconsole
	endif()
endif()
