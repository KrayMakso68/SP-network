from sp_network import encode, decode
import customtkinter
import re

app = customtkinter.CTk()
app.title("my app")
app.geometry("600x400")

tabview = customtkinter.CTkTabview(master=app)
tabview.pack(expand=True, fill='both', padx=5, pady=(0, 5))

tabview.add("Шифратор")  # add tab at the end
tabview.add("Метод встречи по середине")  # add tab at the end
tabview.set("Шифратор")  # set currently visible tab


def validate_binary_string(newval):
    if re.match('^[01]{0,9}$', newval):
        return True
    else:
        return False


def validate_1_or_0_string(newval):
    if re.match('^[01]{0,1}$', newval):
        return True
    else:
        return False


plaintext_frame = customtkinter.CTkFrame(master=tabview.tab("Шифратор"), fg_color='gray20')
tabview.tab("Шифратор").columnconfigure(0, weight=1)
plaintext_frame.grid(row=0, column=0)
plaintext_label = customtkinter.CTkLabel(master=plaintext_frame, text='Открытый текст')
plaintext_label.grid(row=0, sticky='w', padx=10, pady=(10, 0))
plaintext_entry = customtkinter.CTkEntry(master=plaintext_frame,
                                         height=40,
                                         placeholder_text='010101010',
                                         font=('', 18),
                                         validate="key",
                                         validatecommand=(app.register(validate_binary_string), '%P')
                                         )
plaintext_entry.grid(row=1, stick='nsew', padx=10, pady=(5, 10))

key_frame = customtkinter.CTkFrame(master=tabview.tab("Шифратор"), fg_color='gray20')
tabview.tab("Шифратор").columnconfigure(1, weight=1)
key_frame.grid(row=0, column=1)
key_label = customtkinter.CTkLabel(master=key_frame, text='Ключ зашифрования')
key_label.grid(row=0, sticky='w', padx=10, pady=(10, 0))
key_entry = customtkinter.CTkEntry(master=key_frame,
                                   placeholder_text='010101010',
                                   height=40,
                                   font=('', 18),
                                   validate="key",
                                   validatecommand=(app.register(validate_binary_string), '%P')
                                   )
key_entry.grid(row=1, sticky='nsew', padx=10, pady=(5, 10))

s_box_frame = customtkinter.CTkFrame(master=tabview.tab("Шифратор"), fg_color='gray20')
tabview.tab("Шифратор").rowconfigure(1, weight=1)
s_box_frame.grid(row=1, sticky='ew', columnspan=2)
s_box_label = customtkinter.CTkLabel(master=s_box_frame, text='S-блок')
s_box_label.grid(row=0, sticky='w', padx=20, pady=(10, 5))
input_s_box_frame = customtkinter.CTkFrame(master=s_box_frame, fg_color='gray30')
input_s_box_frame.grid(row=1, sticky='ew', padx=20, pady=(0, 10), ipadx=10)
in_s_box_label = customtkinter.CTkLabel(master=input_s_box_frame, text='ВХОД')
in_s_box_label.grid(row=0, column=0, padx=5)
out_s_box_label = customtkinter.CTkLabel(master=input_s_box_frame, text='ВЫХОД')
out_s_box_label.grid(row=1, column=0, padx=5)

# инпупы для клеток S-блока
for i in range(8):
    ent = customtkinter.CTkEntry(master=input_s_box_frame, width=22, state='normal')
    ent.insert(0, f'{i}')
    ent.grid(row=0, column=i + 1, pady=(5, 2))
    ent.configure(state='disable')

# инпуты для ввода значений S-блока
entry_s_box_list = []
for i in range(8):
    ent = customtkinter.CTkEntry(master=input_s_box_frame,
                                 width=22,
                                 state='normal',
                                 validate="key",
                                 validatecommand=(app.register(validate_1_or_0_string), '%P')
                                 )
    ent.grid(row=1, column=i + 1, pady=(2, 5))
    entry_s_box_list.append(ent)
    # для валидации кнопок в цикле for
    # https://stackoverflow.com/questions/32037769/how-do-i-link-python-tkinter-widgets-created-in-a-for-loop
    # валидация
    # https://pythonru.com/uroki/sozdanie-izmenenie-i-proverka-teksta-tkinter-2
    # https://metanit.com/python/tkinter/2.8.php
error_s_box_label = customtkinter.CTkLabel(master=s_box_frame, text='Ошибка ввода значения S-блока', text_color='red')
error_s_box_label.grid(row=1, column=1, sticky='w', padx=20, pady=(0, 5))

app.mainloop()
