# tests/test_auth.py

def test_login_page_loads(client):
    """
    Test 1: Does the login page load correctly?
    """
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Iniciar Sesi" in response.data # Looks for part of the title text

def test_successful_login(client, new_user):
    """
    Test 2: Can a user with correct credentials log in?
    """
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True) # Follows the redirect to the dashboard

    assert response.status_code == 200
    assert b"Dashboard de Inventario" in response.data
    assert b"Bienvenido, Test" in response.data

def test_failed_login(client, new_user):
    """
    Test 3: Is an error message shown with incorrect credentials?
    """
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Correo o contrase" in response.data # Looks for part of the error message
    assert b"Dashboard de Inventario" not in response.data

def test_logout(client, new_user):
    """
    Test 4: Does logout work and redirect to login?
    """
    # First, log in to have an active session
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })

    # Then, test logout
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Ha cerrado sesi" in response.data # Looks for part of the flash message
    assert b"Iniciar Sesi" in response.data
