
from datetime import datetime

from fastapi import UploadFile
from conexio import conexio

#Metode que retorna un producte en format JSON
def producte_schema(producte)->dict:
    return{"Id":producte[0],
           "Nom":producte[1],
           "Descripcio":producte[2],
           "Companyia":producte[3],
           "Preu":producte[4],
           "Unitats":producte[5],
           "Subcategoria":producte[6],
           "Creat":producte[7],
           "Actualitzat":producte[8]
           }


#Segona versio per retornar productes amb categoria i subcategoria en format JSON
def producte_schema2(producte)->dict:
    return{"Categoria":producte[0],
           "Subcategoria":producte[1],
           "Nom":producte[2],
           "Companyia":producte[3],
           "Preu":producte[4]
           }


#Metode que retorna un llistat de productes en format JSON
def productes_schema(productes)->dict:
    return[producte_schema(producte) for producte in productes]


#Segona versio que retorna un llistat de productes amb categoria i subcategoria
def productes_schema2(productes)->dict:
    return[producte_schema2(producte) for producte in productes]


#Metode que llegeix tots els registres de la taula product
def read():
    try:
        conn=conexio()
        cur=conn.cursor()
        cur.execute("select * from product")
        result = cur.fetchall()
    except Exception as e:
        return{"status":-1,"message":f"Error de connexió:{e}"}
    finally:
        conn.close()

    return result


#Metode que llegeix un registre de la taula product segons el ID
def producte_search_by_id(id)->dict:
    try:
        conn=conexio()
        cur=conn.cursor()
        cur.execute(f"select * from product WHERE product_id={id}")
        result = cur.fetchall()
    except Exception as e:
        return{"status":-1,"message":f"Error de connexió:{e}"}
    finally:
        conn.close()

    return productes_schema(result)


#Metode que afegeix un nou registre a la taula productes fent primer una consulta a subcategoria per asegurarse que existeix
def create_producte(nom:str,descripcio:str,companyia:str,preu:float,unitats:int,subcategoria:str):
    try:
        conn=conexio()
        cur=conn.cursor()
        cur.execute(f"select subcategory_id from subcategory where name = '{subcategoria}'")
        idSubcat = cur.fetchone()[0]        
        cur.execute(f"insert into product(name,description,company,price,units,subcategory_id) VALUES('{nom}','{descripcio}','{companyia}',{preu},{unitats},{idSubcat});")
        conn.commit()
    except Exception as e:
        return{"status":-1,"message":f"Error de connexió:{e}"}
    finally:
        conn.close()


#Metode que actualitza el preu de un producte segons la ID
def update_preu(id:int,preu:float):
    try:
        conn=conexio()
        cur=conn.cursor()
        query = f"update product set price = {preu} WHERE product_id = {id};"
        cur.execute(query)
        conn.commit()
        cur.execute(f"Select * from product where product_id={id}")
        result = productes_schema(cur.fetchall())
    except Exception as e:
        return{"status":-1,"message":f"Error de connexió:{e}"}
    finally:
        conn.close()
    
    return result


#Metode que borra un producte segons ID
def delete_producte(id:int):
    try:
        conn=conexio()
        cur=conn.cursor()
        query = f"DELETE FROM product WHERE product_id = {id};"
        cur.execute(query)
        conn.commit()
    except Exception as e:
        return{"status":-1,"message":f"Error de connexió:{e}"}
    finally:
        conn.close()  


#Metode que retorna una llista amb la categoria,subcategoria,producte,marca y preu de cada producte
def get_all():
    try:
        conn=conexio()
        cur=conn.cursor()
        query = ("SELECT c.name,s.name,p.name,p.company,p.price FROM product as p LEFT OUTER JOIN subcategory as s " 
        + "on p.subcategory_id = s.subcategory_id LEFT OUTER JOIN category as c on s.category_id = c.category_id ")
        cur.execute(query)
        result = cur.fetchall()
    except Exception as e:
        return{"status":-1,"message":f"Error de connexió:{e}"}
    finally:
        conn.close() 
    return productes_schema2(result)


#Metode que retorna una llista amb la categoria,subcategoria,producte,marca y preu de cada producte
#també utilitzem el query parameter per ordenar la llista per nom asc o desc
def get_all_order_by(orderby:str):
    try:
        conn=conexio()
        cur=conn.cursor()
        query = ("SELECT c.name,s.name,p.name,p.company,p.price FROM product as p LEFT OUTER JOIN subcategory as s " 
        + "on p.subcategory_id = s.subcategory_id LEFT OUTER JOIN category as c on s.category_id = c.category_id "
        + f"order by p.name {orderby};")
        cur.execute(query)
        result = cur.fetchall()
    except Exception as e:
        return{"status":-1,"message":f"Error de connexió:{e}"}
    finally:
        conn.close() 
    return productes_schema2(result)


#Metode que retorna una llista amb la categoria,subcategoria,producte,marca y preu de cada producte
#que contingui la string pasada al seu nom
def get_all_contains(contains:str):
    try:
        conn=conexio()
        cur=conn.cursor()
        query = ("SELECT c.name,s.name,p.name,p.company,p.price FROM product as p LEFT OUTER JOIN subcategory as s " 
        + "on p.subcategory_id = s.subcategory_id LEFT OUTER JOIN category as c on s.category_id = c.category_id "
        + f"where p.name LIKE '%{contains}%';")
        cur.execute(query)
        result = cur.fetchall()
    except Exception as e:
        return{"status":-1,"message":f"Error de connexió:{e}"}
    finally:
        conn.close() 
    return productes_schema2(result)


#Metode que retorna una llista amb la categoria,subcategoria,producte,marca y preu de cada producte
#retornara el numero de productes començant per skip fins al valor de limit
def get_all_skip_limit(skip:int|None = None, limit:int|None = None):
    try:
        conn=conexio()
        cur=conn.cursor()
        query = ("SELECT c.name,s.name,p.name,p.company,p.price FROM product as p LEFT OUTER JOIN subcategory as s " 
        + "on p.subcategory_id = s.subcategory_id LEFT OUTER JOIN category as c on s.category_id = c.category_id ")

        if skip is not None and limit is not None:
            query += f"LIMIT {skip}, {limit};"
        elif skip is not None:
            query += f"OFFSET {skip} ROWS;"
        elif limit is not None:
            query += f"LIMIT {limit};"
        else:
            query += ";"

        cur.execute(query)
        result = cur.fetchall()
    except Exception as e:
        return{"status":-1,"message":f"Error de connexió:{e}"}
    finally:
        conn.close() 
    return productes_schema2(result)


#Aquest metode permet carregar de forma masiva categories,subcategories y productes desde un arxiu csv amb un format concret y de forma asyncrona
async def carrega_masiva(fitxer:UploadFile):
    dades = []
    with fitxer.file as f:
        for line in f:
            dades.append(str(line,"UTF-8").strip().split(","))
    dades.pop(0)
    try:
        conn=conexio()
        cur=conn.cursor()
        for dada in dades:
            idCat = None
            idSubcat= None
            idProd = None
            hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #comprobem si existeix la categoria, en cas positiu guardem el seu id i fem update sino inserim
            cur.execute(f"select category_id from category where name = '{dada[1]}';")
            
            idCat = cur.fetchone()
        
            if(idCat != None):
                hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                query = "UPDATE category SET name = %s, updated_at = %s WHERE category_id = %s"
                values = (dada[1], hora, idCat[0])
                cur.execute(query, values)
            else:
                cur.execute(f"Insert into category(name) VALUES('{dada[1]}');")
                
            conn.commit()

            #Tornem a agafar la id de la categoria en cas de que sigues nova per a utilitzar-ho a la inserció/update de subcategoria    
            cur.execute(f"select category_id from category where name = '{dada[1]}';")
            idCat = cur.fetchone()

            #comporbem si existeix la subcategoria en cas positiu guardem el seu id i fem update sino inserim
            cur.execute(f"select subcategory_id from subcategory where name='{dada[3]}';")
            idSubcat = cur.fetchone()
            if(idSubcat != None):
                hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                query="update subcategory set name=%s, category_id = %s, updated_at=%s where subcategory_id = %s;"
                values=(dada[3],idCat[0],hora,idSubcat[0])
                cur.execute(query,values)
            else:
                cur.execute(f"Insert into subcategory(name,category_id) VALUES('{dada[3]}',{idCat[0]});")
            
            conn.commit()
            
            
            #Tornem a agafar la id de la subcategoria en cas de que sigues nova per a utilitzar-ho a la inserció/update del producte
            cur.execute(f"select subcategory_id from subcategory where name='{dada[3]}';")
            idSubcat = cur.fetchone()
            
            cur.execute(f"Select product_id from product where name='{dada[5]}';")
            idProd = cur.fetchone()
            
            if(idProd != None):
                hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                query = "UPDATE product set name=%s,description=%s,company=%s,price=%s,units=%s,subcategory_id = %s, updated_at=%s where product_id = %s;"
                values = (dada[5],dada[6],dada[7],dada[8],dada[9],idSubcat[0],hora,idProd[0])
                cur.execute(query,values)
            else:
                query = "INSERT INTO product(name, description, company, price, units, subcategory_id) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (dada[5], dada[6], dada[7], dada[8], dada[9], idSubcat[0])
                cur.execute(query,values)   
                  
            conn.commit()
            

        
    except Exception as e:
        return{"status":-1,"message":f"Error de connexió:{e}"}
    finally:
        conn.close() 
    
