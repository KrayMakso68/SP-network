import random
import re
import time
from decimal import Decimal

from spn import SPN, gen_pbox, int_to_str_with_fill
import customtkinter

customtkinter.set_appearance_mode("dark")

S: int = 3  # число входов в s-блок
N: int = 3  # число s-блоков
Str_len: int = S * N  # длина входного слова
Rounds: int = 2  # кол-во полных раундов шифрования
P_option: bool = False  # операция перестановки в конце


def validate_binary_string(newval):
    """
    Function to validate binary string taking into account the changing length of the string

    Parameters
    ----------
    newval: str
         String to be validated

    Returns
    -------
    bool
        True if the string is valid otherwise False
    """
    reg_exp = '^[01]{0,' + str(Str_len) + '}$'
    if re.match(reg_exp, newval):
        return True
    else:
        return False


def validate_s_box(action, value_if_allowed):
    """
    Validate input in s_box

    Parameters
    ----------
    value_if_allowed: str
        Allowed input value
    action: str
        Type of operation

    Returns
    -------
    bool
        Release permission value

    """
    input_limit = 2 ** S
    if action == "1":
        try:
            if len(value_if_allowed) > 1 and value_if_allowed[0] == "0":
                return False
            num = int(value_if_allowed)
            if 0 <= num < input_limit:
                return True
            else:
                return False
        except ValueError:
            return False
    else:
        return True


def generate_binary_string():
    """
    Generates a string of a given length, consisting of a random combination of 0 and 1.

    Parameters
    ----------

    Returns
    -------
    str
        Returns a new generated string
    """
    binary_digits = ['0', '1']
    length: int = Str_len
    binary_string = ''.join(random.choices(binary_digits, k=length))
    return binary_string


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

        self.plaintext_entry = customtkinter.CTkEntry(master=self)
        self.plaintext_entry.configure(height=40, placeholder_text=generate_binary_string(), font=('', 18),
                                       validate="key", validatecommand=(self.register(validate_binary_string), '%P'))
        self.plaintext_entry.grid(row=1, sticky='nsew', padx=10, pady=(5, 10))

        self.error_plaintext_label = customtkinter.CTkLabel(master=self)
        self.error_plaintext_label.configure(text='', text_color='brown2', width=240, height=35)
        self.error_plaintext_label.grid(row=2, sticky='w', padx=10, pady=(2, 10))

    def get(self):
        return self.plaintext_entry.get()

    def set_error(self, error):
        self.error_plaintext_label.configure(text=error)

    def reset_input(self):
        self.plaintext_entry.delete(0, 'end')


class InputKeyFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color='gray20')
        self.columnconfigure(0, weight=1)

        self.key_label = customtkinter.CTkLabel(master=self, text='Ключ зашифрования')
        self.key_label.grid(row=0, sticky='w', padx=10, pady=(10, 0))

        self.key_entry = customtkinter.CTkEntry(master=self)
        self.key_entry.configure(placeholder_text=generate_binary_string(), height=40, font=('', 18),
                                 validate="key", validatecommand=(self.register(validate_binary_string), '%P'))
        self.key_entry.grid(row=1, sticky='ew', padx=10, pady=(5, 10))

        self.error_key_label = customtkinter.CTkLabel(master=self)
        self.error_key_label.configure(text='', text_color='brown2', width=240, height=35)
        self.error_key_label.grid(row=2, sticky='we', padx=10, pady=(2, 10))

    def get(self):
        return self.key_entry.get()

    def set_error(self, error):
        self.error_key_label.configure(text=error)

    def reset_input(self):
        self.key_entry.delete(0, 'end')


class SboxScrollableFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, orientation='horizontal')

        self.columnconfigure(0, weight=1)
        self.configure(fg_color='gray20')

        self.s_box_label = customtkinter.CTkLabel(master=self, text='S-блок')
        self.s_box_label.grid(row=0, sticky='w', padx=10, pady=(10, 5))

        self.input_s_box_frame = InputSboxFrame(master=self)
        self.input_s_box_frame.grid(row=1, sticky='nsew', padx=10, pady=(0, 10), ipadx=10)

        self.error_s_box_label = customtkinter.CTkLabel(master=self, text='', text_color='brown2', height=35)
        self.error_s_box_label.grid(row=2, column=0, sticky='w', padx=20, pady=(2, 5))

    def set_error(self, error):
        self.error_s_box_label.configure(text=error)


class InputSboxFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color='gray30')

        self.in_s_box_label = customtkinter.CTkLabel(master=self, text='ВХОД')
        self.in_s_box_label.grid(row=0, column=0, padx=5)
        self.out_s_box_label = customtkinter.CTkLabel(master=self, text='ВЫХОД')
        self.out_s_box_label.grid(row=1, column=0, padx=5)

        self.sbox_labels_list = self.create_sbox_labels(master=self)
        self.sbox_entries_list = self.create_sbox_entries(master=self)

    def create_sbox_labels(self, master):
        label_s_box_list = []
        global S
        limit = 2 ** S
        for i in range(limit):
            ent = customtkinter.CTkEntry(master, width=35, state='normal')
            ent.insert(0, f'{i}')
            ent.grid(row=0, column=i + 1, pady=(5, 2))
            ent.configure(state='disable')
            label_s_box_list.append(ent)
        return label_s_box_list

    def create_sbox_entries(self, master):
        entry_s_box_list = []
        global S
        limit = 2 ** S
        for i in range(limit):
            ent = customtkinter.CTkEntry(master=master)
            ent.configure(width=35, state='normal', validate="key",
                          validatecommand=(self.register(validate_s_box), '%d', '%P'))
            ent.grid(row=1, column=i + 1, pady=(2, 5))
            entry_s_box_list.append(ent)
        return entry_s_box_list

    def get_sbox_entries(self):
        return self.sbox_entries_list


class OutCiphertextFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.configure(fg_color='gray20')

        customtkinter.CTkLabel(master=self, text='Зашифрованный текст').grid(row=0, sticky='w', padx=10, pady=(10, 0))
        self.cipher_text_entry = customtkinter.CTkEntry(master=self, height=40, font=('', 18))
        self.cipher_text_entry.grid(row=1, sticky='nsew', padx=10, pady=(5, 10))
        self.cipher_text_entry.configure(state='disable')

    def set_cipher_text(self, cipher_text):
        self.cipher_text_entry.configure(state='normal')
        self.cipher_text_entry.delete(0, 'end')
        self.cipher_text_entry.insert(0, cipher_text)
        self.cipher_text_entry.configure(state='disable')


class StartEncryptionFrame(customtkinter.CTkFrame):
    def __init__(self, master, command):
        super().__init__(master)

        self.columnconfigure(1, weight=1)
        self.rowconfigure((0, 2, 4), weight=1)
        self.start_command = command

        self.start_encryption_button = customtkinter.CTkButton(master=self)
        self.start_encryption_button.configure(text='Зашифровать', height=50, command=self.start_command)
        self.start_encryption_button.grid(row=1, column=0, sticky='nsew', columnspan=2)

        self.reset_input = customtkinter.CTkButton(master=self)
        self.reset_input.configure(text='Сбросить', width=80, fg_color='firebrick4', hover_color='firebrick',
                                   command='')
        self.reset_input.grid(row=3, column=1, sticky='e')

        self.execution_time = customtkinter.CTkLabel(master=self)
        self.execution_time.configure(text='Время выполнения: ')
        self.execution_time.grid(row=3, column=0, sticky='w')

    def set_ex_time(self, ex_time: float | str):
        if type(ex_time) is float and not ex_time > 0:
            ex_time = 'мгн'
        self.execution_time.configure(text='Время выполнения: {}'.format(ex_time))


class ConfigurationFrame(customtkinter.CTkFrame):
    def __init__(self, master, root):
        super().__init__(master)

        self.columnconfigure((1, 2), weight=1)
        self.columnconfigure((0, 3), weight=2)

        self.root = root
        self.tab_view = root.tab_view

        customtkinter.CTkLabel(master=self, text="Число входов в S-блок:"
                               ).grid(row=0, column=1, padx=0, pady=0, sticky='e')
        self.S_var = customtkinter.StringVar(value='3')
        self.s_entry = customtkinter.CTkEntry(master=self, textvariable=self.S_var, width=40)
        self.s_entry.grid(row=0, column=2, padx=(0, 20), pady=5)

        customtkinter.CTkLabel(master=self, text='Число S-блоков:'
                               ).grid(row=1, column=1, padx=0, pady=0, sticky='e')
        self.N_var = customtkinter.StringVar(value='3')
        self.n_entry = customtkinter.CTkEntry(master=self, textvariable=self.N_var, width=40)
        self.n_entry.grid(row=1, column=2, padx=(0, 20), pady=5)

        customtkinter.CTkLabel(master=self, text="Количество раундов шифрования: \n(без учёта последнего раунда)"
                               ).grid(row=2, column=1, padx=0, pady=0, sticky='e')
        self.rounds_var = customtkinter.StringVar(value='2')
        self.rounds_entry = customtkinter.CTkEntry(master=self, textvariable=self.rounds_var, width=40)
        self.rounds_entry.grid(row=2, column=2, padx=(0, 20), pady=5)

        customtkinter.CTkLabel(master=self, text="Операция перестановки в последнем раунде:"
                               ).grid(row=3, column=1, padx=0, pady=0, sticky='e')
        self.p_option_var = customtkinter.BooleanVar(value=False)
        self.config_option_checkbox = customtkinter.CTkCheckBox(master=self, variable=self.p_option_var, text='')
        self.config_option_checkbox.grid(row=3, column=2, padx=(20, 0), pady=5, sticky='e')

        self.set_button = customtkinter.CTkButton(master=self)
        self.set_button.configure(text='Установить конфигурацию шифратора', height=40, command=self.set_config)
        self.set_button.grid(row=0, column=3, padx=0, pady=0, ipadx=10)

    def set_config(self):
        global S, N, Str_len, Rounds, P_option
        S = int(self.S_var.get())
        N = int(self.N_var.get())
        Str_len = S * N
        Rounds = int(self.rounds_var.get())
        P_option = self.p_option_var.get()
        self.root.update_input()
        self.tab_view.set("Шифратор")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("SP-network")
        self.geometry("900x550")

        self.tab_view = TabView(self)
        self.tab_view.pack(expand=True, fill='both', padx=5, pady=(0, 5))

        self.plaintext_frame = InputPlaintextFrame(master=self.tab_view.tab("Шифратор"))
        self.plaintext_frame.grid(row=0, column=0, sticky='ew', padx=20)

        self.key_frame = InputKeyFrame(master=self.tab_view.tab("Шифратор"))
        self.key_frame.grid(row=0, column=1, sticky='ew', padx=20)

        self.s_box_frame = SboxScrollableFrame(master=self.tab_view.tab("Шифратор"))
        self.s_box_frame.grid(row=1, sticky='ew', columnspan=2, padx=20, pady=20)

        self.cipher_text_frame = OutCiphertextFrame(master=self.tab_view.tab("Шифратор"))
        self.cipher_text_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=(0, 20))

        self.start_encryption_button = StartEncryptionFrame(master=self.tab_view.tab("Шифратор"),
                                                            command=self.start_encryption)
        self.start_encryption_button.grid(row=2, column=1, sticky='nsew', padx=20, pady=(0, 20))

        self.configuration_frame = ConfigurationFrame(master=self.tab_view.tab("Конфигурация шифратора"),
                                                      root=self)
        self.configuration_frame.pack(fill='x', padx=10, pady=20)

    def update_input(self):
        self.plaintext_frame.plaintext_entry.destroy()
        self.plaintext_frame.plaintext_entry = customtkinter.CTkEntry(master=self.plaintext_frame)
        self.plaintext_frame.plaintext_entry.configure(height=40, placeholder_text=generate_binary_string(),
                                                       font=('', 18),
                                                       validate="key",
                                                       validatecommand=(self.register(validate_binary_string), '%P'))
        self.plaintext_frame.plaintext_entry.grid(row=1, sticky='nsew', padx=10, pady=(5, 10))

        self.key_frame.key_entry.destroy()
        self.key_frame.key_entry = customtkinter.CTkEntry(master=self.key_frame)
        self.key_frame.key_entry.configure(placeholder_text=generate_binary_string(), height=40, font=('', 18),
                                           validate="key",
                                           validatecommand=(self.register(validate_binary_string), '%P'))
        self.key_frame.key_entry.grid(row=1, sticky='ew', padx=10, pady=(5, 10))

        self.s_box_frame.input_s_box_frame.destroy()
        self.s_box_frame.input_s_box_frame = InputSboxFrame(master=self.s_box_frame)
        self.s_box_frame.input_s_box_frame.grid(row=1, sticky='nsew', padx=10, pady=(0, 10), ipadx=10)

        self.cipher_text_frame.set_cipher_text('')
        self.start_encryption_button.set_ex_time('')

    def check_configuration(self):
        global Str_len
        entry_limit = Str_len
        error = False

        if len(self.plaintext_frame.get()) != entry_limit:
            error = True
            self.plaintext_frame.set_error('Ошибка ввода открытого текста\nЧисло должно быть девятизначным')
        else:
            self.plaintext_frame.set_error('')
        if len(self.key_frame.get()) != entry_limit:
            error = True
            self.key_frame.set_error('Ошибка ввода ключа\nЧисло должно быть девятизначным')
        else:
            self.key_frame.set_error('')
        s_box_list = []
        self.s_box_frame.set_error('')
        for entry in self.s_box_frame.input_s_box_frame.get_sbox_entries():
            value = entry.get()
            if len(value) == 0:
                error = True
                self.s_box_frame.set_error('Ошибка ввода значений S-блока\nВведите все значения S-блока')
                break
            if int(value) in s_box_list:
                error = True
                self.s_box_frame.set_error('Ошибка ввода значений S-блока\nЗначения S-блока дублируются')
                break
            s_box_list.append(int(value))
        return error

    def start_encryption(self):
        global Str_len, S, N, Rounds, P_option

        if not self.check_configuration():
            plaintext = int(self.plaintext_frame.get(), 2)
            key = int(self.key_frame.get(), 2)
            s_box = [int(entry.get()) for entry in self.s_box_frame.input_s_box_frame.get_sbox_entries()]
            p_box = gen_pbox(S, N)
            implementation = int(P_option)
            sp = SPN(s_box, p_box, key, Rounds, implementation)

            start = time.time()
            print(start)
            encrypted_plaintext = sp.encrypt(plaintext)
            end = time.time()
            print(end)
            ex_time = float(round(Decimal(end - start), 5))
            self.start_encryption_button.set_ex_time(ex_time)

            out_cipher_text = int_to_str_with_fill(encrypted_plaintext, Str_len)
            self.cipher_text_frame.set_cipher_text(out_cipher_text)

    def clear_input(self):
        self.plaintext_frame.reset_input()
        self.key_frame.reset_input()


app = App()
app.mainloop()
