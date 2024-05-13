from sp_network import encode, decode
import customtkinter

app = customtkinter.CTk()
app.title("my app")
app.geometry("600x400")

tabview = customtkinter.CTkTabview(master=app)
tabview.pack(expand=True, fill='both', padx=5, pady=5)

tabview.add("Шифратор")  # add tab at the end
tabview.add("Метод встречи по середине")  # add tab at the end
tabview.set("Шифратор")  # set currently visible tab

button = customtkinter.CTkButton(master=tabview.tab("Шифратор"))
button.pack(padx=20, pady=20)

app.mainloop()
