from flask import Flask
import hmrm

app = hmrm.create_app()

if __name__ == "__main__":
    app.run(debug=True, port=8080)
