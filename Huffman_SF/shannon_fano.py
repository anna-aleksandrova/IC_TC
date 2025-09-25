"""Shannon-Fano algorithm.

Input: alphabet X = [x1, x2, ..., x_n] (finiteness assumed),
       distribution P = [p1, p2, ..., p_n], where p_i = p(x_i).

Output: symbols x_i encoded in A = {0, 1}.

Side effects: binary tree is created; helps in decoding from A to X.
"""

class Symbol:
    def __init__(self, name, prob):
        self.name = name
        self.p = prob
        self.leaf = None
        self.encoded = None
    
    def __repr__(self):
        return f"Name: {self.name}; P: {self.p}\n"

class Node:
    def __init__(self, array):
        self.array = array
        self.n = None         
        self.par = None
        self.left = None
        self.right = None
    
    def set_left(self, child):
        self.left = child
        child.n = "1"
        child.par = self
    
    def set_right(self, child):
        self.right = child
        child.n = "0"
        child.par = self


class ShannonFano:
    def __init__(self, x: list[str], p: list[float]):
        self.X = []
        if len(x) != len(p):
            raise Exception("X and P must have the same amount of elements.")
        for i in range(len(x)):
            self.X.append(Symbol(x[i], p[i]))
    
    @staticmethod
    def sort(X: list[Node]):
        if len(X) == 1:
            return X
        med = len(X) // 2
        left = X[:med]
        right = X[med:]
        ShannonFano.sort(left)
        ShannonFano.sort(right)

        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i].p > right[j].p:
                X[k] = left[i]
                i += 1
            else:
                X[k] = right[j]
                j += 1    
            k += 1
        
        while i < len(left):
            X[k] = left[i]
            i += 1
            k += 1
        
        while j < len(right):
            X[k] = right[j]
            j += 1
            k += 1 
    
    @staticmethod
    def divide(array: list[Symbol]):
        total = sum(s.p for s in array)
        left_sum = 0
        best_diff = float("inf")
        res = 1
        for i in range(len(array) - 1):
            left_sum += array[i].p
            right_sum = total - left_sum
            diff = abs(right_sum - left_sum)
            if diff < best_diff:
                best_diff = diff
                res = i + 1
        return res 
    
    @staticmethod
    def build_node(root: Node):
        ind = ShannonFano.divide(root.array)
        left_child = Node(root.array[:ind])
        root.set_left(left_child)
        right_child = Node(root.array[ind:])
        root.set_right(right_child)

        for child in [root.left, root.right]:
            if len(child.array) != 1:
                ShannonFano.build_node(child)
            else:
                child.array[0].leaf = child
    
    def build_tree(self):
        ShannonFano.sort(self.X)
        root = Node(self.X)
        ShannonFano.build_node(root)
        return root
    
    def encode(self):
        self.build_tree()
        self.d = {}
        for symb in self.X:
            res = ""
            current = symb.leaf
            while current is not None:
                if current.n:
                    res += current.n
                current = current.par
            symb.encoded = res[::-1]
            self.d[symb.name] = symb.encoded
    
    def encode_message(self, message: str):
        res = ""
        for symb in message:
            if symb not in self.d:
                raise Exception("Unknown symbol")
            else:
                res += self.d[symb]
        return res
            

    def show_encoded(self):
        for symb in self.X:
            print(f"{symb.name} <-> {symb.encoded}")    


if __name__ == "__main__":
    X1 = ["a", "b", "c"]
    P1 = [0.2, 0.2, 0.6]
    obj1 = ShannonFano(X1, P1)
    obj1.encode()
    obj1.show_encoded()

    print()

    X2 = ["М", "У", "Б", "Ю", "А"]
    P2 = [0.35, 0.2, 0.25, 0.05, 0.15]
    obj2 = ShannonFano(X2, P2)
    obj2.encode()
    obj2.show_encoded()
    m = "МУМБУЮМБУБУММАМБАБАМ"
    print(obj2.encode_message(m))
