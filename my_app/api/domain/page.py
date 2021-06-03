from typing import List


class Page:
    def __init__(
            self,
            page: int,
            page_size: int,
            total_records: int,
            data: List,
    ):
        """
        Creates a new page

        Parameters
        ----------
        page: int
            Page number
        page_size: int
            Elements per page
        total_records: int
            Total query records
        data: List[DomainEntity]
            A list of a Domain class that implements the "to_json" method.
        Returns
        ----------
        query: BaseQuery
            Query with limit and offset
        """
        self.page = page
        self.page_size = page_size
        self.total_records = total_records
        self.data = data

    def to_json(self):
        return {
            "page": self.page,
            "page_size": self.page_size,
            "total_records": self.total_records,
            "data": list(map(lambda element: element.to_json(), self.data)),
        }
