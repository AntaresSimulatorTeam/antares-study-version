import typing as t


class ValidationError(ValueError):
    """
    Exception raised when a validation error occurs.
    """

    def __init__(self, description: str, errors: t.Dict[str, str]):
        super().__init__(description, errors)

    @property
    def description(self) -> str:
        return self.args[0]

    @property
    def errors(self) -> t.Dict[str, str]:
        return self.args[1]

    def __str__(self):
        # {count} invalid fields
        count = len(self.errors)
        msg = {
            0: "No errors",
            1: f"{count} invalid field",
            2: f"{count} invalid fields",
        }[min(count, 2)]
        lines = [f"{self.description}: {msg}"]
        lines += [f"- {field}: {error}" for field, error in self.errors.items()]
        return "\n".join(lines)
