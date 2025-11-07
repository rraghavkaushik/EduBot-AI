"""
Mutmut configuration for EduBot
"""
def pre_mutation(context):
    """Skip certain mutations"""
    # Skip mutations in test files
    if 'test_' in context.filename:
        return False
    # Skip migrations and config
    if 'migration' in context.filename or 'config' in context.filename:
        return False
    return True

