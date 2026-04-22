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

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

add_subdirectory(thirdlib/webui-2f7e622 EXCLUDE_FROM_ALL)

include(cmake/WebUIApp.cmake)
discover_webui_apps()
