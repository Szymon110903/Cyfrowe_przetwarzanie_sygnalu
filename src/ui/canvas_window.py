from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg


class MplCanvas(FigureCanvasQTAgg):
   def __init__(self, parent=None, width=5, height=4, dpi=100):
      fig = Figure(figsize=(width, height), dpi=dpi)
      self.axes = fig.add_subplot(111)

      # Włączenie dynamicznego dopasowywania marginesów zapobiega ucinaniu tekstów
      try:
         fig.set_layout_engine('tight')  # Dla nowszych wersji Matplotlib (>= 3.6)
      except AttributeError:
         fig.set_tight_layout(True)  # Dla starszych wersji Matplotlib

      super().__init__(fig)