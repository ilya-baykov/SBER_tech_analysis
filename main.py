import requests
import apimoex
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from ta.trend import SMAIndicator, EMAIndicator


class Dataset:
    def __init__(self, ticket: str, period: tuple):
        self.__ticket = ticket
        self.__period = period
        self.__dataset = self.dataset_formation()

    def dataset_formation(self):
        with requests.Session() as session:
            dataset = pd.DataFrame(
                apimoex.get_board_history(session=session, security=self.__ticket, start=self.__period[0],
                                          end=self.__period[1], columns=("TRADEDATE", "CLOSE", "VOLUME", "VALUE")))
            dataset = dataset.set_index("TRADEDATE")
            return dataset

    def data_recording(self):
        self.__dataset.to_csv(f"Цены на акцию {self.__ticket}")
        print(
            f"Запись цен акций {self.__ticket} за последний год ( с {self.__period[1]} по {self.__period[0]} ) выполнилась "
            f"успешно !",
            '\n')
        print(self.__dataset.info)


class UserInteraction:
    __offer_update_data = False
    __today = None
    __day_year_ago = None

    def __init__(self):
        UserInteraction.__defines_period()
        UserInteraction.__offer_update_data = UserInteraction.__handling_input()
        UserInteraction.__update_data()

    @classmethod
    def __handling_input(cls):
        with open("last_upd", "a+") as last_date_update:
            last_date_update.seek(0)
            answer = input(
                f"Последние данные были обновлены {last_date_update.readline().strip()}."
                f" Хотите загрузить новые ? (1 / 0 )\t\t")
            if "1" in answer:
                last_date_update.seek(0)
                last_date_update.truncate()
                last_date_update.write(str(cls.__today))
                return True
            else:
                return False

    @classmethod
    def __defines_period(cls):
        cls.__today = datetime.date.today()
        cls.__day_year_ago = cls.__today.replace(year=cls.__today.year - 1)

    @classmethod
    def get_period(cls) -> tuple[str, str]:
        return str(cls.__day_year_ago), str(cls.__today)

    @classmethod
    def __update_data(cls):
        if cls.__offer_update_data:
            SBER = Dataset(ticket="SBER", period=(cls.get_period()))
            SBER.dataset_formation()
            SBER.data_recording()


class TechnicalIndicators:
    @staticmethod
    def sma_indicator(close, window=21):
        SMA = SMAIndicator(close, window)
        return SMA.sma_indicator()

    @staticmethod
    def ema_indicator(close, window=21):
        EMA = EMAIndicator(close, window)
        return EMA.ema_indicator()


class DrawingGraphs:
    @staticmethod
    def draw_graphs(graphs: list, labels: list):
        colors = ["blue", "green", "red"]
        for i, (graph, label) in enumerate(zip(graphs, labels)):
            plt.plot(graph, label=label, color=colors[i])
        plt.xlabel("Date")
        plt.ylabel('Close Price')
        plt.title('Stock Price')
        plt.xticks(dataset.index[::10], rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.xticks(rotation=45)
        plt.show()


if __name__ == '__main__':
    _USER = UserInteraction()
    dataset = pd.read_csv("Цены на акцию SBER", index_col="TRADEDATE")
    sma = TechnicalIndicators.sma_indicator(dataset["CLOSE"], 21)
    ema = TechnicalIndicators.ema_indicator(dataset["CLOSE"], 21)
    DrawingGraphs.draw_graphs([dataset["CLOSE"], sma, ema], ["CLOSE", "SMA", "EMA"])
