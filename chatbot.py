from transformers import pipeline
from db_utils import fetch_products, fetch_suppliers


generator = pipeline("text-generation", model="gpt2")  

def process_user_query(user_query):
    """
    Process the user's query, fetch data from the database, and enhance the response using LLM.
    """
   
    user_query = user_query.lower()
    
    if "product" in user_query or "show me products" in user_query:
        data = fetch_products()
        if not data:
            return "No products found in the database."
        data_type = "products"
    elif "supplier" in user_query or "show me suppliers" in user_query:
        data = fetch_suppliers()
        if not data:
            return "No suppliers found in the database."
        data_type = "suppliers"
    else:
        return "I didn't understand your query. Please ask about products or suppliers."

   
    formatted_data = f"Here are the {data_type} details:\n" + "\n".join([str(item) for item in data])

    
    response_text = generator(
        formatted_data, max_new_tokens=50, num_return_sequences=1, do_sample=True, temperature=0.7
    )[0]["generated_text"]

    
    return response_text


if __name__ == "__main__":
    user_query = "Show me all products."
    print(process_user_query(user_query))

    user_query = "Which suppliers are available?"
    print(process_user_query(user_query))

    user_query = "Tell me about laptops."
    print(process_user_query(user_query))
