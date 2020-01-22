import sys


class Command(object):
    def __init__(self, obj):
        self.obj = obj

    def execute(self):
        raise NotImplementedError


# __file commands
class CreateFileCommand(Command):
    def execute(self):
        self.obj.create_file()


class OpenFileCommand(Command):
    def execute(self):
        self.obj.open_file()


class SaveFileCommand(Command):
    def execute(self):
        self.obj.save_file()


class CloseFileCommand(Command):
    def execute(self):
        self.obj.close_file()


# window commands
class InsertChCommand(Command):
    def __init__(self, obj, ch):
        super().__init__(obj)
        self.ch = ch

    def execute(self):
        self.obj.ins_ch(self.ch)


# movement commands
class MoveToBeginningOfLineCommand(Command):
    def execute(self):
        self.obj.move_to_beginning_of_line()


class MoveToEndOfLineCommand(Command):
    def execute(self):
        self.obj.move_to_end_of_line()


class MoveForwardOneCharCommand(Command):
    def execute(self):
        self.obj.move_forward_one_char()


class MoveBackwardOneCharCommand(Command):
    def execute(self):
        self.obj.move_backward_one_char()


class MoveToPreviousLineCommand(Command):
    def execute(self):
        self.obj.move_to_previous_line()


class MoveToNextLineCommand(Command):
    def execute(self):
        self.obj.move_to_next_line()


# other commands
class BackspaceCommand(Command):
    def execute(self):
        self.obj.backspace()


class NewlineCommand(Command):
    def execute(self):
        self.obj.newline()


class ExitCommand(Command):
    def execute(self):
        sys.exit()
