"""B-Tree — balanced multi-way search tree."""
class BTreeNode:
    def __init__(self, t, leaf=True):
        self.t = t; self.keys = []; self.children = []; self.leaf = leaf

class BTree:
    def __init__(self, t=3):
        self.t = t; self.root = BTreeNode(t)
    def search(self, key, node=None):
        if node is None: node = self.root
        i = 0
        while i < len(node.keys) and key > node.keys[i]: i += 1
        if i < len(node.keys) and key == node.keys[i]: return True
        if node.leaf: return False
        return self.search(key, node.children[i])
    def insert(self, key):
        r = self.root
        if len(r.keys) == 2*self.t - 1:
            s = BTreeNode(self.t, False)
            s.children.append(self.root)
            self._split(s, 0); self.root = s
        self._insert_non_full(self.root, key)
    def _insert_non_full(self, node, key):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(0)
            while i >= 0 and key < node.keys[i]:
                node.keys[i+1] = node.keys[i]; i -= 1
            node.keys[i+1] = key
        else:
            while i >= 0 and key < node.keys[i]: i -= 1
            i += 1
            if len(node.children[i].keys) == 2*self.t - 1:
                self._split(node, i)
                if key > node.keys[i]: i += 1
            self._insert_non_full(node.children[i], key)
    def _split(self, parent, i):
        t = self.t; y = parent.children[i]
        z = BTreeNode(t, y.leaf)
        parent.keys.insert(i, y.keys[t-1])
        parent.children.insert(i+1, z)
        z.keys = y.keys[t:]; y.keys = y.keys[:t-1]
        if not y.leaf:
            z.children = y.children[t:]; y.children = y.children[:t]
    def inorder(self, node=None):
        if node is None: node = self.root
        result = []
        for i, key in enumerate(node.keys):
            if not node.leaf: result.extend(self.inorder(node.children[i]))
            result.append(key)
        if not node.leaf: result.extend(self.inorder(node.children[-1]))
        return result

if __name__ == "__main__":
    bt = BTree(3)
    for x in [10,20,5,6,12,30,7,17]:
        bt.insert(x)
    result = bt.inorder()
    print(f"B-Tree inorder: {result}")
    assert result == sorted(result)
    assert bt.search(12) and bt.search(30)
    assert not bt.search(11) and not bt.search(99)
    print("All tests passed!")
