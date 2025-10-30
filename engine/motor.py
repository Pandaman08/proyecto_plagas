from experta import KnowledgeEngine
from knowledge.hechos import Caso

from knowledge.reglas_piña import ReglasPiña
from knowledge.reglas_uva import ReglasUva
from knowledge.reglas_limon import ReglasLimon

MAPA_CULTIVOS = {
    "piña": ReglasPiña,
    "uva": ReglasUva,
    "limon": ReglasLimon,
    
}

class SistemaExpertoPlagas:
    def diagnosticar(self, cultivo: str, sintomas: list):
        cultivo_key = cultivo.lower()
        if cultivo_key not in MAPA_CULTIVOS:
            return {
                "error": f"Cultivo '{cultivo}' no soportado aún.",
                "diagnosticos": [],
                "reglas_activadas": []
            }

        clase_reglas = MAPA_CULTIVOS[cultivo_key]
        motor = clase_reglas()
        motor.reset()
        motor.declare(Caso(cultivo=cultivo_key, sintomas=set(sintomas)))
        motor.run()

        diagnosticos = [
            fact for fact in motor.facts.values()
            if isinstance(fact, dict) and 'plaga' in fact
        ]
        diagnosticos.sort(key=lambda x: x.get('certeza', 0), reverse=True)

        return {
            "diagnosticos": diagnosticos,
            "reglas_activadas": [d.get("regla_activada") for d in diagnosticos]
        }