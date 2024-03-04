from components.models import DataSource, Usecase
from components.usecase.TriggerEmailOnSteadyClick import TriggerEmailOnSteadyClick

DATA_SOURCE="Select Data Source"
DATA_SOURCE_BE=DataSource(
    option="Backend Server",
    description="In this setup, consumer will poll BE to get latest updates"
)
DATA_SOURCE_KAFKA=DataSource(
    option="Kafka Stream",
    description="In this setup, consumer will fetch the latest data from the Kafka Stream"
)



USECASE="Select Usecase"
EMAIL_USECASE_1=Usecase(
    option="Trigger email on steady clicks",
    trigger="5 click events in a space of 10 seconds",
    condition="Clicks must be from the same IP Address",
    action="Trigger email to click_updates@ese.com",
    reason="Product feels this metric is enough to nudge the customer by sending a follow-up email",
    listener=TriggerEmailOnSteadyClick
)