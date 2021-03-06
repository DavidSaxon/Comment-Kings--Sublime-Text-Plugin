import sublime, sublime_plugin

LINE_LENGTH = 80

class InsertTitlePromptCommand(sublime_plugin.WindowCommand):

    def run(self):

        self.window.show_input_panel(
            "Insert Title:", "", self.on_done, None, None)


    def on_done(self, text):

        try:
            name = str(text)
            name = name.upper()
            if self.window.active_view():
                self.window.active_view().run_command(
                    "insert_title", {"name": name} )
        except ValueError:
            pass



class InsertTitleCommand(sublime_plugin.TextCommand):

    def run(self, edit, name):

        view = self.view
        sel  = view.sel()

        #get the current indentation
        indent = view.rowcol(sel[0].begin())[1]

        #build the string
        line1 = "//" + ("-" * (LINE_LENGTH - (indent + 2)))
        line2 = (" " * indent) + "//"
        centre = (80 - (len(line2) + len(name) - 2)) / 2
        line2 += (" " * centre) + name
        line3 = (" " * indent) + "//" + ("-" * (LINE_LENGTH - (indent + 2)))
        title = line1 + "\n" + line2 + "\n" + line3 + "\n"

        #place the title in the buffer
        self.view.insert(edit, self.view.sel()[0].begin(), title)
