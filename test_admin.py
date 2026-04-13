import app, uuid, sqlite3

app.init_db()

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('DELETE FROM volunteer_hours')
cursor.execute('DELETE FROM users')
conn.commit()
conn.close()

c = app.app.test_client()

# Sign up first user - should be admin
u1 = f'First User {uuid.uuid4().hex[:8]}'
print(f"Signing up first user: {u1}")
r = c.post('/signup', data={'username': u1, 'password': 'pass123', 'age': '14', 'grade_level': '8th Grade'})
print(f"Signup status: {r.status_code}")
assert r.status_code == 302

# Check database to verify is_admin = 1
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute("SELECT username, age, grade_level, is_admin FROM users WHERE username = ?", (u1,))
result = cursor.fetchone()
conn.close()
print(f"Database: username={result[0]}, age={result[1]}, grade_level={result[2]}, is_admin={result[3]}")

# Sign up second user - should NOT be admin
u2 = f'Second User {uuid.uuid4().hex[:8]}'
print(f"\nSigning up second user: {u2}")
r = c.post('/signup', data={'username': u2, 'password': 'pass123', 'age': '15', 'grade_level': '9th Grade'})
assert r.status_code == 302

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute("SELECT username, age, grade_level, is_admin FROM users WHERE username = ?", (u2,))
result = cursor.fetchone()
conn.close()
print(f"Database: username={result[0]}, age={result[1]}, grade_level={result[2]}, is_admin={result[3]}")

# Login as first user and try admin page
print(f"\nLogging in as {u1} and accessing /admin...")
c.post('/login', data={'username': u1, 'password': 'pass123'}, follow_redirects=True)
r = c.get('/admin')
print(f"Admin page status: {r.status_code}")
if r.status_code == 200 and b'Access denied' not in r.data:
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
if b'Access denied' in r.data:
    print("CORRECT - Non-admin user denied access")
