import tkinter as tk
import src as tk_a

if __name__ == "__main__":
    app = tk.Tk()
    app.geometry('600x600')

    alert_generator = tk_a.AlertGenerator(app)

    show_notification_btn = tk.Button(app)
    show_notification_btn.configure(
        text="Send Alert",
        command=lambda: alert_generator.send(
            "Information Alert",
            tk_a.AlertType.INFO,
            tk.NW)
    )
    show_notification_btn.pack()

    app.mainloop()
