from fastapi import APIRouter, Depends, HTTPException
from app.database import supabase

router = APIRouter()

@router.get("/recommendations")
def get_recommendations(user_id: str):
    # Fetch user preferences
    user = supabase.table("users").select("preferences").eq("id", user_id).single().execute()
    if not user.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    preferences = user.data["preferences"]
    location = preferences.get("location")
    price_range = preferences.get("price_range")
    facilities = preferences.get("facilities")

    # Filter hotels based on preferences
    query = supabase.table("hotels").select("*")
    if location:
        query = query.eq("location", location)
    if price_range:
        query = query.gte("price", price_range["min"]).lte("price", price_range["max"])
    if facilities:
        for facility in facilities:
            query = query.contains("facilities", [facility])

    results = query.execute()
    return results.data
