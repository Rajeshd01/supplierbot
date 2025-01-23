from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatbot import process_user_query
from db_utils import fetch_suppliers, fetch_products, insert_supplier, insert_product


class QueryRequest(BaseModel):
    query: str  


class SupplierDetails(BaseModel):
    name: str
    contact_info: str
    categories: str

app = FastAPI()


@app.get("/suppliers")
def get_suppliers():
    """
    Fetch and return all suppliers from the database.
    """
    try:
        suppliers = fetch_suppliers()
        if not suppliers:
            return {"message": "No suppliers found in the database."}
        return {"suppliers": suppliers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/suppliers")
def post_suppliers(request: QueryRequest):
    """
    Handle user query to add a new supplier or fetch existing suppliers.
    - "Show me all suppliers": Fetch and display all suppliers.
    - "Add supplier": Add a new supplier (details should be parsed from the query).
    """
    try:
        user_query = request.query.lower()

        if "show me all suppliers" in user_query:
            suppliers = fetch_suppliers()
            if not suppliers:
                return {"message": "No suppliers found in the database."}
            return {"suppliers": suppliers}

        elif "add supplier" in user_query:
            
            if "name=" in user_query and "contact_info=" in user_query and "categories=" in user_query:
                details = user_query.split(",")
                name = details[0].split("=")[1].strip()
                contact_info = details[1].split("=")[1].strip()
                categories = details[2].split("=")[1].strip()

                insert_supplier(name, contact_info, categories)
                return {"message": f"Supplier '{name}' added successfully."}
            else:
                return {
                    "message": "Invalid query format. Use: 'Add supplier: name=<name>, contact_info=<email>, categories=<categories>'"
                }

        else:
            return {"message": "Invalid query. Please ask about showing or adding suppliers."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products")
def get_products():
    """
    Fetch and return all products from the database.
    """
    try:
        products = fetch_products()
        if not products:
            return {"message": "No products found in the database."}
        return {"products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/products")
def post_products(request: QueryRequest):
    """
    Handle user query to add a new product or fetch existing products.
    - "Show me all products": Fetch and display all products.
    - "Add product": Add a new product (details should be parsed from the query).
    """
    try:
        user_query = request.query.lower()

        if "show me all products" in user_query:
            products = fetch_products()
            if not products:
                return {"message": "No products found in the database."}
            return {"products": products}

        elif "add product" in user_query:
            
            if "name=" in user_query and "brand=" in user_query and "price=" in user_query and "category=" in user_query and "description=" in user_query and "supplier_id=" in user_query:
                details = user_query.split(",")
                name = details[0].split("=")[1].strip()
                brand = details[1].split("=")[1].strip()
                price = float(details[2].split("=")[1].strip())
                category = details[3].split("=")[1].strip()
                description = details[4].split("=")[1].strip()
                supplier_id = int(details[5].split("=")[1].strip())

                insert_product(name, brand, price, category, description, supplier_id)
                return {"message": f"Product '{name}' added successfully."}
            else:
                return {
                    "message": "Invalid query format. Use: 'Add product: name=<name>, brand=<brand>, price=<price>, category=<category>, description=<description>, supplier_id=<supplier_id>'"
                }

        else:
            return {"message": "Invalid query. Please ask about showing or adding products."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
def chat_endpoint(request: QueryRequest):
    """
    Handle user queries for chatbot interactions (supplier/product or general queries).
    """
    try:
        user_query = request.query.lower()

        
        chatbot_response = process_user_query(user_query)

        return {"response": chatbot_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
