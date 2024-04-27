create table if not exists names_man
(
    id   serial
        primary key,
    name varchar(100) not null
);
create table if not exists names_woman
(
    id   serial
        primary key,
    name varchar(100) not null
);
INSERT INTO names_woman (id, name) VALUES
                                              (DEFAULT, 'Ирина'),
                                              (DEFAULT, 'Анна'),
                                              (DEFAULT, 'Ольга'),
                                              (DEFAULT, 'Евгения');
INSERT INTO names_man (id, name) VALUES
                                              (DEFAULT, 'Александр'),
                                              (DEFAULT, 'Игорь'),
                                              (DEFAULT, 'Евгений'),
                                              (DEFAULT, 'Владимир');