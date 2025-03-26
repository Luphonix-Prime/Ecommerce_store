import urllib.parse

username = "Luphonix"
password = "LoopPheonix@2025"

encoded_username = urllib.parse.quote_plus(username)
encoded_password = urllib.parse.quote_plus(password)

print(f"Encoded Username: {encoded_username}")
print(f"Encoded Password: {encoded_password}")
