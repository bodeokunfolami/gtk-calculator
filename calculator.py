import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk, Gdk


class Handlers:

    def __init__(self, entry):
        self.screen = entry

    @staticmethod
    def on_destroy(*args):
        gtk.main_quit()

    def on_reset_clicked(self, button):
        self.screen.set_text('')

    def on_del_clicked(self, button):
        text = self.screen.get_text()
        text = text[:-1]
        self.screen.set_text(text)
        self.screen.set_position(len(text))

    def on_button_clicked(self, button):
        text = button.get_label()
        entry = self.screen.get_text()
        new_text = (entry + text)
        self.screen.set_text(new_text)
        self.screen.set_position(len(new_text))

    def on_entry_changed(self, entry):
        screen_context = self.screen.get_style_context()
        if screen_context.has_class("danger-border"):
            screen_context.remove_class("danger-border")

    def calculate(self, entry):
        expression = self.screen.get_text()

        expression = expression.replace("÷", "/")
        expression = expression.replace("×", "*")

        try:
            result = str(eval(expression))
            self.screen.set_text(result)
            self.screen.set_position(len(result))
        except (SyntaxError, NameError):
            screen_context = self.screen.get_style_context()
            screen_context.add_class("danger-border")


def main():
    builder = gtk.Builder()
    builder.add_from_file("window.glade")
    entry = builder.get_object("screen")
    handlers = Handlers(entry)
    builder.connect_signals(handlers)

    window = builder.get_object("window1")
    window.set_position(gtk.WindowPosition.CENTER_ALWAYS)
    window.show_all()


if __name__ == '__main__':
    style_provider = gtk.CssProvider()
    style_provider.load_from_path('css/style.css')
    gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        style_provider,
        gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
    main()
    gtk.main()
