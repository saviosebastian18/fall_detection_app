import jwt

decoded_token = jwt.decode(
    token,
    public_key,
    algorithms=["RS256"],
    audience="authenticated",  # 🔹 Ensure this matches your Supabase settings
)
