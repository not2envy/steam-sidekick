# Steam Sidekick

A Steam Deck-inspired companion dashboard for SteamOS.

Steam Sidekick displays live system information from a SteamOS gaming PC on a dedicated secondary display such as a Lenovo Yoga Tab 3.

## Features

### Current
- Live CPU temperature
- Live GPU edge temperature
- Live GPU junction temperature
- Live GPU memory temperature
- FastAPI backend
- Podman container support

### Planned
- CPU usage
- GPU usage
- RAM usage
- VRAM usage
- GPU clocks
- GPU power
- Fan speeds
- Current game information
- FPS monitoring
- Download progress
- Sleep mode screen
- Steam-inspired interface

## Hardware

### Steam Machine
- AMD Ryzen 2600
- AMD Radeon RX 6800
- SteamOS

### Companion Display
- Lenovo Yoga Tab 3

## Project Structure

```
steam-dashboard/
├── backend/
├── dashboard/
├── docs/
├── screenshots/
├── README.md
└── LICENSE
```

## Roadmap

- [x] Read CPU and GPU temperatures
- [x] Containerize backend
- [x] Publish project to GitHub
- [x] Automatically discover hardware sensors
- [ ] CPU and GPU utilization
- [ ] Memory monitoring
- [ ] Fan monitoring
- [ ] Dashboard UI
- [ ] Gaming mode
- [ ] ASP.NET Core backend

## License

MIT
