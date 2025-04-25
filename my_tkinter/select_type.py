import tkinter as tk

class SelectType():
    def __init__(self, text_list:list[str], value_list:list):
        if len(text_list) != len(value_list):
            print("設定値を確認してください")
            exit()
        self.dialog = tk.Tk()
        self.dialog.attributes('-topmost', True) # メッセージボックスを画面の最前面にする
        self.dialog.withdraw()
        self.dialog.geometry("300x150")

        self.text_list = text_list
        self.value_list = value_list

    def _on_ok(self):
        self.result = self.var.get()
        self.dialog.destroy()  # ダイアログを閉じる

    def show_checkbox_dialog(self):
        # ダイアログウィンドウを作成
        self.dialog.deiconify()
        self.result = "A"
        self.dialog.title("チェックボックスダイアログ")

        # 変数の作成（チェックボックスの選択状態を保持）
        self.var = tk.StringVar(value="C")

        for i in range(len(self.text_list)):
            checkbox = tk.Radiobutton(self.dialog, text=self.text_list[i], variable=self.var, value=self.value_list[i])
            checkbox.pack(anchor=tk.W)

        # OKボタンの作成
        ok_button = tk.Button(self.dialog, text="OK", command=self._on_ok)
        ok_button.pack()

        self.dialog.mainloop()  # ダイアログが閉じるまで待機

    def get_type(self):
        return self.result

if __name__ == "__main__":
    title_list = ["full analysis", "only graph"]
    value_list = ["FULL", "GRAPH"]
    s = SelectType(title_list, value_list)
    s.show_checkbox_dialog()
    data = s.get_type()
    print(data)
