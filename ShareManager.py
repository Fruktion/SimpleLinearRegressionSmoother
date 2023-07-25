class ShareManager(multiprocessing.managers.BaseManager):

    """
    ShareManager class for managing the data sharing between multiple processes.

    Examples:

        The example for the intended use:
            "
            ShareManager.register('MyCustomClass', MyCustomClass)
            with ShareManager() as manager:
                # Equivalent to "manager.MyCustomClass(10)" except the fact that the equivalent notation (the one in
                # double quotes) raises a warning:
                shared_custom = getattr(manager, manager.MyCustomClass.__name__)(10)
                        with concurrent.futures.ProcessPoolExecutor() as executor:
                            futures = [
                                executor.submit(
                                    shared_custom.get_storage,  # Run some method on the called object
                                    shared_custom  # Pass the object to some method if necessary
                                )
                                for _ in range(4)
                            ]

                            for future in concurrent.futures.as_completed(futures):
                                future.result()
    """

    registered_classes: dict[str, Callable[..., object]] = dict()

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def custom_register(cls, typeid: str, fn: Callable[..., object]) -> None:

        """
        Method used as a register for the ShareManager class.

        Args:
            typeid: The name for the type.
            fn: Callable for the type.

        Raises:
            TypeError: If any of the arguments' types does not match the correct ones.
        """

        if isinstance(typeid, str):
            pass
        else:
            raise TypeError(f"typeid should be of type {str.__name__}. {type(typeid).__name__} given instead.")

        if isinstance(fn, Callable):
            pass
        else:
            raise TypeError(f"fn should be of type {Callable.__name__}. {type(fn).__name__} given instead.")

        setattr(cls, typeid, fn)
        cls.registered_classes[typeid]: Callable[..., object] = fn
        cls.register(typeid, fn)
