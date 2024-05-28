import re

import customtkinter

customtkinter.set_appearance_mode("dark")

S: int = 3  # число входов в s-блок
N: int = 3  # число s-блоков
Str_len: int = S * N  # длина входного слова
Rounds: int = 2  # кол-во полных раундов шифрования
P_option: bool = False  # операция перестановки в конце


def validate_binary_string(newval):
    reg_exp = '^[01]{0,' + str(Str_len) + '}$'
    if re.match(reg_exp, newval):
        return True
    else:
        return False


class TabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("Конфигурация шифратора")
        self.add("Шифратор")
        self.add("Метод встречи по середине")
        self.set("Шифратор")

        self.tab("Шифратор").columnconfigure((0, 1), weight=1)
        self.tab("Шифратор").rowconfigure(1, weight=1)


class InputPlaintextFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color='gray20')
        self.columnconfigure(0, weight=1)

        self.plaintext_label = customtkinter.CTkLabel(master=self, text='Открытый текст')
        self.plaintext_label.grid(row=0, sticky='w', padx=10, pady=(10, 0))
        self.plaintext_entry = customtkinter.CTkEntry(master=self,
                                                      height=40,
                                                      placeholder_text='010101010',
                                                      font=('', 18),
                                                      validate="key",
                                                      validatecommand=(self.register(validate_binary_string), '%P')
                                                      )
        self.plaintext_entry.grid(row=1, sticky='nsew', padx=10, pady=(5, 10))
        self.error_plaintext_label = customtkinter.CTkLabel(master=self,
                                                            text='',
                                                            text_color='brown2',
                                                            width=240,
                                                            height=35
                                                            )
        self.error_plaintext_label.grid(row=2, sticky='w', padx=10, pady=(2, 10))


class InputСiphertextFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color='gray20')
        self.columnconfigure(0, weight=1)

        self.key_label = customtkinter.CTkLabel(master=self, text='Ключ зашифрования')
        self.key_label.grid(row=0, sticky='w', padx=10, pady=(10, 0))
        self.key_entry = customtkinter.CTkEntry(master=self,
                                                placeholder_text='010101010',
                                                height=40,
                                                font=('', 18),
                                                validate="key",
                                                validatecommand=(self.register(validate_binary_string), '%P')
                                                )
        self.key_entry.grid(row=1, sticky='ew', padx=10, pady=(5, 10))
        self.error_key_label = customtkinter.CTkLabel(master=self,
                                                      text='',
                                                      text_color='brown2',
                                                      width=240,
                                                      height=35
                                                      )
        self.error_key_label.grid(row=2, sticky='we', padx=10, pady=(2, 10))


class ConfigurationFrame(customtkinter.CTkFrame):
    def __init__(self, master, tab_view):
        super().__init__(master)

        self.columnconfigure((1, 2), weight=1)
        self.columnconfigure((0, 3), weight=2)
        self.tab_view = tab_view

        customtkinter.CTkLabel(master=self,
                               text="Число входов в S-блок:"
                               ).grid(row=0, column=1, padx=0, pady=0, sticky='e')
        self.S_var = customtkinter.StringVar(value='3')
        self.s_entry = customtkinter.CTkEntry(master=self, textvariable=self.S_var, width=40)
        self.s_entry.grid(row=0, column=2, padx=(0, 20), pady=5)
        customtkinter.CTkLabel(master=self,
                               text='Число S-блоков:'
                               ).grid(row=1, column=1, padx=0, pady=0, sticky='e')
        self.N_var = customtkinter.StringVar(value='3')
        self.n_entry = customtkinter.CTkEntry(master=self, textvariable=self.N_var, width=40)
        self.n_entry.grid(row=1, column=2, padx=(0, 20), pady=5)
        customtkinter.CTkLabel(master=self,
                               text="Количество раундов шифрования: \n(без учёта последнего раунда)"
                               ).grid(row=2, column=1, padx=0, pady=0, sticky='e')
        self.rounds_var = customtkinter.StringVar(value='2')
        self.rounds_entry = customtkinter.CTkEntry(master=self, textvariable=self.rounds_var, width=40)
        self.rounds_entry.grid(row=2, column=2, padx=(0, 20), pady=5)
        customtkinter.CTkLabel(master=self,
                               text="Операция перестановки в последнем раунде:"
                               ).grid(row=3, column=1, padx=0, pady=0, sticky='e')
        self.p_option_var = customtkinter.BooleanVar(value=False)
        self.config_option_checkbox = customtkinter.CTkCheckBox(master=self, variable=self.p_option_var, text='')
        self.config_option_checkbox.grid(row=3, column=2, padx=(20, 0), pady=5, sticky='e')
        self.set_button = customtkinter.CTkButton(master=self,
                                                  text='Установить конфигурацию шифратора',
                                                  height=40,
                                                  command=self.set_config)
        self.set_button.grid(row=0, column=3, padx=0, pady=0, ipadx=10)

    def set_config(self):
        global S, N, Str_len, Rounds, P_option
        S = int(self.S_var.get())
        N = int(self.N_var.get())
        Str_len = S * N
        Rounds = int(self.rounds_var.get())
        P_option = self.p_option_var.get()
        self.tab_view.set("Шифратор")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("SP-network")
        self.geometry("850x550")

        self.tab_view = TabView(self)
        self.tab_view.pack(expand=True, fill='both', padx=5, pady=(0, 5))

        self.plaintext_frame = InputPlaintextFrame(master=self.tab_view.tab("Шифратор"))
        self.plaintext_frame.grid(row=0, column=0, sticky='ew', padx=20)

        self.key_frame = InputСiphertextFrame(master=self.tab_view.tab("Шифратор"))
        self.key_frame.grid(row=0, column=1, sticky='ew', padx=20)

        self.configuration_frame = ConfigurationFrame(master=self.tab_view.tab("Конфигурация шифратора"),
                                                      tab_view=self.tab_view)
        self.configuration_frame.pack(fill='x', padx=10, pady=20)


app = App()
app.mainloop()
