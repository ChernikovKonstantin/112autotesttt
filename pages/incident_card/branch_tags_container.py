from pages.incident_card.base_container import BaseContainer


class BranchTagsContainer(BaseContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._incident_content_branch = self.element.s('//div[@class="incident-content__branch"]')
        self._elements_for_assert = [
            self._incident_content_branch,
        ]
