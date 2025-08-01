from supabase import create_client, Client
from core.config import settings

print("Initializing Supabase client...")
print(f"Supabase URL: {settings.supabase_url}")
supabase: Client = create_client(settings.supabase_url, settings.supabase_key)
