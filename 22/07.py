from pathlib import Path
import dataclasses as dc
from typing import List, Optional, Tuple, Iterator


@dc.dataclass
class FileSystemNode:
    is_dir: bool = False
    size: int = 0
    name: str = ""
    children: List['FileSystemNode'] = dc.field(default_factory=list)
    parent: Optional['FileSystemNode'] = None

    def calculate_size(self):
        if self.is_dir:
            self.size = 0
            for child in self.children:
                child.calculate_size()
                self.size += child.size

    def __iter__(self) -> Iterator['FileSystemNode']:
        if self.is_dir:
            for child in self.children:
                yield from child
        yield self

    def path(self):
        result = ""
        if self.parent:
            result = self.parent.path()
            result += "/"
        return result + self.name


# Gather commands and their output
cmd_and_output: List[Tuple[str, List[str]]] = []
with open(Path(__file__).parent/"07.txt") as f:
    for line in f:
        line = line.strip()
        if line.startswith("$ "):
            cmd_and_output.append((line[2:], []))
        else:
            cmd_and_output[-1][1].append(line)

root_node: FileSystemNode = FileSystemNode(True)
cur_node: FileSystemNode = root_node

# Process commands
for cmd, output_lines in cmd_and_output:
    if cmd.startswith("cd "):
        dst = cmd[3:]
        if dst == "..":
            assert cur_node.parent
            cur_node = cur_node.parent
        elif dst == "/":
            cur_node = root_node
        else:
            matches = [ch for ch in cur_node.children if ch.name == dst]
            assert len(matches) == 1
            cur_node = matches[0]
    elif cmd == "ls":
        assert not cur_node.children
        for entry in output_lines:
            if entry.startswith("dir "):
                cur_node.children.append(FileSystemNode(is_dir=True, name=entry[4:], parent=cur_node))
            else:
                size, name = entry.split(" ")
                cur_node.children.append(FileSystemNode(is_dir=False, name=name, size=int(size)))
    else:
        assert False

# Calculate sizes for all directories
root_node.calculate_size()

# Task 1:
print(f"Sum of directories with size < 100k: {sum(d.size for d in root_node if d.is_dir and d.size <= 100000)}")

# Task 2:
space_avail = 70000000 - root_node.size
space_needed = 30000000 - space_avail
print(f"Space available: {space_avail}, needed: {space_needed}")
del_candidates = [d for d in root_node if d.is_dir and d.size >= space_needed]
del_candidates.sort(key=lambda d: d.size)
print(f"Smallest directory which frees sufficient space: {del_candidates[0].path()}: {del_candidates[0].size}")
