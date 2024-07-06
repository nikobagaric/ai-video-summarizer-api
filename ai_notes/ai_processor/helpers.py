import shutil

def cleanup_temp_files(temp_dir):
    """
    Deletes a temporary directory
    """
    shutil.rmtree(temp_dir)
