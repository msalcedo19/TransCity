from utils.generator import Generator
from utils.GUI import GUI


def main():
    gen = Generator()
    gen.load_map()
    GUI(gen)


main()

