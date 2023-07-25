class ProgressBar:

    """
    Progress bar class showing the progress bar in the console.
    """

    def __init__(self, total: int | float = 100, description: str | None = None) -> None:

        """
        Constructor for the ProgressBar class.

        Args:
            total (int | float): The total value to be achieved by the progress bar. 100 by default.
            description (str): Description to the progress bar shown on the left. None by default.

        Raises:
            TypeError: If the type of any argument does not match the correct one.
        """

        if isinstance(description, str) or description is None:
            pass
        else:
            raise TypeError(f"description type should match either {str.__name__} or {types.NoneType.__name__}. "
                            f"{type(description).__name__} given instead.")

        if isinstance(total, (int, float)):
            pass
        else:
            raise TypeError(f"total type should match either {int.__name__} or {float.__name__}. "
                            f"{type(total).__name__} given instead.")

        self.progress_bar: tqdm.tqdm = tqdm.tqdm(total=total, desc=description)

    def increase(self, value: int | float) -> None:

        """
        Method used for increasing the value of the progress bar.

        Args:
            value (int | float): The value to be added to the current progress value.

        Raises:
            TypeError: If the value argument is not int or float.
        """

        if isinstance(value, (int, float)):
            pass
        else:
            raise TypeError(f"value type should match either {int.__name__} or {float.__name__}. "
                            f"{type(value).__name__} given instead.")

        self.progress_bar.update(value)

    def __add__(self, other: int | float) -> ProgressBar:

        """
        Overriden special method that makes possible increasing the progress bar value using the "+" operator.

        Args:
            other (int | float): A value to be added to current progress on the progress bar. Must be positive.

        Examples:
            "bar + 5" = "bar.increase(5)"
        """

        self.increase(value=other)

        return self

    def __del__(self) -> None:

        """
        Overriden __del__ special method used for object deletion. Automatically called by the garbage collector.
        In here closes the progress bar by calling the self.progress_bar.close() method.
        """

        self.progress_bar.close()
