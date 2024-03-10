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
    utils.models.User(telegram_id="292667494", username="vcdddk").save()
    utils.models.Teacher(first_name="Alan", last_name="Gazziev", patronymic="gazievich",user="292667494").save()

if __name__ == '__main__':
    configure_and_fill_database_tables()
