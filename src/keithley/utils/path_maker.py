
import os


def make_folder(folder, new=False):
    """A function to make folders.

    If new=False, it does not create a new folder if it just exist.
    If new=True, it creates a new folder anyway (if the folder exist,
    a number is added at the end of the folder's name).

    :param folder: Folder's name (str). It contains all the path.
    :param new: Indicate what happens if folder already exists.
    :return: Path to folder created (str).
    """
    if new:
        i = 0
        new_folder = folder
        while os.path.exists('"' + new_folder + '"'):
            i += 1
            new_folder = folder + '_(%d)' % i
        folder = new_folder
        os.system('mkdir ' + '"' + folder + '"')

    else:
        if not os.path.exists(folder):
            os.system('mkdir ' + '"' + folder + '"')

    return folder


def make_file(file, extension='.txt', new=False, header=False):
    """A function to make files.

    If new=False, it does not create a new file if it just exist.
    If new=True, it creates a new file anyway (if the file exist,
    a number is added at the end of the file's name).

    :param file: File's name (str). It contains all the path without extension.
    :param extension: File's extension. Default: .txt
    :param new: Indicate what happens if file already exists.
    :param header: Indicate if a header is written in the file or not.
    :return: Path to file created (str).
    """
    if new:
        i = 0
        new_file = file + extension
        while os.path.exists('"' + new_file + '"'):
            i += 1
            new_file = file + '_(%d)' % i + extension
        file = new_file
        txt = open(file, 'w')
        if header:
            txt.write(
                '#       File        |   PCE        |   FF         '
                '| Pmax (W/cm2) |  Jsc (A/cm2) |  Voc (V)     '
                '| P_sol (W/cm2)|  area (cm2)   \n')
        txt.close()

    else:
        file += extension
        if not os.path.exists('"' + file + '"'):
            txt = open(file, 'w')
            if header:
                txt.write(
                    '#       File        |   PCE        |   FF         '
                    '| Pmax (W/cm2) |  Jsc (A/cm2) |  Voc (V)     '
                    '| P_sol (W/cm2)|  area (cm2)   \n')
            txt.close()

    return file
