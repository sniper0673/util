from pathlib import Path
def get_feather_path() -> Path:
    """
    현재 파일 기준으로 상위 디렉토리를 탐색하여 feather 폴더를 찾고,
    해당 폴더의 경로를 반환합니다.
    
    Returns: Path
        발견한 feather 디렉토리의 경로
    """
    return get_target_path("feather", caller_path=__file__)
def get_credentials_path() -> Path:
    """
    현재 파일 기준으로 상위 디렉토리를 탐색하여 credentials 폴더를 찾고,
    해당 폴더의 경로를 반환합니다.
    
    Returns: Path
        발견한 credentials 디렉토리의 경로
    """
    return get_target_path("credentials", caller_path=__file__)    

def get_target_path(target_dir_name: str, caller_path=None) -> Path:
    """
    현재 파일 기준으로 상위 디렉토리를 탐색하여 target_dir_name 폴더를 찾고,
    해당 폴더의 경로를 반환합니다.

    Args:
        target_dir_name (str): 찾으려는 대상 디렉토리 이름
        caller_path (Path or str, optional): 탐색을 시작할 경로 (기본: 현재 작업 디렉토리)

    Returns:
        Path: 발견한 target_dir_name 디렉토리의 경로

    Raises:
        FileNotFoundError: target_dir_name 디렉토리를 찾지 못한 경우
    """
    # 시작 경로 설정
    if caller_path is None:
        current = Path.cwd()
    else:
        current = Path(caller_path).resolve()

    # 루트까지 상위 디렉토리를 탐색
    while current != current.parent:
        target_path = current / target_dir_name
        if target_path.exists() and target_path.is_dir():
            return target_path
        current = current.parent

    raise FileNotFoundError(f"상위 디렉토리에 '{target_dir_name}' 폴더를 찾을 수 없습니다.")
