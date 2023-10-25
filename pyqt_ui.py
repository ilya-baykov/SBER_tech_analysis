import pandas as pd
from PyQt5 import uic, QtWidgets

from main import UserInteraction, TechnicalIndicators, DrawingGraphs

Form, _ = uic.loadUiType("Tech_analysis.ui")


class Ui(QtWidgets.QDialog, Form):
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.printButtonPressed)
        self.checkBox_SMA.setChecked(True)
        self.checkBox_EMA.setChecked(True)
        self.checkBox_RSI.setChecked(True)
        self.checkBox_BB.setChecked(True)

    def printButtonPressed(self):
        check_box_checker = {key: value for key, value in
                             {"CLOSE": True, "SMA": self.checkBox_SMA.isChecked(), "EMA": self.checkBox_EMA.isChecked(),
                              "RSI": self.checkBox_RSI.isChecked(), "BB": self.checkBox_BB.isChecked()}.items() if
                             value}
        indicators_mapping = {
            "CLOSE": dataset["CLOSE"],
            "SMA": sma,
            "EMA": ema,
            "RSI": rsi_14,
            "BB": bb_21
        }
        selected_indicators = {}
        for key, value in check_box_checker.items():
            selected_indicators[key] = indicators_mapping[key]

        DrawingGraphs.draw_graphs([indicator for indicator in selected_indicators.values()],
                                  [label_indicator for label_indicator in selected_indicators],
                                  dataset=dataset)
        TechnicalIndicators.intersection_SMA_EMA_search(sma, ema)
        if self.checkBox_MDD.isChecked():
            TechnicalIndicators.maxDrawnDown(dataset)


if __name__ == '__main__':
    import sys

    _USER = UserInteraction()
    dataset = pd.read_csv("Цены на акцию SBER", index_col="TRADEDATE")
    sma = TechnicalIndicators.sma_indicator(dataset["CLOSE"], 21)
    ema = TechnicalIndicators.ema_indicator(dataset["CLOSE"], 21)
    rsi_14 = TechnicalIndicators.rsi_indicator(dataset["CLOSE"], 14)
    bb_21 = TechnicalIndicators.bollinger_bands(dataset["CLOSE"], 21)

    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    w.show()
    sys.exit(app.exec_())
