import tkinter as tk
import tk_alert as tk_a


if __name__ == "__main__":
    app = tk.Tk()
    app.geometry("800x800")

    alert_generator = tk_a.AlertGenerator(app)

    show_notification_btn = tk.Button(app)
    show_notification_btn.configure(
        text="Send Alert",
        command=lambda: alert_generator.send(
            text="Alert information: Lorem Ipsum",
            type=tk_a.AlertType.INFO,
            anchor=tk.SE,
            duration=10
        ),
    )
    show_notification_btn.pack()

    app.mainloop()