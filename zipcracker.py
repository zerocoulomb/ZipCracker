import zipfile

import pyzipper
import tqdm
import sys
from colorama import Fore, init
import os
import logging
from dataclasses import dataclass

init(autoreset=True)


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s]: %(message)s'
    )


@dataclass
class CrackResult:
    cracked: bool
    password: str | None


class ZipCracker:
    """Cracks zip files
    """

    def __init__(self, zip_path: str) -> None:
        """Checks path and initializes zip file

        Arguments:
            zip_path (str) path of zip file
        """

        self._crack_result = CrackResult(False, None)

        self._zip_file = None

        try:

            self._zip_file = pyzipper.AESZipFile(zip_path)

        except (zipfile.BadZipFile, FileNotFoundError):

            logging.debug(Fore.RED+"Please enter exist zip file")

    def crack(self, pass_path: str) -> CrackResult | None:
        """Cracks zip file

        Arguments:
            pass_path (str) password wordlist file path
        """
        if self._zip_file is not None:

            if not os.path.isfile(pass_path):
                logging.debug(Fore.RED+"Please enter exist wordlist")
                sys.exit(1)

            logging.debug(Fore.BLUE + "Zip File: " + Fore.LIGHTWHITE_EX + os.path.abspath(self._zip_file.filename))
            logging.debug(Fore.BLUE + "Wordlist: " + Fore.LIGHTWHITE_EX  + os.path.abspath(pass_path))

            if self._start_cracking(pass_path):
                self._log_result()

        return self._crack_result

    def _start_cracking(self, pass_path: str) -> bool:
        """Starts cracking pocess

        Arguments:
            pass_path (str) password wordlist file path
        """
        print()

        try:
            with self._create_bar(pass_path) as bar:

                for password in bar:

                    bar.set_postfix_str(password.decode(), refresh=False)

                    self._crack_result = self._try_password(password)

                    if self._crack_result.cracked:
                        break

        except KeyboardInterrupt:

            logging.debug(Fore.RED + "Stopping")

            return False

        finally:

            self._zip_file.close()

        return True


    def _create_bar(self, pass_path: str) -> tqdm.tqdm:
        """Creates status bar

        Arguments:
            pass_path (str) password wordlist file path

        Returns:
            tqdm.tqdm: status bar
        """
        size = self._get_size(pass_path)

        password_generator = self._create_generator(pass_path)

        bar = tqdm.tqdm(
            password_generator,
            total=size,
            desc=Fore.BLUE+"cracking"+Fore.RESET,
            unit=" password",
            dynamic_ncols=True,
            mininterval=0.5,
            colour="red",
            leave=False,
            )

        return bar

    def _try_password(self, password: bytes) -> CrackResult:
        """Tries password to match with zip file's password

        Arguments:
            password (bytes) password to try
        """
        try:
            self._zip_file.setpassword(password)
            self._zip_file.extractall()

        except RuntimeError:

            return CrackResult(False,password.decode())

        return CrackResult(True,password.decode())

    def _get_size(self, pass_path: str) -> int:
        """Get count of passwords in wordlist

        Arguments:
            pass_path (str) password wordlist file path

        Returns:
            int: count of passwords
        """
        with open(pass_path, "rb", buffering=8192) as pass_file:
            return sum(1 for _ in pass_file)

    def _create_generator(self, pass_path: str):
        """Generator for passwords in password wordlist

        Arguments:
            pass_path (str) password wordlist file path

        Yields:
            bytes: password in wordlist
        """
        with open(pass_path, "rb", buffering=8192) as pass_file:
            for password in pass_file:
                yield password.strip()

    def _log_result(self) -> None:
        """Logs cracked status
        """
        if self._crack_result.cracked:

            logging.debug(Fore.BLUE + "Status:" + Fore.GREEN + " cracked")
            logging.debug(
                Fore.BLUE+"Password: "+Fore.GREEN + self._crack_result.password
            )
        else:
            logging.debug(Fore.BLUE+"Status:"+Fore.RED + " not cracked\n")
