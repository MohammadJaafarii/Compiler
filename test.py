from anytree import Node, RenderTree, PostOrderIter


def dfs(node, visited=None):
    if visited is None:
        visited = set()

    # اگر نود قبلاً بازدید شده، از آن عبور کن
    if node in visited:
        return

    # نود جاری را بازدید کن
    print(node.name)
    visited.add(node)

    # بازدید از بچه‌های نود جاری
    for child in node.children:
        dfs(child, visited)