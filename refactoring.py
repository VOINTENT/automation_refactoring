import random
from enum import IntEnum

from metrics import calculate_energy
from models import EntitiesHierarchy, Entity, Method
from simulated_annealing import get_transition_probability, is_transition, decrease_temperature


class ActionsEnum(IntEnum):
    up_method = 0
    down_method = 1

    divide_entities = 2
    unite_entities = 3

    make_abstract = 4
    make_not_abstract = 5

    delete_entity = 6
    delete_method = 7


def get_next_action() -> ActionsEnum:
    value = random.randint(0, 8)
    return ActionsEnum(value)


def get_random_entity_from_hierarchy(entities_hierarchy: EntitiesHierarchy) -> Entity:
    value = random.randint(0, len(entities_hierarchy.entities))
    return entities_hierarchy.entities[value]


def get_random_method_from_hierarchy(entities_hierarchy: EntitiesHierarchy) -> Method:
    methods = []
    for entity in entities_hierarchy.entities:
        methods += entity.methods
    value = random.randint(0, len(methods))
    return methods[value]


def do_up_method(entities_hierarchy: EntitiesHierarchy) -> EntitiesHierarchy:
    method = get_random_method_from_hierarchy(entities_hierarchy)
    entity = method.entity
    if entity.parent_entity:
        parent_entity = entity.parent_entity
        parent_entity.methods += method
        method.entity = parent_entity
        entity.methods.remove(method)
    return entities_hierarchy


def do_down_method(entities_hierarchy: EntitiesHierarchy) -> EntitiesHierarchy:
    method = get_random_method_from_hierarchy(entities_hierarchy)
    entity = method.entity
    if entity.sub_entities:
        value = random.randint(0, len(entity.sub_entities))
        sub_entity = entity.sub_entities[value]

        sub_entity.methods += method
        method.entity = sub_entity
        entity.methods.remove(method)
    return entities_hierarchy


def do_divide_entities(entities_hierarchy: EntitiesHierarchy) -> EntitiesHierarchy:
    entity = get_random_entity_from_hierarchy(entities_hierarchy)
    new_entity = Entity(
        methods=[], sub_entities=entity.sub_entities, parent_entity=entity, is_abstract=False,
        used_methods=entity.used_methods
    )
    entity.is_abstract = True
    entity.sub_entities = [new_entity]
    return entities_hierarchy


def do_unite_entities(entities_hierarchy: EntitiesHierarchy) -> EntitiesHierarchy:
    entity = get_random_entity_from_hierarchy(entities_hierarchy)
    if entity.sub_entities:
        value = random.randint(0, len(entity.sub_entities))
        sub_entity = entity.sub_entities[value]
        sub_entity.methods += entity.methods
        sub_entity.used_methods += entity.used_methods
        sub_entity.parent_entity = entity.parent_entity
        del entity
    return entities_hierarchy


def do_make_abstract(entities_hierarchy: EntitiesHierarchy) -> EntitiesHierarchy:
    entity = get_random_entity_from_hierarchy(entities_hierarchy)
    if not entity.is_abstract:
        entity.is_abstract = True
    return entities_hierarchy


def do_make_not_abstract(entities_hierarchy: EntitiesHierarchy) -> EntitiesHierarchy:
    entity = get_random_entity_from_hierarchy(entities_hierarchy)
    if not entity.is_abstract:
        entity.is_abstract = False
    return entities_hierarchy


def do_delete_entity(entities_hierarchy: EntitiesHierarchy) -> EntitiesHierarchy:
    entity = get_random_entity_from_hierarchy(entities_hierarchy)
    if not entity.used_methods and not entity.methods:
        del entity
    return entities_hierarchy


def do_delete_method(entities_hierarchy: EntitiesHierarchy) -> EntitiesHierarchy:
    method = get_random_method_from_hierarchy(entities_hierarchy)
    entity = method.entity
    if not entity.is_method_used(method):
        del method
    return entities_hierarchy


def get_new_candidate_by_action(action: ActionsEnum, entities_hierarchy: EntitiesHierarchy) -> EntitiesHierarchy:
    if action == ActionsEnum.up_method:
        return do_up_method(entities_hierarchy)
    elif action == ActionsEnum.down_method:
        return do_down_method(entities_hierarchy)
    elif action == ActionsEnum.divide_entities:
        return do_divide_entities(entities_hierarchy)
    elif action == ActionsEnum.unite_entities:
        return do_unite_entities(entities_hierarchy)
    elif action == ActionsEnum.make_abstract:
        return do_make_abstract(entities_hierarchy)
    elif action == ActionsEnum.make_not_abstract:
        return do_make_not_abstract(entities_hierarchy)
    elif action == ActionsEnum.delete_entity:
        return do_delete_entity(entities_hierarchy)
    elif action == ActionsEnum.delete_method:
        return do_delete_method(entities_hierarchy)
    else:
        raise ValueError


def generate_new_candidate(entities_hierarchy: EntitiesHierarchy) -> EntitiesHierarchy:
    action = get_next_action()
    return get_new_candidate_by_action(action, entities_hierarchy)


def run_simulated_annealing(
        entities_hierarchy: EntitiesHierarchy, initial_temperature: float, end_temperature: float
) -> EntitiesHierarchy:
    current_energy = calculate_energy(entities_hierarchy)
    t = initial_temperature

    for i in range(25_000):
        entities_hierarchy_candidate = generate_new_candidate(entities_hierarchy)
        candidate_energy = calculate_energy(entities_hierarchy_candidate)

        if candidate_energy < current_energy:
            current_energy = candidate_energy
            entities_hierarchy = entities_hierarchy_candidate
        else:
            p = get_transition_probability(candidate_energy - current_energy, t)
            if is_transition(probability=p):
                current_energy = candidate_energy
                entities_hierarchy = entities_hierarchy_candidate

        t = decrease_temperature(initial_temperature, i)

        if t < end_temperature:
            break

    return entities_hierarchy
