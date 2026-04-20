# Exceptions Errors para o projeto A-Maze-ing


class MazeError(Exception):
    """Base exception for all maze-related errors."""
    pass


class ConfigError(MazeError):
    """Raised when the configuration file has issues."""
    pass


class MazeGenerationError(MazeError):
    """Raised when maze generation fails (e.g., impossible parameters)."""
    pass


class MazeWriteError(MazeError):
    """Raised when writing the maze output file fails."""
    pass


class ConfigFileNotFoundError(ConfigError):
    """Raised when the configuration file does not exist."""
    pass


class ConfigSyntaxError(ConfigError):
    """Raised when a line in the config file has invalid syntax."""
    pass
class ConfigMissingKeyError(ConfigError):
    """Raised when a mandatory key is missing from the config."""
    pass
class ConfigValueError(ConfigError):
    """Raised when a config value is invalid (wrong type, out of range, etc.)."""
    pass