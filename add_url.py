from pathlib import Path
import argparse as ap
import sys
import subprocess as sp

c_url_template = """#include "webui.h"

#define TARGET_URL "%s"

int main() {
	size_t my_window = webui_new_window();
	webui_show(my_window, TARGET_URL);
	webui_clean();
	return 0;
}

#if defined(_MSC_VER)
int APIENTRY WinMain(HINSTANCE hInst, HINSTANCE hInstPrev, PSTR cmdline, int cmdshow) { return main(); }
#endif
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

icon_template = """101 ICON {}
"""


class Proj_creater(object):
	def __init__(
	    self, target_name: str, cf_name: str, url: str, icon_path: str | None
	) -> None:
		self.target_name = target_name
		self.cf_name = cf_name
		self.url = url
		self.icon_path = icon_path

	def release_proj(self, target_path: str):
		'''Release target proj dir to target_path'''
		pass

	def gen_cmake(self):
		cmake_code = cmake_template.format(self.target_name, self.cf_name)
		if self.icon_path:
			cmake_code += cmake_icon_ext.format(self.target_name, self.cf_name)
		return cmake_code

	def gen_c_code(self):
		return c_url_template % self.url

	def gen_icon_rc(self):
		return icon_template.format("%s.ico" % self.cf_name)

	def gen_icon_ico(self):
		return icon_template.format("%s.ico" % self.cf_name)


def add_url(
    target_name: str, cf_name: str, url: str, icon_path: str | None = None
):

	c_code = c_url_template % url
	Path("src", f"{cf_name}.c").write_text(c_code)

	cmake_code = cmake_template.format(target_name, cf_name)
	with open("CMakeLists.txt", "a") as f:
		f.write(cmake_code)
		if icon_path:
			cmake_code = cmake_icon_ext.format(target_name, cf_name)
			f.write(cmake_code)

	if icon_path:
		rc_code = icon_template.format(f"{cf_name}.ico")
		Path("icons", f"{cf_name}.rc").write_text(rc_code)
		icp = Path(icon_path)
		if icp.suffix != ".ico":
			try:
				err_info = sp.check_output(
				    f"""ffmpeg -hide_banner -i {icp.absolute()} -filter_complex "split=6[a][b][c][d][e][f];[a]scale=16:16[b];[b]scale=32:32[c];[c]scale=48:48[d];[d]scale=64:64[e];[e]scale=128:128[f];[f]scale=256:256[g]" -map "[b]" -map "[c]" -map "[d]" -map "[e]" -map "[f]" -map "[g]" -c:v bmp icons/{cf_name}.ico"""
				)
				if b'Error' in err_info.split(b'\n')[-1]:
					print('FFMpeg ran into error: %s' % err_info)
			except sp.CalledProcessError:
				print(
				    "Failed to convert icon to .ico format, please check ffmpeg installation"
				)
		else:
			Path("icons", f"{cf_name}.ico").write_bytes(icp.read_bytes())


def main():
	if sys.argv.__len__() < 2:
		print("-- Interactive mode")

		target_name = input(
		    "Enter the cmake target name (as is execution name): "
		)
		cf_name = input("Enter the c file name (without extension): ")
		url = input("Enter the URL: ")
		icon_path = input("Enter the icon path (leave empty if no any): ")

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
		icon_path = args.icon

	return add_url(target_name, cf_name, url, icon_path)


if __name__ == "__main__":
	main()
