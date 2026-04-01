import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

# 导入所有功能
from features import merge_by_helper
from features import split_order
from features import other_feature

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("EXCEL合并拆分工具 V1.0")
        self.root.geometry("550x380")
        self.root.resizable(False, False)

        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()

        self.opt_merge = tk.BooleanVar()
        self.opt_split = tk.BooleanVar()
        self.opt_other = tk.BooleanVar()

        self.create_widgets()

    def create_widgets(self):
        title_label = ttk.Label(
            self.root,
            text="EXCEL合并拆分工具",
            font=("微软雅黑", 16, "bold")
        )
        title_label.pack(pady=15)

        frame1 = ttk.Frame(self.root)
        frame1.pack(pady=5, fill=tk.X, padx=20)
        ttk.Label(frame1, text="源文件：", font=("微软雅黑", 10)).pack(side=tk.LEFT)
        ttk.Entry(frame1, textvariable=self.input_path, width=45).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame1, text="选择文件", command=self.select_file).pack(side=tk.LEFT)

        frame2 = ttk.Frame(self.root)
        frame2.pack(pady=5, fill=tk.X, padx=20)
        ttk.Label(frame2, text="保存至：", font=("微软雅黑", 10)).pack(side=tk.LEFT)
        ttk.Entry(frame2, textvariable=self.output_path, width=45).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame2, text="选择路径", command=self.select_save).pack(side=tk.LEFT)

        group_func = ttk.LabelFrame(self.root, text="请勾选需要执行的功能（可多选）")
        group_func.pack(padx=20, pady=15, fill=tk.X)

        ttk.Checkbutton(group_func, text="按辅助单号合并", variable=self.opt_merge, command=self.check_ready).pack(anchor=tk.W, padx=15, pady=4)
        ttk.Checkbutton(group_func, text="单据拆分", variable=self.opt_split, command=self.check_ready).pack(anchor=tk.W, padx=15, pady=4)
        ttk.Checkbutton(group_func, text="其他功能", variable=self.opt_other, command=self.check_ready).pack(anchor=tk.W, padx=15, pady=4)

        self.status_var = tk.StringVar(value="请先选择文件和保存路径")
        ttk.Label(self.root, textvariable=self.status_var, font=("微软雅黑", 9)).pack(pady=5)

        self.start_btn = ttk.Button(
            self.root,
            text="开始处理",
            command=self.start_process,
            state=tk.DISABLED
        )
        self.start_btn.pack(pady=10, ipadx=20, ipady=5)

    def select_file(self):
        path = filedialog.askopenfilename(filetypes=[("Excel 文件", "*.xlsx")])
        if path:
            self.input_path.set(path)
        self.check_ready()

    def select_save(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel 文件", "*.xlsx")],
            initialfile="合并完成结果.xlsx"
        )
        if path:
            self.output_path.set(path)
        self.check_ready()

    def check_ready(self):
        if (self.input_path.get() and self.output_path.get() and self.opt_merge.get()):
            self.start_btn.config(state=tk.NORMAL)
            self.status_var.set("✅ 已就绪，点击开始处理")
        else:
            self.start_btn.config(state=tk.DISABLED)
            if self.input_path.get() and self.output_path.get() and not self.opt_merge.get():
                self.status_var.set("⚠️ 仅【按辅助单号合并】功能可用")

    def start_process(self):
        try:
            self.start_btn.config(state=tk.DISABLED, text="处理中...")
            self.status_var.set("正在处理数据，请稍候...")
            self.root.update()

            i = self.input_path.get()
            o = self.output_path.get()

            if self.opt_merge.get():
                merge_by_helper.run(i, o)

            if self.opt_split.get():
                split_order.run(i, o)

            if self.opt_other.get():
                other_feature.run(i, o)

            self.status_var.set("✅ 处理完成！")
            messagebox.showinfo("成功", "处理完成！")
            os.startfile(os.path.dirname(o))

        except Exception as e:
            messagebox.showerror("错误", f"失败：{str(e)}")
            self.status_var.set("处理失败")

        finally:
            self.start_btn.config(state=tk.NORMAL, text="开始处理")