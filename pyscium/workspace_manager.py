from command_invoker import CommandInvoker
from commands.commands import AddChCommand
from commands.commands import CloseFileCommand
from commands.commands import SaveFileCommand
from commands.commands import ExitCommand
from logger import pyscium_logger
from window import Window


class WorkspaceManager(object):
    logger = pyscium_logger.get_logger(__name__, 'workspace_manager.log')

    def __init__(self, filename):
        self.__window = Window(filename)

    def start(self):
        WorkspaceManager.logger.info("start()")
        invoker = CommandInvoker()

        window = self.__window.get_window()
        while True:
            ch = window.getch()

            if ch == 24:
                invoker.execute(CloseFileCommand(self.__window))
                invoker.execute(ExitCommand(None))

            elif ch == 19:
                invoker.execute(SaveFileCommand(self.__window))

            else:
                invoker.execute(AddChCommand(self.__window, ch))
