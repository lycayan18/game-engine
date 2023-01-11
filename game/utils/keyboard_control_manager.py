from core.utils.event_emitter import EventEmitter


class KeyboardControlManager:
    def __init__(self):
        self.keys: dict[list[str]] = {}

        # Dictionary, representing action ( key ) - how many keys are triggering this action ( value )
        self.actions: dict[int] = {}

    def bind_key(self, key: int, action: str):
        if key not in self.keys:
            self.keys[key] = []

        self.keys[key].append(action)

        if action not in self.actions:
            self.actions[action] = 0

    def unbind_key(self, key: int, action: str):
        if action in self.keys[key]:
            self.keys[key].remove(action)

    def get_keys(self, action: str) -> list[int]:
        """
        Returns list of keys binded to provided action.\n
        Note: that function is expensive, so frequent calls not expected.
        """

        out = []

        for key in self.keys.keys():
            if action in self.keys[key]:
                out.append(key)

        return out

    def handle_key_down(self, key: int):
        for action in self.keys.get(key, []):
            self.actions[action] += 1

    def handle_key_up(self, key: int):
        for action in self.keys.get(key, []):
            self.actions[action] -= 1

    def is_active(self, action: str) -> bool:
        """
        Returns True if at least one key is triggering this action.
        """

        return self.actions[action] > 0
