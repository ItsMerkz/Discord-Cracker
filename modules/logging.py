from datetime import datetime
from colorama import Fore, init

init()


class Logger:
    def __init__(self):
        self.colours = (
            Fore.RED,
            Fore.GREEN,
            Fore.BLUE,
            Fore.YELLOW,
            Fore.WHITE,
            Fore.MAGENTA,
            Fore.LIGHTRED_EX,
            Fore.LIGHTGREEN_EX
        )
        self.reset = Fore.RESET

    def _success(self, content: str) -> None:
        the_time = datetime.now().strftime("%H:%M:%S")
        print(
            "[%s %s %s] %s %s"
            % (self.colours[2], the_time, self.reset, self.colours[1], content)
        )

    def _fail(self, content: str) -> None:
        the_time = datetime.now().strftime("%H:%M:%S")
        print(
            "%s[%s %s %s] %s %s"
            % (
                self.reset,
                self.colours[2],
                the_time,
                self.reset,
                self.colours[0],
                content,
            )
        )

    def _error(self, content: str) -> None:
        the_time = datetime.now().strftime("%H:%M:%S")
        print(
            "%s[%s %s %s] %s %s"
            % (
                self.reset,
                self.colours[2],
                the_time,
                self.reset,
                self.colours[3],
                content,
            )
        )

    def _info(self, content: str) -> None:
        the_time = datetime.now().strftime("%H:%M:%S")
        print(
            "%s[%s %s %s] %s %s"
            % (
                self.reset,
                self.colours[2],
                the_time,
                self.reset,
                self.colours[5],
                content,
            )
        )

    def _debug(self, content: str) -> None:
        the_time = datetime.now().strftime("%H:%M:%S")
        print(
            "%s DEBUG -> [%s %s %s] %s %s"
            % (
                self.reset,
                self.colours[2],
                the_time,
                self.reset,
                self.colours[6],
                content,
            )
        )
    def _title(self, content: str) -> None:
        the_time = datetime.now().strftime("%H:%M:%S")
        print(
            "%s %s"
            % (
                self.colours[7],
                content,
            )
        )