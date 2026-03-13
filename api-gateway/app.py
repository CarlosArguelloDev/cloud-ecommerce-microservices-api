import os
import requests
from flask import Flask, request, jsonify, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"])

PRODUCTS_URL = os.getenv("PRODUCTS_SERVICE_URL", "http://products-service:5001")
USERS_URL    = os.getenv("USERS_SERVICE_URL",    "http://users-service:5002")
ORDERS_URL   = os.getenv("ORDERS_SERVICE_URL",   "http://orders-service:5003")
PAYMENTS_URL = os.getenv("PAYMENTS_SERVICE_URL", "http://payments-service:5004")


def _proxy(base_url, path, method, req):
    """Forward a request to a downstream service and stream back the response."""
    url = f"{base_url}{path}"
    headers = {
        key: value for key, value in req.headers
        if key.lower() not in ("host", "content-length", "transfer-encoding")
    }
    try:
        resp = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=req.args,
            json=req.get_json(silent=True),
            timeout=10,
        )
        excluded = {"content-encoding", "transfer-encoding", "connection"}
        response_headers = [
            (k, v) for k, v in resp.headers.items()
            if k.lower() not in excluded
        ]
        return Response(resp.content, status=resp.status_code, headers=response_headers)
    except requests.exceptions.ConnectionError as e:
        return jsonify({"error": "Service unavailable", "detail": str(e)}), 503
    except requests.exceptions.Timeout:
        return jsonify({"error": "Service timeout"}), 504


# ── Health ──────────────────────────────────────────────────────────────────
@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "api-gateway"}), 200


# ── Products ─────────────────────────────────────────────────────────────────
@app.route("/products", methods=["GET"])
@app.route("/products/<path:subpath>", methods=["GET"])
def products_proxy(subpath=""):
    path = f"/products/{subpath}" if subpath else "/products"
    return _proxy(PRODUCTS_URL, path, request.method, request)


# ── Users ─────────────────────────────────────────────────────────────────────
@app.route("/users/<path:subpath>", methods=["GET", "POST", "DELETE", "PUT"])
def users_proxy(subpath):
    return _proxy(USERS_URL, f"/users/{subpath}", request.method, request)


# ── Orders ────────────────────────────────────────────────────────────────────
@app.route("/orders", methods=["POST"])
@app.route("/orders/<path:subpath>", methods=["GET", "POST", "PUT"])
def orders_proxy(subpath=""):
    path = f"/orders/{subpath}" if subpath else "/orders"
    return _proxy(ORDERS_URL, path, request.method, request)


# ── Payments ──────────────────────────────────────────────────────────────────
@app.route("/payments", methods=["POST"])
@app.route("/payments/<path:subpath>", methods=["GET", "POST"])
def payments_proxy(subpath=""):
    path = f"/payments/{subpath}" if subpath else "/payments"
    return _proxy(PAYMENTS_URL, path, request.method, request)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
