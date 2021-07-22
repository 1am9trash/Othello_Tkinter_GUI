from App import App
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-b", action="store", dest="board",
                    default=8, help="Set board's size", type=int)
# parser.add_argument("-m", action="store", dest="mode", help="Use GUI or CMD")

results = parser.parse_args()

app = App(results.board, True, True)
app.render()
app.root.mainloop()
