from config.supabase_client import supabase

if supabase:
    print("Supabase client initialized successfully!")
else:
    print("Supabase client initialization failed.")