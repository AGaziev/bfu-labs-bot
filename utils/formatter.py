class Formatter:
    @staticmethod
    def list_of_students(studs: dict[int, str]):
        """
        formatting student list like:
        {id}. {creds}
        1. Иван Иванов
        2. Андрей Кутузов
        3. Евгений Пригожин
        """
        return '\n'.join([f"{id_}. {credentials}" for id_, credentials in studs.items()])

    @staticmethod
    def group_menu_lab_stats(lab_stats: ([dict], [dict])):
        """
        formatting lab_stats for menu:
        {accepted}/{not_done}
        Не сделаны:
        {id}.{descr}
        """
        accepted, not_done = len(lab_stats[0]), len(lab_stats[1])
        result = f"{accepted}/{not_done}\n"
        for lab in lab_stats:
            if lab["status"] == "Не сдано":
                result += f"{lab['number']}. {lab['descr']}\n"
        return result
