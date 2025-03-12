import frappe
import requests
from frappe.model.document import Document

class Pincodetoaddress(Document):
    pass

@frappe.whitelist()
def get_address_details(pincode):
    url = f"https://api.postalpincode.in/pincode/{pincode}"
    
    try:
        response = requests.post(url, timeout=10)  
        response.raise_for_status() 
        data = response.json()
        
        if data and data[0].get("Status") == "Success":
            return data[0]  
        
        return {"Status": "Error", "Message": "Invalid Pincode or No records found"}
    
    except requests.exceptions.Timeout:
        return {"Status": "Error", "Message": "API request timed out. Please try again."}
    
    except requests.exceptions.RequestException as e:
        return {"Status": "Error", "Message": f"API request failed: {str(e)}"}

