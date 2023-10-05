import heapq
from heapq import heappop, heappush
from collections import Counter


class Node:
    def __init__(self, ch, freq, left=None, right=None):
        self.ch = ch
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


def is_leaf(root):
    return root.left is None and root.right is None


def encode(root, s, huffman_code):
    if root is None:
        return

    if is_leaf(root):
        huffman_code[root.ch] = s if len(s) > 0 else '1'

    encode(root.left, s + '0', huffman_code)
    encode(root.right, s + '1', huffman_code)


def decode(root, index, s, ans):
    if root is None:
        return index

    if is_leaf(root):
        ans.append(root.ch)
        return index

    index = index + 1
    root = root.left if s[index] == '0' else root.right
    return decode(root, index, s, ans)


def build_huffman_tree(text):
    if len(text) == 0:
        return

    freq = Counter(text)

    pq = [Node(k, v) for k, v in freq.items()]
    heapq.heapify(pq)

    while len(pq) != 1:
        left = heappop(pq)
        right = heappop(pq)
        total = left.freq + right.freq
        heappush(pq, Node(None, total, left, right))

    root = pq[0]
    huffmanCode = {}
    encode(root, '', huffmanCode)

    print('Huffman Codes are:', huffmanCode)
    print('The original string is:', text)

    s = ''.join([huffmanCode.get(i) for i in text])
    print('The encoded string is:', s)

    ans = []
    if is_leaf(root):
        while root.freq > 0:
            ans.append(root.ch)
            root.freq = root.freq - 1
    else:
        index = -1
        while index < len(s) - 1:
            index = decode(root, index, s, ans)
    result = ''.join(ans)
    print('The decoded string is:', result)


if __name__ == '__main__':
    text = 'The quick brown fox jumps over the lazy dog'
    build_huffman_tree(text)