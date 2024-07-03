import tkinter as tk
from tkinter import messagebox

class HotelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Seleccionar habitación")
        self.root.geometry("1000x580")

        # Variables
        self.room_index = 0
        self.rooms = [
            {"type": "Familiar", "image": "room1.png", "description": "Habitación Familiar"},
            {"type": "Single", "image": "room2.png", "description": "Habitación Individual"},
            {"type": "Doble", "image": "room3.png", "description": "Habitación Doble"},
            {"type": "Triple", "image": "room4.png", "description": "Habitación Triple"}
        ]

        # Create Widgets
        self.create_widgets()

    def create_widgets(self):
        # Room Display
        self.room_frame = tk.Frame(self.root)
        self.room_frame.pack(pady=20)

        self.room_image_label = tk.Label(self.room_frame)
        self.room_image_label.pack()

        self.room_description_label = tk.Label(self.room_frame, text="")
        self.room_description_label.pack()

        # Navigation Buttons
        self.prev_button = tk.Button(self.root, text="<", command=self.prev_room)
        self.prev_button.pack(side=tk.LEFT, padx=20)

        self.next_button = tk.Button(self.root, text=">", command=self.next_room)
        self.next_button.pack(side=tk.RIGHT, padx=20)

        # Action Buttons
        self.description_button = tk.Button(self.root, text="Descripción", command=self.show_description)
        self.description_button.pack(side=tk.LEFT, padx=20)

        self.reserve_button = tk.Button(self.root, text="Reservar", command=self.reserve_room)
        self.reserve_button.pack(side=tk.RIGHT, padx=20)

        # Load initial room
        self.load_room()

    def load_room(self):
        room = self.rooms[self.room_index]
        self.room_image_label.config(text=room["image"])  # Replace with image loading
        self.room_description_label.config(text=room["type"])

    def prev_room(self):
        if self.room_index > 0:
            self.room_index -= 1
        else:
            self.room_index = len(self.rooms) - 1
        self.load_room()

    def next_room(self):
        if self.room_index < len(self.rooms) - 1:
            self.room_index += 1
        else:
            self.room_index = 0
        self.load_room()

    def show_description(self):
        room = self.rooms[self.room_index]
        messagebox.showinfo("Descripción", room["description"])

    def reserve_room(self):
        room = self.rooms[self.room_index]
        messagebox.showinfo("Reserva", f"Reservaste la {room['description']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelApp(root)
    root.mainloop()
