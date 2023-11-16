from typing import Any, Callable, Pattern, Set, Type, Generator
import os
from passlib.hash import pbkdf2_sha256


class BaseUtils:

    @classmethod
    def all_base_classes(cls, class_: Type) -> Set:
        base_class_set = set(class_.__bases__)
        all_base_class_set = {class_}
        all_base_class_set.update(base_class_set)
        for base in base_class_set:
            all_base_class_set.update(cls.all_base_classes(base))
        return all_base_class_set

    @classmethod
    def walk_all_parent_dirs(cls, path: str) -> Generator:
        """
        Yield directories starting from the given directory up to the root
        """
        if not os.path.exists(path):
            raise IOError("Starting path not found")

        if os.path.isfile(path):
            path = os.path.dirname(path)

        last_dir = None
        current_dir = os.path.abspath(path)
        while last_dir != current_dir:
            yield current_dir
            parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
            last_dir, current_dir = current_dir, parent_dir
