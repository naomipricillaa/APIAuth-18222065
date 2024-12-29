from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from datetime import date
from app.database import supabase

router = APIRouter()

@router.get("/hotels")
def search_hotels(
    location: Optional[str] = None,
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    pet_category: Optional[str] = None,
    pet_size: Optional[str] = None,
    booking_from: Optional[date] = None,  # Tanggal mulai booking
    booking_to: Optional[date] = None,    # Tanggal akhir booking
):
    # Mulai query dari tabel 'hotels'
    query = supabase.table("hotels").select("*")

    if location:
        query = query.eq("location", location)

    if min_price:
        query = query.gte("price", min_price)
    if max_price:
        query = query.lte("price", max_price)

    if pet_category:
        query = query.eq("pet_category", pet_category)

    if pet_size:
        query = query.eq("pet_size", pet_size)

    # Filter berdasarkan tanggal booking
    if booking_from and booking_to:
        # Cek jika booking_to >= available_from dan booking_from <= available_to
        query = query.gte("available_to", str(booking_from))
        query = query.lte("available_from", str(booking_to))

    elif booking_from or booking_to:
        raise HTTPException(
            status_code=400,
            detail="Both 'booking_from' and 'booking_to' must be provided together."
        )

    # Eksekusi query
    results = query.execute()

    # Pengecekan hasil
    if not results.data:
        return {"message": "No hotels available for the given criteria."}

    return results.data
