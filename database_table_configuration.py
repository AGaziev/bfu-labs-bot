from data import configuration
from utils.enums import LabStatus


def configure_and_fill_database_tables() -> None:
    from repositories import db
    import utils.models
    alltables = [utils.models.User,
                 utils.models.Teacher,
                 utils.models.Group,
                 utils.models.GroupMember,
                 utils.models.LabRegistry,
                 utils.models.Status,
                 utils.models.LabWork]
    #db.drop_tables(alltables, safe=False)
    db.create_tables(alltables)
    lab_statuses = [
        {"title": LabStatus.ACCEPTED.value},
        {"title": LabStatus.NOTCHECKED.value},
        {"title": LabStatus.REJECTED.value},
    ]
    utils.models.Status.insert_many(lab_statuses).execute()
    user, is_exists = utils.models.User.get_or_create(telegram_id=configuration.admins[0], username="vcdddk")
    utils.models.Teacher.get_or_create(first_name="admin", last_name="adminov", patronymic="adminovich", user=user)


if __name__ == '__main__':
    configure_and_fill_database_tables()
