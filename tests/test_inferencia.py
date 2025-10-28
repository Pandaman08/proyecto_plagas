from engine import SistemaExpertoPlagas

def test_gallina_ciega_completa():
    motor = SistemaExpertoPlagas()
    res = motor.diagnosticar("piña", ["marchitez", "enrojecimiento_foliar", "raices_dañadas"])
    assert res["diagnosticos"][0]["plaga"] == "Gallina ciega (Phyllophaga sp.)"
    assert res["diagnosticos"][0]["certeza"] == 1.0

def test_cochinilla_con_hormigas():
    motor = SistemaExpertoPlagas()
    res = motor.diagnosticar("piña", ["colonias_algodonosas", "hormigas"])
    assert "Cochinilla harinosa" in res["diagnosticos"][0]["plaga"]
    assert res["diagnosticos"][0]["certeza"] == 0.7