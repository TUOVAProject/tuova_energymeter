# tuova_energymeter

## Dev setup

```bash
uv sync # or pip install -e .
```

## RPi setup

### Components used

- Carlo Gavazzi EM530 Energy Analyzer
- Raspberry Pi Zero 2W
- RS485 HAT

### Installation

```
???
```

### Deployment

```bash
???
```

## Notes

Serial port on the RPi (`/dev/ttyS0`) can be tunneled via SSH to the dev machine (`./ttyS0`) as follows (requires `socat` installed on both ends):

```bash
# adjust paths as needed
socat PTY,link=./ttyS0,rawer,echo=0 EXEC:"ssh USER@RASPI 'socat - FILE:/dev/ttyS0,rawer,b9600'"
```
