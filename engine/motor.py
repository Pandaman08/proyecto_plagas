from knowledge.reglas_piña import ReglasPiña
from knowledge.hechos import Caso

class SistemaExpertoPlagas(ReglasPiña):
    def diagnosticar(self, cultivo: str, sintomas: list):
        self.reset()
        self.declare(Caso(cultivo=cultivo.lower(), sintomas=set(sintomas)))
        self.run()

        diagnosticos = []
        for fact_id, fact in self.facts.items():
            if isinstance(fact, dict) and 'plaga' in fact:
                diagnosticos.append(fact)

        # Ordenar por certeza descendente
        diagnosticos.sort(key=lambda x: x.get('certeza', 0), reverse=True)

        return {
            "diagnosticos": diagnosticos,
            "reglas_activadas": [d.get("regla_activada") for d in diagnosticos]
        }