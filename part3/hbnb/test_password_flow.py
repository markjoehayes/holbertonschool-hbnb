# test_password_flow.py
from app import create_app
from app.services.facade import HBnBFacade

app = create_app()

with app.app_context():
    print("=== Testing Password Flow ===")
    facade = HBnBFacade()
    
    # Test 1: Create a user directly through facade
    print("1. Creating user directly through facade...")
    user_data = {
        'first_name': 'PasswordTest',
        'last_name': 'User', 
        'email': 'passwordtest@example.com',
        'password': 'test123'
    }
    
    user = facade.create_user(user_data)
    print(f"   ✅ User created: {user.email}")
    print(f"   ✅ Stored password: {user.password}")
    print(f"   ✅ Is hashed: {user.password.startswith('$2b$')}")
    
    # Test 2: Verify password
    print("2. Testing password verification...")
    check1 = user.verify_password("test123")
    check2 = user.verify_password("wrongpassword")
    print(f"   ✅ Correct password: {check1}")
    print(f"   ✅ Wrong password: {check2}")
    
    # Test 3: Try to retrieve and verify
    print("3. Testing retrieval and verification...")
    retrieved_user = facade.get_user_by_email('passwordtest@example.com')
    if retrieved_user:
        check3 = retrieved_user.verify_password("test123")
        print(f"   ✅ Retrieved user password check: {check3}")
    else:
        print("   ❌ Could not retrieve user")
    
    print("🎉 Password flow test complete!")
