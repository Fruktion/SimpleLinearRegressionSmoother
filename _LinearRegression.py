class _LinearRegression:

    """
    Class used for linear regression calculations.
    """

    def __init__(self, data_dict: dict[int | float, int | float]) -> None:

        """
        Constructor for LinearRegression.

        Args:
            data_dict (dict[int | float, int | float]): A dictionary with keys as arguments and values as values of
            the function.

        Raises:
            TypeError: If the argument is not a proper dictionary or contains invalid types.
        """

        if isinstance(data_dict, dict):
            pass
        else:
            raise TypeError(f"data_dict type should be {dict.__name__}. {type(data_dict).__name__} given instead.")

        if all(isinstance(argument, (int, float)) for argument in data_dict.keys()):
            pass
        else:
            for argument in data_dict.keys():
                if not isinstance(argument, (int, float)):
                    raise TypeError(f"Each argument of the function should be of type {int.__name__} or "
                                    f"{float.__name__}. At least one element's type is {type(argument).__name__}.")

        if all(isinstance(value, (int, float)) for value in data_dict.values()):
            pass
        else:
            for value in data_dict.values():
                if not isinstance(value, (int, float)):
                    raise TypeError(f"Each value of the function should be of type {int.__name__} or {float.__name__}. "
                                    f"At least one element's type is {type(value).__name__}.")

        self.__x: np.ndarray[int | float] = np.array(list(data_dict.keys()))
        self.__y: np.ndarray[int | float] = np.array(list(data_dict.values()))

        self.__n: int = np.size(self.x)

        self.__mean_x: np.float64 = np.mean(self.x)
        self.__mean_y: np.float64 = np.mean(self.y)

        self.__a: float = self.coefficient('a')

    @property
    def x(self) -> np.ndarray[int | float]:

        """
        Getter for the self.__x attribute

        Returns:
            np.ndarray[int | float]: value of the self.__x attribute
        """

        return self.__x

    @property
    def y(self) -> np.ndarray[int | float]:

        """
        Getter for the self.__y attribute

        Returns:
            np.ndarray[int | float]: value of the self.__y attribute
        """

        return self.__y

    @property
    def n(self) -> int:

        """
        Getter for the self.__n attribute

        Returns:
            int: value of the self.__n attribute
        """

        return self.__n

    @property
    def mean_x(self) -> np.float64:

        """
        Getter for the self.__mean_x attribute

        Returns:
            np.float64: value of the self.__mean_x attribute
        """

        return self.__mean_x

    @property
    def mean_y(self) -> np.float64:

        """
        Getter for the self.__mean_y attribute

        Returns:
            np.float64: value of the self.__mean_y attribute
        """

        return self.__mean_y

    @property
    def a(self) -> float:

        """
        Getter for the self.__a attribute

        Returns:
            float: value of the self.__a attribute
        """

        return self.__a

    def coefficient(self, coefficient: str | None = None) -> float | dict[str, float]:

        """
        Method for getting the coefficients.

        Args:
            coefficient (str | None): The coefficient to return. If not specified, both 'a' and 'b' are returned.

        Returns:
            float | dict[str, float]: Single coefficient value or a dictionary of coefficients based on the given
            argument.

        Raises:
            ValueError: If an incorrect coefficient is passed as an argument.
        """

        if coefficient is None:
            return {'a': self.__coefficient('a'), 'b': self.__coefficient('b')}
        elif coefficient.lower() in {'a', 'b'}:
            return self.__coefficient(coefficient.lower())
        elif coefficient.lower() == 'ab':
            return self.__coefficient('a') + self.__coefficient('b')
        else:
            raise ValueError("Unsupported coefficient. Either 'a' (or 'A') or 'b' (or 'B') should be passed.")

    @functools.singledispatchmethod
    def __coefficient(self, coefficient: str | None = None) -> NoReturn:

        """
        Generic method called when an inappropriate argument is passed to the private __coefficient method.

        Args:
            coefficient (str | None): The coefficient to be returned. None by default (both are returned).

        Raises:
            NotImplementedError: If the given coefficient does not match one of the following: 'a' or 'b'.
        """

        raise NotImplementedError(f"Unsupported coefficient. Either 'a' or 'b' should be passed. "
                                  f"{coefficient} given instead.")

    @__coefficient.register(str)
    def _(self, coefficient: str) -> float:

        """
        Method that returns the 'a' or 'b' coefficient of the linear regression equation.

        Args:
            coefficient (str): The coefficient to be returned ('a' or 'b').

        Returns:
            float: The value of the specified coefficient.

        Raises:
            ValueError: If an incorrect coefficient is passed as an argument.
        """

        match coefficient:
            case 'a':
                return (
                        np.sum(self.y * self.x) - self.n * self.mean_y * self.mean_x
                ) / (
                        np.sum(self.x * self.x) - self.n * self.mean_x * self.mean_x
                )
            case 'b':
                return self.mean_y - self.a * self.mean_x
            case _:
                raise ValueError("Unsupported coefficient. Either 'a' or 'b' should be passed.")
