import configparser
from pathlib import Path


class Config:
    def __init__(self):
        self.file_path = Path("config.ini")
        self.config = configparser.ConfigParser()

        # Check if the file exists, if not, create it
        if not self.file_path.exists():
            self.file_path.touch()

        self.config.read(self.file_path)

    def get_value(self, section, key, fallback=None):
        """Get the value of a key in a specific section. Returns fallback if not found."""
        return self.config.get(section, key, fallback=fallback)

    def set_value(self, section, key, value):
        """Set the value of a key in a specific section."""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)
        self._save()

    def remove_option(self, section, key):
        """Remove a specific key from a section."""
        if self.config.has_section(section):
            self.config.remove_option(section, key)
            self._save()

    def remove_section(self, section):
        """Remove a section from the .ini file."""
        if self.config.has_section(section):
            self.config.remove_section(section)
            self._save()

    def get_sections(self):
        """Return a list of all sections in the .ini file."""
        return self.config.sections()

    def get_options(self, section):
        """Return a list of all options (keys) in a specific section."""
        if self.config.has_section(section):
            return self.config.options(section)
        return []

    def _save(self):
        """Save the current state of the config to the .ini file."""
        with open(self.file_path, 'w') as configfile:
            self.config.write(configfile)
