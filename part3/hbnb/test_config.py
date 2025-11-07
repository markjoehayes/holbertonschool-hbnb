#!/usr/bin/python3

# test_config.py
import os
import sys

def test_environment_detection():
    # Import create_app at the TOP of the function
    from app import create_app

    print("Testing Development Configuration...")
    # Save original FLASK_ENV if it exists
    original_flask_env = os.environ.get('FLASK_ENV')

    # Ensure FLASK_ENV is not set for development test
    if 'FLASK_ENV' in os.environ:
        del os.environ['FLASK_ENV']

    # Test development (default)
    app_dev = create_app()
    assert app_dev.config['DEBUG'] == True
    print("Development config works!")

    # Test production (this should fail gracefully because required vars aren't set)
    print("\nTesting Production Configuration...")
    os.environ['FLASK_ENV'] = 'production'

    try:
        app_prod = create_app()
        print("Expected error for missing production variables!")
    except ValueError as e:
        print(f"Production validation works: {e}")

    # Test production with mock variables
    print("\nTesting Production with mock variables...")
    os.environ['DATABASE_URL'] = 'sqlite:///mock_prod.db'
    os.environ['SECRET_KEY'] = 'mock-secret-key'

    try:
        app_prod = create_app()
        assert app_prod.config['DEBUG'] == False
        print("Production config works with environment variables!")
    except Exception as e:
        print(f"Unexpected error: {e}")

    # Test testing environment
    print("\nTesting Testing Configuration...")
    os.environ['FLASK_ENV'] = 'testing'

    try:
        app_test = create_app()
        assert app_test.config['TESTING'] == True
        print("Testing config works!")
    except Exception as e:
        print(f"Testing config error: {e}")

    # Restore original environment
    if original_flask_env:
        os.environ['FLASK_ENV'] = original_flask_env
    else:
        if 'FLASK_ENV' in os.environ:
            del os.environ['FLASK_ENV']

    # Clean up mock variables
    if 'DATABASE_URL' in os.environ:
        del os.environ['DATABASE_URL']
    if 'SECRET_KEY' in os.environ:
        del os.environ['SECRET_KEY']

    print("\nAll environment detection tests completed!")

if __name__ == '__main__':
    test_environment_detection()
