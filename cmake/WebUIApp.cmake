# WebUIApp.cmake - Common functions for adding WebUI applications

# add_webui_app(app_name [SOURCE source_file] [ICON icon_file] [ICON_DIR icon_dir])
# Adds an executable linking to webui library, with optional Windows icon resource.
# If SOURCE is not provided, defaults to src/${app_name}.c
# If ICON is provided and ICON_DIR is not, defaults to icons/${ICON}
# Usage:
# add_webui_app(DeepSeek)
# add_webui_app(Qwen ICON qwen.rc)
# add_webui_app(CustomApp SOURCE src/custom/app.c ICON custom.rc ICON_DIR src/custom)
function(add_webui_app app_name)
    set(options "")
    set(oneValueArgs SOURCE ICON ICON_DIR)
    set(multiValueArgs "")
    cmake_parse_arguments(ARG "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

    # Determine source file
    if(ARG_SOURCE)
        set(src_file ${ARG_SOURCE})
    else()
        set(src_file "src/${app_name}.c")
    endif()

    # Add executable
    message(STATUS "Adding WebUI application: ${app_name}")
    add_executable(${app_name} ${src_file})
    target_link_libraries(${app_name} webui)

    # Windows icon resource
    if(WIN32 AND ARG_ICON)
        if(ARG_ICON_DIR)
            set(icon_file "${ARG_ICON_DIR}/${ARG_ICON}")
        endif()

        if(EXISTS ${icon_file})
            message(STATUS "Enabled ${app_name} icon: ${icon_file}")
            target_sources(${app_name} PRIVATE ${icon_file})
        else()
            message(WARNING "Icon file not found: ${icon_file}")
        endif()
    endif()

    # Set window subsystem for non-debug builds
    if(NOT CMAKE_BUILD_TYPE MATCHES "Deb")
        if(MSVC)
            target_link_options(${app_name} PRIVATE /SUBSYSTEM:WINDOWS /ENTRY:mainCRTStartup)
        else()
            target_link_options(${app_name} PRIVATE -mwindows) # -mconsole
        endif()
    endif()
endfunction()

# discover_webui_apps()
# Automatically discover WebUI applications in src/ subdirectories.
# Each subdirectory under src/ is considered an application.
# It should contain a .c file (if multiple, the first one is used).
# Optionally may contain .rc icon file (same basename as .c file).
function(discover_webui_apps)
    message(STATUS "Discovering WebUI applications in src/ subdirectories...")

    # Get all subdirectories under src/
    file(GLOB app_dirs RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}/src" "${CMAKE_CURRENT_SOURCE_DIR}/src/*")
    list(FILTER app_dirs INCLUDE REGEX "^[^.]")
    message(STATUS "Found subdirectories: ${app_dirs}")

    foreach(app_dir ${app_dirs})
        message(STATUS "Checking src/${app_dir}")

        # Check if it's a directory
        if(IS_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/src/${app_dir}")
            # Find .c files in this directory
            file(GLOB c_files RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}/src/${app_dir}/*.c")
            list(LENGTH c_files num_c_files)

            if(num_c_files EQUAL 0)
                message(WARNING "No .c files found in src/${app_dir}, skipping")
                continue()
            endif()

            # Use the first .c file
            list(GET c_files 0 src_file)
            message(STATUS "  Using source: ${src_file}")

            # Determine app name (use directory name)
            set(app_name ${app_dir})

            # Look for .rc file with same basename as source file
            get_filename_component(src_basename ${src_file} NAME_WE)
            set(rc_file "${CMAKE_CURRENT_SOURCE_DIR}/src/${app_dir}/${src_basename}.rc")

            if(EXISTS ${rc_file})
                # Use relative path for icon
                set(icon_file "${src_basename}.rc")
                message(STATUS "  Found icon: ${icon_file}")
                add_webui_app(${app_name} SOURCE ${src_file} ICON ${icon_file} ICON_DIR "${CMAKE_CURRENT_SOURCE_DIR}/src/${app_dir}")
            else()
                # No icon
                message(STATUS "  No icon found")
                add_webui_app(${app_name} SOURCE ${src_file})
            endif()
        endif()
    endforeach()

    message(STATUS "Application discovery complete")
endfunction()