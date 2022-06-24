from website import create_app #import von website folder

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000) #Debug um nicht immer neustarten zu müssen