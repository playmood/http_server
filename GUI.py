# -*- coding: utf8 -*-

import os
import shutil
import subprocess
import threading
import PySimpleGUI as sg
import time

import socket
import struct
import fcntl
import inspect
import ctypes
import re
      

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

def no_refresh_log(command, ip, port, mode):
    show_run = 'The server is running on ' + ip + ':' + port + ' in ' + mode + ' mode...'
    print(str(show_run))
    proc = os.system(command)
        


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
    doc_path = '/home/playmood/'
    menu_bar = [['&Help', '&About']]
    menu = sg.Menu(menu_bar, tearoff=True)

    cbin =  [[sg.Text("Choose a mode: ", size=(16, 1)), 
                sg.Combo(list(bin.keys()), size=(40,4), enable_events=True, key='cbin')]]
    

    port_submit = [sg.Text('PORT: '), sg.InputText(size=(6,1)), sg.Text('show log:'), sg.CBox(''), sg.Button("Run"), sg.Button("Stop")]

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
            if values[2]:
                mode_key = values['cbin']
                mode_value = bin[mode_key]
                port = values[1]
                command = doc_path + 'http_server/exec_compare_gui/' + mode_value + ' ' + port
                ip = str(get_host_ip())
                show_log = threading.Thread(target=refresh_log, args=(command, ip, port, mode_key))
                show_log.start()
            else:
                mode_key = values['cbin']
                mode_value = bin[mode_key]
                port = values[1]
                command = doc_path + 'http_server/exec_compare/' + mode_value + ' ' + port
                ip = str(get_host_ip())
                no_show_log = threading.Thread(target=no_refresh_log, args=(command, ip, port, mode_key))
                no_show_log.start()
        if event == 'Stop':
            if values[2] != True:
                cmd = 'ps aux | grep exec_compare'
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                while proc.poll() is None:
                    out = proc.stdout.readline().decode('utf-8')
                    out = out.replace('\n', '')
                    pid = re.findall(r'\d+', out)
                    cmd = 'kill -9 ' + str(int(pid[0]) + 1)
                    subprocess.Popen(cmd, shell=True)
                    print('The server is shutting down...')
            else:
                cmd = 'ps aux | grep exec_compare_gui'
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                while proc.poll() is None:
                    out = proc.stdout.readline().decode('utf-8')
                    out = out.replace('\n', '')
                    pid = re.findall(r'\d+', out)
                    cmd = 'kill -9 ' + str(int(pid[0]) + 1)
                    subprocess.Popen(cmd, shell=True)
                    print('The server is shutting down...')
                
 

    window.close()