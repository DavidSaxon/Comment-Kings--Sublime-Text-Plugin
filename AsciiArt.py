import sublime, sublime_plugin
import lib/png, math, array, os

class InsertAsciiArtPromptCommand(sublime_plugin.WindowCommand):

    def run(self):

        self.window.show_input_panel("Path to png image:", "", self.on_done, None, None)
        pass

    def on_done(self, text):

        try:

            filename = str(text)
            if self.window.active_view():
                self.window.run_command("ascii_art_size_prompt", {"filename": filename} )

        except ValueError:
            pass

class AsciiArtSizePromptCommand(sublime_plugin.WindowCommand):

    f = ""

    def run(self, filename):

        self.f = filename
        self.window.show_input_panel("Size of image (where 1 is full size, 2 is half size and so on):", "", self.on_done, None, None)
        pass

    def on_done(self, text):

        try:

            size = int(text)
            if self.window.active_view():
                self.window.active_view().run_command("insert_ascii_art", {"filename": self.f, "size": size} )

        except ValueError:
            pass


class InsertAsciiArtCommand(sublime_plugin.TextCommand):

    def run(self, edit, filename, size):

        filename = str(os.path.expanduser(filename))
        file = open(filename)

        view = self.view
        sel  = view.sel()

        #get the data from the image
        reader = png.Reader(file)
        w, h, pixels, metadata = reader.read_flat()
        pixelWidth = 4 if metadata["alpha"] else 3

        #TODO: average skipped data
        #iterate over the image to get the characters for the pixels
        text = "/*\n"
        scale = int(math.ceil(w / 80.0)) * size
        for y in range (0, h, scale * 2):
            for x in range(0, w * pixelWidth, pixelWidth * scale):

                #get the data from pixels
                sumVal = 0
                count = 0
                for j in range(0, scale * 2):

                    if (y + j >= h):
                        break

                    for i in range(0, scale):

                        if (x + (i * pixelWidth) >= w * pixelWidth):
                            break

                        count += 1
                        value =  256 - pixels[(x + (i * pixelWidth)) + (w * pixelWidth * (y + j))]
                        value += 256 - pixels[(x + (i * pixelWidth)) + (w * pixelWidth * (y + j)) + 1]
                        value += 256 - pixels[(x + (i * pixelWidth)) + (w * pixelWidth * (y + j)) + 2]
                        value /= 3

                        if (pixelWidth == 4):
                            value *= pixels[(x + (i * pixelWidth))  + (w * pixelWidth * (y + j)) + 3] / 255

                        sumVal += value

                #average data
                if (count == 0):
                    break
                sumVal /= count

                if (sumVal == 0):
                    text += " "
                elif (sumVal <= 32):
                    text += "."
                elif (sumVal <= 64):
                    text += ","
                elif (sumVal <= 96):
                    text += ":"
                elif (sumVal <= 128):
                    text += ";"
                elif (sumVal <= 160):
                    text += "\'"
                elif (sumVal <= 192):
                    text += "+"
                elif (sumVal <= 224):
                    text += "@"
                else:
                    text += "#"

            text += "\n"

        text += "*/\n"

        #place the title in the buffer
        self.view.insert(edit, self.view.sel()[0].begin(), text)
