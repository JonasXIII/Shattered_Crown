import pygame
from enum import Enum, auto
from typing import Dict, List, Optional, Callable, Tuple, Set

from constants import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_INTERACT, KEY_ATTACK
from engine.game_state import GameState


class InputAction(Enum):
    """Enum representing possible game actions triggered by input"""
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    ATTACK = auto()
    INTERACT = auto()
    OPEN_INVENTORY = auto()
    OPEN_CHARACTER = auto()
    OPEN_QUEST_LOG = auto()
    CONFIRM = auto()
    CANCEL = auto()
    PAUSE = auto()
    END_TURN = auto()
    USE_SKILL_1 = auto()
    USE_SKILL_2 = auto()
    USE_SKILL_3 = auto()
    USE_SKILL_4 = auto()
    QUICK_SAVE = auto()
    QUICK_LOAD = auto()


class InputState(Enum):
    """Enum representing the state of an input"""
    JUST_PRESSED = auto()
    HELD = auto()
    JUST_RELEASED = auto()
    INACTIVE = auto()


class InputType(Enum):
    """Enum representing the type of input device"""
    KEYBOARD = auto()
    MOUSE = auto()
    GAMEPAD = auto()


class MouseButton(Enum):
    """Enum representing mouse buttons"""
    LEFT = auto()
    RIGHT = auto()
    MIDDLE = auto()
    WHEEL_UP = auto()
    WHEEL_DOWN = auto()


class InputHandler:
    """
    Handles all input processing for the game, translating raw input events
    to game actions based on the current context.
    """
    
    def __init__(self):
        """Initialize the input handler"""
        # Initialize pygame's input modules
        pygame.key.set_repeat(500, 50)  # Key repeat delay and interval
        
        # Mappings from inputs to actions for different contexts
        self._keyboard_mappings: Dict[GameState, Dict[int, InputAction]] = {}
        self._mouse_mappings: Dict[GameState, Dict[MouseButton, InputAction]] = {}
        self._gamepad_mappings: Dict[GameState, Dict[int, InputAction]] = {}
        
        # Current state of actions
        self._action_states: Dict[InputAction, InputState] = {
            action: InputState.INACTIVE for action in InputAction
        }
        
        # Previous state of keyboard keys and mouse buttons
        self._prev_keys: Set[int] = set()
        self._prev_mouse_buttons: Set[int] = set()
        
        # Input history for combo detection
        self._input_history: List[Tuple[InputAction, float]] = []
        self._history_max_size = 10
        self._history_max_age = 2.0  # seconds
        
        # Mouse position and motion
        self._mouse_pos = (0, 0)
        self._mouse_rel = (0, 0)
        
        # UI callbacks for mouse interaction
        self._ui_element_callbacks: Dict[Tuple[int, int, int, int], Callable] = {}
        
        # Initialize default mappings
        self._init_default_mappings()
    
    def _init_default_mappings(self):
        """Initialize default input mappings for different game states"""
        # Default keyboard mappings for overworld
        overworld_keyboard = {
            KEY_UP: InputAction.MOVE_UP,
            KEY_DOWN: InputAction.MOVE_DOWN,
            KEY_LEFT: InputAction.MOVE_LEFT,
            KEY_RIGHT: InputAction.MOVE_RIGHT,
            KEY_INTERACT: InputAction.INTERACT,
            pygame.K_i: InputAction.OPEN_INVENTORY,
            pygame.K_c: InputAction.OPEN_CHARACTER,
            pygame.K_q: InputAction.OPEN_QUEST_LOG,
            pygame.K_ESCAPE: InputAction.PAUSE,
            pygame.K_F5: InputAction.QUICK_SAVE,
            pygame.K_F9: InputAction.QUICK_LOAD,
        }
        
        # Default keyboard mappings for combat
        combat_keyboard = {
            KEY_UP: InputAction.MOVE_UP,
            KEY_DOWN: InputAction.MOVE_DOWN,
            KEY_LEFT: InputAction.MOVE_LEFT,
            KEY_RIGHT: InputAction.MOVE_RIGHT,
            KEY_ATTACK: InputAction.ATTACK,
            pygame.K_1: InputAction.USE_SKILL_1,
            pygame.K_2: InputAction.USE_SKILL_2,
            pygame.K_3: InputAction.USE_SKILL_3,
            pygame.K_4: InputAction.USE_SKILL_4,
            pygame.K_SPACE: InputAction.END_TURN,
            pygame.K_i: InputAction.OPEN_INVENTORY,
            pygame.K_ESCAPE: InputAction.PAUSE,
        }
        
        # Default mouse mappings for overworld
        overworld_mouse = {
            MouseButton.LEFT: InputAction.INTERACT,
            MouseButton.RIGHT: InputAction.CANCEL,
        }
        
        # Default mouse mappings for combat
        combat_mouse = {
            MouseButton.LEFT: InputAction.ATTACK,
            MouseButton.RIGHT: InputAction.CANCEL,
        }
        
        # Set mappings for different game states
        self._keyboard_mappings[GameState.OVERWORLD] = overworld_keyboard
        self._keyboard_mappings[GameState.LOCAL_AREA] = overworld_keyboard.copy()
        self._keyboard_mappings[GameState.COMBAT] = combat_keyboard
        
        self._mouse_mappings[GameState.OVERWORLD] = overworld_mouse
        self._mouse_mappings[GameState.LOCAL_AREA] = overworld_mouse.copy()
        self._mouse_mappings[GameState.COMBAT] = combat_mouse
        
        # Add common mappings for menu states
        for state in [GameState.INVENTORY, GameState.DIALOG, GameState.SHOP, GameState.QUEST_LOG]:
            self._keyboard_mappings[state] = {
                pygame.K_ESCAPE: InputAction.CANCEL,
                pygame.K_RETURN: InputAction.CONFIRM,
            }
            self._mouse_mappings[state] = {
                MouseButton.LEFT: InputAction.CONFIRM,
                MouseButton.RIGHT: InputAction.CANCEL,
            }
    
    def update(self, delta_time: float, current_state: GameState):
        """
        Update input states based on current pygame events
        
        Args:
            delta_time: Time since last frame in seconds
            current_state: Current game state
        """
        # Get current keyboard state
        current_keys = set(pygame.key.get_pressed())
        
        # Get current mouse state
        mouse_buttons = pygame.mouse.get_pressed(num_buttons=3)
        current_mouse_buttons = set(i for i, pressed in enumerate(mouse_buttons) if pressed)
        self._mouse_pos = pygame.mouse.get_pos()
        self._mouse_rel = pygame.mouse.get_rel()
        
        # Process keyboard input
        if current_state in self._keyboard_mappings:
            mapping = self._keyboard_mappings[current_state]
            self._process_keyboard_input(mapping, current_keys)
        
        # Process mouse input
        if current_state in self._mouse_mappings:
            mapping = self._mouse_mappings[current_state]
            self._process_mouse_input(mapping, current_mouse_buttons)
        
        # Update input history
        self._update_input_history(delta_time)
        
        # Store current input state for next frame
        self._prev_keys = current_keys
        self._prev_mouse_buttons = current_mouse_buttons
    
    def _process_keyboard_input(self, mapping: Dict[int, InputAction], current_keys: Set[int]):
        """
        Process keyboard input and update action states
        
        Args:
            mapping: Key to action mapping for current game state
            current_keys: Currently pressed keys
        """
        # Check each mapped key
        for key, action in mapping.items():
            if key in current_keys and key not in self._prev_keys:
                self._action_states[action] = InputState.JUST_PRESSED
                self._input_history.append((action, pygame.time.get_ticks() / 1000.0))
            elif key in current_keys and key in self._prev_keys:
                self._action_states[action] = InputState.HELD
            elif key not in current_keys and key in self._prev_keys:
                self._action_states[action] = InputState.JUST_RELEASED
            elif action in self._action_states and self._action_states[action] != InputState.INACTIVE:
                if key not in current_keys:
                    self._action_states[action] = InputState.INACTIVE
    
    def _process_mouse_input(self, mapping: Dict[MouseButton, InputAction], current_buttons: Set[int]):
        """
        Process mouse input and update action states
        
        Args:
            mapping: Mouse button to action mapping for current game state
            current_buttons: Currently pressed mouse buttons
        """
        # Convert from integer buttons to enum
        button_to_enum = {
            0: MouseButton.LEFT,
            1: MouseButton.MIDDLE,
            2: MouseButton.RIGHT
        }
        
        # Check each mapped mouse button
        for button_idx, button_enum in button_to_enum.items():
            if button_enum in mapping:
                action = mapping[button_enum]
                
                if button_idx in current_buttons and button_idx not in self._prev_mouse_buttons:
                    self._action_states[action] = InputState.JUST_PRESSED
                    self._input_history.append((action, pygame.time.get_ticks() / 1000.0))
                elif button_idx in current_buttons and button_idx in self._prev_mouse_buttons:
                    self._action_states[action] = InputState.HELD
                elif button_idx not in current_buttons and button_idx in self._prev_mouse_buttons:
                    self._action_states[action] = InputState.JUST_RELEASED
                elif action in self._action_states and self._action_states[action] != InputState.INACTIVE:
                    if button_idx not in current_buttons:
                        self._action_states[action] = InputState.INACTIVE
    
    def _update_input_history(self, delta_time: float):
        """
        Update input history, removing old inputs
        
        Args:
            delta_time: Time since last frame in seconds
        """
        # Limit history size
        if len(self._input_history) > self._history_max_size:
            self._input_history = self._input_history[-self._history_max_size:]
        
        # Remove old inputs
        current_time = pygame.time.get_ticks() / 1000.0
        self._input_history = [
            (action, time) for action, time in self._input_history
            if current_time - time <= self._history_max_age
        ]
    
    def handle_event(self, event, current_state: GameState) -> bool:
        """
        Process a pygame event and update action states
        
        Args:
            event: Pygame event to process
            current_state: Current game state
            
        Returns:
            True if the event was consumed, False otherwise
        """
        # Handle mouse wheel events
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                action = self._mouse_mappings.get(current_state, {}).get(MouseButton.WHEEL_UP)
                if action:
                    self._action_states[action] = InputState.JUST_PRESSED
                    self._input_history.append((action, pygame.time.get_ticks() / 1000.0))
                    return True
            elif event.y < 0:
                action = self._mouse_mappings.get(current_state, {}).get(MouseButton.WHEEL_DOWN)
                if action:
                    self._action_states[action] = InputState.JUST_PRESSED
                    self._input_history.append((action, pygame.time.get_ticks() / 1000.0))
                    return True
        
        # Handle UI element clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rect, callback in self._ui_element_callbacks.items():
                x, y, width, height = rect
                if x <= event.pos[0] <= x + width and y <= event.pos[1] <= y + height:
                    callback()
                    return True
        
        return False
    
    def is_action_pressed(self, action: InputAction) -> bool:
        """
        Check if an action was just pressed this frame
        
        Args:
            action: Action to check
            
        Returns:
            True if the action was just pressed, False otherwise
        """
        return self._action_states.get(action) == InputState.JUST_PRESSED
    
    def is_action_held(self, action: InputAction) -> bool:
        """
        Check if an action is being held
        
        Args:
            action: Action to check
            
        Returns:
            True if the action is being held, False otherwise
        """
        return self._action_states.get(action) == InputState.HELD
    
    def is_action_released(self, action: InputAction) -> bool:
        """
        Check if an action was just released this frame
        
        Args:
            action: Action to check
            
        Returns:
            True if the action was just released, False otherwise
        """
        return self._action_states.get(action) == InputState.JUST_RELEASED
    
    def is_action_active(self, action: InputAction) -> bool:
        """
        Check if an action is either just pressed or held
        
        Args:
            action: Action to check
            
        Returns:
            True if the action is active, False otherwise
        """
        state = self._action_states.get(action)
        return state == InputState.JUST_PRESSED or state == InputState.HELD
    
    def get_mouse_position(self) -> Tuple[int, int]:
        """
        Get the current mouse position
        
        Returns:
            Tuple of (x, y) mouse coordinates
        """
        return self._mouse_pos
    
    def get_mouse_movement(self) -> Tuple[int, int]:
        """
        Get the relative mouse movement since last frame
        
        Returns:
            Tuple of (dx, dy) mouse movement
        """
        return self._mouse_rel
    
    def register_ui_element(self, rect: Tuple[int, int, int, int], callback: Callable) -> None:
        """
        Register a UI element for click detection
        
        Args:
            rect: Rectangle (x, y, width, height) defining the UI element
            callback: Function to call when the element is clicked
        """
        self._ui_element_callbacks[rect] = callback
    
    def unregister_ui_element(self, rect: Tuple[int, int, int, int]) -> None:
        """
        Unregister a UI element
        
        Args:
            rect: Rectangle (x, y, width, height) defining the UI element
        """
        if rect in self._ui_element_callbacks:
            del self._ui_element_callbacks[rect]
    
    def clear_ui_elements(self) -> None:
        """Clear all registered UI elements"""
        self._ui_element_callbacks.clear()
    
    def detect_combo(self, combo: List[InputAction], max_time: float = 1.0) -> bool:
        """
        Check if a specific sequence of inputs has occurred recently
        
        Args:
            combo: List of actions in the desired sequence
            max_time: Maximum time window for the combo in seconds
            
        Returns:
            True if the combo was performed, False otherwise
        """
        if len(self._input_history) < len(combo):
            return False
        
        # Check if the most recent inputs match the combo
        recent_actions = [action for action, _ in self._input_history[-len(combo):]]
        if recent_actions != combo:
            return False
        
        # Check if the combo was performed within the time window
        start_time = self._input_history[-len(combo)][1]
        end_time = self._input_history[-1][1]
        return end_time - start_time <= max_time
    
    def rebind_key(self, game_state: GameState, key: int, action: InputAction) -> None:
        """
        Rebind a key to a different action for a specific game state
        
        Args:
            game_state: Game state to modify bindings for
            key: New key to bind
            action: Action to bind the key to
        """
        if game_state not in self._keyboard_mappings:
            self._keyboard_mappings[game_state] = {}
        
        # Remove any existing bindings for this key and action
        for k in list(self._keyboard_mappings[game_state].keys()):
            if self._keyboard_mappings[game_state][k] == action:
                del self._keyboard_mappings[game_state][k]
        
        # Add the new binding
        self._keyboard_mappings[game_state][key] = action
    
    def rebind_mouse(self, game_state: GameState, button: MouseButton, action: InputAction) -> None:
        """
        Rebind a mouse button to a different action for a specific game state
        
        Args:
            game_state: Game state to modify bindings for
            button: Mouse button to bind
            action: Action to bind the button to
        """
        if game_state not in self._mouse_mappings:
            self._mouse_mappings[game_state] = {}
        
        # Remove any existing bindings for this button and action
        for b in list(self._mouse_mappings[game_state].keys()):
            if self._mouse_mappings[game_state][b] == action:
                del self._mouse_mappings[game_state][b]
        
        # Add the new binding
        self._mouse_mappings[game_state][button] = action
    
    def get_key_for_action(self, game_state: GameState, action: InputAction) -> Optional[int]:
        """
        Get the key bound to a specific action for a game state
        
        Args:
            game_state: Game state to check bindings for
            action: Action to find key for
            
        Returns:
            Key code bound to the action, or None if no binding exists
        """
        if game_state not in self._keyboard_mappings:
            return None
        
        for key, bound_action in self._keyboard_mappings[game_state].items():
            if bound_action == action:
                return key
        
        return None
    
    def save_bindings(self) -> Dict:
        """
        Save the current input bindings
        
        Returns:
            Dictionary of serialized input bindings
        """
        # Convert state enums to strings for serialization
        keyboard_bindings = {}
        for state, mapping in self._keyboard_mappings.items():
            keyboard_bindings[state.name] = {
                str(key): action.name for key, action in mapping.items()
            }
        
        mouse_bindings = {}
        for state, mapping in self._mouse_mappings.items():
            mouse_bindings[state.name] = {
                button.name: action.name for button, action in mapping.items()
            }
        
        return {
            "keyboard": keyboard_bindings,
            "mouse": mouse_bindings
        }
    
    def load_bindings(self, bindings: Dict) -> None:
        """
        Load input bindings from a saved configuration
        
        Args:
            bindings: Dictionary of serialized input bindings
        """
        try:
            # Clear existing mappings
            self._keyboard_mappings.clear()
            self._mouse_mappings.clear()
            
            # Load keyboard bindings
            for state_str, mapping in bindings.get("keyboard", {}).items():
                state = GameState[state_str]
                self._keyboard_mappings[state] = {
                    int(key): InputAction[action] for key, action in mapping.items()
                }
            
            # Load mouse bindings
            for state_str, mapping in bindings.get("mouse", {}).items():
                state = GameState[state_str]
                self._mouse_mappings[state] = {
                    MouseButton[button]: InputAction[action] for button, action in mapping.items()
                }
                
        except (KeyError, ValueError) as e:
            print(f"Error loading input bindings: {e}")
            # Revert to defaults if loading fails
            self._init_default_mappings()