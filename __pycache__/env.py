from dotenv import load_dotenv
import os

load_dotenv()

print("SUPABASE_URL:", os.getenv("SUPABASE_URL"))
print("SUPABASE_KEY:", os.getenv("SUPABASE_KEY"))
print("GEMINI_API_KEY:", os.getenv("GEMINI_API_KEY"))