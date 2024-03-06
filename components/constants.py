from components.models import DataSource, Usecase

from components.usecase.trigger_email_on_steady_click.impl_usecase import TriggerEmailOnSteadyClick
from components.usecase.dummy_usecase_example.impl_usecase import DummyUsecaseExample



DATA_SOURCE    = "Select Data Source"
DATA_SOURCE_BE = DataSource(
    option      = "Backend Server",
    description = "In this setup, consumer will poll BE to get latest updates"
)
DATA_SOURCE_KAFKA=DataSource(
    option      = "Kafka Stream",
    description = "In this setup, consumer will fetch the latest data from the Kafka Stream"
)



USECASE       = "Select Usecase"
DUMMY_USECASE = Usecase(
    option    = "Dummy usecase example",
    trigger   = "What action lead to this thing happening",
    condition = "What condition must be met to act on this trigger",
    action    = "What action should be done when the condition is met",
    reason    = "What is the reason for having this usecase",
    listener  = DummyUsecaseExample
)
EMAIL_USECASE_1=Usecase(
    option    = "Trigger email on steady clicks",
    trigger   = "5 click events in a space of 10 seconds",
    condition = "Clicks must be from the same IP Address",
    action    = "Trigger email to click_updates@ese.com",
    reason    = "Product feels this metric is enough to nudge the customer by sending a follow-up email",
    listener  = TriggerEmailOnSteadyClick
)