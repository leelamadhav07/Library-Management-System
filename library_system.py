# library_system.py
import os
from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

# Supabase client
sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# ===================== 1. Create =====================

def add_member(name, email):
    """Register a new member"""
    try:
        resp = sb.table("members").insert({"name": name, "email": email}).execute()
        return resp.data
    except Exception as e:
        print("Error adding member:", e)
        return None

def add_book(title, author, category, stock):
    """Add a new book"""
    try:
        resp = sb.table("books").insert({
            "title": title,
            "author": author,
            "category": category,
            "stock": stock
        }).execute()
        return resp.data
    except Exception as e:
        print("Error adding book:", e)
        return None

# ===================== 2. Read =====================

def list_books():
    """List all books with availability"""
    resp = sb.table("books").select("*").execute()
    for b in resp.data:
        print(f"{b['book_id']}: {b['title']} by {b['author']} - Stock: {b['stock']}")

def search_books(term):
    """Search books by title, author, or category"""
    resp = sb.table("books").select("*").or_(
        f"title.ilike.%{term}%,author.ilike.%{term}%,category.ilike.%{term}%"
    ).execute()
    for b in resp.data:
        print(f"{b['book_id']}: {b['title']} by {b['author']} - Stock: {b['stock']}")

def member_borrowed_books(member_id):
    """Show member details and their borrowed books"""
    member = sb.table("members").select("*").eq("member_id", member_id).execute().data
    if not member:
        print("Member not found")
        return
    print(f"Member: {member[0]['name']} ({member[0]['email']})")
    records = sb.table("borrow_records").select("book_id, borrow_date, return_date, books(title,author)").eq("member_id", member_id).execute().data
    if not records:
        print("No borrowed books.")
        return
    for r in records:
        book = r.get("books", {})
        print(f"{book.get('title','')} by {book.get('author','')} - Borrowed: {r['borrow_date']} - Returned: {r['return_date']}")

# ===================== 3. Update =====================

def update_book_stock(book_id, new_stock):
    """Update book stock"""
    resp = sb.table("books").update({"stock": new_stock}).eq("book_id", book_id).execute()
    return resp.data

def update_member_email(member_id, new_email):
    """Update member email"""
    resp = sb.table("members").update({"email": new_email}).eq("member_id", member_id).execute()
    return resp.data

# ===================== 4. Delete =====================

def delete_member(member_id):
    """Delete a member if no borrowed books"""
    borrowed = sb.table("borrow_records").select("*").eq("member_id", member_id).execute().data
    if borrowed:
        print("Cannot delete: Member has borrowed books")
        return
    resp = sb.table("members").delete().eq("member_id", member_id).execute()
    return resp.data

def delete_book(book_id):
    """Delete a book if not borrowed"""
    borrowed = sb.table("borrow_records").select("*").eq("book_id", book_id).execute().data
    if borrowed:
        print("Cannot delete: Book is borrowed")
        return
    resp = sb.table("books").delete().eq("book_id", book_id).execute()
    return resp.data

# ===================== 5. Borrow Book (Transaction) =====================

def borrow_book(member_id, book_id):
    """Borrow a book: check stock and insert borrow record"""
    try:
        # 1. Check stock
        book = sb.table("books").select("*").eq("book_id", book_id).execute().data
        if not book:
            print("Book not found")
            return
        if book[0]["stock"] <= 0:
            print("Book not available")
            return
        # 2. Decrease stock
        sb.table("books").update({"stock": book[0]["stock"] - 1}).eq("book_id", book_id).execute()
        # 3. Insert borrow record
        sb.table("borrow_records").insert({"member_id": member_id, "book_id": book_id}).execute()
        print("Book borrowed successfully")
    except Exception as e:
        print("Error borrowing book:", e)

# ===================== 6. Return Book (Transaction) =====================

def return_book(member_id, book_id):
    """Return a borrowed book"""
    try:
        # 1. Find borrow record without return_date
        record = sb.table("borrow_records").select("*").eq("member_id", member_id).eq("book_id", book_id).eq("return_date", None).execute().data
        if not record:
            print("No borrowed record found")
            return
        record_id = record[0]["record_id"]
        # 2. Update return_date
        sb.table("borrow_records").update({"return_date": datetime.utcnow().isoformat()}).eq("record_id", record_id).execute()
        # 3. Increase book stock
        book = sb.table("books").select("*").eq("book_id", book_id).execute().data
        sb.table("books").update({"stock": book[0]["stock"] + 1}).eq("book_id", book_id).execute()
        print("Book returned successfully")
    except Exception as e:
        print("Error returning book:", e)

# ===================== 7. Reports =====================

def top_5_borrowed_books():
    """List top 5 most borrowed books"""
    resp = sb.table("borrow_records").select("book_id, count:book_id").execute()
    # Could also use SQL via Supabase query for aggregation
    print(resp.data)

def members_with_overdue_books():
    """List members with books borrowed >14 days and not returned"""
    overdue_date = (datetime.utcnow() - timedelta(days=14)).isoformat()
    resp = sb.table("borrow_records").select("member_id, book_id, borrow_date").lt("borrow_date", overdue_date).is_("return_date", None).execute()
    print(resp.data)

def count_books_borrowed_per_member():
    """Count total books borrowed per member"""
    resp = sb.table("borrow_records").select("member_id, count:member_id").execute()
    print(resp.data)
