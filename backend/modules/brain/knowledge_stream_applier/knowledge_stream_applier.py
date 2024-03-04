from abc import abstractmethod,ABC


class KnowledgeStreamApplier(ABC):
    @abstractmethod
    def fetch_data(self, source, auth):
        pass

    @abstractmethod
    def data_processing(self):
        pass

    @abstractmethod
    def ingest_knowledge(self):
        pass
