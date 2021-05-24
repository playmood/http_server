# -*- coding: utf8 -*-

import os
import shutil
import subprocess
import threading
import PySimpleGUI as sg

import socket
import struct
import fcntl

def refresh_log(command, ip, port, mode):
    show_run = 'The server is running on ' + ip + ':' + port + ' in ' + mode + ' mode...'
    print(str(show_run))
    try:
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while proc.poll() is None:
            out = proc.stdout.readline().decode('utf-8')
            out = out.replace('\n', '')
            print(out)
    finally:
        proc.kill()

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
        return ip

sg.theme('Default')
sg.theme('DefaultNoMoreNagging')

bin = {
    'SEE': 'synlog_listenET_connET',
    'SEL': 'synlog_listenET_connLT',
    'SLE': 'synlog_listenLT_connET',
    'SLL': 'synlog_listenLT_connLT',
    'AEE': 'asynlog_listenET_connET',
    'AEL': 'asynlog_listenET_connLT',
    'ALE': 'asynlog_listenLT_connET',
    'ALL': 'asynlog_listenLT_connLT'
}

if __name__ == '__main__':

    menu_bar = [['&Help', '&About']]
    menu = sg.Menu(menu_bar, tearoff=True)

    cbin =  [[sg.Text("Choose a mode: ", size=(16, 1)), 
                sg.Combo(list(bin.keys()), size=(40,4), enable_events=True, key='cbin')]]
    

    port_submit = [sg.Text('PORT: '), sg.InputText(), sg.Button("Run")]

    output = sg.Frame('Log', [[sg.Output(key='output', size=(65, 15))]])

    layout = [[menu], cbin, port_submit, [output]] # [output],

    window = sg.Window('Server Launcher', layout)

    while True:
        event, values = window.read()
        # print(event, values)
        if event == 'About':
            sg.popup('A graduate design.', 'from scd\'s Github: https://github.com/playmood/http_server', 
                title='About this server', font=(None, 13), button_type=5)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Run':
            mode_key = values['cbin']
            mode_value = bin[mode_key]
            port = values[1]
            command = '/home/playmood/http_server/exec_compare_gui/' + mode_value + ' ' + port
            ip = str(get_host_ip())
            threading.Thread(target=refresh_log, args=(command, ip, port, mode_key)).start()
                
 

    window.close()