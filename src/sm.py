from typing import Optional, TypeVar, Generic

T = TypeVar('T')


class State(Generic[T]):
    if_true: 'State'
    if_false: 'State'
    _id: T

    def get_id(self):
        return self._id

    def __init__(self, _id: T, if_true: Optional['State'] = None, if_false: Optional['State'] = None):
        self._id = _id

        if if_true is None:
            self.if_true = self
        else:
            self.if_true = if_true

        if if_false is None:
            self.if_false = self
        else:
            self.if_false = if_false

    def __getitem__(self, item: bool):
        if item:
            return self.if_true
        else:
            return self.if_false

    def __str__(self):
        return "{}({},{})".format(self.get_id(), self.if_false.get_id(), self.if_true.get_id())


final = State(0)
s = State(1, if_false=final)
print(s, s[True], s[False])

