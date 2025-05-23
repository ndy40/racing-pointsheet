import warnings
from pointsheet.domain.value_objects import TeamMember as _TeamMember

# For backward compatibility
TeamMember = _TeamMember

# Add a deprecation warning
warnings.warn(
    "Importing TeamMember from modules.account.domain.value_objects is deprecated. "
    "Import from pointsheet.domain.value_objects instead.",
    DeprecationWarning,
    stacklevel=2,
)
