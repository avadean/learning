from program import Program, updateDisplay
from setting import Settings


if __name__ == '__main__':
    settings = Settings()
    program = Program(settings)

    while program.running:
        program.handleEvents()
        program.update()
        program.draw()

        program.clock.tick(60)

        updateDisplay()

    exit(0)
