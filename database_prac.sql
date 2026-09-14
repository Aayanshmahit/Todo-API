CREATE TABLE todos(
    id integer primary key,
    title text not NULL,
    descripton text,
    completion boolean
);

INSERT INTO todos(title , descripton , completion)
VALUES('fastapi' , 'learn fast api' , false);
INSERT INTO todos(title , descripton , completion)
VALUES('sql' , 'learn sql' , false);
INSERT INTO todos(title , descripton , completion)
VALUES('doubts' , 'clear project doubts' , true);

SELECT * FROM todos
WHERE title = "sql";

UPDATE todos
SET completion = true
where id == 2;

UPDATE todos
SET title = "sql learning"
where id = 2;

UPDATE todos
SET descripton 