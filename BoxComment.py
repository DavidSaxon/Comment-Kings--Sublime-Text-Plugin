import sublime, sublime_plugin
import re

class InsertBoxPromptCommand(sublime_plugin.WindowCommand):

    def run(self):

        self.window.show_input_panel(
            "Insert Box:", "", self.on_done, None, None)

    def on_done(self, text):

        try:
            content = str(text)
            if self.window.active_view():
                self.window.active_view().run_command(
                    "insert_box", {"text": content} )
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

            #indent
            line2 += (" " * indent) + "| "

            #split at the last possible space
            spaces = [m.start() for m in re.finditer(" ", text)]
            split = -1
            for index in range(0, len(spaces)):
                if (spaces[index] + indent + 4 > 80):
                    split = spaces[index - 1]
                    break

            #write the line
            lineLength = 0;
            if (split >= 0):
                t = text[:split]
                lineLength = len(t) + indent + 4
                line2 += t + (" " * (longestLine - (len(t) + indent + 4)))
                text = text[split + 1:]
            else:
                lineLength = len(text) + indent + 4
                line2 += text + (" " * (longestLine - (len(text) + indent + 4)))
                text = ""
            line2 += " |\n"

            #store the longest line
            if (lineLength > longestLine):
                longestLine = lineLength

        #create the top and bottom bars
        line1 = "/" + ("*" * (longestLine - (indent + 2))) + "\\"

        line3 = (
            (" " * indent) + "\\" + ("*" * (longestLine - (indent + 2))) + "/")

        title = line1 + "\n" + line2 + line3 + "\n"

        #place the title in the buffer
        self.view.insert(edit, self.view.sel()[0].begin(), title)
