from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import uuid
from fastapi import HTTPException

app = FastAPI()

# In-memory storage (Keeping simple just for now, when deploying we can integrate an external db like MySQL)
contacts = []


# Contact model
class Contact(BaseModel):
    id: Optional[str] = None # primary key, auto created using uuid
    name: str
    phone: str
    email: str


class MergeRequest(BaseModel):
    contact_id_1: str
    contact_id_2: str


@app.get("/")
def read_root():
    return {"message": "Contact Book API is running"}

@app.post("/contacts")
def add_contact(contact: Contact):
    contact.id = str(uuid.uuid4()) # unique id for the contact using uuid 
    contacts.append(contact)
    return {"message": "Contact added", "contact": contact}

@app.get("/contacts")
def get_contacts():
    return contacts

# search by name, phone or email (pass the query in the api url)
@app.get("/search")
def search_contacts(query: str):
    results = []
    query_lower = query.lower() # case insensitive search

    for contact in contacts:
        if (
            query_lower in contact.name.lower()  # partial search works fine
            or query_lower in contact.phone
            or query_lower in contact.email.lower()
        ):
            results.append(contact)

    return results

# delete by contact_id
@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: str):
    for i, contact in enumerate(contacts):
        if contact.id == contact_id:
            deleted = contacts.pop(i)
            return {"message": "Contact deleted", "contact": deleted}

    return {"message": "Contact not found"}

@app.post("/merge")
def merge_contacts(request: MergeRequest):
    contact1 = None
    contact2 = None

    # Find contacts using the contact id
    for contact in contacts:
        if contact.id == request.contact_id_1:
            contact1 = contact
        if contact.id == request.contact_id_2:
            contact2 = contact

    if not contact1 or not contact2:
        raise HTTPException(status_code=404, detail="One or both contacts not found")

    # Merge logic (prefer non-empty values)
    merged_contact = Contact(
        id=str(uuid.uuid4()),
        name=contact1.name if contact1.name else contact2.name,
        phone=contact1.phone if contact1.phone else contact2.phone,
        email=contact1.email if contact1.email else contact2.email,
    )

    # Remove old contacts
    contacts.remove(contact1)
    contacts.remove(contact2)

    # Add merged contact
    contacts.append(merged_contact)

    return {
        "message": "Contacts merged successfully",
        "merged_contact": merged_contact
    }