from sp_network import encode, number_to_byte_str
import customtkinter
import re

customtkinter.set_appearance_mode("dark")

app = customtkinter.CTk()
app.title("my app")
app.geometry("650x500")

tabview = customtkinter.CTkTabview(master=app)
tabview.pack(expand=True, fill='both', padx=5, pady=(0, 5))

tabview.add("Шифратор")
tabview.add("Метод встречи по середине")
tabview.set("Шифратор")


def validate_binary_string(newval):
    if re.match('^[01]{0,9}$', newval):
        return True
    else:
        return False


def validate_s_box(newval):
    if re.match('^[0-7]?$', newval):
        return True
    else:
        return False


def check_configuration() -> bool:
    error = False
    if len(plaintext_entry.get()) != 9:
        error = True
        error_plaintext_label.configure(text='Ошибка ввода открытого текста\nЧисло должно быть девятизначным')
    else:
        error_plaintext_label.configure(text='')
    if len(key_entry.get()) != 9:
        error = True
        error_key_label.configure(text='Ошибка ввода ключа\nЧисло должно быть девятизначным')
    else:
        error_key_label.configure(text='')
    s_box_list = []
    error_s_box_label.configure(text='')
    for entry in entry_s_box_list:
        value = entry.get()
        if len(value) == 0:
            error = True
            error_s_box_label.configure(text='Ошибка ввода значений S-блока\nВведите все значения S-блока')
            break
        if int(value) in s_box_list:
            error = True
            error_s_box_label.configure(text='Ошибка ввода значений S-блока\nЗначения S-блока дублируются')
            break
        s_box_list.append(int(value))
    return error


def start_encryption():
    cipher_text_entry.configure(state='normal')
    cipher_text_entry.delete(0, 9)
    if not check_configuration():
        plaintext = int(plaintext_entry.get(), 2)
        key = int(key_entry.get(), 2)
        s_box = [int(entry.get()) for entry in entry_s_box_list]
        encrypted_plaintext = encode(plaintext, key, s_box)
        cipher_text_entry.insert(0, number_to_byte_str(encrypted_plaintext))
        cipher_text_entry.configure(state='disable')


# рамка ввода открытого текста
plaintext_frame = customtkinter.CTkFrame(master=tabview.tab("Шифратор"), fg_color='gray20')
tabview.tab("Шифратор").columnconfigure(0, weight=1)
plaintext_frame.grid(row=0, column=0, sticky='ew', padx=20)
plaintext_label = customtkinter.CTkLabel(master=plaintext_frame, text='Открытый текст')
plaintext_label.grid(row=0, sticky='w', padx=10, pady=(10, 0))
plaintext_entry = customtkinter.CTkEntry(master=plaintext_frame,
                                         height=40,
                                         placeholder_text='010101010',
                                         font=('', 18),
                                         validate="key",
                                         validatecommand=(app.register(validate_binary_string), '%P')
                                         )
plaintext_entry.grid(row=1, sticky='nsew', padx=10, pady=(5, 10))
error_plaintext_label = customtkinter.CTkLabel(master=plaintext_frame,
                                               text='',
                                               text_color='brown2',
                                               width=240,
                                               height=35
                                               )
error_plaintext_label.grid(row=2, sticky='w', padx=10, pady=(2, 10))

# рамка ввода ключа
key_frame = customtkinter.CTkFrame(master=tabview.tab("Шифратор"), fg_color='gray20')
tabview.tab("Шифратор").columnconfigure(1, weight=1)
key_frame.grid(row=0, column=1, sticky='ew', padx=20)
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
error_key_label = customtkinter.CTkLabel(master=key_frame,
                                         text='',
                                         text_color='brown2',
                                         width=240,
                                         height=35
                                         )
error_key_label.grid(row=2, sticky='we', padx=10, pady=(2, 10))

# рамка ввода S-блока
s_box_frame = customtkinter.CTkFrame(master=tabview.tab("Шифратор"), fg_color='gray20')
tabview.tab("Шифратор").rowconfigure(1, weight=1)
s_box_frame.grid(row=1, sticky='nsew', columnspan=2, padx=20, pady=20)
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
                                 validatecommand=(app.register(validate_s_box), '%P')
                                 )
    ent.grid(row=1, column=i + 1, pady=(2, 5))
    entry_s_box_list.append(ent)

error_s_box_label = customtkinter.CTkLabel(master=s_box_frame, text='', text_color='brown2')
error_s_box_label.grid(row=1, column=1, sticky='w', padx=20, pady=(2, 5))

# рамка вывода зашифрованного текста
cipher_text_frame = customtkinter.CTkFrame(master=tabview.tab("Шифратор"), fg_color='gray20')
cipher_text_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=(0, 20))
cipher_text_label = customtkinter.CTkLabel(master=cipher_text_frame, text='Зашифрованный текст')
cipher_text_label.grid(row=0, sticky='w', padx=10, pady=(10, 0))
cipher_text_entry = customtkinter.CTkEntry(master=cipher_text_frame,
                                           height=40,
                                           font=('', 18)
                                           )
cipher_text_entry.grid(row=1, sticky='nsew', padx=10, pady=(5, 10))
cipher_text_entry.configure(state='disable')
start_encryption_button = customtkinter.CTkButton(master=tabview.tab("Шифратор"),
                                                  text='Зашифровать',
                                                  height=40,
                                                  command=start_encryption
                                                  )
start_encryption_button.grid(row=2, column=1, sticky='ew', padx=20, pady=(0, 20))


app.mainloop()
