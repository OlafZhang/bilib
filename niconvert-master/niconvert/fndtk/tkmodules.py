import os
from os.path import join, dirname
from pathlib import Path
import tkinter
import tkinter.ttk
import tkinter.font
import tkinter.filedialog
import tkinter.messagebox
import tkinter.scrolledtext

tk = tkinter
ttk = tkinter.ttk

# MonkeyPatch 来让 ScrolledText 用上 ttk 的组件
tk.scrolledtext.Frame = ttk.Frame
tk.scrolledtext.Scrollbar = ttk.Scrollbar
ttk.ScrolledText = tk.scrolledtext.ScrolledText

class tku:

    @staticmethod
    def add_border_space(widget, padx, pady, recursive=True):
        ''' 给每个 widget 增加指定像素的距离 '''
        widget.pack_configure(padx=padx, pady=pady)
        if recursive:
            for subwidget in widget.pack_slaves():
                subwidget.pack_configure(padx=padx, pady=pady)
            for subwidget in widget.grid_slaves():
                subwidget.grid_configure(padx=padx, pady=pady)

    @staticmethod
    def move_to_screen_center(win):
        ''' 把窗口移动到屏幕中间 '''
        win.update_idletasks()
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        window_size = win.geometry().split('+')[0]
        window_width, window_height = map(int, window_size.split('x'))
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        y -= 40  # 状态栏大约高度
        win.geometry('{:d}x{:d}+{:d}+{:d}'.format(
            window_width, window_height, x, y))

    @staticmethod
    def asset_path(name):
        return join(dirname(__file__), 'assets', name)

    @staticmethod
    def on_filedialog(parent, **kwargs):
        strvar = kwargs.pop('strvar')
        method = kwargs.pop('method')

        current_path = strvar.get().strip()
        if current_path == '':
            foldername, filename = os.getcwd(), ''
        elif os.path.isdir(current_path):
            foldername, filename = current_path, ''
        else:
            foldername, filename = os.path.split(current_path)

        if method == 'save':
            ask_func = tk.filedialog.asksaveasfilename
            title = '保存文件'
        else:
            ask_func = tk.filedialog.askopenfilename
            title = '选择文件'

        def wrapper():
            selected = ask_func(parent=parent,
                                title=title,
                                initialdir=foldername,
                                initialfile=filename,
                                **kwargs)
            if selected is None or len(selected) == 0:
                return
            if selected == '':
                selected = os.getcwd()
            else:
                selected = str(Path(selected))
            strvar.set(selected)

        return wrapper
