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

from experta import Fact

class Caso(Fact):
    """Entrada del usuario: cultivo, síntomas observados, conteo (si aplica)."""
    pass

class Diagnostico(Fact):
    """Resultado del motor: plaga, certeza, recomendaciones, ACB, umbral."""
    pass
