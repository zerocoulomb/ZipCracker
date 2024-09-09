import zipfile
import tqdm
import sys
from colorama import Fore, init
import os
import logging
import signal

init(autoreset=True)


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s]: %(message)s'
    )


class ZipCracker():
    """Cracks zip files
    """

    def __init__(self, zip_path: str) -> None:
        """Checks path and initializes zip file

        Arguments:
            zip_path (str) path of zip file
        """
        signal.signal(signal.SIGINT, self._handler)

        self._password = None

        if not os.path.exists(zip_path):
            logging.error(Fore.RED+"Please enter exist zip file")
            return

        self.zip_file = zipfile.ZipFile(zip_path)

    def crack(self, pass_path: str) -> None:
        """Cracks zip file

        Arguments:
            pass_path (str) password wordlist file path
        """
        if not os.path.exists(pass_path):
            logging.error(Fore.RED+"Please enter exists wordlist")
            return

        self._start_cracking(pass_path)
        self._log_cracked()

    def _handler(self, signum, frame):
        sys.exit(0)

    def _start_cracking(self, pass_path: str) -> None:
        """Starts cracking process

        Arguments:
            pass_path (str) password wordlist file path
        """

        bar = self._create_bar(pass_path)

        for password in bar:
            bar.set_postfix_str(password.decode(), refresh=False)
            if self._try_password(password):
                self._password = password.decode()
                break

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
            colour="red"
            )

        return bar

    @property
    def cracked(self) -> bool:
        """Checks zip cracked or not

        Returns:
            bool: cracked or not
        """
        return self.password is not None

    @property
    def password(self) -> str:
        """Gets cracked password

        Returns:
            str: cracked password
        """
        return self._password

    def _try_password(self, password: bytes) -> None:
        """Tries password to match with zip file's password

        Arguments:
            password (bytes) password to try
        """
        try:
            self.zip_file.extractall(pwd=password)
        except Exception:
            return False
        return True

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

    def _log_cracked(self) -> None:
        """Logs cracked status
        """
        if self.cracked:
            logging.debug(Fore.BLUE + "Status:" + Fore.GREEN + " cracked")
            logging.debug(
                Fore.BLUE+"Password: "+Fore.GREEN + self.password
            )
        else:
            logging.debug(Fore.BLUE+"Status:"+Fore.RED + " not cracked\n")
