import os
import pathlib
import sys

from rich import print
from rich.tree import Tree


class Node:
    def __init__(self, name, is_file=False):
        self.name = name
        self.is_file = is_file
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return (
            f"[blue]{self.name}[/]"
            if self.is_file
            else f"[bold magenta]:open_file_folder: {self.name}"
        )


class FileTree:
    def __init__(self, root):
        self.root = root

    def add_file(self, file_path):
        # Split the file path into its constituent parts
        parts = file_path.split("/")

        # Add each folder to the tree
        node = self.root
        for part in parts[:-1]:
            # Check if the folder already exists
            found = False
            for child in node.children:
                if child.name == part:
                    node = child
                    found = True
                    break

            # If the folder does not exist, create a new node and add it to the tree
            if not found:
                new_node = Node(part)
                node.add_child(new_node)
                node = new_node

        # Add the file to the last folder
        node.add_child(Node(parts[-1], is_file=True))


def get_modified_files(path: pathlib.Path) -> list:
    command = f"git --git-dir={path}/.git --work-tree={path} diff --name-only"
    modified_files = os.popen(command).read().splitlines()
    return modified_files


def build_rich_subtree(node: Node) -> Tree:
    # Recursively build a rich subtree.
    tree = Tree(repr(node))
    for child in node.children:
        if child.is_file:
            tree.add(repr(child))
        else:
            sub_tree = build_rich_subtree(child)
            tree.add(sub_tree)
    return tree


def create_root_node(directory: str) -> Node:
    repo_name = directory.split("/")[-1]
    command = f"git --git-dir={directory}/.git --work-tree={directory} diff --shortstat"

    repo_stats = os.popen(command).read()
    (added, modified, deleted) = repo_stats.split(",")

    changes = f"{repo_name}:[green]{added}[/], [yellow]{modified}[/], [red]{deleted}[/]"
    return Node(changes)


def create_file_tree(root: Node, file_names) -> FileTree:
    tree = FileTree(root)

    for filename in file_names:
        tree.add_file(filename)

    return tree


def main():
    try:
        directory = os.path.abspath(sys.argv[1])
    except IndexError:
        print("[b]Usage:[/] gittree <directory>")
    else:
        modified_files = get_modified_files(pathlib.Path(directory))
        root = create_root_node(directory)
        file_tree = create_file_tree(root, modified_files)
        rich_tree = build_rich_subtree(file_tree.root)

        print(rich_tree)


if __name__ == "__main__":
    main()
