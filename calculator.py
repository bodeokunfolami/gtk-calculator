gi.require_version('Gtk', '3.0')
import gi
from gi.repository import Gtk as gtk, Gdk



class CalculatorWindow(gtk.Window):

    answer = None

    def __init__(self):
        super().__init__()
        self.set_title("Calculator")
        self.set_resizable(False)
        self.set_border_width(5)

        grid = gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_spacing(10)

        self.button_panel = gtk.Grid()
        self.button_panel.set_column_homogeneous(True)
        self.button_panel.set_column_spacing(10)
        self.button_panel.set_row_spacing(10)

        self.entry = gtk.Entry()
        self.entry.set_size_request(0, 60)
        self.entry.set_alignment(1)
        self.entry.connect('activate', self.calculate)

        self.set_button_row(1, 7)
        self.set_button_row(0)
        self.set_button_row(2, 4)
        self.set_button_row(3, 1)
        # Draw the last row of the calculator
        self.set_button_row(4)
        grid.attach(self.entry, 0, 0, 1, 1)

        grid.attach(self.button_panel, 0, 1, 1, 1)
        self.add(grid)

    def set_button_row(self, row_number, first_number=None):
        if row_number == 0:
            for i in range(0, 4):
                if i == 0:
                    button = gtk.Button(label='C')
                    button_context = button.get_style_context()
                    button_context.add_class('reset-button')
                    button.connect('clicked', self.on_reset_click)
                if i == 1:
                    button = gtk.Button(label='DEL')
                    button.connect('clicked', self.on_del_click)
                if i == 2:
                    button = gtk.Button(label='%')
                if i == 3:
                    button = gtk.Button(label='÷')
                    button.connect('clicked', self.on_button_click)
                button.set_size_request(78, 45)
                button.set_can_focus(False)
                self.button_panel.attach(button, i, row_number, 1, 1)
        if row_number < 4 and row_number > 0:
            for i in range(0, 3):
                number = '%s' % (i + first_number)
                button = gtk.Button(label=number)
                button.connect('clicked', self.on_button_click)
                button.set_can_focus(False)
                button.set_size_request(78, 45)
                self.button_panel.attach(button, i, row_number, 1, 1)
        if row_number == 1:
            operation_button = gtk.Button(label='×')
            operation_button.connect('clicked', self.on_button_click)
            operation_button.set_can_focus(False)
            self.button_panel.attach(operation_button, 3, row_number, 1, 1)
        if row_number == 2:
            operation_button = gtk.Button(label='−')
            operation_button.set_can_focus(False)
            operation_button.connect('clicked', self.on_button_click)
            self.button_panel.attach(operation_button, 3, row_number, 1, 1)
        if row_number == 3:
            operation_button = gtk.Button(label='+')
            operation_button.set_can_focus(False)
            operation_button.connect('clicked', self.on_button_click)
            self.button_panel.attach(operation_button, 3, row_number, 1, 1)
        if row_number == 4:
            for i in range(0, 4):
                if i == 0:
                    button = gtk.Button(label='0')
                    button.connect('clicked', self.on_button_click)
                if i == 1:
                    button = gtk.Button(label='.')
                    button.connect('clicked', self.on_button_click)
                if i == 2:
                    button = gtk.Button(label='ANS')
                    button.connect('clicked', self.on_ans_click)
                if i == 3:
                    button = gtk.Button(label='=')
                    button.connect('clicked', self.calculate)
                    button_context = button.get_style_context()
                    button_context.add_class("calculate")
                button.set_can_focus(False)
                button.set_size_request(78, 45)
                self.button_panel.attach(button, i, row_number, 1, 1)

    def on_reset_click(self, widget):
        self.entry.set_text('')

    def on_del_click(self, widget):
        text = self.entry.get_text()
        # remove the last character in a string
        text = text[:-1]
        self.entry.set_text(text)
        self.entry.set_position(len(text))

    def on_button_click(self, widget):
        text = widget.get_label()
        entry = self.entry.get_text()
        self.entry.set_text(entry + text)
        length = len(entry + text)
        self.entry.set_position(length)

    def on_ans_click(self, widget):
        answer = CalculatorWindow.answer
        text = self.entry.get_text()
        if answer != None:
            self.entry.set_text(text + answer)
            self.entry.set_position(len(text + answer))

    def calculate(self, widget):
        result = 1
        command = self.entry.get_text()
        # find oprators
        mult = command.find('×')
        div = command.find('÷')
        add = command.find('+')
        sub = command.find('−')

        if div != -1:
            command = command.replace('÷', '/')
        if mult != -1:
            command = command.replace('×', '*')
        if add != -1:
            command = command.replace('+', '+')
        if sub != -1:
            command = command.replace('−', '-')

        result = eval(command)
        if result % 1 == 0:
            result = int(result)

        CalculatorWindow.answer = str(result)
        self.entry.set_text(str(result))
        self.entry.set_position(len(str(result)))


if __name__ == '__main__':
    style_provider = gtk.CssProvider()
    style_provider.load_from_path('css/style.css')
    gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        style_provider,
        gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
    calculator = CalculatorWindow()
    calculator.connect("delete-event", gtk.main_quit)
    calculator.show_all()
    gtk.main()
