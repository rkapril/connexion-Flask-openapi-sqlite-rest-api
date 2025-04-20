import sqlite3 
import json 
from flask import Response 
from flask import request   

def retrieveAllProducts():
  con = sqlite3.connect("./db/products.db")
  cursor = con.cursor()
  cursor.execute("SELECT * FROM products")
  columns = [column[0] for column in cursor.description]
  data = [dict(zip(columns, row)) for row in cursor.fetchall()]
  cursor.close()

  return Response(json.dumps(data), status=200, mimetype='application/json')

def retrieveProductById(product_id):
  con = sqlite3.connect("./db/products.db")
  cursor = con.cursor()
  cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
  columns = [column[0] for column in cursor.description]
  data = [dict(zip(columns, row)) for row in cursor.fetchall()]
  cursor.close()

  if len(data) == 1:
    data = data[0]
    return Response(json.dumps(data), status=200, mimetype='application/json')
  
  else:
    return Response('productId {} does not exist'.format(product_id), status=404)
  
def createNewProduct():
    product = request.get_json()

    if not product:
        return Response('Failed to create product due to invalid input', status=400)

    con = sqlite3.connect("./db/products.db")
    cursor = con.cursor()
    cursor.execute('''
            INSERT INTO products (sku_code, product_name, product_description, brand, model, category, quantity_on_hand, unit_price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (product['sku_code'], product['product_name'], product['product_description'], product['brand'], product['model'], product['category'], product['quantity_on_hand'], product['unit_price']))
    con.commit()
    cursor.close()
    con.close()

    if cursor.rowcount == 0:
        return Response('Failed to create product', status=409)
    else:
        return Response('Product created successfully with new Product ID: {}'.format(cursor.lastrowid), status=200)

def updateProduct(product_id):

    product = request.get_json()

    if not product:
        return Response('Failed to update product due to invalid input', status=400)

    con = sqlite3.connect("./db/products.db")
    cursor = con.cursor()
    cursor.execute('''
            UPDATE products
            SET sku_code = ?, product_name = ?, product_description = ?, brand = ?, model = ?, category = ?, quantity_on_hand = ?, unit_price = ?
            WHERE product_id = ?
        ''', (product['sku_code'], product['product_name'], product['product_description'], product['brand'], product['model'], product['category'], product['quantity_on_hand'], product['unit_price'], product_id))
    con.commit()
    cursor.close()
    con.close()

    if cursor.rowcount == 0:
        return Response('Failed to update product', status=400)
    
    else:
        return Response('Product updated successfully', status=200)

def deleteProduct(product_id):
    con = sqlite3.connect("./db/products.db")
    cursor = con.cursor()
    cursor.execute('''
            DELETE FROM products WHERE product_id = ?
        ''', (product_id,))
    con.commit()
    cursor.close()
    con.close()

    if cursor.rowcount == 0:
        return Response('Failed to delete product', status=404)
    
    else:
        return Response('Product deleted successfully', status=200)
