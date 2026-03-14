import os
from pathlib import Path

c_url_template = """
#include "webui.h"

int main() {
	size_t my_window = webui_new_window();
	webui_show(my_window, "%s");
	webui_clean();
	return 0;
}
"""

cmake_template = """
add_executable({0} src/{1}.c)
target_link_libraries({0} webui)

if(WIN32 AND EXISTS icons/{1}.rc)
	# linux cmake cant recognize .rc file
	# NOTE: Use MSVC CMake instead of mingw version if build failed here
	target_sources({0} PRIVATE icons/{1}.rc)
endif()

if(NOT CMAKE_BUILD_TYPE MATCHES "Deb")
	if(MSVC)
		target_link_options({0} PRIVATE /SUBSYSTEM:WINDOWS /ENTRY:mainCRTStartup)
	else()
		target_link_options({0} PRIVATE -mwindows) # -mconsole
	endif()
endif()
"""

icon_template = """
IDI_ICON1 ICON {}
"""


def main():
	target_name = input("Enter the cmake target name (as is execution name): ")
	cf_name = input("Enter the c file name (without extension): ")
	url = input("Enter the URL: ")
	icon = input("Enter the icon path (leave empty if no any): ")

	c_code = c_url_template % url
	(Path("src") / f"{cf_name}.c").write_text(c_code)

	cmake_code = cmake_template.format(target_name, cf_name)
	with open("CMakeLists.txt", "a") as f:
		f.write(cmake_code)

	if not icon:
		return

	icon_code = icon_template.format(icon)
	(Path("icons") / f"{target_name}.rc").write_text(icon_code)


if __name__ == "__main__":
	main()
