""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from pathlib import Path


def extract(
        path: Path, *, save_as: Path
) -> None:
    """
    """


def parse_index(value: str) -> int | slice:
    """
    """
    if ':' not in value:
        try:
            return int(value)

        except ValueError as error:
            raise ValueError(
                f"unsupported index {value!r}"
            ) from error

    parts = value.split(':')

    if len(parts) > 3:
        raise ValueError(
            f"invalid index component {value!r}"
        )

    parsed = []
    for part in parts:
        part = part.strip()

        if part:
            try:
                parsed.append(int(part))

            except ValueError as error:
                raise ValueError(
                    f"invalid index component {value!r}"
                ) from error

        else:
            parsed.append(None)

    while len(parsed) < 3:
        parsed.append(None)

    if parsed[2] == 0:
        raise ValueError(
            f"slice step cannot be zero in index {value!r}"
        )

    return slice(*parsed)
