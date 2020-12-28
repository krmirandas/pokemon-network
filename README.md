# Pokemon-Network

## Integrantes

* Licon Colon Francisco Arturo
* Miranda Sanchez Kevin Ricardo
* Molina Bis Victor Hugo

# Ejecución del programa

Al ingresar al directorio, lo primero que debera hacerse sera:
```bash
make
```
Lo que permitirá ver los comandos que ayudar a la instalación del proyecto.

Se deberá tener previamente instalado python 3  y  `pip3` y debera ejecutarse:
```bash
make prepare-env
```

Ahora bien, se instalara la base de datos y el manual de Unix
```bash
make build
```
El comando para limpiar el proyecto es
```bash
make clean
```
---

Para ejecutar el cliente se deberá ejecutar el siguiente comando
```bash
make run_pokemon_client
```

Para ejecutar el servidor se deberá ejecutar el siguiente comando
```bash
make run_pokemon_server
```
---

Deberá ejecutarse antes el servidor, pues un cliente no puede conectarse a un servicio que no existe

## Manuales de Unix

```
man pokemon_client
```

```
man pokemon_server
```

---
## Documentación

La documentación fue hecha en
[Sphinx](http://www.sphinx-doc.org/en/1.5/index.html#).
Se generaron documentos html en la carpeta `doc/build/html`, aqui solo debe abrirse `index.html`.
# pokemon-network
