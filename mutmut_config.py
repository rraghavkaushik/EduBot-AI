"""
Mutmut configuration for EduBot
"""
import os
import shutil

def pre_mutation(context):
    """Skip certain mutations"""
    # Skip mutations in test files
    if 'test_' in context.filename:
        return False
    # Skip migrations and config
    if 'migration' in context.filename or 'config' in context.filename:
        return False
    return True

def post_mutation(context):
    """Copy dependencies to mutants directory after mutation"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    mutants_dir = os.path.join(base_dir, 'mutants')
    
    # Copy services directory if it doesn't exist
    services_src = os.path.join(base_dir, 'services')
    services_dst = os.path.join(mutants_dir, 'services')
    if os.path.exists(services_src) and not os.path.exists(services_dst):
        shutil.copytree(services_src, services_dst)
    
    # Copy other dependencies
    for dep_file in ['gemini_service.py', 'text_extractor.py']:
        src = os.path.join(base_dir, dep_file)
        dst = os.path.join(mutants_dir, dep_file)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)

