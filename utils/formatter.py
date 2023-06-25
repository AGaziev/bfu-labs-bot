class Formatter:
    @staticmethod
    def list_of_students(studs: dict[int:str]):
        """
        formatting student list like:
        {id}. {creds}
        1. Иван Иванов
        2. Андрей Кутузов
        3. Евгений Пригожин
        """
        return "\n".join([f"{i}. {s}" for i, s in studs])