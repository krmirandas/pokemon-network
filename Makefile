.PHONY: all prepare-env create_manual create_db build manual_pokemon_server manual_pokemon_client clean run_pokemon_client run_pokemon_server

UNAME_S=$(shell uname -s)

all:

	@cat logo.txt
	@echo "make prepare-env"
	@echo "    Prepara el entorno."
	@echo "    Se necesita ejecutar con sudo para instalar el manejador de paquetes de Python3."
	@echo "create_manual"
	@echo "    Crea el manual."
	@echo "make build"
	@echo "    Construye el proyecto."
	@echo "make create_db"
	@echo "    Crea el directorio de la base de datos y la incializa."
	@echo "make clean"
	@echo "    Limpia el proyecto y eleimina los archivos generados en el build."
	@echo "make run_pokemon_client"
	@echo "    Ejecuta el cliente de Pokemon."
	@echo "make run_pokemon_server"
	@echo "    Ejecuta el servidor de Pokemon."

prepare-env:
			echo ....................Se instalaran las dependencias para levantar el proyecto........................\
			sudo easy_install pip; \
			echo OK; \
			sudo apt-get install python3-pip; \
			echo OK; \
			pip3 install -r requirements.txt

create_manual:
		@if [ $(UNAME_S) = "Darwin" ]; then \
			cp manpages/pokemon_server.1 /usr/local/share/man/man1/pokemon_server.1; \
			gzip /usr/local/share/man/man1/pokemon_server.1; \
			cp manpages/pokemon_client.1 /usr/local/share/man/man1/pokemon_client.1; \
			gzip /usr/local/share/man/man1/pokemon_client.1; \
			echo OK; \
		fi

create_db:
		@if [ ! -d "src/DB" ]; then \
			cd src && mkdir db && python3 seed.py; \
			echo "La base de datos fue inicializada"; \
		fi
		@echo OK;

clean:
		@rm -rf src/db 2> /dev/null || true
		@rm -rf src/__pycache__ 2> /dev/null || true
		@rm src/*.png 2> /dev/null || true

run_pokemon_client:
		@cd src && python3 client.py

run_pokemon_server:
		@cd src && python3 server.py

build: create_manual create_db
		@echo OK
