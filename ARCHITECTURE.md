# Project Architecture - Dreamy Runner

## 📁 Project Structure

```
pygamecos10009/
├── main.py                 # Entry point (96 lines) - starts game
├── game.py                 # Game class with core logic  
├── events.py               # Input handling by state
├── screens.py              # All rendering/drawing functions
│
├── player.py               # Player class
├── obstacle.py             # Obstacle class
├── coin.py                 # Coin class
├── game_state.py           # Game state enum
├── settings.py             # Config constants
│
└── assets/                 # Game images
    ├── background.png
    ├── mountain.png
    ├── road.png
    ├── idle.png
    ├── jump.png
    ├── duck.png
    ├── run_1.png
    └── run_2.png
```

## 🎮 Core Components

### **main.py** (Entry Point)
- Initializes pygame and loads assets
- Creates Game instance
- Main event loop
- Handles state transitions
- **~96 lines** - Clean and readable

### **game.py** (Game Logic)
- `Game` class - manages all game state
- Handles game updates (collisions, spawning, scoring)
- Manages scrolling backgrounds
- Updates and renders game objects
- Settings management

### **events.py** (Input Handling)
- State-based input handlers
- `handle_menu_input()` - Menu navigation
- `handle_settings_input()` - Settings adjustment  
- `handle_running_input()` - Game controls
- `handle_game_over_input()` - Retry/Menu
- `process_events()` - Main dispatcher

### **screens.py** (UI Rendering)
- All drawing functions
- `draw_menu()` - Main menu
- `draw_settings()` - Settings screen
- `draw_start_screen()` - Pre-game screen
- `draw_game_over()` - Game over screen
- `draw_background()`, `draw_ground()`, `draw_ui()`

### **player.py** (Player Class)
- Player logic and rendering
- Animation handling
- Jump and duck mechanics

### **obstacle.py** (Obstacle Class)
- Obstacle spawning and movement
- Collision boxes
- Visual rendering

### **coin.py** (Coin Class)
- Coin spawning and animation
- Floating effect with sine wave
- Scale animation

## 🔄 Game States (game_state.py)

```python
GameState.MENU          # Main menu
GameState.SETTINGS      # Settings screen
GameState.START         # Pre-game ready screen
GameState.RUNNING       # Actual gameplay
GameState.GAME_OVER     # Game over screen
```

## 📊 Game Flow

```
START
  ↓
MENU (UP/DOWN to select, SPACE to choose)
  ├→ PLAY → START (SPACE to begin)
  │           ↓
  │       RUNNING (W/UP jump, S/DOWN duck, ESC menu)
  │           ↓
  │       [COLLISION]
  │           ↓
  │       GAME_OVER (SPACE retry, ESC menu)
  │           ↓
  │       START → RUNNING (loop)
  │
  ├→ SETTINGS (UP/DOWN select, LEFT/RIGHT change, ESC back)
  │
  └→ QUIT → EXIT
```

## 🎯 Game Settings

```python
settings = {
    "volume": 50          # 0-100%
    "difficulty": 1       # 1=Easy, 2=Normal, 3=Hard
}
```

## 📈 Benefits of This Structure

✅ **Separation of Concerns**
- Each file has a clear responsibility
- Easy to find and modify specific features

✅ **Maintainability**
- max 200 lines per file (except main.py ~96 lines)
- Clear function and class organization
- Comments for complex logic

✅ **Scalability**
- Easy to add new states
- Simple to extend rendering
- Modular input handling

✅ **Testing**
- Each component can be tested independently
- Pure functions in screens.py and events.py

✅ **Readability**
- Entry point (main.py) is very clean
- Each module focuses on one thing
- Easy to understand game flow

## 🔧 Future Improvements

1. Add sound effects module
2. Create particle effects system
3. Add high score persistence (JSON/SQLite)
4. Separate physics engine
5. Add level manager for difficulty implementation
6. Create menu animations
