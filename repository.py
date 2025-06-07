from dagster import repository, schedule
from orchestration import run_elt

@repository
def prague_apartments_repo():
    return [run_elt]
