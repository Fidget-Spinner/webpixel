"""
Common coroutines that almost all view .py files will use.
"""
import logging
import aiofiles
import os

#logging.basicConfig(level=logging.WARNING)

DIR_NAME = os.path.dirname(__file__)    # directory path containing this script


async def parse_file(file_name: str, template: dict) -> str:
    """ Attempts to emulate a template engine parser.
    Reads a HTML/CSS/JS file and substitutes the placeholders using simple str.format.

    :param file_name: name of the file to read
    :param template: key-value pairs where key=name of value to replace in file, value=value to substitute in
    """
    raw_file = await read_file(file_name)
    return raw_file.format(**template)


async def read_file(file_name: str, is_relative_path: bool = True) -> str:
    """ Async file reader using aiofiles. Currently reads the whole raw file and returns it as a string.
    Should not be used on gigantic files for memory reasons.
    Not using a file iterator/generator to read as response has to be a whole string anyways.

    :param file_name: relative or abs file path
    :param is_relative_path: if False, assumed to be absolute file path
    :returns the entire file as a string
    """
    if is_relative_path:
        file_name = os.path.join(DIR_NAME, file_name)
    try:
        async with aiofiles.open(file_name, mode="r") as html_file:
            logging.info("Opened file..")
            result = await html_file.read()
            logging.info(f"File \"{file_name}\" successfully read ")
            return result
    except FileNotFoundError:
        logging.error(f"File \"{file_name}\" not found")
        return ""
