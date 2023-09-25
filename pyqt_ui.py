import pandas as pd
from PyQt5 import uic, QtWidgets

from main import UserInteraction, TechnicalIndicators, DrawingGraphs

Form, _ = uic.loadUiType("Tech_analysis.ui")


class Ui(QtWidgets.QDialog, Form):
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.printButtonPressed)

    def printButtonPressed(self):
        _USER = UserInteraction()
        dataset = pd.read_csv("Цены на акцию SBER", index_col="TRADEDATE")
        sma = TechnicalIndicators.sma_indicator(dataset["CLOSE"], 21)
        ema = TechnicalIndicators.ema_indicator(dataset["CLOSE"], 21)
        rsi_14 = TechnicalIndicators.rsi_indicator(dataset["CLOSE"], 14)
        bb_21 = TechnicalIndicators.bollinger_bands(dataset["CLOSE"], 21)
        DrawingGraphs.draw_graphs([dataset["CLOSE"], sma, ema, rsi_14, bb_21], ["CLOSE", "SMA", "EMA", "RSI", "BB"],
                                  dataset=dataset)
        TechnicalIndicators.intersection_SMA_EMA_search(sma, ema)
        TechnicalIndicators.maxDrawnDown(dataset)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    w.show()
    sys.exit(app.exec_())
