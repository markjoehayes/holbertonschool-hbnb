# test_both_flows.py
from app import create_app
from app.services.facade import HBnBFacade

app = create_app()

with app.app_context():
    print("=== Testing Both Registration Flows ===")
    facade = HBnBFacade()
    
    # Test credentials
    test_data = {
        'first_name': 'Compare',
        'last_name': 'Test', 
        'email': 'compare@example.com',
        'password': 'test123'
    }
    
    print("1. Direct facade creation (plain password):")
    user1 = facade.create_user(test_data)
    print(f"   Password: {user1.password}")
    print(f"   Verify 'test123': {user1.verify_password('test123')}")
    
    print("2. Manual hash then facade creation (hashed password):")
    from app import bcrypt
    hashed = bcrypt.generate_password_hash(test_data['password']).decode('utf-8')
    print(f"   Hash: {hashed}")
    
    test_data_hashed = test_data.copy()
    test_data_hashed['password'] = hashed
    
    user2 = facade.create_user(test_data_hashed)
    print(f"   Password: {user2.password}")
    print(f"   Verify 'test123': {user2.verify_password('test123')}")
    
    print("3. Are passwords the same?", user1.password == user2.password)
    
    print("🎉 Comparison complete!")
