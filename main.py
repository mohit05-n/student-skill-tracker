from app import app, db

# Import models and routes after app is created
import models
import routes

if __name__ == '__main__':
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Initialize default data
        from routes import create_default_data
        create_default_data()
    
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)
