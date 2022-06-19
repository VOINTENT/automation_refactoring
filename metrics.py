from models import EntitiesHierarchy


W_COUNT_ABSTRACT_SUPER_ENTITIES = 3
W_COUNT_REPEATED_CODE = -3
W_COUNT_UNUSED_METHODS = -2
W_COUNT_FACELESS_ENTITIES = -1


def get_count_abstract_super_entities(entities_hierarchy: EntitiesHierarchy) -> int:
    total_count = 0
    for entity in entities_hierarchy.entities:
        if entity.is_abstract and entity.is_super:
            total_count += 1
    return total_count


def get_count_repeated_methods(entities_hierarchy: EntitiesHierarchy):
    total_count = 0
    repeated_methods_map = {}
    for entity in entities_hierarchy.entities:
        for method in entity.methods:
            if method.name in repeated_methods_map:
                total_count += 1
            else:
                repeated_methods_map[method.name] = True
    return total_count


def get_count_unused_methods(entities_hierarchy: EntitiesHierarchy) -> int:
    total_count = 0
    for entity in entities_hierarchy.entities:
        used_methods = entity.used_methods
        implemented_methods = entity.implemented_methods
        if len(implemented_methods) > len(used_methods):
            total_count += len(implemented_methods)
    return total_count


def get_count_faceless_entity(entities_hierarchy: EntitiesHierarchy) -> int:
    total_count = 0
    for entity in entities_hierarchy.entities:
        if not entity.used_methods and not entity.methods:
            total_count += 1
    return total_count


def calculate_energy(entities_hierarchy: EntitiesHierarchy) -> int:
    total_count = 0
    total_count += get_count_abstract_super_entities(entities_hierarchy)
    total_count += get_count_repeated_methods(entities_hierarchy)
    total_count += get_count_unused_methods(entities_hierarchy)
    total_count += get_count_faceless_entity(entities_hierarchy)
    return total_count
