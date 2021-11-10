from typing import Iterable, Any, List

from prefect import task


@task()
def flatten_iterable_of_variables(iter: Iterable[Iterable[Any]]) -> List[Any]:
    output = []
    for top_list in iter:
        for var in top_list:
            output.append(var)
    return output
