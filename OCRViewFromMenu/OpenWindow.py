import tkinter as tk
from PIL import ImageTk, Image
import time
import os


class Open_Win:
    """
    概要: TKinterメインWindowクラス
    """

    def __init__(self, window_root, title_n):
        w = window_root
        width_of_window = 427
        height_of_window = 427

        screen_width = w.winfo_screenwidth()
        screen_height = w.winfo_screenheight()
        x_coodinate = (screen_width / 2) - (width_of_window / 2)
        y_coodinate = (screen_height / 2) - (height_of_window / 2)
        w.geometry(
            "%dx%d+%d+%d"
            % (width_of_window, height_of_window, x_coodinate, y_coodinate)
        )
        w.overrideredirect(1)

        def new_win():
            q = tk.Tk()
            q.tatile("main window")
            q.mainloop()

        tk.Frame(w, width=427, height=250, bg="#60cad1").place(x=0, y=0)
        label1 = tk.Label(w, text=title_n, fg="snow", bg="#60cad1")
        label1.configure(font=("HGｺﾞｼｯｸE", 24, "bold"))
        label1.place(x=80, y=80)
        label2 = tk.Label(w, text="Loading...", fg="snow", bg="#60cad1")
        label2.configure(font=("HGｺﾞｼｯｸE", 11))
        label2.place(x=10, y=200)
        try:
            image_a = ImageTk.PhotoImage(
                Image.open(os.getcwd() + r"\OCRView\D_curcle_a.png"), master=w
            )
            image_b = ImageTk.PhotoImage(
                Image.open(os.getcwd() + r"\OCRView\D_curcle_b.png"), master=w
            )
        except:
            image_a = ImageTk.PhotoImage(
                Image.open(os.getcwd() + r"\D_curcle_a.png"), master=w
            )
            image_b = ImageTk.PhotoImage(
                Image.open(os.getcwd() + r"\D_curcle_b.png"), master=w
            )

        for i in range(3):
            l1 = tk.Label(w, image=image_a, border=0, relief=tk.SUNKEN).place(
                x=180, y=145
            )
            l2 = tk.Label(w, image=image_b, border=0, relief=tk.SUNKEN).place(
                x=200, y=145
            )
            l3 = tk.Label(w, image=image_b, border=0, relief=tk.SUNKEN).place(
                x=220, y=145
            )
            l4 = tk.Label(w, image=image_b, border=0, relief=tk.SUNKEN).place(
                x=240, y=145
            )
            w.update_idletasks()
            time.sleep(0.5)

            l1 = tk.Label(w, image=image_b, border=0, relief=tk.SUNKEN).place(
                x=180, y=145
            )
            l2 = tk.Label(w, image=image_a, border=0, relief=tk.SUNKEN).place(
                x=200, y=145
            )
            l3 = tk.Label(w, image=image_b, border=0, relief=tk.SUNKEN).place(
                x=220, y=145
            )
            l4 = tk.Label(w, image=image_b, border=0, relief=tk.SUNKEN).place(
                x=240, y=145
            )
            w.update_idletasks()
            time.sleep(0.5)

            l1 = tk.Label(w, image=image_b, border=0, relief=tk.SUNKEN).place(
                x=180, y=145
            )
            l2 = tk.Label(w, image=image_b, border=0, relief=tk.SUNKEN).place(
                x=200, y=145
            )
            l3 = tk.Label(w, image=image_a, border=0, relief=tk.SUNKEN).place(
                x=220, y=145
            )
            l4 = tk.Label(w, image=image_b, border=0, relief=tk.SUNKEN).place(
                x=240, y=145
            )
            w.update_idletasks()
            time.sleep(0.5)

            l1 = tk.Label(w, image=image_b, border=0, relief=tk.SUNKEN).place(
                x=180, y=145
            )
            l2 = tk.Label(w, image=image_b, border=0, relief=tk.SUNKEN).place(
                x=200, y=145
            )
            l3 = tk.Label(w, image=image_b, border=0, relief=tk.SUNKEN).place(
                x=220, y=145
            )
            l4 = tk.Label(w, image=image_a, border=0, relief=tk.SUNKEN).place(
                x=240, y=145
            )
            w.update_idletasks()
            time.sleep(0.5)
        w.destroy()


def RoundButton(w, img1, img2, cmd):
    image_a = ImageTk.PhotoImage(Image.open(img1), master=w)
    image_b = ImageTk.PhotoImage(Image.open(img2), master=w)

    def on_enter(e):
        btn["image"] = image_b

    def on_leave(e):
        btn["image"] = image_a

    btn = tk.Button(
        w, image=image_b, border=0, cursor="hand2", command=cmd, relief=tk.SUNKEN
    )
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


def Open(title_n):
    main_window = tk.Tk()
    # Viewクラス生成
    Open_Win(main_window, title_n)
    # 　フレームループ処理
    # main_window.mainloop()
    return


def FontSearch():
    for f in tk.Tk().call("font", "families"):
        print(f)


if __name__ == "__main__":
    Open("OCR読取 Ver:0.9")
    # FontSearch()
    # 　Tk MainWindow 生成
    # main_window = tk.Tk()
    # main_window = tk.Tk()
    # Viewクラス生成
    # ViewGUI(main_window, "./")

    # 　フレームループ処理
    # main_window.mainloop()
