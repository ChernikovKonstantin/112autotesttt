from pages.incident_card.branch_tags_container import BranchTagsContainer
from pages.incident_card.custom_elements.modal_windows.added_but_not_save_window import AddedButNotSaveWindow
from pages.incident_card.question_list_container import QuestionListContainer
from pages.incident_card.what_happens_content_branches import FirstBranch, SecondBranch, ThirdBranch
from pages.incident_card.saved_accident_сard_page import SavedAccidentCardPage


class AdditionalModeCardPage(SavedAccidentCardPage):
    def __init__(self):
        super().__init__()
        self.question_list = QuestionListContainer(css='#question-list-container')
        self.added_but_not_save_window = AddedButNotSaveWindow(css='#existUnsafeAdditionsWithGoToShowing')
        self.branch_tags = BranchTagsContainer(css='#branch-container')
        self.what_happens_content_branch_1 = FirstBranch(css='#branch-1')
        self.what_happens_content_branch_2 = SecondBranch(css='#branch-2')
        self.what_happens_content_branch_3 = ThirdBranch(css='#branch-3')
