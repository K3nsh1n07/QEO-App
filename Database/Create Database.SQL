Create database QEOApp;
use QEOApp;

CREATE TABLE clientes (
    id_cliente INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(50) NOT NULL,
	nombreCompleto VARCHAR(100),
	telefono int,

	CONSTRAINT pkIdCliente PRIMARY KEY (id_cliente)
);

CREATE TABLE menu  (
    id_menu INT NOT NULL AUTO_INCREMENT,
    nombre varchar(100),
	descripcion varchar(500),
	precio_venta float,

	CONSTRAINT pkIdMenu PRIMARY KEY (id_menu)
);

CREATE TABLE mesa  (
    id_mesa INT NOT NULL AUTO_INCREMENT,
    descripcion varchar(100),

	CONSTRAINT pkIdMesa PRIMARY KEY (id_mesa)
);

CREATE TABLE estado  (
    id_estado INT NOT NULL AUTO_INCREMENT,
    descripcion varchar(100),

	CONSTRAINT pkIdEstado PRIMARY KEY (id_estado)
);

CREATE TABLE metodo_pago (
    id_pago INT NOT NULL AUTO_INCREMENT,
    descripcion varchar(100),

	CONSTRAINT pkIdPago PRIMARY KEY (id_pago)
);


CREATE TABLE orden  (
    id_orden INT NOT NULL AUTO_INCREMENT,
    id_cliente int,
	id_mesa int,
	fecha datetime,
	total float,
	facturado int,
	id_estado int,
	id_metodo_pago int,

	CONSTRAINT pkIdorden PRIMARY KEY (id_orden),
	CONSTRAINT fk_id_cliente FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
	CONSTRAINT fk_id_mesa FOREIGN KEY (id_mesa) REFERENCES mesa(id_mesa),
	CONSTRAINT fk_id_metodo_pago FOREIGN KEY (id_metodo_pago) REFERENCES metodo_pago(id_pago)
);

CREATE TABLE orden_detalle  (
    id_orden_detalle INT NOT NULL AUTO_INCREMENT,
    id_orden int,
	id_menu int,
	id_estado int,
	precio float,
	comentarios varchar(250),
	cantidad INT,

	CONSTRAINT pkIdordenDetalle PRIMARY KEY (id_orden_detalle),
	CONSTRAINT fk_id_orden FOREIGN KEY (id_orden) REFERENCES orden(id_orden),
	CONSTRAINT fk_idMenu FOREIGN KEY (id_menu) REFERENCES menu(id_menu),
	CONSTRAINT fk_idEstado FOREIGN KEY (id_estado) REFERENCES estado(id_estado)
);


/*
#Las siguientes tablas no son creadas, ya que el alcance del proyecto se redujo.
CREATE TABLE Perfiles  (
    id_perfil INT NOT NULL AUTO_INCREMENT,
	nombre varchar(50) NOT NULL,
	descripcion varchar(50) NOT NULL,

	CONSTRAINT pkIdPerfil PRIMARY KEY (id_perfil)
);

#Usuarios Empleados o adm / #Ni los crearia
CREATE TABLE usuarios (
    id_usuario INT NOT NULL AUTO_INCREMENT,
	id_perfil INT, 
	nombre VARCHAR(20),
	apellido VARCHAR(20),
	dni int,
	passwd varchar(100),

	CONSTRAINT pkIdUsuario PRIMARY KEY (id_usuario),
	CONSTRAINT fk_idPerfil FOREIGN KEY (id_perfil) REFERENCES perfiles (id_perfil)
);
#Se quito llave en email, ya que si es PK, si el mismo cliente quiere crear una orden, es necesario levantar los creados validarlos etc.
CREATE TABLE clientes (
    id_cliente INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(100) UNIQUE NOT NULL,
	nombreCompleto VARCHAR(100),
	telefono int,

	CONSTRAINT pkIdCliente PRIMARY KEY (id_cliente)
);

CREATE TABLE categorias (
    id_categoria INT NOT NULL AUTO_INCREMENT,
    nombre varchar(100),
    
	CONSTRAINT pk_idCategoria PRIMARY KEY (id_categoria)
);

CREATE TABLE marcas (
    id_marca INT NOT NULL AUTO_INCREMENT,
    nombre varchar(100),
	
	CONSTRAINT pkIdMarca PRIMARY KEY (id_marca)
);


CREATE TABLE menu_detalle  (
    id_menu_detalle INT NOT NULL AUTO_INCREMENT,
	id_menu INT,
	id_producto INT,
	precio_articulo float,


	CONSTRAINT pkIdMenuDetalle PRIMARY KEY (id_menu_detalle),
	CONSTRAINT fk_id_menu FOREIGN KEY (id_menu) REFERENCES menu(id_menu),
	CONSTRAINT fk_idProducto FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

CREATE TABLE productos  (
    id_producto INT NOT NULL AUTO_INCREMENT,
	id_categoria INT,
	id_marca INT,
	nombre varchar(50) NOT NULL,
	precio float,
	eliminado bit,


	CONSTRAINT pkIdProducto PRIMARY KEY (id_producto),
	CONSTRAINT fk_idCategoria FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),
	CONSTRAINT fk_idMarca FOREIGN KEY (id_marca) REFERENCES marcas(id_marca)
);



*/

