class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

#TODO
# [] optimize passing data between function in main

class AVLTree:
    def __left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def __right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, root, key):
        if root is None:
            return AVLNode(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and key < root.left.key:
            return self.__right_rotate(root)
        if balance < -1 and key > root.right.key:
            return self.__left_rotate(root)
        if balance > 1 and key > root.left.key:
            root.left = self.__left_rotate(root.left)
            return self.__right_rotate(root)
        if balance < -1 and key < root.right.key:
            root.right = self.__right_rotate(root.right)
            return self.__left_rotate(root)

        return root

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def inorder_traversal(self, root, result):
        if root:
            self.inorder_traversal(root.left, result)
            result.append(root.key)
            self.inorder_traversal(root.right, result)
    

    def remove(self, root, key):
        if root is None:
            return root

        if key < root.key:
            root.left = self.remove(root.left, key)
        elif key > root.key:
            root.right = self.remove(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.right = self.remove(root.right, temp.key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.__right_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.__left_rotate(root.left)
            return self.__right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.__left_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.__right_rotate(root.right)
            return self.__left_rotate(root)

        return root

    def get_min_value_node(self, root):
        if root is None or root.left is None:
            return root
        return self.get_min_value_node(root.left)
