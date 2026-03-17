from pathlib import Path
import argparse as ap
import sys

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

if(NOT CMAKE_BUILD_TYPE MATCHES "Deb")
	if(MSVC)
		target_link_options({0} PRIVATE /SUBSYSTEM:WINDOWS /ENTRY:mainCRTStartup)
	else()
		target_link_options({0} PRIVATE -mwindows) # -mconsole
	endif()
endif()
"""

cmake_icon_ext = """
if(WIN32)
	# linux cmake cant recognize .rc file
	# NOTE: Use MSVC CMake instead of mingw version if build failed here
	message(STATUS "Enabled {0} icon")
	target_sources({0} PRIVATE icons/{1}.rc)
endif()
"""

icon_template = """
101 ICON {}
"""


def add_url(target_name: str, cf_name: str, url: str, icon: str | None = None):

	c_code = c_url_template % url
	Path("src", f"{cf_name}.c").write_text(c_code)

	cmake_code = cmake_template.format(target_name, cf_name)
	with open("CMakeLists.txt", "a") as f:
		f.write(cmake_code)
		if icon:
			cmake_code = cmake_icon_ext.format(target_name, cf_name)
			f.write(cmake_code)

	if icon:
		icon_code = icon_template.format(icon)
		Path("icons", f"{target_name}.rc").write_text(icon_code)
		print(f"Icon rc:\n{icon_code}")


def main():
	if sys.argv.__len__() < 2:
		print("-- Interactive mode")

		target_name = input(
		    "Enter the cmake target name (as is execution name): "
		)
		cf_name = input("Enter the c file name (without extension): ")
		url = input("Enter the URL: ")
		icon = input("Enter the icon path (leave empty if no any): ")

	else:
		print("-- CLI mode")
		ap_parser = ap.ArgumentParser()
		ap_parser.add_argument(
		    "--name",
		    type=str,
		    required=True,
		    help="The cmake target name (as is execution name)"
		)
		ap_parser.add_argument("--url", type=str, required=True, help="The URL")
		ap_parser.add_argument(
		    "--icon",
		    type=str,
		    default=None,
		    help="The icon path (leave empty if no any)"
		)
		args = ap_parser.parse_args()

		target_name = args.name
		cf_name = args.name
		url = args.url
		icon = args.icon

	return add_url(target_name, cf_name, url, icon)


if __name__ == "__main__":
	main()
