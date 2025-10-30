import collections.abc

# Parche para compatibilidad con Python 3.10+
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
collections.MutableSequence = collections.abc.MutableSequence
collections.Sequence = collections.abc.Sequence
collections.Iterable = collections.abc.Iterable
collections.Iterator = collections.abc.Iterator
collections.MutableSet = collections.abc.MutableSet
collections.Callable = collections.abc.Callable

from experta import KnowledgeEngine
from knowledge.hechos import Caso

from knowledge.reglas_piña import ReglasPiña
from knowledge.reglas_uva import ReglasUva

MAPA_CULTIVOS = {
    "piña": ReglasPiña,
    "uva": ReglasUva,
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