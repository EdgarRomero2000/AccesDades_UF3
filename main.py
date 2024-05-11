from enum import Enum
from typing import Union
from fastapi import FastAPI, UploadFile
import botiga_db
from pydantic import BaseModel

app = FastAPI()

#Fem el model del producte per a que si pasem una variable de un tipus equivocat peti abans el codi
class producte(BaseModel):
    nom:str
    descripcio:str
    companyia:str
    preu:float
    unitats:int
    subcategoria:str


class orderbyEnum(str,Enum):
    ascendiente = "asc"
    descendiente = "desc"

#Metode per llegir tots els productes de la base de dades de la taula product
@app.get("/product/")
def llegir_productes():
    return botiga_db.productes_schema(botiga_db.read())

#Metode per llegir el producte asociat amb la id que pasem
@app.get("/product/{product_id}")
def llegir_un_producte(product_id:int):
    return botiga_db.producte_search_by_id(product_id)

#Metode per afegir un producte 
@app.post("/product/")
def afegir_un_producte(data:producte):
    nom = data.nom
    descripcio = data.descripcio
    companyia = data.companyia
    preu = data.preu
    unitats = data.unitats
    subcategoria = data.subcategoria
    botiga_db.create_producte(nom,descripcio,companyia,preu,unitats,subcategoria)
    return {
        "Missatge":" “S'ha afegit correctement"
    }

#Metode per canviar el preu d'un producte del qual pasem la id
@app.put("/product/producte/{id}")
def actualitzar_producte(id:int,preu:float):
    modificat = botiga_db.update_preu(id,preu)
    return{
        "Objecte": modificat,
        "Missatge":"S'ha modificat correctament"
    }

#Metode per borrar un producte del qual pasem la id
@app.delete("/producte/{id}")
def borrar_producte(id:int):
    botiga_db.delete_producte(id)
    return{
        "Missatge":"S'ha borrat correctament"
    }

#Metode per mostrar tots els productes de la taula de product amb la seva subategoria y categoria
@app.get("/productAll/")
def llegir_productes_orderby():
    return botiga_db.get_all()

#Metode per mostrar tots els productes de la taula de product amb la seva subategoria y categoria y amb el query parameter order by
@app.get("/productAllOrderBy/")
def llegir_productes_orderby(orderby:orderbyEnum):
    return botiga_db.get_all_order_by(orderby)

#Metode per mostrar els productes ,que contenen la string del query parameter, de la taula de product amb la seva subategoria y categoria.
@app.get("/productAllText/")
def llegir_productes_contains(contains:str):
    return botiga_db.get_all_contains(contains)

#Metode per mostrar els productes de la taula de product amb la seva subategoria y categoria começant a partir del skip y el nombre de limit.
@app.get("/productAllSkipLimit/")
def llegir_productes_skip_limit(skip:int|None=None,limit:int|None=None):
    if skip != None and limit !=None:
        if skip < 0 or limit < 0:
            return{
                "Missatge":"Els valors de skip o limit no pot ser Negatiu"
            }
        elif skip > 100 or limit > 100:
            return{
                "Missatge":"Els valors de skip o limit no poden superar 100"
            }
    return botiga_db.get_all_skip_limit(skip,limit)

#Metode per  a la carrega masiva de dades a traves d'un fitxer
@app.post("/loadProducts")
async def carregar_molts_productes(fitxer:UploadFile):
    error = await botiga_db.carrega_masiva(fitxer)
    if(error != None):
        return {
        "Missatge":error
    }
    return {
        "Missatge":"S'han carregat les dades correctament"
    }
    