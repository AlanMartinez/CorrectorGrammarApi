import sys
print(f"Python version: {sys.version}")

try:
    from app.main import app
    print("Successfully imported app")
except Exception as e:
    print(f"Error importing app: {e}")
    import traceback
    traceback.print_exc() 