import heapq
from graphviz import Digraph

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(char_freqs):
    heap = [Node(char, freq) for char, freq in char_freqs.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(heap, merged)

    return heap[0]

def generate_codes(node, prefix="", code_map={}):
    if node is not None:
        if node.char is not None:
            code_map[node.char] = prefix
        generate_codes(node.left, prefix + '0', code_map)
        generate_codes(node.right, prefix + '1', code_map)
    return code_map

def calculate_wpl(node, depth=0):
    if node is not None:
        if node.char is not None:
            return node.freq * depth
        return calculate_wpl(node.left, depth + 1) + calculate_wpl(node.right, depth + 1)
    return 0

def visualize_huffman_tree(root):
    dot = Digraph(comment='Huffman Tree')

    def add_nodes_edges(node, label):
        if node is not None:
            node_label = f'({node.freq})'
            if node.char:
                node_label = f'{node.char}\n' + node_label
            dot.node(label, node_label)
            if node.left is not None:
                left_label = label + 'L'
                dot.edge(label, left_label)
                add_nodes_edges(node.left, left_label)
            if node.right is not None:
                right_label = label + 'R'
                dot.edge(label, right_label)
                add_nodes_edges(node.right, right_label)

    add_nodes_edges(root, 'root')
    return dot

# 数据输入
char_freqs = {
    'A': 4,
    'B': 2,
    'C': 7,
    'D': 11,
    'E': 8,
    'F': 9
}

# 构建树
root = build_huffman_tree(char_freqs)

# 生成编码
huffman_codes = generate_codes(root)

# 计算带权路径长度
wpl = calculate_wpl(root)

# 可视化
dot = visualize_huffman_tree(root)
dot.render('output/huffman_tree', view=True)

# 打印结果
print("Huffman Codes:", huffman_codes)
print("Weighted Path Length (WPL):", wpl)
