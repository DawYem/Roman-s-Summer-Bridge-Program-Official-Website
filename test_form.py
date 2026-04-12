import uuid, app, os

app.init_db()
os.makedirs(app.app.config['UPLOAD_FOLDER'], exist_ok=True)

c = app.app.test_client()
u = 'test_' + uuid.uuid4().hex[:8]

# Signup
print("Signing up...")
r1 = c.post('/signup', data={'username': u, 'password': 'testpass'})
print('Signup status:', r1.status_code)

# Login with follow_redirects to establish session
print("Logging in...")
r2 = c.post('/login', data={'username': u, 'password': 'testpass'}, follow_redirects=True)
print('Login status:', r2.status_code)

# Dashboard POST with all fields (image is optional)
print("Submitting dashboard form...")
from werkzeug.datastructures import FileStorage
from io import BytesIO

# Create a minimal test image file
image_data = BytesIO(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00')
test_image = FileStorage(stream=image_data, filename="test.png", content_type="image/png")

r3 = c.post('/dashboard', data={
    'hours': '5.5',
    'task': 'painting',
    'date': '2026-04-11',
    'image': test_image
})
print('Dashboard POST status:', r3.status_code)

if r3.status_code not in [200, 302]:
    print('Error response:', r3.data.decode()[:500])
else:
    print('SUCCESS - form submitted without date column error!')
