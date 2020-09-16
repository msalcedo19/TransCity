from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class Observer(ABC):
    """
    The Observer interface declares the update method, used by observed.
    """

    @abstractmethod
    def update(self) -> None:
        """
        Receive update from observed.
        """
        pass


class ObserverManager(ABC):
    """
    The ObserverManager interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the observerManager.
        """
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the observerManger.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        pass


class ObserverLogic(ObserverManager):

    _observers: List[Observer] = []

    def __init__(self):
        super().__init__()

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    """
    The subscription management methods.
    """

    def notify(self) -> None:
        """
        Trigger an update in each subscriber.
        """

        print("Subject: Notifying GUI")
        for observer in self._observers:
            observer.update()
