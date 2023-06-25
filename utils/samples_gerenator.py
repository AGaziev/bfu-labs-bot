from io import BytesIO

class SamplesGenerator:
    @staticmethod
    def get_students_list_txt_example()->BytesIO:
        utf8_txt = "Иван Иванов\n"+\
                    "Андрей Кутузов\n"+\
                    "Евгений Пригожин\n"+\
                    "Александр Пушкин\n"+\
                    "Федор Достоевский\n"+\
                    "Михаил Лермонтов\n"+\
                    "Александр Грибоедов\n"+\
                    "Эдуард Успенский\n"+\
                    "Александр Солженицын\n"+\
                    "Михаил Шолохов\n"+\
                    "Захар Прилепин\n"
        return BytesIO(utf8_txt.encode('utf-8'))

    @staticmethod
    def get_students_list_xlsx_example()->BytesIO:
        ...

    @staticmethod
    def get_students_list_csv_example()->BytesIO:
        ...