import sublime, sublime_plugin
import re

class InsertBoxPromptCommand(sublime_plugin.WindowCommand):

    def run(self):

        self.window.show_input_panel("Insert Box:", "", self.on_done, None, None)
        pass

    def on_done(self, text):

        try:

            content = str(text)
            if self.window.active_view():
                self.window.active_view().run_command("insert_box", {"text": content} )

        except ValueError:
            pass



class InsertBoxCommand(sublime_plugin.TextCommand):

    def run(self, edit, text):

        view = self.view
        sel  = view.sel()

        #get the current indentation
        indent = view.rowcol(sel[0].begin())[1]

        #build the string
        longestLine = 0
        #TODO: deal with no spaces
        line2 = ""
        while (len(text) > 0):
            for i in range(indent):
                line2 += " "
            line2 += "| "

            spaces = [m.start() for m in re.finditer(" ", text)]
            split = -1
            for index in range(0, len(spaces)):
                if (spaces[index] + indent + 4 > 80):
                    split = spaces[index - 1]
                    break

            lineLength = 0;
            if (split >= 0):
                lineLength = len(text[:split]) + indent + 4
                line2 += text[:split]
                text = text[split + 1:]
            else:
                lineLength = len(text) + indent + 4
                line2 += text
                for fill in range(len(text) + indent + 4, longestLine):
                    line2 += " "
                text = ""

            line2 += " |\n"

            if (lineLength > longestLine):
                longestLine = lineLength

        line1 = "/"
        for i in range(indent + 2, longestLine):
            line1 += "*"
        line1 += "\\"

        line3 = ""
        for i in range(indent):
            line3 += " "
        line3 += "\\"
        for i in range(indent + 2, longestLine):
            line3 += "*"
        line3 += "/"

        title = line1 + "\n" + line2 + line3 + "\n"

        #place the title in the buffer
        self.view.insert(edit, self.view.sel()[0].begin(), title)
