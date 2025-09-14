from app import create_app

# สร้างอ็อบเจกต์แอปพลิเคชันโดยใช้ Application Factory Pattern
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)