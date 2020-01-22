from command_invoker import CommandInvoker
from commands.commands import InsertChCommand
from commands.commands import CloseFileCommand
from commands.commands import SaveFileCommand
from commands.commands import MoveToBeginningOfLineCommand
from commands.commands import MoveToEndOfLineCommand
from commands.commands import MoveForwardOneCharCommand
from commands.commands import MoveBackwardOneCharCommand
from commands.commands import MoveToPreviousLineCommand
from commands.commands import MoveToNextLineCommand
from commands.commands import BackspaceCommand
from commands.commands import NewlineCommand
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

        window = self.__window.get_internal_window()
        while True:
            ch = window.getch()

            if ch == 24:  # ^x
                invoker.execute(CloseFileCommand(self.__window))
                invoker.execute(ExitCommand(None))

            elif ch == 19:  # ^s
                invoker.execute(SaveFileCommand(self.__window))

            elif ch == 1:  # ^a
                invoker.execute(MoveToBeginningOfLineCommand(self.__window))

            elif ch == 5:  # ^e
                invoker.execute(MoveToEndOfLineCommand(self.__window))

            elif ch == 6:  # ^f
                invoker.execute(MoveForwardOneCharCommand(self.__window))

            elif ch == 2:  # ^b
                invoker.execute(MoveBackwardOneCharCommand(self.__window))

            elif ch == 14:  # ^n
                invoker.execute(MoveToNextLineCommand(self.__window))

            elif ch == 16:  # ^p
                invoker.execute(MoveToPreviousLineCommand(self.__window))

            elif ch == 263:  # backspace
                invoker.execute(BackspaceCommand(self.__window))

            elif ch == 10:  # newline
                invoker.execute(NewlineCommand(self.__window))

            else:
                invoker.execute(InsertChCommand(self.__window, ch))
