import time
import sys
import os
from colorama import Fore as color
#from globals import *


def progress_bar(actual_value,
                 max_value,
                 size_bar=50,
                 character='■',
                 initial_message="Progress:",
                 end_message='',
                 error_indicator=False):
    percent = actual_value / max_value
    message = '\r' + initial_message + ' [{0:' + str(size_bar) + 's}] {1:6d}/{2:1d} ' + end_message
    if percent < 1:
        if error_indicator:
            sys.stdout.write(
                color.LIGHTRED_EX + message.format(character * int(size_bar * percent), actual_value, max_value))
        else:
            sys.stdout.write(
                color.LIGHTYELLOW_EX + message.format(character * int(size_bar * percent), actual_value, max_value))
        sys.stdout.flush()
    else:
        sys.stdout.write(color.BLUE + message.format(character * int(size_bar * percent), actual_value, max_value))
        sys.stdout.flush()

    if percent == 1: print(color.RESET)
    # Formato:
    # initial_message [■■■■■■■■                                          ]    230/151100 end_message


def get_str_time_running(t_begin):
    t_running = time.time() - t_begin
    hours = int(t_running / (60 * 60))
    minutes = int(t_running / 60 - 60 * int(t_running / (60 * 60)))
    seconds = int(t_running - 60 * int(t_running / 60))
    return '0' * (2 - len(str(hours))) + str(hours) + 'h ' + '0' * (2 - len(str(minutes))) + str(
        minutes) + 'min ' + '0' * (2 - len(str(seconds))) + str(seconds) + 's'


def verify_create_folder(dir_folder, verbose=True):
    try:
        os.makedirs(dir_folder)
        if verbose: print('\tLa carpeta \'' + dir_folder + '\' ha sido creada EXITOSAMENTE')
    except FileExistsError:
        if verbose: print('\tLa carpeta \'' + dir_folder + '\' ya ha sido creada')


def size_archive(dir_archive):
    return round(os.stat(dir_archive).st_size * 1e-6, 2)


def get_files(folder, extension=None):
    # folder, subfolders, files
    folder, _, files = list(os.walk(folder))[0]  # Solo obtenemos datos de la carpeta especificada como argumento
    if not (extension is None):
        files = [f for f in files if f.endswith(extension)]
    return folder, files
