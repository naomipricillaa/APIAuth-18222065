from supabase import create_client
from app.config import settings

# Buat koneksi ke Supabase
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
