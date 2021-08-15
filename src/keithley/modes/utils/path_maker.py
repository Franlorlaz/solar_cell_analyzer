"""Functions to make folders and files."""

import os
from pathlib import Path


def make_folder(folder, new=False):
    """Make folders.

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
        while os.path.exists(Path(new_folder).resolve()):
            i += 1
            new_folder = folder + '_(%d)' % i
        folder = Path(new_folder).resolve()
        os.system('mkdir ' + '"' + str(folder) + '"')

    else:
        folder = Path(folder).resolve()
        if not os.path.exists(folder):
            os.system('mkdir ' + '"' + str(folder) + '"')

    return str(folder)


def make_file(file, new=False, header=False, extension='.txt'):
    """Make files.

    If new=False, it does not create a new file if it just exist.
    If new=True, it creates a new file anyway (if the file exist,
    a number is added at the end of the file's name).

    :param file: File's name (str). It contains all the path without extension.
    :param extension: File's extension. Default: .txt. If extension is given
    in "file", set extension=None
    :param new: Indicate what happens if file already exists.
    :param header: Indicate if a header is written in the file or not.
    :return: Path to file created (str).
    """
    if not extension:
        split = file.split('.')
        extension = '.' + split[-1]
        file = '.'.join(split[:-1])

    if new:
        i = 0
        new_file = file + extension
        while os.path.exists(Path(new_file).resolve()):
            i += 1
            new_file = file + '_(%d)' % i + extension
        file = Path(new_file).resolve()
        with open(file, 'w') as txt:
            if header:
                txt.write(
                    '#       File        |   PCE        |   FF         '
                    '| Pmax (W/cm2) |  Jsc (A/cm2) |  Voc (V)     '
                    '| P_sol (W/cm2)|  area (cm2)   \n')

    else:
        file += extension
        file = Path(file).resolve()
        if not os.path.exists(file):
            with open(file, 'w') as txt:
                if header:
                    txt.write(
                        '#       File        |   PCE        |   FF         '
                        '| Pmax (W/cm2) |  Jsc (A/cm2) |  Voc (V)     '
                        '| P_sol (W/cm2)|  area (cm2)   \n')

    return str(file)


def set_up_directories(cell_name, directory):
    """Make a folders tree useful for place data files.

    In `directory`, make a folder named `cell_name` and inside, make a
    folder for every electrode. Inside of every electrode folder, make
    a folder for every mode.

    :param cell_name: Name for the first folder of the folders tree (str).
    :param directory: Existing directory where to make the folders tree
    (str or path object).
    :return: Base directory (str): directory/cell_name
    """
    cell_name = str(cell_name)
    directory = Path(directory).resolve()

    if not os.path.exists(directory):
        raise ValueError(f'The selected directory does not exist: {directory}')

    base_dir = directory.joinpath(cell_name)
    make_folder(base_dir, new=False)

    for elect in ['A', 'B', 'C', 'D']:
        electrode_dir = base_dir.joinpath(elect)
        make_folder(electrode_dir, new=False)
        for mode in ['lineal', 'hysteresis']:
            mode_dir = electrode_dir.joinpath(mode)
            make_folder(mode_dir, new=False)

    return str(base_dir.resolve())
