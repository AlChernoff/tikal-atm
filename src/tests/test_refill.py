def test_not_valid_input_(test_app):
    response = test_app.post(
        url="/atm/refill",
        headers={"Content-Type": "application/json"},
        json={"money": {"0.1": 5, "5": 20, "20": 15, "2000": 30}}
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": "One of bills/coins is not supported. Supported values are: ['20', '100', '200', '0.01', '0.1', "
                  "'1', '5', '10']"
    }
