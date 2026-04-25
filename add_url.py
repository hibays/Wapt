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

icon_template = """101 ICON "{}"
"""


def add_url(
    target_name: str, cf_name: str, url: str, icon_path: str | None = None
):
	# Create application directory
	app_dir = Path("src") / target_name
	app_dir.mkdir(parents=True, exist_ok=True)

	# Write C source file
	c_code = c_url_template % url
	(app_dir / f"{cf_name}.c").write_text(c_code)

	# No longer need to modify CMakeLists.txt directly
	# The discover_webui_apps() function will automatically find the application

	if icon_path:
		# Write .rc file
		rc_code = icon_template.format(f"{cf_name}.ico")
		(app_dir / f"{cf_name}.rc").write_text(rc_code)

		# Process icon file
		icp = Path(icon_path)
		icon_output = app_dir / f"{cf_name}.ico"

		if icp.suffix != ".ico":
			try:
				err_info = sp.check_output(
				    f"""ffmpeg -hide_banner -i {icp.absolute()} -filter_complex "split=6[a][b][c][d][e][f];[a]scale=16:16[b];[b]scale=32:32[c];[c]scale=48:48[d];[d]scale=64:64[e];[e]scale=128:128[f];[f]scale=256:256[g]" -map "[b]" -map "[c]" -map "[d]" -map "[e]" -map "[f]" -map "[g]" -c:v bmp {icon_output.absolute()}"""
				)
				if b'Error' in err_info.split(b'\n')[-1]:
					print('FFMpeg ran into error: %s' % err_info)
			except sp.CalledProcessError:
				print(
				    "Failed to convert icon to .ico format, please check ffmpeg installation"
				)
		else:
			icon_output.write_bytes(icp.read_bytes())


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
