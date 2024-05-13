from sp_network import encode, decode
import customtkinter

app = customtkinter.CTk()
app.title("my app")
app.geometry("600x400")

tabview = customtkinter.CTkTabview(master=app)
tabview.pack(expand=True, fill='both', padx=5, pady=(0, 5))

tabview.add("Шифратор")  # add tab at the end
tabview.add("Метод встречи по середине")  # add tab at the end
tabview.set("Шифратор")  # set currently visible tab

# button = customtkinter.CTkButton(master=tabview.tab("Шифратор"))
# button.pack(padx=20, pady=20)
# валидаци "^[1,0]{9}$"

plaintext_frame = customtkinter.CTkFrame(master=tabview.tab("Шифратор"))
tabview.tab("Шифратор").columnconfigure(0, weight=1)
plaintext_frame.grid(row=0, column=0)
plaintext_label = customtkinter.CTkLabel(master=plaintext_frame, text='Открытый текст')
plaintext_label.grid(row=0, sticky='w')
plaintext_entry = customtkinter.CTkEntry(master=plaintext_frame, placeholder_text='011000100')
plaintext_entry.grid(row=1, stick='we')

key_frame = customtkinter.CTkFrame(master=tabview.tab("Шифратор"))
tabview.tab("Шифратор").columnconfigure(1, weight=1)
key_frame.grid(row=0, column=1)
key_label = customtkinter.CTkLabel(master=key_frame, text='Ключ зашифрования')
key_label.grid(row=0, sticky='w')
key_entry = customtkinter.CTkEntry(master=key_frame, placeholder_text='010101010')
key_entry.grid(row=1, sticky='we')

s_box_frame = customtkinter.CTkFrame(master=tabview.tab("Шифратор"), fg_color='white')
tabview.tab("Шифратор").rowconfigure(1, weight=1)
s_box_frame.grid(row=1, sticky='ew', columnspan=2)
s_box_label = customtkinter.CTkLabel(master=s_box_frame, text='S-блок')
s_box_label.grid(row=0, sticky='w')

app.mainloop()
