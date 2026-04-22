#include "webui.h"

int main() {
	size_t my_window = webui_new_window();
	webui_show(my_window, "https://chat.deepseek.com");
	webui_clean();
	return 0;
}

#if defined(_MSC_VER)
int APIENTRY WinMain(HINSTANCE hInst, HINSTANCE hInstPrev, PSTR cmdline, int cmdshow) { return main(); }
#endif
