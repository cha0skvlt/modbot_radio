class Player:
    def __init__(self) -> None:
        self.playing = False

    async def join(self, chat_id: int) -> None:
        pass

    async def play(self) -> None:
        self.playing = True

    async def stop(self) -> None:
        self.playing = False

    async def skip(self) -> None:
        pass


def get_player() -> Player:
    global _player
    try:
        return _player
    except NameError:
        _player = Player()
        return _player
