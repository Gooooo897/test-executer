import tkinter as tk
from tkinter import messagebox

def _update_timer(r_time:int, p_up:tk.Tk, lbl:tk.Label):
    if r_time > 0:
        r_time -= 1
        lbl.config(text=f"残り{r_time}秒...")
        # 1秒後にこの関数を再度呼び出す
        p_up.after(1000, _update_timer, r_time, p_up, lbl)
    else:
        _close_popup(p_up)

def _close_popup(popup:tk.Tk):
    popup.quit() # これないとmainloop以降の処理が実行されない。
    popup.destroy()
    # ここに後続処理を追加

def show_remaining_time_to_wait(remaining_time_s:int):
    '''
    引数分 待機する。残り待機時間をポップアップで表示する。
    '''
    # ポップアップを作成する
    popup = tk.Tk()
    popup.attributes('-topmost', True) # メッセージボックスを画面の最前面にする

    popup.title("KeyOn マスク待機中")
    popup.geometry("300x150")

    # 残り時間を保持する変数
    label = tk.Label(popup, text=f"残り{remaining_time_s}秒...",font=("Arial", 18))
    label.pack(pady=20)

    # タイマーを更新開始
    _update_timer(remaining_time_s, popup, label)

    # ポップアップを表示する
    popup.mainloop()



def ask_checker_ready()->str:
    '''
    チェッカーSWが初期位置であることをMessageBoxで確認します。
    - Parameter
        - none
    - Return
        - string : "yes", "no"
    '''
    return messagebox.askquestion('チェッカー確認', 'チェッカーSWが初期位置であることは確認しましたか?')

def ask_checker_sw_control(sw_order):
    messagebox.showinfo('チェッカー確認', f"チェッカーを{sw_order}してください。{sw_order}したらOKをおしてください。")

def ask_continue():
    return messagebox.askquestion('テスト継続確認', 'テスト継続しますか?')

def order_with_sound(procedure_message:str):
    return messagebox.showinfo('作業指示',procedure_message)

def order_without_sound(procedure_message:str):
    return messagebox.askquestion('作業指示',procedure_message)

class DeleteLogOrNot:
    def __init__(self):
        pass

    def on_button_click(self):
        self.responce = messagebox.askquestion("LOG削除", "LOGの削除を続行しますか?")
        self.root.destroy()

    def check(self):
        self.root = tk.Tk()
        self.root.title("log削除確認")

        button = tk.Button(self.root, text="log削除の確認", command=self.on_button_click)
        button.pack(pady=40)

        self.root.mainloop()

if __name__ == "__main__":

    module = DeleteLogOrNot()
    module.check()
    print(module.responce)
    # if ask_checker_ready() == "yes":
    #     print("continue.")
    # else:
    #     exit

    # wait_time_s = 3
    # show_remaining_time_to_wait(wait_time_s)
    # print("ポップアップが閉じられ、後続処理が開始されました。")

    # ask_checker_sw_control("起動・停止")