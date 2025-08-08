from floors import floor_bp
from rooms import room_bp
from Residents import resident_bp
from login import login_bp
from flask import Flask

app = Flask(__name__)

app.register_blueprint(login_bp)
app.register_blueprint(floor_bp)
app.register_blueprint(room_bp)
app.register_blueprint(resident_bp)


if __name__ == "__main__":
    for rule in app.url_map.iter_rules():
        print(f"{rule.methods} -> {rule}")
    app.run(debug=True)
