import math
from fastapi.testclient import TestClient
from main import app, history

client = TestClient(app)

def test_basic_division():
    r = client.post("/calculate", params={"expr": "30/4"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 7.5) < 1e-9

def test_percent_subtraction():
    r = client.post("/calculate", params={"expr": "100 - 6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 94.0) < 1e-9

def test_standalone_percent():
    r = client.post("/calculate", params={"expr": "6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 0.06) < 1e-9

def test_invalid_expr_returns_ok_false():
    r = client.post("/calculate", params={"expr": "2**(3"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert "error" in data and data["error"] != ""


# --- Additional Arithmetic Tests ---

def test_basic_addition():
    r = client.post("/calculate", params={"expr": "15 + 27"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["result"] == 42
    assert data["error"] == ""

def test_basic_subtraction():
    r = client.post("/calculate", params={"expr": "50 - 18"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["result"] == 32
    assert data["error"] == ""

def test_basic_multiplication():
    r = client.post("/calculate", params={"expr": "7 * 8"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["result"] == 56
    assert data["error"] == ""

def test_operator_precedence_and_parentheses():
    r = client.post("/calculate", params={"expr": "(2 + 3) * 4 - 5"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["result"] == 15

def test_float_arithmetic():
    r = client.post("/calculate", params={"expr": "1.5 * 2.5"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 3.75) < 1e-9

def test_exponentiation():
    r = client.post("/calculate", params={"expr": "2 ** 4"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["result"] == 16


# --- Mathematical Constants Tests ---

def test_math_constant_pi():
    r = client.post("/calculate", params={"expr": "pi * 2"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - (2 * math.pi)) < 1e-9

def test_math_constant_e():
    r = client.post("/calculate", params={"expr": "e + 1"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - (math.e + 1)) < 1e-9


# --- Percent Operations Tests ---

def test_percent_addition():
    r = client.post("/calculate", params={"expr": "50 + 10%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 55.0) < 1e-9

def test_percent_multiplication():
    r = client.post("/calculate", params={"expr": "200 * 15%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 30.0) < 1e-9

def test_percent_division():
    r = client.post("/calculate", params={"expr": "40 / 50%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 80.0) < 1e-9

def test_two_standalone_percents_sum():
    r = client.post("/calculate", params={"expr": "10% + 20%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 0.3) < 1e-9


# --- Error Handling & Validation Tests ---

def test_division_by_zero():
    r = client.post("/calculate", params={"expr": "10 / 0"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert "ZeroDivisionError" in data["error"]
    assert data["result"] == ""

def test_undefined_variable():
    r = client.post("/calculate", params={"expr": "unknown_var + 1"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert "NameError" in data["error"]

def test_disallowed_import():
    r = client.post("/calculate", params={"expr": "__import__('os')"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert data["error"] != ""

def test_missing_expr_parameter():
    r = client.post("/calculate")
    assert r.status_code == 422


# --- History Endpoints Tests ---

def test_get_empty_history():
    history.clear()
    r = client.get("/history")
    assert r.status_code == 200
    assert r.json() == []

def test_delete_history():
    history.clear()
    history.append({"expr": "1+1", "result": 2})
    assert len(history) == 1

    r_del = client.delete("/history")
    assert r_del.status_code == 200

    r_get = client.get("/history")
    assert r_get.status_code == 200
    assert r_get.json() == []

def test_calculate_adds_to_history():
    history.clear()
    r = client.post("/calculate", params={"expr": "10 + 5"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["result"] == 15

    r_hist = client.get("/history")
    assert r_hist.status_code == 200
    hist = r_hist.json()
    assert len(hist) == 1
    assert hist[0]["expr"] == "10 + 5"
    assert hist[0]["result"] == 15
    assert "timestamp" in hist[0]

def test_calculate_error_does_not_add_to_history():
    history.clear()
    r = client.post("/calculate", params={"expr": "10 / 0"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False

    r_hist = client.get("/history")
    assert r_hist.status_code == 200
    assert len(r_hist.json()) == 0

def test_history_limit_parameter():
    history.clear()
    for i in range(5):
        client.post("/calculate", params={"expr": f"{i} + 1"})
    
    r = client.get("/history", params={"limit": 3})
    assert r.status_code == 200
    hist = r.json()
    assert len(hist) == 3
    assert hist[-1]["expr"] == "4 + 1"
    assert hist[-1]["result"] == 5
