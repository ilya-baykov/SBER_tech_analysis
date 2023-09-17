import requests
import apimoex
import pandas as pd
import datetime


class Dataset:
    def __init__(self, ticket: str, period: tuple):
        self.ticket = ticket
        self.period = period
        self.dataset = self.get_dataset()

    def get_dataset(self):
        with requests.Session() as session:
            dataset = pd.DataFrame(
                apimoex.get_board_history(session=session, security=self.ticket, start=self.period[0],
                                          end=self.period[1], columns=("TRADEDATE", "CLOSE", "VOLUME", "VALUE")))
            dataset = dataset.set_index("TRADEDATE")
            return dataset

    def data_recording(self):
        self.dataset.to_csv(f"Цены на акцию {self.ticket}")
        print(
            f"Запись цен акций {self.ticket} за последний год ( с {self.period[1]} по {self.period[0]} ) выполнилась "
            f"успешно !",
            '\n')
        print(self.dataset.info)

    class TechnicalIndicators:
        pass

    class DrawingGraphs:
        pass


if __name__ == '__main__':
    SBER = Dataset("SBER", ("2022-9-17", "2023-9-17"))
    SBER.data_recording()
