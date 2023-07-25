class LinearRegression(_LinearRegression):

    """
    Class for calculation of simple linear regression.
    """

    def __init__(self, single_regression_len: int, values: list[int | float] | tuple[int | float]) -> None:

        """
        Constructor of the LinearRegression class.

        Args:
            single_regression_len (int): number of values taken into account during calculation of the single simple
            linear regression.
            values (list[int | float] | tuple[int | float]): the iterable with the values given to calculate the simple
            linear regression on them.
        """

        if isinstance(values, (list, tuple)):
            pass
        else:
            raise TypeError(f"values should be of type either {list.__name__} or {tuple.__name__}. "
                            f"{type(values).__name__} given instead.")

        if all(isinstance(element, (int, float)) for element in values):
            pass
        else:
            for element in values:
                if isinstance(element, (int, float)):
                    pass
                else:
                    raise TypeError(f"Each element in values should be of type either {int.__name__} or "
                                    f"{float.__name__}. {type(element).__name__} given instead.")

        if isinstance(single_regression_len, int):
            pass
        else:
            raise TypeError(f"single_regression_len should be of type {int.__name__}. "
                            f"{type(single_regression_len).__name__} given instead.")

        super().__init__(
            {
                index: value
                for index, value in enumerate(values)
            }
        )

        self.__values: tuple[int | float] = tuple(values)
        self.__single_regression_len: int = single_regression_len
        self.__progress_bar_share: ProgressBar = ...

    @property
    def single_regression_len(self) -> int:

        """
        Getter for the self.__single_regression_len attribute.

        Returns:
            int: Value of the self.__single_regression_len attribute.
        """

        return self.__single_regression_len

    @property
    def progress_bar_share(self) -> ProgressBar:

        """
        Getter for the self.__progress_bar_share attribute.

        Returns:
            ProgressBar: The value of the self.__progress_bar_share attribute.
        """

        return self.__progress_bar_share

    @progress_bar_share.setter
    def progress_bar_share(self, value: ProgressBar) -> None:

        """
        Setter for the self.__progress_bar_share attribute.

        Args:
            value (ProgressBar): The new value for the self.__progress_bar_share attribute.
        """

        self.__progress_bar_share: ProgressBar = value

    @property
    def values(self) -> tuple[int | float]:

        """
        Getter for the self.__values attribute.

        Returns:
            tuple[int | float]: The value of the self.__values attribute.
        """

        return self.__values

    def moving_linear_regression(self, coefficient: str) -> list[float]:

        """
        Method for calculation of values of the moving linear regression.

        Args:
            coefficient (str): The coefficient of the linear regression. "a" returns "a" coefficients of the linear
            regression, "b" returns the "b" coefficients of the linear regression, "ab" returns the values of the linear
            regression.

        Returns:
            list[float]: list of values of linear regression

        Raises:
            TypeError: If the given coefficient argument is not of type str.
            ValueError: If the given coefficient argument is of type str, however it does not match any of the
            following:
            - "a",
            - "b",
            - "ab".
        """

        if isinstance(coefficient, str):
            pass
        else:
            raise TypeError(f"coefficient should be of type {str.__name__}. "
                            f"{type(coefficient).__name__} given instead.")

        if coefficient in {'a', 'b', 'ab'}:
            pass
        else:
            raise ValueError(f"coefficient should be equal to either {'a'}, {'b'} or {'ab'}. "
                             f"{coefficient} given instead.")

        values_length: int = len(self.values)
        if not (cpu_count := os.cpu_count()) % 2:
            step: int = values_length // cpu_count
        else:
            try:
                step: int = values_length // (cpu_count - 1)
            except ZeroDivisionError:
                raise ValueError(f"cpu_count should be higher or equal to {2}.")

        ranges: list[tuple[int]] = list()
        for index in range(self.single_regression_len, values_length, step):
            if index + step >= values_length:
                ranges.append(tuple(range(index, values_length)))
            else:
                ranges.append(tuple(range(index, index + step)))

        dict_linear_regressions: dict[int, list[float]] = dict()

        ShareManager.custom_register('ProgressBar', ProgressBar)

        with ShareManager() as manager:
            self.progress_bar_share: ProgressBar = getattr(
                manager, manager.registered_classes['ProgressBar'].__name__
            )(values_length - self.single_regression_len, 'LinearRegressionProgress')

            with concurrent.futures.ProcessPoolExecutor() as executor:
                futures: list[concurrent.futures.Future[tuple[int, list[float]]]] = [
                    executor.submit(
                        self._calculate_regression,
                        index_of_range,
                        range_of_indexes,
                        coefficient
                    )
                    for index_of_range, range_of_indexes in enumerate(ranges)
                ]

                for future in concurrent.futures.as_completed(futures):
                    future_result: tuple[int, list[float]] = future.result()
                    dict_linear_regressions[future_result[0]]: list[float] = future_result[1]

        return [value for key in sorted(dict_linear_regressions.keys()) for value in dict_linear_regressions[key]]

    def _calculate_regression(self, index_of_range: int, range_of_indexes: list[int] | tuple[int],
                              coefficient: str) -> tuple[int, list[float]]:

        """
        Method calling the regression calculating method and returning its value with the index of range, so it is known
        how much regression is still left.

        Args:
            index_of_range: The index of the range list.
            range_of_indexes: The list (or tuple) of the indexes on which the regression is about to be done.
            coefficient (str): The coefficient of the linear regression. "a" returns "a" coefficients of the linear
            regression, "b" returns the "b" coefficients of the linear regression, "ab" returns the values of the linear
            regression.

        Returns:
            tuple[int, list[float]]: returns the index of the range list and the list of linear regressions on the given
            range.

        Raises:
            TypeError: If any of the arguments' types do not match the correct ones.
        """

        if isinstance(index_of_range, int):
            pass
        else:
            raise TypeError(f"index_of_range type should match {int.__name__}. "
                            f"{type(index_of_range).__name__} given instead.")

        if isinstance(range_of_indexes, (list, tuple)):
            pass
        else:
            raise TypeError(f"range_of_indexes type should match either {list.__name__} or {tuple.__name__}. "
                            f"{type(range_of_indexes).__name__} given instead.")

        return index_of_range, self.__regression_on_range(range_of_indexes, coefficient)

    def __regression_on_range(self, range_of_index: list[int], coefficient: str) -> list[float]:

        """
        Method for computation of the regression on some range in order to speed up the process of regression creation.
        """

        regression_coefficients: list[float] = list()
        current_index: int = range_of_index[0]
        ending_index: int = range_of_index[-1]
        counter: int = 0
        for index in range(current_index, ending_index):
            counter += 1
            super().__init__(
                {
                    index: value
                    for index, value in enumerate(
                        [
                            self.values[index - self.single_regression_len + i]
                            for i in range(self.single_regression_len)
                        ]
                    )
                }
            )
            regression_coefficients.append(
                super().coefficient(coefficient)
            )
            if not counter - 100:
                self.progress_bar_share.increase(100)
                current_index: int = index
                counter: int = 0

        self.progress_bar_share.increase(ending_index - current_index)
        return regression_coefficients
