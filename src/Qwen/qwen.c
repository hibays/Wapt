#include "webui.h"

#define TARGET_URL "https://chat.qwen.ai/"

int main() {
	size_t my_window = webui_new_window();
	webui_show(my_window, TARGET_URL);
	webui_clean();
	return 0;
}

#if defined(_MSC_VER)
int APIENTRY WinMain(HINSTANCE hInst, HINSTANCE hInstPrev, PSTR cmdline, int cmdshow) { return main(); }
#endif
