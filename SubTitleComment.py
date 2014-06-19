import sublime, sublime_plugin

LINE_LENGTH = 80

class InsertSubTitlePromptCommand(sublime_plugin.WindowCommand):

    def run(self):

        self.window.show_input_panel("Insert Sub Title:", "", self.on_done, None, None)
        pass

    def on_done(self, text):

        try:

            name = str(text)
            name = name.upper()
            if self.window.active_view():
                self.window.active_view().run_command("insert_sub_title", {"name": name} )

        except ValueError:
            pass


class InsertSubTitleCommand(sublime_plugin.TextCommand):

    def run(self, edit, name):

        view = self.view
        sel  = view.sel()

        #get the current indentation
        indent = view.rowcol(sel[0].begin())[1]

        #build the string
        title = "//"
        title += "-" * (((LINE_LENGTH - indent - len(name)) / 2) - 1)
        title += name
        title += "-" * (LINE_LENGTH - len(title))

        #place the title in the buffer
        self.view.insert(edit, self.view.sel()[0].begin(), title)
