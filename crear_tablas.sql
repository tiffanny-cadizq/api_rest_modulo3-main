create table usuarios(
cedula_identidad numeric(8) primary key,
nombre varchar(30),
primer_apellido varchar(30),
segundo_apellido varchar(30),
fecha_nacimiento date);

insert into usuarios values(1234,'juan','Perez','Guzman','1960-04-12'),
(1236,'Ana','Barbara','Rodriguez','1970-11-12'),
(1237,'Jorge','Alvarez','Mamani','1990-09-01');