from components.mailer.configs import MailerViewConfig



def get_mailer_config(ctx) -> MailerViewConfig: 
    ctx.markdown("##### Mailer Configuration")
    queu_col, channel_col = ctx.columns(2)

    queue_url    = queu_col.text_input("Provide mailer queue URL", placeholder="localhost", value="192.168.29.191")
    channel_name = channel_col.text_input("Provide mailer channel name", placeholder="email_channel", value="email_channel")

    return MailerViewConfig(queue_url, channel_name)