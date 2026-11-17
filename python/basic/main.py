class Pokemon:
    type1: str
    type2: str
    name: str
    stats: dict

    def __init__(self, type1: str, type2: str, name: str, stats: dict) -> None:
        self.type1 = type1
        self.type2 = type2
        self.name = name
        self.stats = stats

    def typing(self) -> str:
        if self.type1 == self.type2:
            return f"{self.name.title()} is a {self.type1.title()} Pokemon"
        else:
            return f"{self.name.title()} is a {self.type1.title()} and {self.type2.title()} Pokemon"


if __name__ == "__main__":
    pikachu = Pokemon("electric", "electric", "Pikachu", {})
    charizard = Pokemon("fire", "flying", "charizard", {})

    print(pikachu.typing())
    print(charizard.typing())
