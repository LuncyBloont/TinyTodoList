'''A todo list tool with tkinter'''
import json
import tkinter as tk
import re
import os
from typing import Optional, Dict

# @ CONFIG:

MEMORY_FILE = './mem.txt'
FACE_STR = r'''
 ____  __  ____   __     __    __  ____  ____ 
(_  _)/  \(    \ /  \   (  )  (  )/ ___)(_  _)
  )( (  O )) D ((  O )  / (_/\ )( \___ \  )(  
 (__) \__/(____/ \__/   \____/(__)(____/ (__) 
'''


# @ CORE VARIABLES:

filter0 = '' # pylint: disable = invalid-name
filter1 = '' # pylint: disable = invalid-name
todo_id_mapping = []
pass_id_mapping = []
FONT = 'TkFixedFont'


# @ FUNCTIONS:

class Config:
    '''Config class'''
    def __init__(self) -> None:
        self.todo_file: str = ''


class ConfigEncoder(json.JSONEncoder):
    '''Encoder of config file'''
    def default(self, o: Config) -> dict:
        return {'todo_file': o.todo_file}



def get_input(title: str, msg: str, callback: callable, defv: str = ''):
    '''Input dialog'''
    top = tk.Tk()
    top.title(title)
    label = tk.Label(top, text=msg, width=64, font=FONT)
    label.grid(column=0, row=0, columnspan=2)

    val = tk.StringVar(top, value=defv)

    entry = tk.Entry(top, textvariable=val, width=60)
    entry.grid(column=0, row=1, columnspan=2)

    def lambda_close_input():
        top.destroy()

    def lambda_callback():
        callback(val.get())
        top.destroy()

    def lambda_input_event(event): # pylint: disable = unused-variable, unused-argument
        lambda_callback()

    cancel = tk.Button(top, text='Cancel', command=lambda_close_input, font=FONT)
    cancel.grid(column=0, row=2, padx=5, pady=5)

    ok = tk.Button(top, text='OK', command=lambda_callback, font=FONT)
    ok.grid(column=1, row=2, padx=5, pady=5)

    # entry.bind('<Return>', lambda_input_event)
    entry.icursor(len(entry.get()))

    entry.focus_force()


def get_confirm(title: str, msg: str, callback: callable):
    '''Confirm dialog'''
    top = tk.Tk()
    top.title(title)
    label = tk.Label(top, text=msg, width=64, font=FONT)
    label.grid(column=0, row=0, columnspan=2)

    def lambda_close_input():
        top.destroy()

    def lambda_callback():
        callback()
        top.destroy()

    def lambda_input_event(event): # pylint: disable = unused-variable, unused-argument
        lambda_callback()

    cancel = tk.Button(top, text='Cancel', command=lambda_close_input, font=FONT)
    cancel.grid(column=0, row=1, padx=5, pady=5)

    ok = tk.Button(top, text='OK', command=lambda_callback, font=FONT)
    ok.grid(column=1, row=1, padx=5, pady=5)

    cancel.focus_force()


def dict2config(d: Dict):
    '''get config from a dict'''
    config = Config()
    config.todo_file = d['todo_file']
    return config


def save(config: Config):
    '''Save config'''
    with open(MEMORY_FILE, 'w', encoding='utf-8') as fw:
        json.dump(config, fw, cls=ConfigEncoder)


def load() -> Config:
    '''Load config from file'''
    config: Config = Config()
    config.todo_file = './todo.txt'

    if not os.path.exists(MEMORY_FILE):
        save(config)

    with open(MEMORY_FILE, 'r', encoding='utf-8') as fr:
        config = json.load(fr, object_hook=dict2config)

    return config


def click_list_todo(event, lb: tk.Listbox, data, more): # pylint: disable = unused-argument
    '''On click'''
    sel = todo_id_mapping[lb.curselection()[0]]

    data['pass'].append(data['todo'][sel])
    del data['todo'][sel]
    refresh_view(*more)


def click_list_pass(event, lb: tk.Listbox, data, more): # pylint: disable = unused-argument
    '''On click'''
    sel = len(data['pass']) - pass_id_mapping[lb.curselection()[0]] - 1

    data['todo'].append(data['pass'][sel])
    del data['pass'][sel]
    refresh_view(*more)


def click_to_add(event, lb: tk.Listbox, data, more): # pylint: disable = unused-argument
    '''On click'''
    sel = lb.curselection()[0]

    if sel == lb.size() - 1:
        def lambda_add_new_item(res: str):
            data['todo'].append(res)
            refresh_view(*more)
        get_input('create', 'Create a new todo item:', lambda_add_new_item, 'a: ')
    else:
        def lambda_set_item(res: str):
            data['todo'][todo_id_mapping[sel]] = res
            refresh_view(*more)
        get_input('modify', 'Modify the exist todo item:', lambda_set_item,
                  data['todo'][todo_id_mapping[sel]])


def make_view(config: Config):
    '''Make view'''
    top = tk.Tk()
    top.title('Todo List')
    top.resizable(False, False)

    todo_data: Optional[Dict] = None

    with open(config.todo_file, 'r', encoding='utf-8') as fr:
        try:
            todo_data = json.load(fr)
        except json.JSONDecodeError as e:
            print(e)

    if todo_data is None:
        todo_data = {}
        todo_data['todo'] = ['add a todo item']
        todo_data['pass'] = ['launch this simple todo list']

    face = tk.Label(top, text=FACE_STR, font=FONT)
    face.grid(column=0, row=0, columnspan=4, padx=2, pady=2)

    def lambda_make_view_align0(a, b):
        dl0.yview('moveto', a)
        tl.yview('moveto', a)
        tlb.yview('moveto', a)
        scl0v.set(a, b)

    def lambda_make_view_align1(a, b):
        dl1.yview('moveto', a)
        pl.yview('moveto', a)
        plb.yview('moveto', a)
        scl1v.set(a, b)

    def lambda_make_view_align0_x(a, b):
        scl0h.set(a, b)

    def lambda_make_view_align1_x(a, b):
        scl1h.set(a, b)

    dl0 = tk.Listbox(top, width=5, font=FONT, yscrollcommand=lambda_make_view_align0)
    dl0.grid(column=0, row=1, padx=2, pady=2, sticky=tk.N + tk.S)

    dl1 = tk.Listbox(top, width=5, font=FONT, yscrollcommand=lambda_make_view_align1)
    dl1.grid(column=0, row=3, padx=2, pady=2, sticky=tk.N + tk.S)

    tl = tk.Listbox(top, font=FONT, width=64, yscrollcommand=lambda_make_view_align0,
                    xscrollcommand=lambda_make_view_align0_x)
    tl.grid(column=1, row=1, sticky=tk.N + tk.W + tk.S + tk.E, padx=2, pady=2, ipady=64)

    pl = tk.Listbox(top, font=FONT, width=64, yscrollcommand=lambda_make_view_align1,
                    xscrollcommand=lambda_make_view_align1_x)
    pl.grid(column=1, row=3, sticky=tk.N + tk.W + tk.S + tk.E, padx=2, pady=2, ipady=64)

    tlb = tk.Listbox(top, width=3, font=FONT, yscrollcommand=lambda_make_view_align0)
    tlb.grid(column=3, row=1, padx=2, pady=2, sticky=tk.N + tk.S)

    plb = tk.Listbox(top, width=3, font=FONT, yscrollcommand=lambda_make_view_align1)
    plb.grid(column=3, row=3, padx=2, pady=2, sticky=tk.N + tk.S)

    scl0v = tk.Scrollbar(top, orient=tk.VERTICAL, command=tl.yview)
    scl0h = tk.Scrollbar(top, orient=tk.HORIZONTAL, command=tl.xview)
    scl0v.grid(column=2, row=1, sticky=tk.N + tk.S)
    scl0h.grid(column=1, row=2, sticky=tk.W + tk.E)

    scl1v = tk.Scrollbar(top, orient=tk.VERTICAL, command=pl.yview)
    scl1h = tk.Scrollbar(top, orient=tk.HORIZONTAL, command=pl.xview)
    scl1v.grid(column=2, row=3, sticky=tk.N + tk.S)
    scl1h.grid(column=1, row=4, sticky=tk.W + tk.E)

    def lambda_set_filter0(s: str):
        global filter0 # pylint: disable = global-statement
        filter0 = s
        refresh_view(dl0, dl1, tl, pl, tlb, plb, todo_data, config)

    def lambda_set_filter1(s: str):
        global filter1 # pylint: disable = global-statement
        filter1 = s
        refresh_view(dl0, dl1, tl, pl, tlb, plb, todo_data, config)

    search0 = tk.Button(top, text='filter', font=FONT, command=
                        lambda: get_input('set filter for todo items',
                                          'Input the filter regex for todo items:',
                                          lambda_set_filter0, filter0))
    search0.grid(column=2, row=2, columnspan=2, padx=2, pady=2)

    search1 = tk.Button(top, text='filter', font=FONT, command=
                        lambda: get_input('set filter for pass items',
                                          'Input the filter regex for pass items:',
                                          lambda_set_filter1, filter1))
    search1.grid(column=2, row=4, columnspan=2, padx=2, pady=2)

    refresh_view(dl0, dl1, tl, pl, tlb, plb, todo_data, config)

    def lambda_at_todo(event):
        if len(tlb.curselection()) == 0:
            return
        if tlb.curselection()[0] == tlb.size() - 1:
            return

        s = todo_data['todo'][todo_id_mapping[tlb.curselection()[0]]]

        get_confirm('confirm', 'send it to pass? \n' + s,
                    lambda: click_list_todo(event, tlb, todo_data,
                                            (dl0, dl1, tl, pl, tlb, plb, todo_data, config)))

    def lambda_at_pass(event):
        if len(plb.curselection()) == 0:
            return

        s = todo_data['pass'][len(todo_data['pass']) - pass_id_mapping[plb.curselection()[0]] - 1]

        get_confirm('confirm', 'send it to todo? \n' + s,
                    lambda: click_list_pass(event, plb, todo_data,
                                            (dl0, dl1, tl, pl, tlb, plb, todo_data, config)))

    def lambda_at_todo_list(event):
        if len(tl.curselection()) == 0:
            return
        click_to_add(event, tl, todo_data, (dl0, dl1, tl, pl, tlb, plb, todo_data, config))

    tlb.bind('<<ListboxSelect>>', lambda_at_todo)
    plb.bind('<<ListboxSelect>>', lambda_at_pass)
    tl.bind('<<ListboxSelect>>', lambda_at_todo_list)

    return top


def refresh_view(dl0: tk.Listbox, dl1: tk.Listbox, tl: tk.Listbox, pl: tk.Listbox,
                 tlb: tk.Listbox, plb: tk.Listbox, data: Dict, config: Config):
    '''Refresh view'''
    dl0.delete(0, dl0.size())
    dl1.delete(0, dl1.size())
    tl.delete(0, tl.size())
    pl.delete(0, pl.size())
    tlb.delete(0, tlb.size())
    plb.delete(0, plb.size())

    data['todo'].sort(key=lambda e: 'z'
                      if (e[0] >= 'a' and e[0] <= 'z') or (e[0] >= 'A' and e[0] <= 'Z')
                      else e[0])
    data['pass'].sort(key=lambda e: 'z'
                      if (e[0] >= 'a' and e[0] <= 'z') or (e[0] >= 'A' and e[0] <= 'Z')
                      else e[0])

    real_filter0 = re.compile(''.join(filter0.split(' ')))
    real_filter1 = re.compile(''.join(filter1.split(' ')))

    k = 0
    todo_id_mapping.clear()
    for e in data['todo']:
        if real_filter0.match(e):
            dl0.insert('end', str(k))
            tl.insert('end', e)
            tlb.insert('end', ' = ')
            todo_id_mapping.append(k)
        k += 1

    dl0.insert('end', '   ')
    tl.insert('end', '[click me to add a new todo item]')
    tlb.insert('end', '   ')

    k = 0
    pass_id_mapping.clear()
    for e in reversed(data['pass']):
        if real_filter1.match(e):
            dl1.insert('end', str(k))
            pl.insert('end', e)
            plb.insert('end', ' - ')
            pass_id_mapping.append(k)
        k += 1

    with open(config.todo_file, 'w', encoding='utf-8') as fw:
        json.dump(data, fw)

def start():
    '''Entry'''
    config = load()
    top = make_view(config)
    top.mainloop()

if __name__ == '__main__':
    start()
