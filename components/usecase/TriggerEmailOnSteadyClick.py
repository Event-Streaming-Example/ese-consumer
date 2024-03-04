from components.models import UsecaseListener
import streamlit as st

BUCKET = []

class TriggerEmailOnSteadyClick(UsecaseListener):

    def __init__(self):
        super().__init__()

    def update(self, data, view_ctx):
        BUCKET.append(data)
        view_ctx.write(BUCKET)

    def view(self, ctx):
        ctx.write(BUCKET)