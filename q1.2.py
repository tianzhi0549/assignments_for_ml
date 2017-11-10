import numpy as np
import itertools

DIMS = [3, 2, 2]
MAX_NUM_COMPONENTS = 2 ** np.prod(DIMS)

class Component(object):
    def __init__(self, arr):
        self.arr = arr

    @staticmethod
    def get_component_from_properties(properties):
        arr = np.zeros(DIMS, np.bool)
        if properties == None:
            return Component(arr)
        indexes = []
        for p in properties:
            if p == "*":
                indexes.append(slice(None))
            else:
                indexes.append(int(p))
        arr[tuple(indexes)] = True
        return Component(arr)

    def merge(self, component):
        return Component(self.arr | component.arr)

    def __eq__(self, component):
        return np.all(component.arr == self.arr)

    def __len__(self):
        return np.sum(self.arr)

    def __str__(self):
        return str(self.arr)

    def __hash__(self):
        val = 0
        for i, num in enumerate(self.arr.ravel()):
            val += int(num) * 2 ** (len(self.arr.ravel()) - i - 1)
        return val


def generate_all_basic_components():
    components = []
    DIMS_ext = [["*"] + range(dim) for dim in DIMS]
    for properties in itertools.product(*DIMS_ext):
        component = Component.get_component_from_properties(properties)
        components.append(component)
    return components


def join_components(components):
    result_component = Component.get_component_from_properties(None)
    for component in components:
        result_component = result_component.merge(component)
    return result_component

K = np.prod(DIMS)
basic_components = generate_all_basic_components()

result_components = []
hash_table = np.zeros(MAX_NUM_COMPONENTS, np.bool)
for k in range(K + 1):
    print "Computing the maximum number of components for K = {}".format(k)
    for components in itertools.combinations(basic_components, k):
        component = join_components(components)
        key = hash(component)
        if not hash_table[key]:
            hash_table[key] = True
            result_components.append(component)
    print len(result_components)
    if len(result_components) >= MAX_NUM_COMPONENTS:
        print "Reached MAX_NUM_COMPONENTS {}".format(MAX_NUM_COMPONENTS)
        exit(0)

'''
    Computing the maximum number of components for K = 0
    1
    Computing the maximum number of components for K = 1
    37
    Computing the maximum number of components for K = 2
    412
    Computing the maximum number of components for K = 3
    1870
    Computing the maximum number of components for K = 4
    3484
    Computing the maximum number of components for K = 5
    4042
    Computing the maximum number of components for K = 6
    4096
    Reached MAX_NUM_COMPONENTS 4096
'''