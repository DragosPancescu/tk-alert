import tkinter as tk
from src import AlertGenerator, AlertType, AlertPlacement

if __name__ == "__main__":
    app = tk.Tk()
    app.geometry('600x600')
    
    alert_generator = AlertGenerator(app)

    show_notification_btn = tk.Button(app)
    show_notification_btn.configure(
        text="Send Alert",
        command=lambda: alert_generator.send("information alert", AlertType.SUCCESS, AlertPlacement.BOTTOM_LEFT)
    )
    show_notification_btn.pack()

    app.mainloop()