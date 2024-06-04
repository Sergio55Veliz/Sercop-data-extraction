import zipfile
import os

from utilities.utilities import (
    verify_create_folder,
    size_archive,
    progress_bar,
    get_files,
)

url_proyect = os.getcwd()


def compress_data_to_zip(dir_folder_tosave,
                         dir_folder_toread,
                         name_zip,
                         limit_to_zip=100,
                         extension='.json'
                         ):
    verify_create_folder(dir_folder_tosave, verbose=False)
    verify_create_folder(dir_folder_toread, verbose=False)

    if not name_zip.endswith('.zip'):
        name_zip += '.zip'

    zip = None  # variable del comprimido

    zips_created = 0
    archives_zipped = 0
    size_zipped = 0
    folder, files = get_files(folder=dir_folder_toread, extension=extension)
    print("\nProceso de compresión... ")
    progress_bar(actual_value=archives_zipped,
                 max_value=len(files),
                 initial_message="Archivos comprimidos:",
                 end_message=' | Total zips: '+str(zips_created))
    for index in range(len(files)):
        file = files[index]

        size_mb = size_archive(os.path.join(folder, file))*0.1

        if (size_zipped + size_mb) >= limit_to_zip:
            # Crear el zip al alcanzar el límite o al llegar al último archivo
            zip.close()
            size_zipped = 0
            zips_created += 1
            progress_bar(actual_value=archives_zipped,
                         max_value=len(files),
                         initial_message="Archivos comprimidos:",
                         end_message=' | Total zips: '+str(zips_created))

        if size_zipped == 0:
            name = name_zip.split('.')[0] + "_"+str(zips_created+1) + '.' + name_zip.split('.')[1]
            zip = zipfile.ZipFile(os.path.join(dir_folder_tosave, name), 'w')

        if (size_zipped+size_mb) < limit_to_zip:  # Límite en MB, 100 por default
            zip.write(os.path.join(folder, file),
                      os.path.relpath(os.path.join(folder, file), dir_folder_toread),
                      compress_type=zipfile.ZIP_DEFLATED)
            size_zipped += size_mb
            archives_zipped += 1
            if index == (len(files) - 1):
                zip.close()
                size_zipped = 0
                zips_created += 1

    progress_bar(actual_value=archives_zipped,
                 max_value=len(files),
                 initial_message="Archivos comprimidos:",
                 end_message=' | Total zips: '+str(zips_created))
    print("\n\tZipped file successfully!!")


def extract_data_from_zip(dir_folder_tosave,
                          dir_zip  # Contiene el nombre del archivo a descomprimir
                          ):
    zip = zipfile.ZipFile(dir_zip)

    verify_create_folder(dir_folder_tosave, verbose=False)

    zip.extractall(dir_folder_tosave)
    zip.close()
    print("\n\tExtracted files successfully!! from: ", dir_zip)
