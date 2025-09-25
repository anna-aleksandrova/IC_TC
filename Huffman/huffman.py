"""Huffman algorithm.

Input: alphabet X = [x1, x2, ..., x_n] (finiteness assumed),
       distribution P = [p1, p2, ..., p_n], where p_i = p(x_i).

Output: symbols x_i encoded in A = {0, 1}.

Side effects: binary tree is created; helps in decoding from A to X.
"""

class Node:
    def __init__(self, name, prob):
        self.name = name
        self.p = prob
        self.union = 0
        self.n = None         
        self.encoded = None   
        self.par = None
        self.left = None
        self.right = None

    def parent(self, par):
        self.par = par
    
    def set_left(self, child):
        self.left = child
        child.n = "0"
    
    def set_right(self, child):
        self.right = child
        child.n = "1"

    def __repr__(self):
        return f"Name: {self.name}; P: {self.p}; union: {self.union}\n"


class Huffman:
    def __init__(self, x: list[str], p: list[float]):
        self.X = []
        if len(x) != len(p):
            raise Exception("X and P must have the same amount of elements.")
        for i in range(len(x)):
            self.X.append(Node(x[i], p[i]))
    
    @staticmethod
    def sort(X: list[Node]):
        if len(X) == 1:
            return X
        med = len(X) // 2
        left = X[:med]
        right = X[med:]
        Huffman.sort(left)
        Huffman.sort(right)

        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i].p > right[j].p:
                X[k] = left[i]
                i += 1
            elif left[i].p < right[j].p:
                X[k] = right[j]
                j += 1
            elif left[i].union > right[j].union:
                X[k] = left[i]
                i += 1
            elif left[i].union < right[j].union:
                X[k] = right[j]
                j += 1
            else:
                X[k] = left[i]
                i += 1      
            k += 1
        
        while i < len(left):
            X[k] = left[i]
            i += 1
            k += 1
        
        while j < len(right):
            X[k] = right[j]
            j += 1
            k += 1      

    def build_tree(self):
        temp = self.X[:]
        while len(temp) != 1:
            Huffman.sort(temp)
            node2 = temp.pop()
            node1 = temp.pop()
            new_node = Node(node1.name + node2.name, node1.p + node2.p)
            new_node.union = node1.union + node2.union + 1
            new_node.set_left(node1)
            new_node.set_right(node2)
            node1.parent(new_node)
            node2.parent(new_node)
            temp.append(new_node)
        self.tree = temp[0]
    
    def encode(self):
        self.build_tree()
        for symb in self.X:
            res = ""
            current = symb
            while current is not None:
                if current.n:
                    res += current.n
                current = current.par
            symb.encoded = res[::-1]

    def show_encoded(self):
        for symb in self.X:
            print(f"{symb.name} <-> {symb.encoded}")    


if __name__ == "__main__":
    X1 = ["a", "b", "c", "d", "e", "f"]
    P1 = [0.05, 0.15, 0.05, 0.4, 0.2, 0.15]
    obj1 = Huffman(X1, P1)
    obj1.encode()
    obj1.show_encoded()

    print()
    
    X2 = ["x1", "x2", "x3", "x4", "x5"]
    P2 = [0.2, 0.2, 0.4, 0.15, 0.05]
    obj2 = Huffman(X2, P2)
    obj2.encode()
    obj2.show_encoded()
