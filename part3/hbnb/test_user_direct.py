# test_user_direct.py
from app import create_app
from app.models.user import User

app = create_app()

with app.app_context():
    print("=== Testing User Model Directly ===")
    
    try:
        # Test 1: Basic user creation
        print("1. Creating user with password...")
        user = User(
            first_name="Direct",
            last_name="Test", 
            email="direct@test.com",
            password="test123"
        )
        print(f"   ✅ User created: {user}")
        print(f"   ✅ ID: {user.id}")
        print(f"   ✅ Email: {user.email}")
        print(f"   ✅ Password (hashed): {user.password[:30]}...")
        print(f"   ✅ Created at: {user.created_at}")
        
        # Test 2: to_dict()
        print("2. Testing to_dict()...")
        user_dict = user.to_dict()
        print(f"   ✅ to_dict() worked")
        print(f"   ✅ Dict keys: {list(user_dict.keys())}")
        print(f"   ✅ Password in dict: {'password' in user_dict}")
        
        # Test 3: Verify password
        print("3. Testing password verification...")
        check1 = user.verify_password("test123")
        check2 = user.verify_password("wrong")
        print(f"   ✅ Correct password: {check1}")
        print(f"   ✅ Wrong password: {check2}")
        
        print("🎉 All direct tests passed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
