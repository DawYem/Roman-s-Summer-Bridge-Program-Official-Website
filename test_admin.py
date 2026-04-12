import app, uuid, sqlite3

app.init_db()
c = app.app.test_client()

# Sign up first user - should be admin
u1 = 'firstuser_' + uuid.uuid4().hex[:8]
print(f"Signing up first user: {u1}")
r = c.post('/signup', data={'username': u1, 'password': 'pass123'})
print(f"Signup status: {r.status_code}")

# Check database to verify is_admin = 1
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute("SELECT username, is_admin FROM users WHERE username = ?", (u1,))
result = cursor.fetchone()
conn.close()
print(f"Database: username={result[0]}, is_admin={result[1]}")

# Sign up second user - should NOT be admin
u2 = 'seconduser_' + uuid.uuid4().hex[:8]
print(f"\nSigning up second user: {u2}")
c.post('/signup', data={'username': u2, 'password': 'pass123'})

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute("SELECT username, is_admin FROM users WHERE username = ?", (u2,))
result = cursor.fetchone()
conn.close()
print(f"Database: username={result[0]}, is_admin={result[1]}")

# Login as first user and try admin page
print(f"\nLogging in as {u1} and accessing /admin...")
c.post('/login', data={'username': u1, 'password': 'pass123'}, follow_redirects=True)
r = c.get('/admin')
print(f"Admin page status: {r.status_code}")
if r.status_code == 200:
    print("SUCCESS - First user has admin access!")
else:
    print(f"ERROR - Admin access denied: {r.data[:100]}")

# Try as second user - should be denied
print(f"\nLogging in as {u2} and trying /admin...")
c2 = app.app.test_client()
r_login = c2.post('/login', data={'username': u2, 'password': 'pass123'}, follow_redirects=True)
print(f"Login redirect status: {r_login.status_code}")
r = c2.get('/admin')
print(f"Admin page status: {r.status_code}")
print(f"Admin page response: {r.data.decode()[:200]}")
if r.status_code != 200:
    print("CORRECT - Non-admin user denied access")
